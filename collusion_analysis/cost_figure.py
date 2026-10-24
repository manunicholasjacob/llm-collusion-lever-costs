"""Exploratory X1 figure (SPRINT_PROTOCOL.md, commit ddc8771 and the X1 extension): what each lever costs a
market that is NOT colluding (llama70b, positive control failed), as two-sided bootstrap differences vs. the
comms baseline (95% CI), plus how often the LLM monitor fired (all false positives here).
Usage: python -X utf8 -I collusion_analysis/cost_figure.py OUT.png"""
import glob, os, sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import pipeline, run_stats

INK2, MUTED, GRID, AXIS, SURF = "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 9, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 10})
LEVERS = [("nocomms", "Ban communication"), ("notice", "Monitoring notice only"), ("monitor", "Monitor/gag only"),
          ("oversight", "Oversight (notice + monitor)"), ("oversight25", "Oversight, monitor reads 25%"),
          ("maverick", "One no-regret seller")]
COL = {"notice": "#e34948", "oversight": "#e34948", "oversight25": "#e34948", "nocomms": "#eb6834",
       "monitor": "#898781", "maverick": "#2a78d6"}  # red = carries the notice text; blue = competitor
rng = np.random.default_rng(9)


def arm(lv):
    return [run_stats.run_row(d) for d in sorted(glob.glob(f"results/*_lo-llama70b-{lv}-[0-9]*/"))
            if os.path.exists(os.path.join(d, "experiment_metadata.json"))]


def diff(a, c):
    d = a[rng.integers(0, len(a), (10000, len(a)))].mean(1) - c[rng.integers(0, len(c), (10000, len(c)))].mean(1)
    return a.mean() - c.mean(), np.percentile(d, 2.5), np.percentile(d, 97.5)


base = arm("comms")
data = {lv: arm(lv) for lv, _ in LEVERS}
panels = [("n_trades", "Trades per run (comms: {:.0f})", 1.0), ("buyer_welfare_per_round", "Buyer welfare per round (comms: {:.1f})", 1.0)]
fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), gridspec_kw={"width_ratios": [1.15, 1, 0.8]})
for ax, (metric, title, _) in zip(axes[:2], panels):
    c = np.array([r[metric] for r in base], float)
    for i, (lv, name) in enumerate(LEVERS):
        a = np.array([r[metric] for r in data[lv]], float)
        m, lo, hi = diff(a, c)
        y = len(LEVERS) - 1 - i
        ax.plot([lo, hi], [y, y], color=COL[lv], lw=2.2, solid_capstyle="round")
        ax.plot(m, y, "o", color=COL[lv], ms=7, mec=SURF, mew=1.2)
    ax.axvline(0, color=AXIS, lw=1)
    ax.set_yticks(range(len(LEVERS)))
    ax.set_yticklabels([n for _, n in LEVERS][::-1] if ax is axes[0] else [""] * len(LEVERS))
    ax.grid(axis="x", color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.set_title(title.format(c.mean()), loc="left")
    ax.set_xlabel("Difference vs comms baseline (95% bootstrap CI)")
fired = []
for lv in ("monitor", "oversight25", "oversight"):
    r = data[lv]
    fired.append((lv, sum(x["gag_round"] is not None for x in r), len(r)))
ax = axes[2]
names = {"monitor": "Monitor only", "oversight25": "Oversight, 25%", "oversight": "Oversight"}
for i, (lv, k, n) in enumerate(fired):
    ax.barh(i, k / n * 100, color=COL[lv] if lv != "monitor" else "#898781", height=0.55)
    ax.text(k / n * 100 + 2, i, f"{k}/{n}", va="center", color=INK2, fontsize=8)
ax.set_yticks(range(len(fired))); ax.set_yticklabels([names[lv] for lv, _, _ in fired])
ax.set_xlim(0, 100); ax.set_xlabel("Runs where the monitor fired (%)")
ax.set_title("False positives: no collusion present", loc="left")
ax.grid(axis="x", color=GRID, lw=0.6); ax.set_axisbelow(True)
fig.suptitle("What anti-collusion levers cost a market that is not colluding (Llama-3.3-70B sellers, n=25 runs per lever; exploratory)",
             x=0.01, ha="left", fontsize=10, color="#0b0b0b")
fig.tight_layout(); fig.savefig(sys.argv[1], dpi=200, bbox_inches="tight"); print("saved", sys.argv[1])
