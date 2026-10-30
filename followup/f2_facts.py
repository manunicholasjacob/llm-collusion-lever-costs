"""Recompute every F2 number the paper will quote, into f2_facts.json.

Companion to sc4ai_facts.py. Run from the PUBLIC REPOSITORY ROOT, the same place
f2_test.py runs from, because it reads results_followup/ through run_stats.

  cd <public-repo> && python -X utf8 <this script>

Nothing here is typed by hand. The estimator is the add-one one-sided bootstrap the
pre-registration specified, identical to f2_test.py and followup/analyze_f1.py, so F2
and H2 are computed the same way and are comparable.
"""

import glob
import json
import os
import sys
import zlib

import numpy as np

sys.path.insert(0, "collusion_analysis")
import run_stats  # noqa: E402

RESULTS = "results_followup"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "f2_facts.json")
REPS = 10000


def _rng(label):
    """A stream of its own per comparison, keyed by name.

    A single shared generator makes every number depend on call order: adding one analysis
    silently moves the draws of every later one. That happened here when the honest-stability
    check went in, and it moved a labelled sensitivity figure in the third decimal. Keying the
    seed to the comparison's name makes each figure reproducible on its own.
    """
    # NOT hash(): Python randomises str hashing per process unless PYTHONHASHSEED is set,
    # which would make this script non-reproducible by default. crc32 is stable forever.
    return np.random.default_rng(zlib.crc32(label.encode()))

# H2's published estimates, from facts.json, for the sign-agreement criterion.
H2 = {"ban": -0.38442099999999996, "oversight25": -0.5001146666666666}
H2_HOLM = {"ban": 0.0164983501649835, "oversight25": 0.0005999400059994001}


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


def boot(a, b, label):
    """mean(a) - mean(b), 95% CI, and the one-sided add-one p for mean(a) >= mean(b)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    rng = _rng(label)
    d = (a[rng.integers(0, len(a), (REPS, len(a)))].mean(1)
         - b[rng.integers(0, len(b), (REPS, len(b)))].mean(1))
    return {"diff": float(a.mean() - b.mean()),
            "ci_lo": float(np.percentile(d, 2.5)),
            "ci_hi": float(np.percentile(d, 97.5)),
            "p": float((1 + (d >= 0).sum()) / (1 + len(d)))}


def descr(rs):
    v = np.array([r["collusion_index_2nd_half"] for r in rs], float)
    g = lambda f: float(np.nanmean([r[f] for r in rs]))
    return {"n": len(rs),
            "index_mean": float(v.mean()), "index_sd": float(v.std(ddof=1)),
            "index_median": float(np.median(v)),
            "index_min": float(v.min()), "index_max": float(v.max()),
            "trade_price": g("trade_price"), "n_trades": g("n_trades"),
            "buyer_welfare_per_round": g("buyer_welfare_per_round"),
            "n_fired": int(sum(r["gag_round"] is not None for r in rs)),
            "fire_rate": float(np.mean([r["gag_round"] is not None for r in rs]))}


def main():
    if not os.path.isdir(RESULTS):
        sys.exit(f"run from the public repository root; {RESULTS}/ not found")

    arms = {k: rows(f"*_fu2-{k}-*") for k in ("none", "ban", "oversight25")}
    f0 = rows("*_fu0-instructed-*")

    short = [k for k, v in arms.items() if len(v) < 10]
    if short:
        sys.exit("arms short of n=10, the stopping rule forbids testing: " + ", ".join(short))

    f = {"phase": "F2", "n_runs": sum(len(v) for v in arms.values()),
         "stack": {"vllm": "0.32.0", "model": "Qwen/Qwen2.5-7B-Instruct-AWQ",
                   "gpus": "2x Tesla T4", "servers": 2, "seed": 0,
                   "note": "no serving-stack version was recorded for F0 or F1, so the "
                           "baseline shift below cannot be attributed to a version change "
                           "or ruled out as one"},
         "arms": {k: descr(v) for k, v in arms.items()},
         "f0_instructed": descr(f0)}

    # The pre-registered test: lever < none, within F2, one-sided, Holm over two.
    base = [r["collusion_index_2nd_half"] for r in arms["none"]]
    est = {a: boot([r["collusion_index_2nd_half"] for r in arms[a]], base, f"prereg/{a}")
           for a in ("ban", "oversight25")}
    adj = holm({a: est[a]["p"] for a in est})
    f["prereg"] = {}
    for a, e in est.items():
        e = dict(e)
        e["holm_p"] = adj[a]
        e["h2_diff"] = H2[a]
        e["h2_holm_p"] = H2_HOLM[a]
        e["sign_agrees_with_h2"] = (e["diff"] < 0) == (H2[a] < 0)
        e["replicated"] = bool(adj[a] < 0.05 and e["sign_agrees_with_h2"])
        # Power matters: a null at n=10 is not proof of no effect. State instead whether
        # F2's interval actually excludes the effect size H2 reported.
        e["h2_effect_excluded_by_f2_ci"] = bool(H2[a] < e["ci_lo"])
        e["margin_to_h2"] = float(e["ci_lo"] - H2[a])
        f["prereg"][a] = e
    f["any_replicated"] = any(v["replicated"] for v in f["prereg"].values())

    # Why: the baseline itself moved between sessions.
    f["baseline_shift"] = boot(base, [r["collusion_index_2nd_half"] for r in f0],
                               "baseline_shift")
    f["baseline_shift"]["f2_none_mean"] = float(np.mean(base))
    f["baseline_shift"]["f0_instructed_mean"] = float(
        np.mean([r["collusion_index_2nd_half"] for r in f0]))
    f["baseline_shift"]["excludes_zero"] = bool(
        f["baseline_shift"]["ci_hi"] < 0 or f["baseline_shift"]["ci_lo"] > 0)

    # Is the shift specific to the INSTRUCTED condition? The honest arms ran in their own
    # session too (F1c, 25 Oct 10:08-18:50, separate from F1a/F1b at 03:11-09:00), so the
    # same non-concurrency applies to the AUC result and has to be checked, not assumed.
    hon = {"f0_honest": rows("*_fu0-honest-*")}
    for a in ("monitor", "oversight", "oversight25"):
        hon["f1c_" + a] = rows(f"*_fu1c-{a}-*")
    f["honest_stability"] = {
        k: {"n": len(v),
            "index_mean": float(np.mean([r["collusion_index_2nd_half"] for r in v]))}
        for k, v in hon.items() if v}
    f0h = [r["collusion_index_2nd_half"] for r in hon["f0_honest"]]
    f1ch = [r["collusion_index_2nd_half"] for r in hon["f1c_monitor"]]
    f["honest_stability"]["f1c_monitor_minus_f0_honest"] = boot(f1ch, f0h, "honest_shift")

    # How much of each H2 effect the baseline shift alone accounts for.
    shift = f["baseline_shift"]["diff"]
    f["accounted"] = {a: {"h2_diff": H2[a], "baseline_shift": shift,
                          "share_of_h2_effect": float(shift / H2[a]),
                          "residual": float(H2[a] - shift)}
                      for a in H2}

    # Sensitivity, pre-registered and labelled as such: H2's arms against the pooled baseline.
    pooled = base + [r["collusion_index_2nd_half"] for r in f0]
    sens, pv = {}, {}
    for a in ("ban", "notice", "monitor", "oversight", "oversight25", "maverick"):
        key = "collusion_index_2nd_half_llm" if a == "maverick" else "collusion_index_2nd_half"
        vals = [r[key] for r in rows(f"*_fu1a-{a}-*", f"*_fu1b-{a}-*")]
        if not vals:
            continue
        sens[a] = boot(vals, pooled, f"sensitivity/{a}")
        sens[a]["n"] = len(vals)
        pv[a] = sens[a]["p"]
    adj2 = holm(pv)
    for a in sens:
        sens[a]["holm_p"] = adj2[a]
        sens[a]["supported"] = bool(adj2[a] < 0.05 and sens[a]["diff"] < 0)
    f["sensitivity_pooled_baseline"] = {"pooled_n": len(pooled),
                                        "pooled_mean": float(np.mean(pooled)),
                                        "levers": sens}

    json.dump(f, open(OUT, "w", encoding="utf-8"), indent=1, sort_keys=True)

    # Print what the paper will quote.
    print(f"F2: {f['n_runs']} runs, 10 per arm. vLLM {f['stack']['vllm']} on {f['stack']['gpus']}\n")
    print(f"  {'arm':<14}{'n':>3}{'index':>8}{'sd':>7}{'price':>8}{'trades':>8}{'fired':>7}")
    for k in ("none", "ban", "oversight25"):
        a = f["arms"][k]
        print(f"  {k:<14}{a['n']:>3}{a['index_mean']:>8.3f}{a['index_sd']:>7.3f}"
              f"{a['trade_price']:>8.2f}{a['n_trades']:>8.1f}{a['fire_rate']:>7.0%}")
    a = f["f0_instructed"]
    print(f"  {'F0 instructed':<14}{a['n']:>3}{a['index_mean']:>8.3f}{a['index_sd']:>7.3f}"
          f"{a['trade_price']:>8.2f}{a['n_trades']:>8.1f}{a['fire_rate']:>7.0%}")

    print("\nPRE-REGISTERED F2 TEST, lever < none inside F2")
    print(f"  {'lever':<14}{'F2 diff':>9}{'95% CI':>22}{'Holm p':>9}   {'H2 diff':>8}{'H2 Holm p':>11}")
    for a, e in f["prereg"].items():
        print(f"  {a:<14}{e['diff']:>+9.3f}  [{e['ci_lo']:>+7.3f}, {e['ci_hi']:>+7.3f}]"
              f"{e['holm_p']:>9.4f}   {e['h2_diff']:>+8.3f}{e['h2_holm_p']:>11.4f}"
              f"  {'REPLICATED' if e['replicated'] else 'NOT replicated'}"
              f"{'' if e['sign_agrees_with_h2'] else ', sign disagrees'}")
    print("  Does F2's interval exclude the effect H2 reported?")
    for a, e in f["prereg"].items():
        print(f"    {a:<14} H2 {e['h2_diff']:+.3f} vs F2 CI lower bound {e['ci_lo']:+.3f}: "
              f"{'EXCLUDED' if e['h2_effect_excluded_by_f2_ci'] else 'not excluded'}"
              f" (margin {e['margin_to_h2']:+.3f})")

    b = f["baseline_shift"]
    print(f"\nBASELINE SHIFT, F2 none minus F0 instructed = {b['diff']:+.3f} "
          f"[{b['ci_lo']:+.3f}, {b['ci_hi']:+.3f}], p={b['p']:.4f}")
    print(f"  F2 none mean {b['f2_none_mean']:+.3f}, F0 instructed mean "
          f"{b['f0_instructed_mean']:+.3f}, CI excludes zero: {b['excludes_zero']}")
    print("\nHow much of each H2 effect the baseline shift alone accounts for")
    for a, v in f["accounted"].items():
        print(f"  {a:<14} H2 {v['h2_diff']:+.3f}, shift {v['baseline_shift']:+.3f}, "
              f"{v['share_of_h2_effect']:.0%} of it, residual {v['residual']:+.3f}")

    h = f["honest_stability"]
    print()
    print("IS THE SHIFT SPECIFIC TO THE INSTRUCTED CONDITION? honest arms across sessions")
    for k in ("f0_honest", "f1c_monitor", "f1c_oversight", "f1c_oversight25"):
        if k in h:
            print(f"  {k:<22} n={h[k]['n']:<3} index {h[k]['index_mean']:+.3f}")
    d = h["f1c_monitor_minus_f0_honest"]
    print(f"  F1c honest-monitor minus F0 honest = {d['diff']:+.3f} "
          f"[{d['ci_lo']:+.3f}, {d['ci_hi']:+.3f}]")

    s = f["sensitivity_pooled_baseline"]
    print(f"\nSENSITIVITY, labelled: F1 arms against the pooled baseline "
          f"(n={s['pooled_n']}, mean {s['pooled_mean']:+.3f})")
    for a, e in s["levers"].items():
        print(f"  {a:<14}{e['diff']:>+9.3f}  [{e['ci_lo']:>+7.3f}, {e['ci_hi']:>+7.3f}]"
              f"{e['holm_p']:>9.4f}  {'supported' if e['supported'] else ''}")

    print(f"\nwrote {os.path.abspath(OUT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
