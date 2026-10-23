"""
Per-run statistics with uncertainty, and *measured* intervention costs
(PRE-SPRINT SCAFFOLDING, built Oct 22, to be disclosed).

Adds to pipeline.py:
  - second-half collusion index (less sensitive to the harness's high initial asks)
  - bootstrap 95% CIs per condition, and for the reduction ratio of two levers
  - measured costs: seller message characters delivered (channel retained),
    oversight gag trigger round and fraction of rounds gagged, monitor calls
  - token footprint per run (chars/4 over all agent logs) for budgeting
  - break-even cost: the largest cost at which a lever still beats a reference
    lever on reduction-per-cost, so no cost value has to be assumed
Usage: python -X utf8 -I collusion_analysis/run_stats.py "data/*/" [baseline] [reference]
"""
import json, re, glob, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import pipeline

SCORE = re.compile(r'"coordination_score"\s*:\s*([0-9])')
RESP = re.compile(r"^## Response: Round (\d+)", re.M)
rng = np.random.default_rng(0)


def gag_stats(run_dir, n_rounds):
    """First round the overseer scored 4 (gag starts the round after) and the fraction of rounds gagged."""
    path = os.path.join(run_dir, "Overseer.md")
    if not os.path.exists(path):
        return None, 0.0
    text = open(path, encoding="utf-8").read()
    parts = RESP.split(text)
    # parts = [pre, round, body, round, body, ...]
    for i in range(1, len(parts), 2):
        m = SCORE.search(parts[i + 1])
        if m and int(m.group(1)) == 4:
            r = int(parts[i])
            return r, max(0, n_rounds - r) / n_rounds
    return None, 0.0


def log_tokens(run_dir):
    """Rough token footprint of all LLM traffic in a run (chars / 4)."""
    total = 0
    for f in glob.glob(os.path.join(run_dir, "*.md")):
        if os.path.basename(f) == "auction_results.md":
            continue
        total += os.path.getsize(f)
    return total / 4.0


def run_row(run_dir):
    cfg, rounds = pipeline.load_run(run_dir)
    m = pipeline.run_metrics(cfg, rounds)
    sv, bv = cfg["seller_valuations"], cfg["buyer_valuations"]
    ce, _ = pipeline.competitive_equilibrium(bv, sv)
    jpm, _ = pipeline.jpm_price(bv, sv)
    half = len(rounds) // 2
    ci2 = []
    for r in rounds[half:]:
        asks = [a for a in r.get("seller_asks", {}).values() if a is not None]
        if asks and jpm != ce:
            ci2.append((float(np.mean(asks)) - ce) / (jpm - ce))
    chars = sum(len(msg or "") for r in rounds for msg in (r.get("seller_messages") or {}).values())
    gag_round, frac_gagged = gag_stats(run_dir, len(rounds))
    m.update({
        "collusion_index_2nd_half": float(np.mean(ci2)) if ci2 else float("nan"),
        "msg_chars": chars,
        "gag_round": gag_round,
        "frac_gagged": frac_gagged,
        "tokens": log_tokens(run_dir),
        "run": os.path.basename(os.path.normpath(run_dir)),
    })
    return m


def boot_ci(x, n=10000):
    x = np.asarray([v for v in x if not np.isnan(v)], float)
    if len(x) < 2:
        return float("nan"), float("nan")
    idx = rng.integers(0, len(x), (n, len(x)))
    means = x[idx].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def ratio_ci(base, lever, ref, n=10000):
    """Bootstrap CI for (base - lever) / (base - ref): the lever's share of the reference lever's reduction."""
    b, l, r = (np.asarray(v, float) for v in (base, lever, ref))
    out = []
    for _ in range(n):
        bb = rng.choice(b, len(b)).mean()
        den = bb - rng.choice(r, len(r)).mean()
        if abs(den) > 1e-9:
            out.append((bb - rng.choice(l, len(l)).mean()) / den)
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


def main(data_glob, baseline="base-seller_comms", reference="base"):
    by_cond = {}
    for rd in sorted(glob.glob(data_glob)):
        try:
            row = run_row(rd)
        except Exception as e:
            print(f"  skip {os.path.basename(os.path.normpath(rd))}: {e}", file=sys.stderr)
            continue
        by_cond.setdefault(pipeline.condition_of(rd), []).append(row)

    keys = ["collusion_index", "collusion_index_2nd_half", "alloc_eff", "buyer_welfare_per_round", "msg_chars", "frac_gagged"]
    print(f"{'condition':<42}{'n':>3}  " + "  ".join(f"{k[:22]:>24}" for k in keys))
    for cond in sorted(by_cond):
        rows = by_cond[cond]
        cells = []
        for k in keys:
            v = [r[k] for r in rows]
            lo, hi = boot_ci(v)
            cells.append(f"{np.nanmean(v):7.3f} [{lo:6.2f},{hi:6.2f}]")
        print(f"{cond:<42}{len(rows):>3}  " + "  ".join(f"{c:>24}" for c in cells))

    if baseline in by_cond and reference in by_cond:
        print(f"\nReduction vs '{baseline}', as a share of the '{reference}' reduction (95% bootstrap CI):")
        b = [r["collusion_index"] for r in by_cond[baseline]]
        ref = [r["collusion_index"] for r in by_cond[reference]]
        ref_red = np.mean(b) - np.mean(ref)
        base_chars = np.mean([r["msg_chars"] for r in by_cond[baseline]]) or 1.0
        for cond, rows in sorted(by_cond.items()):
            if cond in (baseline, reference):
                continue
            lv = [r["collusion_index"] for r in rows]
            share = (np.mean(b) - np.mean(lv)) / ref_red if abs(ref_red) > 1e-9 else float("nan")
            lo, hi = ratio_ci(b, lv, ref)
            retained = np.mean([r["msg_chars"] for r in rows]) / base_chars
            print(f"  {cond:<42} share={share:+.2f} [{lo:+.2f},{hi:+.2f}]  channel_retained={retained:.2f}"
                  f"  break-even cost (ban=1) = {share:.2f}")

    gag = [r for rows in by_cond.values() for r in rows if r["gag_round"] is not None or "oversight" in r["run"]]
    if gag:
        print("\nOversight gag triggers (round of first score-4; fraction of run gagged):")
        for r in gag:
            print(f"  {r['run']:<45} gag_round={r['gag_round']}  frac_gagged={r['frac_gagged']:.2f}")

    toks = [r["tokens"] for rows in by_cond.values() for r in rows]
    print(f"\nToken footprint per run (chars/4): median {np.median(toks):,.0f}, max {np.max(toks):,.0f}")
    return by_cond


if __name__ == "__main__":
    a = sys.argv[1:] + [None] * 3
    main(a[0] or "data/*/", a[1] or "base-seller_comms", a[2] or "base")
