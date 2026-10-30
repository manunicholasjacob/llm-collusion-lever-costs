"""The pre-registered F2 test, written before the data exists so it cannot be tuned to it.

SPRINT_PROTOCOL.md section 14, verbatim:
  Tests: ban < none and oversight25 < none on the second-half collusion index; one-sided
  bootstrap (10,000), Holm over two. A result counts as replicated if Holm p < 0.05 and the
  estimate has the same sign as in H2.
  Also reported: F1 H2 re-run with the pooled baseline (F0 + F2 none) as a sensitivity check,
  labelled as such.

The p estimator is the add-one bootstrap form the pre-registration specified and that
followup/analyze_f1.py uses, (1 + #{d >= 0}) / (1 + reps), so it matches H2's method exactly.

The stopping rule applies: if any arm is short of n=10, this script REFUSES to test and prints
what is missing, because section 13 says a short phase is topped up before any test is run.
Pass --allow-short only to see the descriptive table, which it then labels as untested.

Usage, from the public repository root:
  python -X utf8 -I <this script> [--allow-short]
"""

import glob
import os
import sys

import numpy as np

sys.path.insert(0, "collusion_analysis")
import run_stats  # noqa: E402

RESULTS = "results_followup"
ARMS = ["ban", "oversight25"]          # the two tested against `none`
N_TARGET = 10
REPS = 10000
rng = np.random.default_rng(0)

# H2's estimates, for the sign-agreement half of the replication criterion.
H2 = {"ban": -0.384, "oversight25": -0.500}


def rows(*pats):
    out = []
    for p in pats:
        for d in sorted(glob.glob(os.path.join(RESULTS, p))):
            if os.path.exists(os.path.join(d, "experiment_metadata.json")):
                out.append(run_stats.run_row(d))
    return out


def holm(pv):
    keys = sorted(pv, key=pv.get)
    adj, run = {}, 0.0
    for r, k in enumerate(keys):
        run = max(run, min(1.0, (len(keys) - r) * pv[k]))
        adj[k] = run
    return adj


def boot(a, b):
    """mean(a) - mean(b), 95% CI, and the one-sided add-one p for mean(a) >= mean(b)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = (a[rng.integers(0, len(a), (REPS, len(a)))].mean(1)
         - b[rng.integers(0, len(b), (REPS, len(b)))].mean(1))
    return (float(a.mean() - b.mean()), float(np.percentile(d, 2.5)),
            float(np.percentile(d, 97.5)), float((1 + (d >= 0).sum()) / (1 + len(d))))


def main():
    allow_short = "--allow-short" in sys.argv
    if not os.path.isdir(RESULTS):
        sys.exit(f"run this from the public repository root; {RESULTS}/ not found")

    arms = {"none": rows("*_fu2-none-*")}
    for a in ARMS:
        arms[a] = rows(f"*_fu2-{a}-*")

    print("F2 runs found")
    short = []
    for k, v in arms.items():
        flag = "" if len(v) >= N_TARGET else f"  SHORT by {N_TARGET - len(v)}"
        print(f"  fu2-{k:<12} n={len(v)}{flag}")
        if len(v) < N_TARGET:
            short.append(k)

    if short and not allow_short:
        print("\nNOT TESTING. Arms short of n=10:", ", ".join(short))
        print("Section 13's stopping rule: a short phase is topped up in the next session")
        print("before any test is run. Top up with a plan whose arms carry the right `start`,")
        print("then re-run this script. --allow-short prints the descriptive table only.")
        return 2

    print("\nDescriptive")
    print(f"  {'arm':<14}{'n':>3}{'index':>9}{'price':>9}{'trades':>8}{'welfare':>9}{'fired':>8}")
    for k, v in arms.items():
        if not v:
            continue
        g = lambda f: float(np.nanmean([r[f] for r in v]))
        fired = float(np.mean([r["gag_round"] is not None for r in v]))
        print(f"  {k:<14}{len(v):>3}{g('collusion_index_2nd_half'):>9.3f}"
              f"{g('trade_price'):>9.2f}{g('n_trades'):>8.1f}"
              f"{g('buyer_welfare_per_round'):>9.1f}{fired:>8.0%}")

    if short:
        print("\nUNTESTED: arms are short, so the table above is descriptive only.")
        return 2

    base = [r["collusion_index_2nd_half"] for r in arms["none"]]
    est, pv = {}, {}
    for a in ARMS:
        vals = [r["collusion_index_2nd_half"] for r in arms[a]]
        est[a] = boot(vals, base)
        pv[a] = est[a][3]
    adj = holm(pv)

    print("\nF2, PRE-REGISTERED: lever < none on the second-half index")
    print("  one-sided bootstrap, 10,000 resamples, Holm over two")
    print(f"  {'lever':<14}{'diff':>9}{'95% CI':>22}{'p':>9}{'Holm p':>9}  verdict")
    replicated = {}
    for a in ARMS:
        d, lo, hi, p = est[a]
        same_sign = (d < 0) == (H2[a] < 0)
        ok = adj[a] < 0.05 and same_sign
        replicated[a] = ok
        print(f"  {a:<14}{d:>+9.3f}  [{lo:>+7.3f}, {hi:>+7.3f}]{p:>9.4f}{adj[a]:>9.4f}  "
              f"{'REPLICATED' if ok else 'not replicated'}"
              f"{'' if same_sign else '  (SIGN DISAGREES with H2)'}")
    print(f"\n  H2 for comparison: ban {H2['ban']:+.3f}, oversight25 {H2['oversight25']:+.3f}")

    # Sensitivity: H2 re-run against the pooled baseline, labelled as such.
    f0 = [r["collusion_index_2nd_half"] for r in rows("*_fu0-instructed-*")]
    pooled = f0 + base
    print("\nSENSITIVITY, labelled: H2's F1 arms against the pooled baseline (F0 + F2 none)")
    print(f"  pooled baseline n={len(pooled)} "
          f"(F0 n={len(f0)} mean {np.mean(f0):+.3f}, F2 none n={len(base)} mean {np.mean(base):+.3f})")
    pv2 = {}
    est2 = {}
    for a in ["ban", "notice", "monitor", "oversight", "oversight25", "maverick"]:
        key = "collusion_index_2nd_half_llm" if a == "maverick" else "collusion_index_2nd_half"
        vals = [r[key] for r in rows(f"*_fu1a-{a}-*", f"*_fu1b-{a}-*")]
        if not vals:
            continue
        est2[a] = boot(vals, pooled)
        pv2[a] = est2[a][3]
    adj2 = holm(pv2)
    print(f"  {'lever':<14}{'diff':>9}{'95% CI':>22}{'Holm p':>9}")
    for a, (d, lo, hi, _) in est2.items():
        print(f"  {a:<14}{d:>+9.3f}  [{lo:>+7.3f}, {hi:>+7.3f}]{adj2[a]:>9.4f}")

    # A session effect was the reason F2 exists; report whether the baselines agree.
    d, lo, hi, _ = boot(base, f0)
    print(f"\n  Baseline session check: F2 none minus F0 instructed = {d:+.3f} "
          f"[{lo:+.3f}, {hi:+.3f}]")
    print("  A CI that excludes 0 means the declared session effect is real and the F1 H2")
    print("  values should be read against the F2 baseline instead.")

    return 0 if all(replicated.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
