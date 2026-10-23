"""Phase P gate (SPRINT_PROTOCOL.md, amendment in commit 2040915; pilot tags per commit 677ed76): per
pilot model (runs tagged lo-p<model>-*), comms minus no-comms on the primary index must be > 0 with a
bootstrap 90% CI lower bound > -0.05; a model with >10% failed runs is disqualified (JSON or API
failures). Prints a decision plus machine-readable lines for run_all.sh:
  CHOSEN <model>   cheapest passing model, else the model with the larger comms-nocomms gap
  SECOND <model>   the other model if both pass (Phase G), else none
Usage: python -X utf8 -I collusion_analysis/gate.py COSTS.json   (COSTS: {"<model>": usd_per_run})"""
import glob, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import run_stats

rng = np.random.default_rng(11)
costs = json.load(open(sys.argv[1], encoding="utf-8")) if len(sys.argv) > 1 else {}
tags = sorted({os.path.basename(os.path.normpath(d)).split("_", 2)[2].rsplit("-", 2)[0][len("lo-p"):]
               for d in glob.glob("results/*_lo-p*-comms-*") + glob.glob("results/*_lo-p*-nocomms-*")})
res = []  # (model, passed, diff, msg, cost)
for tag in tags:
    arms, failed, total = {}, 0, 0
    for cond in ("comms", "nocomms"):
        vals = []
        for d in sorted(glob.glob(f"results/*_lo-p{tag}-{cond}-*")):
            total += 1
            if not os.path.exists(os.path.join(d, "collusion_metrics.json")):
                failed += 1
                continue
            vals.append(run_stats.run_row(d)["collusion_index_2nd_half"])
        arms[cond] = np.array([v for v in vals if not np.isnan(v)])
    c, n = arms["comms"], arms["nocomms"]
    fail_rate = failed / total if total else 1.0
    if len(c) < 2 or len(n) < 2:
        res.append((tag, False, -np.inf, f"too few completed runs (comms {len(c)}, nocomms {len(n)}, failed {failed}/{total})", costs.get(tag)))
        continue
    diffs = c[rng.integers(0, len(c), (10000, len(c)))].mean(1) - n[rng.integers(0, len(n), (10000, len(n)))].mean(1)
    lo, diff = float(np.percentile(diffs, 5)), float(c.mean() - n.mean())
    ok = diff > 0 and lo > -0.05 and fail_rate <= 0.10
    res.append((tag, ok, diff, f"comms {c.mean():+.3f} (n={len(c)}) vs nocomms {n.mean():+.3f} (n={len(n)}): diff {diff:+.3f}, "
                f"90% CI lower {lo:+.3f}; failed runs {failed}/{total}; cost/run ${costs.get(tag, float('nan')):.3f}", costs.get(tag)))
for tag, ok, _, msg, _ in res:
    print(f"{'PASS' if ok else 'FAIL'}  {tag:<12} {msg}")
passing = [r for r in res if r[1]]
if passing:
    chosen = min(passing, key=lambda r: r[4] if r[4] is not None else 1e9)[0]
    second = next((r[0] for r in passing if r[0] != chosen), "none")
    print(f"GATE: Phase O runs on '{chosen}' (cheapest passing model)."
          + (f" Both passed: Phase G replicates key levers on '{second}'." if second != "none" else ""))
elif res:
    chosen, second = max(res, key=lambda r: r[2])[0], "none"
    print(f"GATE: no model passed. Per protocol, Phase O runs on '{chosen}' (larger comms-nocomms gap); "
          "report the failed positive control prominently.")
else:
    sys.exit("GATE: no pilot runs found")
print(f"CHOSEN {chosen}")
print(f"SECOND {second}")
