"""F1 (SPRINT_PROTOCOL.md, specified in commit 45ce6ad before Phase O data): how often does the LLM monitor
fire, how early, and how much message channel does it cost, per monitoring arm and model family. With the
llama70b positive control failed, every firing there is a false positive (no collusion to prevent).
Usage: python -X utf8 -I collusion_analysis/f1_monitor.py OUT.md"""
import glob, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import pipeline, run_stats

ARMS = [("gpt-4.1 (2025)", "oversight", "data/*_oversight-[0-9]*/", "data/*_base-seller_comms-*/"),
        ("gpt-4.1 (2025)", "boss + oversight", "data/*_boss_pressure-oversight-*/", "data/*_base-seller_comms-*/"),
        ("llama70b", "oversight", "results/*_lo-llama70b-oversight-[0-9]*/", "results/*_lo-llama70b-comms-*/"),
        ("llama70b", "monitor only", "results/*_lo-llama70b-monitor-*/", "results/*_lo-llama70b-comms-*/"),
        ("llama70b", "oversight, 25% sampling", "results/*_lo-llama70b-oversight25-*/", "results/*_lo-llama70b-comms-*/")]


def rows(pattern, cond_exact=None):
    out = []
    for d in sorted(glob.glob(pattern)):
        if not os.path.exists(os.path.join(d, "auction_results.md")) or not os.path.exists(os.path.join(d, "experiment_metadata.json")):
            continue
        out.append(run_stats.run_row(d))
    return out


lines = ["F1: monitor firing per arm. For llama70b the positive control failed (no collusion), so every firing "
         "is a false positive.\n", "| Model | Arm | n | Runs where monitor fired | Median first-fire hour | "
         "Rounds gagged (mean) | Channel retained vs comms |", "|---|---|---|---|---|---|---|"]
for model, arm, pat, comms_pat in ARMS:
    r = rows(pat)
    if not r:
        lines.append(f"| {model} | {arm} | 0 | not run yet | | | |"); continue
    base = np.mean([x["msg_chars"] for x in rows(comms_pat)] or [np.nan])
    fired = [x for x in r if x["gag_round"] is not None]
    med = np.median([x["gag_round"] for x in fired]) if fired else float("nan")
    lines.append(f"| {model} | {arm} | {len(r)} | {len(fired)}/{len(r)} ({100 * len(fired) / len(r):.0f}%) | "
                 f"{med:.0f} | {100 * np.mean([x['frac_gagged'] for x in r]):.0f}% | "
                 f"{np.mean([x['msg_chars'] for x in r]) / base:.0%} |")
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
