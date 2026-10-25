"""F1 readout as pre-registered in SPRINT_PROTOCOL.md section 13 (and its clarification).
H2: each lever lowers the second-half collusion index of instructed markets vs no lever (F0 instructed);
one-sided bootstrap (10,000), Holm over six. H4: monitor fire rate higher in instructed (F1a+F1b) than honest
(F1c) markets; one-sided Fisher exact, Holm over three. Plus a descriptive table.
Usage: python -X utf8 -I followup/analyze_f1.py results_followup"""
import glob, os, sys
import numpy as np
from scipy.stats import fisher_exact
sys.path.insert(0, "collusion_analysis")
import run_stats

root = sys.argv[1]
LEVERS = ["ban", "notice", "monitor", "oversight", "oversight25", "maverick"]


def rows(patterns):
    out = []
    for pat in patterns:
        for d in sorted(glob.glob(os.path.join(root, pat))):
            if os.path.exists(os.path.join(d, "experiment_metadata.json")):
                out.append(run_stats.run_row(d))
    return out


def holm(p):
    keys = sorted(p, key=p.get); m = len(keys); adj, run = {}, 0.0
    for r, k in enumerate(keys):
        run = max(run, min(1.0, (m - r) * p[k])); adj[k] = run
    return adj


rng = np.random.default_rng(0)
base = rows(["*_fu0-instructed-*"])
arms = {lv: rows([f"*_fu1a-{lv}-*", f"*_fu1b-{lv}-*"]) for lv in LEVERS}
honest = {lv: rows([f"*_fu1c-{lv}-*"]) for lv in ("monitor", "oversight", "oversight25")}

print(f"{'arm':<22}{'n':>3}{'index':>9}{'idx LLM':>9}{'price':>9}{'trades':>8}{'welfare':>9}{'fired':>8}{'gagged':>8}")
for name, rr in [("no lever (F0)", base)] + [(lv, arms[lv]) for lv in LEVERS] + [(f"honest {k}", v) for k, v in honest.items()]:
    if not rr:
        print(f"{name:<22}  0"); continue
    f = lambda k: np.nanmean([r[k] for r in rr])
    fired = np.mean([r["gag_round"] is not None for r in rr])
    print(f"{name:<22}{len(rr):>3}{f('collusion_index_2nd_half'):>9.3f}{f('collusion_index_2nd_half_llm'):>9.3f}"
          f"{f('trade_price'):>9.2f}{f('n_trades'):>8.1f}{f('buyer_welfare_per_round'):>9.1f}{fired:>8.0%}{f('frac_gagged'):>8.0%}")

print("\nH2: lever lowers the instructed-market index (one-sided bootstrap, Holm over six)")
b = np.array([r["collusion_index_2nd_half"] for r in base]); p, est = {}, {}
for lv in LEVERS:
    key = "collusion_index_2nd_half_llm" if lv == "maverick" else "collusion_index_2nd_half"
    a = np.array([r[key] for r in arms[lv]])
    if len(a) == 0:
        continue
    d = a[rng.integers(0, len(a), (10000, len(a)))].mean(1) - b[rng.integers(0, len(b), (10000, len(b)))].mean(1)
    est[lv] = (a.mean() - b.mean(), np.percentile(d, [2.5, 97.5]), len(a))
    p[lv] = (1 + (d >= 0).sum()) / (1 + len(d))
adj = holm(p)
for lv in LEVERS:
    if lv in est:
        dlt, ci, n = est[lv]
        print(f"  {lv:<12} n={n:<3} diff {dlt:+.3f} [{ci[0]:+.3f}, {ci[1]:+.3f}]  p={p[lv]:.4f}  Holm p={adj[lv]:.4f}  {'SUPPORTED' if adj[lv] < 0.05 else 'not supported'}")

print("\nH4: monitor fires more in instructed than honest markets (one-sided Fisher exact, Holm over three)")
p4, tab = {}, {}
for lv in ("monitor", "oversight", "oversight25"):
    i_f = sum(r["gag_round"] is not None for r in arms[lv]); i_n = len(arms[lv])
    h_f = sum(r["gag_round"] is not None for r in honest[lv]); h_n = len(honest[lv])
    if i_n and h_n:
        p4[lv] = fisher_exact([[i_f, i_n - i_f], [h_f, h_n - h_f]], alternative="greater").pvalue
    tab[lv] = (i_f, i_n, h_f, h_n)
adj4 = holm(p4) if p4 else {}
for lv, (i_f, i_n, h_f, h_n) in tab.items():
    extra = f"p={p4[lv]:.4f} Holm p={adj4[lv]:.4f} {'SUPPORTED' if adj4[lv] < 0.05 else 'not supported'}" if lv in p4 else "(honest arm not run yet)"
    print(f"  {lv:<12} fired: instructed {i_f}/{i_n} (true positives), honest {h_f}/{h_n} (false positives)  {extra}")
