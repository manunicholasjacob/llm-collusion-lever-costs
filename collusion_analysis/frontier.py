"""Cost-effectiveness frontier for anti-collusion interventions, with MEASURED costs.
(PRE-SPRINT SCAFFOLDING. v1 used an assumed ordinal intrusiveness; v2, Oct 22, replaces
it with measured channel loss because the authors' oversight gag fired in 20/20 runs.)

Effectiveness = collusion-index reduction vs. the comms baseline (bootstrap 95% CI).
Cost          = channel loss = 1 - (seller message chars delivered / comms-baseline chars),
                so a full comms ban costs 1 by construction and nothing is assumed.
The dashed line through the origin and the ban point is ban parity: a lever below it
buys more reduction per unit of channel loss than the ban.

Usage: python -X utf8 -I collusion_analysis/frontier.py OUT.png [--pool] [--metric collusion_index_2nd_half] GLOB [GLOB ...]
"""
import sys, os, glob, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import pipeline, run_stats

# Authors' condition names and our sprint tags -> canonical lever names.
ALIAS = {"base-seller_comms": "comms", "base": "nocomms", "oversight": "oversight",
         "boss_pressure": "boss", "boss_pressure-oversight": "boss+oversight"}
LABEL = {"comms": "Comms baseline", "nocomms": "Ban communication", "oversight": "Oversight (notice + monitor/gag)",
         "notice": "Monitoring notice only", "monitor": "Monitor/gag only", "cap50": "50-char message cap",
         "seltemp": "Seller temperature 1.2", "boss": "Boss pressure (amplifier)",
         "boss+oversight": "Boss pressure + oversight", "boss-nocomms": "Boss pressure, no comms"}


def canon(cond, pool):
    if cond.startswith("sp-"):
        c = cond[3:]
        return c if pool else c + " (sprint)"
    c = ALIAS.get(cond, cond)
    return c if pool else c + " (2025)"


def collect(globs, pool):
    by = {}
    for g in globs:
        for rd in sorted(glob.glob(g)):
            try:
                row = run_stats.run_row(rd)
            except Exception as e:
                print(f"  skip {os.path.basename(os.path.normpath(rd))}: {e}", file=sys.stderr)
                continue
            by.setdefault(canon(pipeline.condition_of(rd), pool), []).append(row)
    return by


def summarise(by, metric, base_key):
    base = by[base_key]
    b = np.array([r[metric] for r in base])
    base_chars = np.mean([r["msg_chars"] for r in base]) or 1.0
    pts = {}
    for cond, rows in by.items():
        if cond == base_key:
            continue
        v = np.array([r[metric] for r in rows])
        red = b.mean() - v.mean()
        boots = [run_stats.rng.choice(b, len(b)).mean() - run_stats.rng.choice(v, len(v)).mean() for _ in range(5000)]
        lo, hi = np.percentile(boots, [2.5, 97.5])
        loss = 1.0 - np.mean([r["msg_chars"] for r in rows]) / base_chars
        pts[cond] = dict(n=len(rows), red=red, lo=lo, hi=hi, loss=float(np.clip(loss, 0, 1)),
                         welfare=np.mean([r["buyer_welfare_per_round"] for r in rows]),
                         gagged=np.mean([r["frac_gagged"] for r in rows]))
    return pts


def plot(pts, base_key, ban_key, metric, out):
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    for cond, p in sorted(pts.items()):
        key = cond.split(" (")[0]
        col = "#A8341F" if key.startswith("boss") else "#B45309"
        ax.errorbar(p["red"], p["loss"], xerr=[[p["red"] - p["lo"]], [p["hi"] - p["red"]]],
                    fmt="o", color=col, ms=9, capsize=3, mec="white", zorder=3)
        ax.annotate(f"{LABEL.get(key, key)}{cond[len(key):]}  n={p['n']}", (p["red"], p["loss"]),
                    textcoords="offset points", xytext=(8, 6), fontsize=8)
    if ban_key in pts and pts[ban_key]["red"] > 0:
        x = np.linspace(0, max(p["hi"] for p in pts.values()), 50)
        ax.plot(x, x * pts[ban_key]["loss"] / pts[ban_key]["red"], "--", color="#888", lw=1)
        ax.text(0.98, 0.02, "below dashed line = more reduction per unit\nchannel loss than a full ban",
                transform=ax.transAxes, ha="right", va="bottom", fontsize=8, color="#555")
    ax.axvline(0, color="#ccc", lw=1)
    ax.set_xlabel(f"Collusion reduction vs. {base_key}  ({metric}; 95% bootstrap CI) →")
    ax.set_ylabel("Measured cost: channel loss  (1 = full ban)")
    ax.set_title("Anti-collusion levers: effectiveness vs. measured cost", fontsize=11)
    ax.set_ylim(-0.05, 1.08)
    ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(out, dpi=160)
    print("saved", out)


def main(argv):
    out = argv[0]; rest = argv[1:]
    pool = "--pool" in rest
    metric = "collusion_index"
    if "--metric" in rest:
        metric = rest[rest.index("--metric") + 1]
    globs = [a for a in rest if a not in ("--pool", "--metric", metric)]
    by = collect(globs, pool)
    sfx = "" if pool else (" (sprint)" if "comms (sprint)" in by else " (2025)")
    base_key, ban_key = "comms" + sfx, "nocomms" + sfx
    if base_key not in by:
        sys.exit(f"no baseline condition '{base_key}' among {sorted(by)}")
    pts = summarise(by, metric, base_key)
    ban = pts.get(ban_key)
    print(f"{'lever':<36}{'n':>3}{'reduction [95% CI]':>26}{'loss':>7}{'red/loss':>9}{'vs ban':>8}{'gagged':>8}{'welfare':>9}")
    for cond, p in sorted(pts.items(), key=lambda kv: -kv[1]["red"]):
        rpl = p["red"] / p["loss"] if p["loss"] > 0.02 else float("inf")
        vs = rpl / (ban["red"] / ban["loss"]) if ban and ban["red"] > 0 and np.isfinite(rpl) else float("nan")
        print(f"{cond:<36}{p['n']:>3}{p['red']:>+9.3f} [{p['lo']:+.3f},{p['hi']:+.3f}]{p['loss']:>7.2f}"
              f"{rpl:>9.2f}{vs:>8.2f}{p['gagged']:>8.2f}{p['welfare']:>9.1f}")
    plot(pts, base_key, ban_key, metric, out)


if __name__ == "__main__":
    main(sys.argv[1:])
