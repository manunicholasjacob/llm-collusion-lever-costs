"""Report tables, hypothesis tests and the per-run strip plot (PRE-SPRINT SCAFFOLDING, built Oct 22).
Implements SPRINT_PROTOCOL.md sections 3 and 5 so Sunday is one command:
  python -X utf8 -I collusion_analysis/report_tables.py OUTDIR [--pool] GLOB [GLOB ...]
Writes OUTDIR/table1.md, table1.csv, tests.md, strip_primary.png, ols_hc3.md.
"""
import os, sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import frontier, run_stats

PRIMARY = "collusion_index_2nd_half"
COLS = [(PRIMARY, "Primary index (rounds 16-30)"), ("collusion_index", "Whole-run index"),
        ("trade_price", "Mean trade price"), ("alloc_eff", "Allocative eff."),
        ("buyer_welfare_per_round", "Buyer welfare/round"), ("judge_score", "Judge score (1-4)"),
        ("frac_gagged", "Rounds gagged")]
rng = np.random.default_rng(1)


def vals(rows, k):
    return np.array([r[k] for r in rows if not np.isnan(r[k])], float)


def ci(x):
    if len(x) < 2:
        return float("nan"), float("nan")
    m = x[rng.integers(0, len(x), (10000, len(x)))].mean(axis=1)
    return np.percentile(m, 2.5), np.percentile(m, 97.5)


def boot_diff(a, b, n=10000):
    """Bootstrap distribution of mean(a) - mean(b)."""
    return a[rng.integers(0, len(a), (n, len(a)))].mean(1) - b[rng.integers(0, len(b), (n, len(b)))].mean(1)


def table1(by, base_key, out):
    base_chars = np.mean([r["msg_chars"] for r in by[base_key]]) or 1.0
    head = ["Condition", "n"] + [c[1] for c in COLS] + ["Channel loss"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    csv = [",".join(["condition", "n"] + [c[0] for c in COLS] + ["channel_loss"])]
    for cond in sorted(by):
        rows = by[cond]
        cells, raw = [], []
        for k, _ in COLS:
            x = vals(rows, k)
            if len(x) == 0:
                cells.append("n/a"); raw.append("")
                continue
            lo, hi = ci(x)
            cells.append(f"{x.mean():.2f} [{lo:.2f}, {hi:.2f}]" if len(x) > 1 else f"{x.mean():.2f}")
            raw.append(f"{x.mean():.4f}")
        loss = 1 - np.mean([r["msg_chars"] for r in rows]) / base_chars
        lines.append(f"| {frontier.LABEL.get(cond.split(' (')[0], cond)}{cond[len(cond.split(' (')[0]):]} | {len(rows)} | "
                     + " | ".join(cells) + f" | {max(0.0, loss):.2f} |")
        csv.append(",".join([cond, str(len(rows))] + raw + [f"{max(0.0, loss):.4f}"]))
    open(os.path.join(out, "table1.md"), "w", encoding="utf-8").write(
        "Table 1. Mean [95% bootstrap CI] per condition.\n\n" + "\n".join(lines) + "\n")
    open(os.path.join(out, "table1.csv"), "w", encoding="utf-8").write("\n".join(csv) + "\n")


def holm(ps):
    order = np.argsort(ps); adj = np.empty(len(ps)); run = 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - rank) * ps[i])); adj[i] = run
    return adj


def tests(by, sfx, out):
    """H1-H4 one-sided bootstrap tests on the primary index (Holm across the four), H5 two-sided."""
    def g(c, metric=PRIMARY):
        # Prefer the arm matching the baseline's data source; fall back to the other source
        # (e.g. boss pressure exists only in the 2025 data).
        for key in (c + sfx, c + " (sprint)", c + " (2025)", c):
            if key in by:
                return vals(by[key], metric)
        return None
    rows = []
    LLM = "collusion_index_2nd_half_llm"  # pre-registered primary for the maverick lever (LLM sellers only)
    # Holm family (commit 2040915): H1, H2, H2b, H-mav. H3/H4 belong to the superseded design and are
    # reported outside the family if their arms exist.
    spec = [("H1", "notice", "comms", "notice < comms", PRIMARY),
            ("H2", "monitor", "comms", "monitor < comms", PRIMARY),
            ("H2b", "oversight25", "comms", "oversight25 < comms", PRIMARY),
            ("H-mav", "maverick", "comms", "maverick < comms (LLM sellers only)", LLM),
            ("H3", "cap50", "comms", "cap50 < comms (outside family)", PRIMARY),
            ("H4", "boss-nocomms", "boss", "boss-nocomms within 0.05 of boss (outside family)", PRIMARY)]
    family = {"H1", "H2", "H2b", "H-mav"}
    ps, names = [], []
    for h, a, b, claim, metric in spec:
        A, B = g(a, metric), g(b, metric)
        if A is None or B is None or len(A) < 2 or len(B) < 2:
            rows.append(f"| {h} | {claim} | not run | | |"); continue
        d = boot_diff(A, B); lo, hi = np.percentile(d, [2.5, 97.5])
        if h == "H4":
            p = float(np.mean(np.abs(d) >= 0.05))  # share of bootstrap mass outside the equivalence band
        else:
            p = float(np.mean(d >= 0))
        if h in family:
            ps.append(p); names.append(h)
        rows.append(f"| {h} | {claim} | {A.mean() - B.mean():+.3f} [{lo:+.3f}, {hi:+.3f}] | {p:.4f} | "
                    + (f"HOLM_{h} |" if h in family else "unadjusted (outside family) |"))
    adj = dict(zip(names, holm(np.array(ps)))) if ps else {}
    for h, p in adj.items():  # match the whole token so HOLM_H2 never eats part of HOLM_H2b
        rows = [r.replace(f"HOLM_{h} |", f"{p:.4f} |") for r in rows]
    s, o = by.get("comms (sprint)"), by.get("comms (2025)")
    if s and o and len(s) > 1:
        d = boot_diff(vals(s, PRIMARY), vals(o, PRIMARY)); lo, hi = np.percentile(d, [2.5, 97.5])
        verdict = "pool" if lo <= 0 <= hi else "do NOT pool"
        rows.append(f"| H5 | sprint comms vs 2025 comms (drift) | {d.mean():+.3f} [{lo:+.3f}, {hi:+.3f}] | | {verdict} |")
    open(os.path.join(out, "tests.md"), "w", encoding="utf-8").write(
        "Pre-registered tests (difference of means [95% bootstrap CI]; one-sided bootstrap p; Holm over the family "
        "H1, H2, H2b, H-mav per commit 2040915; H-mav uses the LLM-sellers-only index).\n\n"
        "| Test | Claim | Difference | p | Holm p / decision |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n")


def strip(by, out):
    conds = sorted(by, key=lambda c: np.mean(vals(by[c], PRIMARY)) if len(vals(by[c], PRIMARY)) else 0)
    fig, ax = plt.subplots(figsize=(7.5, 0.45 * len(conds) + 1.4))
    for i, c in enumerate(conds):
        x = vals(by[c], PRIMARY)
        ax.scatter(x, i + rng.uniform(-0.12, 0.12, len(x)), s=22, alpha=.75,
                   color="#A8341F" if c.startswith("boss") else "#B45309", zorder=3)
        if len(x):
            ax.plot([x.mean()] * 2, [i - .3, i + .3], color="#222", lw=2)
    ax.set_yticks(range(len(conds)))
    ax.set_yticklabels([f"{frontier.LABEL.get(c.split(' (')[0], c)}{c[len(c.split(' (')[0]):]}" for c in conds], fontsize=8)
    ax.axvline(0, color="#999", lw=1, ls="--"); ax.axvline(1, color="#999", lw=1, ls=":")
    ax.set_xlabel("Collusion index, rounds 16-30  (0 = competitive price, 1 = joint-profit price; bar = mean)")
    ax.grid(axis="x", alpha=.25); fig.tight_layout()
    fig.savefig(os.path.join(out, "strip_primary.png"), dpi=160)


def ols_hc3(by, base_key, out):
    """Pooled OLS of the per-run primary index on condition dummies (baseline = comms), HC3 errors."""
    conds = [c for c in sorted(by) if c != base_key]
    y, X = [], []
    for c in [base_key] + conds:
        for v in vals(by[c], PRIMARY):
            y.append(v); X.append([1.0] + [1.0 if c == k else 0.0 for k in conds])
    y, X = np.array(y), np.array(X)
    XtX_inv = np.linalg.pinv(X.T @ X); beta = XtX_inv @ X.T @ y; e = y - X @ beta
    h = np.einsum("ij,jk,ik->i", X, XtX_inv, X)
    cov = XtX_inv @ (X.T * (e / (1 - np.clip(h, 0, 0.999))) ** 2) @ X @ XtX_inv
    se = np.sqrt(np.diag(cov))
    lines = ["| Term | Coef | HC3 SE | 95% CI |", "|---|---|---|---|"]
    for name, b, s in zip(["(intercept) " + base_key] + conds, beta, se):
        lines.append(f"| {name} | {b:+.3f} | {s:.3f} | [{b - 1.96 * s:+.3f}, {b + 1.96 * s:+.3f}] |")
    open(os.path.join(out, "ols_hc3.md"), "w", encoding="utf-8").write(
        f"Robustness: pooled OLS of the primary index on condition dummies, n={len(y)} runs.\n\n" + "\n".join(lines) + "\n")


def main(argv):
    out = argv[0]; rest = argv[1:]
    pool = "--pool" in rest
    suffix = rest[rest.index("--suffix") + 1] if "--suffix" in rest else None  # e.g. llama70b for lo-llama70b-* runs
    globs = [a for a in rest if a not in ("--pool", "--suffix", suffix)]
    os.makedirs(out, exist_ok=True)
    by = frontier.collect(globs, pool)
    sfx = f" ({suffix})" if suffix else ("" if pool else (" (sprint)" if "comms (sprint)" in by else " (2025)"))
    base_key = "comms" + sfx
    if base_key not in by:
        sys.exit(f"no baseline '{base_key}' among {sorted(by)}")
    table1(by, base_key, out); tests(by, sfx, out); strip(by, out); ols_hc3(by, base_key, out)
    for f in ("table1.md", "tests.md", "ols_hc3.md"):
        print(open(os.path.join(out, f), encoding="utf-8").read())
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1:])
