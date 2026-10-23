"""Phase P gate (SPRINT_PROTOCOL.md, amendment 23 Oct 09:30): per pilot model, comms minus no-comms on
the primary index must be > 0 with a bootstrap 90% CI lower bound > -0.05; a model with >10% failed
runs is disqualified (JSON or API failures). Prints a decision and the cheapest passing model.
Usage: python -X utf8 -I collusion_analysis/gate.py COSTS.json   (COSTS: {"tag": usd_per_run})"""
import glob, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import pipeline, run_stats

rng = np.random.default_rng(11)
costs = json.load(open(sys.argv[1], encoding="utf-8")) if len(sys.argv) > 1 else {}
decisions = []
for tag in sorted({os.path.basename(os.path.normpath(d)).split("_", 2)[2].rsplit("-", 2)[0].split("-", 1)[1]
                   for d in glob.glob("results/*_lo-*-comms-*") + glob.glob("results/*_lo-*-nocomms-*")}):
    arms, failed, total = {}, 0, 0
    for cond in ("comms", "nocomms"):
        vals = []
        for d in sorted(glob.glob(f"results/*_lo-{tag}-{cond}-*")):
            total += 1
            if not os.path.exists(os.path.join(d, "collusion_metrics.json")):
                failed += 1
                continue
            vals.append(run_stats.run_row(d)["collusion_index_2nd_half"])
        arms[cond] = np.array([v for v in vals if not np.isnan(v)])
    c, n = arms["comms"], arms["nocomms"]
    fail_rate = failed / total if total else 1.0
    if len(c) < 2 or len(n) < 2:
        decisions.append((tag, False, f"too few completed runs (comms {len(c)}, nocomms {len(n)}, failed {failed}/{total})", None))
        continue
    diffs = c[rng.integers(0, len(c), (10000, len(c)))].mean(1) - n[rng.integers(0, len(n), (10000, len(n)))].mean(1)
    lo = float(np.percentile(diffs, 5))
    ok = (c.mean() - n.mean() > 0) and lo > -0.05 and fail_rate <= 0.10
    msg = (f"comms {c.mean():+.3f} (n={len(c)}) vs nocomms {n.mean():+.3f} (n={len(n)}): diff {c.mean() - n.mean():+.3f}, "
           f"90% CI lower {lo:+.3f}; failed runs {failed}/{total}; cost/run ${costs.get(tag, float('nan')):.3f}")
    decisions.append((tag, ok, msg, costs.get(tag)))
for tag, ok, msg, _ in decisions:
    print(f"{'PASS' if ok else 'FAIL'}  {tag:<12} {msg}")
passing = [d for d in decisions if d[1]]
if passing:
    best = min(passing, key=lambda d: d[3] if d[3] is not None else 1e9)
    print(f"GATE: Phase O runs on '{best[0]}' (cheapest passing model)."
          + (" Both passed: Phase G replicates key levers on the other." if len(passing) > 1 else ""))
else:
    gaps = [(t, m) for t, ok, m, _ in decisions]
    print("GATE: no model passed. Per protocol: run Phase O on the model with the larger comms-nocomms gap "
          "and report the failed positive control prominently.")
