"""Minimum detectable effect (80% power, one-sided alpha 0.05, exact noncentral t) for a two-arm difference in
the second-half collusion index, using the 2025 gpt-4.1 spreads: comms SD against itself and against the ban.
Usage: python -X utf8 -I collusion_analysis/power.py   (prints the MDE range for n=10 and n=25 per arm)"""
import glob, math, os, sys
import numpy as np
from scipy.optimize import brentq
from scipy.stats import nct, t
sys.path.insert(0, os.path.dirname(__file__))
import run_stats


def sd(pat):
    rows = [run_stats.run_row(d) for d in sorted(glob.glob(pat)) if os.path.exists(os.path.join(d, "experiment_metadata.json"))]
    return float(np.std([r["collusion_index_2nd_half"] for r in rows], ddof=1))


def mde(sa, sb, n, alpha=0.05, power=0.8):
    se, df = math.sqrt(sa ** 2 / n + sb ** 2 / n), 2 * n - 2
    crit = t.ppf(1 - alpha, df)
    return brentq(lambda d: (1 - nct.cdf(crit, df, d / se)) - power, 1e-3, 5)


def ranges():
    s_comms, s_ban = sd("data/*_base-seller_comms-*/"), sd("data/*_base-[0-9]*/")
    return {n: sorted((mde(s_comms, s_ban, n), mde(s_comms, s_comms, n))) for n in (10, 25)}, s_comms, s_ban


if __name__ == "__main__":
    r, sc, sb = ranges()
    print(f"SD comms {sc:.2f}, SD ban {sb:.2f}")
    for n, (lo, hi) in r.items():
        print(f"n={n} per arm: MDE {lo:.2f} to {hi:.2f}")
