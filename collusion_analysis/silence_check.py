"""Exploratory (added 23 Oct after seeing A6, labelled exploratory in the report): is collusion
'informationally silent'? Per run: mean per-seller entropy of ask MOVES (down/flat/up, rounds 8-30)
and share of flat moves, against the primary collusion index and the LLM-judge score. Also reruns
the TE detector on moves instead of levels (stationary input) for the comms vs no-comms AUC."""
import glob, os, sys
import numpy as np
from scipy.stats import spearmanr, mannwhitneyu
sys.path.insert(0, os.path.dirname(__file__))
import detector_eval as D, net_influence as N, pipeline, run_stats

def moves(path):
    d = np.diff(np.asarray(path, float))
    return [0 if x < -0.005 else (2 if x > 0.005 else 1) for x in d]

def main():
    rows = []
    for g in sys.argv[1:]:
        for rd in sorted(glob.glob(g)):
            cfg, rounds = pipeline.load_run(rd)
            paths = {s: p[7:30] for s, p in D.ask_paths(rounds).items()}
            mv = {s: moves(p) for s, p in paths.items() if not np.isnan(p).any()}
            if len(mv) < 3: continue
            ent = np.mean([N._counts_entropy(m) for m in mv.values()])
            flat = np.mean([np.mean(np.array(m) == 1) for m in mv.values()])
            obs = D.mean_te(mv); T = len(next(iter(mv.values())))
            null = np.array([D.mean_te({s: x[-k:] + x[:-k] for s, x in mv.items() for k in [int(D.rng.integers(1, T))]}) for _ in range(200)])
            base = run_stats.run_row(rd)
            rows.append(dict(cond=pipeline.condition_of(rd), ent=ent, flat=flat, te_z=(obs - null.mean()) / (null.std() + 1e-12),
                             primary=base["collusion_index_2nd_half"], judge=base["judge_score"],
                             comms=cfg["seller_comms_enabled"], ov=cfg["oversight_enabled"], boss=cfg["boss_pressure"]))
    for k in ("ent", "flat"):
        for y in ("primary", "judge"):
            r = spearmanr([x[k] for x in rows], [x[y] for x in rows])
            print(f"Spearman {k:<4} vs {y:<7}: rho={r.statistic:+.3f} p={r.pvalue:.4f} (n={len(rows)})")
    for c in sorted({x['cond'] for x in rows}):
        v = [x for x in rows if x['cond'] == c]
        print(f"  {c:<26} n={len(v):>2} ask-move entropy={np.mean([x['ent'] for x in v]):.2f} bits  flat moves={np.mean([x['flat'] for x in v]):.0%}  primary={np.mean([x['primary'] for x in v]):+.2f}")
    t = [x['te_z'] for x in rows if x['comms'] and not x['ov'] and not x['boss']]; q = [x['te_z'] for x in rows if not x['comms'] and not x['boss']]
    u = mannwhitneyu(t, q, alternative="two-sided")
    print(f"TE on moves, comms vs no-comms: AUC={u.statistic/(len(t)*len(q)):.3f} p={u.pvalue:.4f}; median te_z comms={np.median(t):+.2f} nocomms={np.median(q):+.2f}")


if __name__ == "__main__":
    main()
