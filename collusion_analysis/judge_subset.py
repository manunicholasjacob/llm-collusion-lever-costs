"""Phase J (SPRINT_PROTOCOL.md, commit 677ed76): run the deferred gpt-4.1-mini judge on up to K runs per
condition for one model tag, stopping when the OpenRouter key's real usage reaches BUDGET_USD.
Usage: python -X utf8 -I collusion_analysis/judge_subset.py <model_tag> [K]   (env: routing + key as for runs)"""
import glob, json, os, sys, urllib.request
from pathlib import Path
sys.path.insert(0, os.getcwd())
os.environ.pop("SKIP_LLM_JUDGE", None)
from src.continuous_double_auction.evaluation.evaluate import compute_metrics_for_exp_dir, write_metrics_to_file

tag, k = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 4
budget = float(os.environ.get("BUDGET_USD", "46"))
url = os.environ.get("USAGE_URL") or os.environ["LOCAL_LLM_BASE_URL"].rstrip("/") + "/key"


def spent():
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {os.environ['LOCAL_LLM_API_KEY']}"})
    return float(json.load(urllib.request.urlopen(req, timeout=30))["data"]["usage"])


conds = sorted({os.path.basename(p).split("_", 2)[2].rsplit("-", 1)[0] for p in glob.glob(f"results/*_lo-{tag}-*")})
done = 0
for cond in conds:
    for d in sorted(glob.glob(f"results/*_{cond}-*"))[:k]:
        if os.path.exists(os.path.join(d, "llm_eval_full.json")) or not os.path.exists(os.path.join(d, "collusion_metrics.json")):
            continue
        if spent() >= budget:
            print(f"BUDGET STOP at ${spent():.2f}; judged {done} runs"); sys.exit(0)
        m = compute_metrics_for_exp_dir(Path(d)); write_metrics_to_file(Path(d), m); done += 1
        print(f"judged {os.path.basename(d)}")
print(f"judged {done} runs; spent ${spent():.2f}")
