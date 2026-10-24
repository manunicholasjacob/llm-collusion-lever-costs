#!/usr/bin/env bash
# POST-SPRINT screen S1 (SPRINT_PROTOCOL.md section 11): comms-only runs of cheap model families, n per model,
# to nominate a model that colludes for the follow-up study. Runs land in results/ as lo-s1<tag>-comms-*;
# move them to results_postsprint/ after, so the sprint analyses (which count results/*_lo-*) are unchanged.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -z "${LOCAL_LLM_API_KEY:-}" ] && [ -f .env.local ]; then set -a; . ./.env.local; set +a; fi
: "${LOCAL_LLM_API_KEY:?put LOCAL_LLM_API_KEY in .env.local}"
export SKIP_LLM_JUDGE=1 WANDB_MODE=disabled BUDGET_USD="${BUDGET_USD:-53.90}"
N="${N:-3}"
for pair in qwen235:qwen/qwen3-235b-a22b-2507 gemflashlite:google/gemini-2.5-flash-lite mistralsmall:mistralai/mistral-small-3.2-24b-instruct; do
  export TAG_MODEL="s1${pair%%:*}" LLM_MODEL_MAP="gpt-4.1=${pair#*:},gpt-4.1-mini=openai/gpt-4.1-mini"
  bash collusion_analysis/run_sprint.sh comms "$N" "$N" || echo "[$TAG_MODEL] stopped (budget or errors)"
done
