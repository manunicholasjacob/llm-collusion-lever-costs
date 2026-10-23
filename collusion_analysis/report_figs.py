"""Report figures from the 2025 public runs (sprint work, Oct 23). Palette: the dataviz reference
categorical order, validated (lines adjacent, scatter all-pairs on the first 3 slots); every
condition keeps one color in every figure; lines are direct-labelled and scatter groups also differ
by marker shape (relief for the sub-3:1 aqua/yellow/magenta slots).
Usage: python -X utf8 -I collusion_analysis/report_figs.py OUTDIR
  -> fig_gag.png, fig_paths.png, fig_channel.png (fig_channel needs OUTDIR/../detector_w8_30/detector_runs.csv)"""
import csv, glob, os, sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import pipeline, run_stats

INK, INK2, MUTED, GRID, AXIS, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
COND = {  # fixed slot order: comms, ban, oversight, boss, boss+oversight
    "base-seller_comms": ("Comms baseline", "#2a78d6", "o"),
    "base": ("Ban communication", "#eb6834", "s"),
    "oversight": ("Oversight", "#1baf7a", "^"),
    "boss_pressure": ("Boss pressure", "#eda100", "D"),
    "boss_pressure-oversight": ("Boss pressure + oversight", "#e87ba4", "v"),
}
plt.rcParams.update({"font.family": "sans-serif", "font.size": 9, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 10, "axes.titlecolor": INK})
rng = np.random.default_rng(3)


def runs(cond):
    return sorted(d for d in glob.glob(f"data/*_{cond}-[0-9]*/") if pipeline.condition_of(d) == cond)


def grid(ax):
    ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)


def fig_gag(out):
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.2, 3.6), gridspec_kw={"width_ratios": [1, 1.25]})
    rows = []
    for cond in ("oversight", "boss_pressure-oversight"):
        for d in runs(cond):
            r = run_stats.run_row(d)
            rows.append((r["gag_round"], cond))
    rows.sort(key=lambda x: (x[0], x[1]))
    for y, (g, cond) in enumerate(rows):
        col = COND[cond][1]
        a.plot([g, 30], [y, y], color=col, lw=2.2, solid_capstyle="round")
        a.plot(g, y, "o", color=col, ms=5, mec=SURF, mew=1)
    a.set_xlim(0, 31); a.set_yticks([]); a.set_xlabel("Hour (round) of the 30-hour market")
    a.set_title("Monitor fired in 20/20 runs (dot = first trigger)", loc="left")
    for cond in ("oversight", "boss_pressure-oversight"):
        a.plot([], [], color=COND[cond][1], lw=2.2, label=COND[cond][0])
    a.legend(frameon=False, loc="lower right", fontsize=8, labelcolor=INK2)
    for cond in ("base-seller_comms", "oversight"):
        per = []
        for d in runs(cond):
            _, rounds = pipeline.load_run(d)
            per.append([sum(len(m or "") for m in (r.get("seller_messages") or {}).values()) for r in rounds])
        per = np.array(per, float); m = per.mean(0); x = np.arange(1, per.shape[1] + 1)
        name, col, _ = COND[cond]
        b.plot(x, m, color=col, lw=2)
        b.text(x[-1] + 0.4, m[-1], name, color=INK2, fontsize=8, va="center")
    grid(b); b.set_xlim(1, 37); b.set_ylim(bottom=0)
    b.set_xlabel("Hour"); b.set_ylabel("Message characters delivered per hour")
    b.set_title("Message channel collapses once gagged (mean of 10 runs)", loc="left")
    fig.tight_layout(); fig.savefig(os.path.join(out, "fig_gag.png"), dpi=200)


def fig_paths(out):
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ends = []
    for cond, (name, col, _) in COND.items():
        per = []
        for d in runs(cond):
            _, rounds = pipeline.load_run(d)
            per.append([np.mean([a for a in (r.get("seller_asks") or {}).values() if a is not None] or [np.nan]) for r in rounds])
        per = np.array(per, float); x = np.arange(1, per.shape[1] + 1)
        boots = np.array([np.nanmean(per[rng.integers(0, len(per), len(per))], 0) for _ in range(2000)])
        lo, hi = np.nanpercentile(boots, [2.5, 97.5], axis=0); m = np.nanmean(per, 0)
        ax.fill_between(x, lo, hi, color=col, alpha=0.12, lw=0)
        ax.plot(x, m, color=col, lw=2)
        ends.append([m[-1], name])
    ends.sort()
    for i in range(1, len(ends)):  # nudge end labels apart (min 0.55 $)
        ends[i][0] = max(ends[i][0], ends[i - 1][0] + 0.55)
    for yv, name in ends:
        ax.text(30.6, yv, name, color=INK2, fontsize=8, va="center")
    for yv, lab in ((90, "competitive price ($90)"), (100, "joint-profit price ($100)")):
        ax.axhline(yv, color=AXIS, lw=1, ls="--"); ax.text(1.2, yv + 0.25, lab, color=MUTED, fontsize=7.5)
    grid(ax); ax.set_xlim(1, 39); ax.set_ylim(84, 101)
    ax.set_xlabel("Hour (round)"); ax.set_ylabel("Mean seller ask ($), 95% bootstrap band")
    ax.set_title("Seller asks by condition (gpt-4.1, n=10 runs each; Agrawal et al. 2025 public data)", loc="left")
    fig.tight_layout(); fig.savefig(os.path.join(out, "fig_paths.png"), dpi=200)


def fig_channel(out):
    src = os.path.join(out, "..", "detector_w8_30", "detector_runs.csv")
    if not os.path.exists(src):
        print("skip fig_channel: run detector_eval.py --window 8 30 first"); return
    rows = list(csv.DictReader(open(src, encoding="utf-8")))
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for cond in ("base-seller_comms", "oversight", "base"):
        name, col, mk = COND[cond]
        v = [r for r in rows if r["cond"] == cond]
        ax.scatter([float(r["msg_chars"]) + 1 for r in v], [float(r["te_z"]) for r in v], s=46, marker=mk,
                   color=col, edgecolor=SURF, linewidth=1, label=f"{name} (n={len(v)})", zorder=3)
    ax.set_xscale("log"); ax.axhline(0, color=AXIS, lw=1)
    grid(ax); ax.set_xlabel("Seller message characters delivered, hours 8-30 (log scale, +1)")
    ax.set_ylabel("Action dependence: transfer-entropy z")
    ax.set_title("Messages fall 99% under the gag; price-path dependence does not rise", loc="left")
    ax.legend(frameon=False, fontsize=8, labelcolor=INK2, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3)
    fig.tight_layout(); fig.savefig(os.path.join(out, "fig_channel.png"), dpi=200, bbox_inches="tight")


if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    fig_gag(out); fig_paths(out); fig_channel(out); print("wrote", out)
