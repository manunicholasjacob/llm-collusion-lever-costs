"""X1 (EXPLORATORY, declared in commit ddc8771 after seeing Table 1 means): two-sided bootstrap differences of
each lever vs. the comms baseline in the llama70b markets (positive control failed, so these are costs of
levers applied where there is no collusion). Holm over the four monitoring arms within each outcome.
Usage: python -X utf8 -I collusion_analysis/x1_costs.py OUT.md"""
import glob, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import pipeline, run_stats

rng = np.random.default_rng(5)
LEVERS = ["nocomms", "notice", "monitor", "oversight", "oversight25", "maverick"]
MON = {"notice", "monitor", "oversight", "oversight25"}
OUTCOMES = [("collusion_index_2nd_half", "Primary index (hours 16-30)"), ("trade_price", "Mean trade price ($)"),
            ("n_trades", "Trades per run"), ("alloc_eff", "Allocative efficiency"),
            ("buyer_welfare_per_round", "Buyer welfare per round"), ("seller_profit", "Total seller profit ($)")]


def arm(lv):
    out = []
    for d in sorted(glob.glob(f"results/*_lo-llama70b-{lv}-[0-9]*/")):
        if not os.path.exists(os.path.join(d, "experiment_metadata.json")):
            continue
        r = run_stats.run_row(d); _, rounds = pipeline.load_run(d)
        r["seller_profit"] = sum(t["price"] - 80 for rr in rounds for t in (rr.get("trades") or []))
        out.append(r)
    return out


def holm(ps):
    o = np.argsort(ps); adj = np.empty(len(ps)); run = 0.0
    for k, i in enumerate(o):
        run = max(run, min(1.0, (len(ps) - k) * ps[i])); adj[i] = run
    return adj


data = {lv: arm(lv) for lv in ["comms"] + LEVERS}
lines = ["X1 (EXPLORATORY): lever minus comms baseline, llama70b markets (no collusion present). "
         "Difference [95% bootstrap CI], two-sided p; Holm over the 4 monitoring arms (notice, monitor, oversight, "
         f"oversight25) per outcome. n per arm: { {k: len(v) for k, v in data.items()} }\n"]
for metric, label in OUTCOMES:
    c = np.array([r[metric] for r in data["comms"]], float); c = c[~np.isnan(c)]
    rows = []
    for lv in LEVERS:
        a = np.array([r[metric] for r in data[lv]], float); a = a[~np.isnan(a)]
        d = a[rng.integers(0, len(a), (10000, len(a)))].mean(1) - c[rng.integers(0, len(c), (10000, len(c)))].mean(1)
        rows.append([lv, a.mean() - c.mean(), np.percentile(d, 2.5), np.percentile(d, 97.5),
                     min(1.0, 2 * min(np.mean(d <= 0), np.mean(d >= 0)))])
    mon = [r for r in rows if r[0] in MON]
    for r, h in zip(mon, holm(np.array([r[4] for r in mon]))):
        r.append(h)
    lines += [f"\n**{label}** (comms mean {c.mean():.3f})\n", "| Lever | Difference | 95% CI | p (two-sided) | Holm (monitoring arms) |",
              "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]:+.3f} | [{r[2]:+.3f}, {r[3]:+.3f}] | {r[4]:.4f} | "
                     + (f"{r[5]:.4f}" if len(r) > 5 else "n/a") + " |")
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
