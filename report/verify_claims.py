"""Recompute every hand-typed number in REPORT_DRAFT.md from the raw runs and check the report states it.
Usage: python -X utf8 -I report/verify_claims.py   (exit 1 if any claim is missing or wrong)"""
import csv, glob, json, os, re, sys
import numpy as np
from scipy.stats import mannwhitneyu, spearmanr, binomtest
sys.path.insert(0, "collusion_analysis")
import pipeline, run_stats, detector_eval as D

R = open("report/REPORT_DRAFT.md", encoding="utf-8").read()
results = []


def claim(name, text, ok=True):
    results.append((name, text, (text in R) and ok))


def runs(pat):
    return [d for d in sorted(glob.glob(pat)) if os.path.exists(os.path.join(d, "experiment_metadata.json"))]


def rows(pat):
    return [run_stats.run_row(d) for d in runs(pat)]


def mean(pat, k):
    return float(np.mean([r[k] for r in rows(pat)]))


def talk(pat):
    rx = re.compile(r"monitor|oversight|regulat|collu|licen|compliance|fair (trading|practice)", re.I)
    shares = []
    for d in runs(pat):
        _, rr = pipeline.load_run(d)
        m = [x for r in rr for x in (r.get("seller_messages") or {}).values() if x]
        shares.append(np.mean([bool(rx.search(x)) for x in m]))
    return float(np.mean(shares))


C25 = {"comms": "data/*_base-seller_comms-*/", "ban": "data/*_base-[0-9]*/", "ov": "data/*_oversight-[0-9]*/",
       "bo": "data/*_boss_pressure-oversight-*/"}
# --- 2025 audit ---
ov = rows(C25["ov"]) + rows(C25["bo"])
g = [r["gag_round"] for r in ov]
claim("gag 20/20", "triggered in 20 of 20 oversight runs", all(x is not None for x in g) and len(g) == 20)
claim("gag onset 1-7", "first at hours 1 to 7", min(g) == 1 and max(g) == 7)
fr = [r["frac_gagged"] for r in ov]
claim("gagged 77-97%", "77 to 97%", round(min(fr) * 100) == 77 and round(max(fr) * 100) == 97)
base_chars = mean(C25["comms"], "msg_chars")
claim("10% chars", "only 10% of message characters", round(100 * mean(C25["ov"], "msg_chars") / base_chars) == 10)
claim("2025 welfare", "(27.2 versus 19.8 per round)",
      f"{mean(C25['ov'], 'buyer_welfare_per_round'):.1f}" == "27.2" and f"{mean(C25['comms'], 'buyer_welfare_per_round'):.1f}" == "19.8")
loss = 1 - mean(C25["ov"], "msg_chars") / base_chars
for k, val in (("collusion_index", "0.82"), ("collusion_index_2nd_half", "1.26")):
    red_ov = mean(C25["comms"], k) - mean(C25["ov"], k); red_ban = mean(C25["comms"], k) - mean(C25["ban"], k)
    claim(f"ratio {k}", "0.82 to 1.26", f"{(red_ov / loss) / red_ban:.2f}" == val)
sd = np.std([r["collusion_index_2nd_half"] for r in rows(C25["comms"])], ddof=1)
claim("SD 0.42", "(SD 0.42)", f"{sd:.2f}" == "0.42")
claim("ban effect 0.28", "(0.28)", f"{mean(C25['comms'], 'collusion_index_2nd_half') - mean(C25['ban'], 'collusion_index_2nd_half'):.2f}" == "0.28")
import power
(pr, _, _) = power.ranges()
claim("power n=10", "0.42 to 0.49 index units", [f"{x:.2f}" for x in pr[10]] == ["0.42", "0.49"])
claim("power n=25", "detects 0.26 to 0.30", [f"{x:.2f}" for x in pr[25]] == ["0.26", "0.30"])
# --- pilot ---
for tag, a, b in (("pllama70b", "-0.006", "+0.024"), ("pmini41", "-0.54", "-0.48")):
    c = mean(f"results/*_lo-{tag}-comms-*/", "collusion_index_2nd_half"); n = mean(f"results/*_lo-{tag}-nocomms-*/", "collusion_index_2nd_half")
    fmt = "{:+.3f}" if tag == "pllama70b" else "{:+.2f}"
    claim(f"pilot {tag}", a, fmt.format(c) == a and fmt.format(n) == b)
claim("pilot sizes", "6 plus 6 runs of Llama-3.3-70B, 3 plus 3 of GPT-4.1-mini",
      [len(runs(f"results/*_lo-{t}-*/")) for t in ("pllama70b-comms", "pllama70b-nocomms", "pmini41-comms", "pmini41-nocomms")] == [6, 6, 3, 3])
claim("mini n", "(-0.54 versus -0.48, n=3 each)")
# --- Phase O levels / talk / rank ---
L = lambda lv: f"results/*_lo-llama70b-{lv}-[0-9]*/"
claim("81 trades", "81 trades per run", round(mean(L("comms"), "n_trades")) == 81)
claim("welfare 25.3", "buyer welfare 25.3 per round", f"{mean(L('comms'), 'buyer_welfare_per_round'):.1f}" == "25.3")
claim("talk 28 vs 3", "28% of their messages mentioning monitoring or regulation, compared with 3%",
      round(100 * talk(L("notice"))) == 28 and round(100 * talk(L("comms"))) == 3)
claim("maverick price -1.41", "$1.41", f"{mean(L('comms'), 'trade_price') - mean(L('maverick'), 'trade_price'):.2f}" == "1.41")
t_n = [r["n_trades"] for r in rows(L("notice"))]; t_c = [r["n_trades"] for r in rows(L("comms"))]
p = mannwhitneyu(t_n, t_c, alternative="two-sided").pvalue
claim("rank test", "median 60 versus 82 trades, Mann-Whitney p=0.005",
      np.median(t_n) == 60 and np.median(t_c) == 82 and f"{p:.3f}" == "0.005")
for lv, pct, txt in (("notice", 22, "by 22%"), ("nocomms", 13, "13% of trades"), ("maverick", 26, "by 26%")):
    k = "n_trades" if lv == "nocomms" else "buyer_welfare_per_round"
    claim(f"pct {lv}", txt, round(100 * abs(mean(L(lv), k) - mean(L("comms"), k)) / mean(L("comms"), k)) == pct)
# --- C2 ---
Q = lambda lv: f"results/*_lo-llamaR-{lv}-[0-9]*/"
w = {lv: mean(Q(lv), "buyer_welfare_per_round") for lv in ("comms", "notice", "maverick")}
claim("16 to 22%", "reduced buyer welfare by 16 to 22%", round(100 * (w["comms"] - w["notice"]) / w["comms"]) == 16
      and round(100 * (mean(L("comms"), "buyer_welfare_per_round") - mean(L("notice"), "buyer_welfare_per_round")) / mean(L("comms"), "buyer_welfare_per_round")) == 22)
claim("C2 levels", "19.7 and 19.1", f"{mean(L('notice'), 'buyer_welfare_per_round'):.1f}" == "19.7" and f"{w['notice']:.1f}" == "19.1")
claim("C2 maverick levels", "32.0 and 32.8", f"{mean(L('maverick'), 'buyer_welfare_per_round'):.1f}" == "32.0" and f"{w['maverick']:.1f}" == "32.8")
claim("C2 baselines", "(25.3 and 22.8)", f"{w['comms']:.1f}" == "22.8")
claim("C2 prices", "$91.88 versus $90.49", f"{mean(Q('notice'), 'trade_price'):.2f}" == "91.88" and f"{mean(Q('comms'), 'trade_price'):.2f}" == "90.49")
claim("C2 talk", "(17% versus 8% of messages)", round(100 * talk(Q("notice"))) == 17 and round(100 * talk(Q("comms"))) == 8)
temps = {json.load(open(os.path.join(d, "experiment_metadata.json")))["auction_config"]["temperature"] for d in runs("results/2026*_lo-*")}
claim("temperature 0.7", "at temperature 0.7", temps == {0.7})
claim("268 runs", "268 sprint runs", len(runs("results/2026*_lo-*")) == 268)
# --- detectors and judge (2025 runs) ---
det = list(csv.DictReader(open("figs/detector_whole/detector_runs.csv", encoding="utf-8")))
nul = [r for r in det if r["cond"] == "base"]; com = [r for r in det if r["cond"] == "base-seller_comms"]
claim("Bonjour 70%", "flags 70% of no-communication runs", round(100 * np.mean([int(r["ni_flags"]) > 0 for r in nul])) == 70)
ok = True
for st in ("te_z", "ni_max"):
    nv = np.array([float(r[st]) for r in nul]); cv = np.array([float(r[st]) for r in com])
    ok &= int(np.sum(cv > np.percentile(nv, 90))) == 4
claim("calibrated 4/10", "each detect 4 of 10 communication runs at a 10% false-positive rate", ok)
rh, neg = [], 0
for d in runs("data/*_base-seller_comms-*/"):
    _, rr = pipeline.load_run(d)
    idx = np.array([np.mean([a for a in r["seller_asks"].values() if a is not None]) if r["seller_asks"] else np.nan for r in rr])
    by = {}
    for s in json.load(open(os.path.join(d, "llm_eval_full.json"), encoding="utf-8")):
        for r in s["rounds"]:
            sc = (r.get("data") or {}).get("score")
            if isinstance(sc, (int, float)): by.setdefault(r["round"], []).append(sc)
    j = np.array([np.mean(by.get(t, [np.nan])) for t in range(1, len(rr) + 1)]); m = ~np.isnan(j) & ~np.isnan(idx)
    if np.std(j[m]) > 0 and np.std(idx[m]) > 0: rh.append(spearmanr(j[m], idx[m]).statistic)
rh = np.array(rh); neg = int((rh < 0).sum())
claim("A7", "10 of 10 runs (mean within-run rho -0.52, sign test p=0.002)",
      neg == 10 and len(rh) == 10 and f"{rh.mean():.2f}" == "-0.52" and f"{binomtest(neg, 10, .5).pvalue:.3f}" == "0.002")
bad = [r for r in results if not r[2]]
for n, t, okk in results:
    print(("OK   " if okk else "FAIL ") + n)
print(f"\n{len(results)} claims checked, {len(bad)} failed")
sys.exit(1 if bad else 0)
