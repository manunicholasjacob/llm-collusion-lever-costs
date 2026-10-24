#!/usr/bin/env bash
# POST-SPRINT pilot P2 (SPRINT_PROTOCOL.md, logged before any run; not part of the sprint submission):
# does profit ("boss") pressure make Llama-3.3-70B sellers price above the competitive level, and does
# communication raise it? Runs land in results/ as lo-pbossllama-*; move them to results_postsprint/ after,
# so the sprint analyses (which count results/*_lo-*) are unchanged.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -z "${LOCAL_LLM_API_KEY:-}" ] && [ -f .env.local ]; then set -a; . ./.env.local; set +a; fi
: "${LOCAL_LLM_API_KEY:?put LOCAL_LLM_API_KEY in .env.local}"
export SKIP_LLM_JUDGE=1 WANDB_MODE=disabled TAG_MODEL=pbossllama BUDGET_USD="${BUDGET_USD:-53}"
export LLM_MODEL_MAP="gpt-4.1=meta-llama/llama-3.3-70b-instruct,gpt-4.1-mini=openai/gpt-4.1-mini"
N="${N:-6}"
bash collusion_analysis/run_sprint.sh boss-comms "$N" 6
bash collusion_analysis/run_sprint.sh boss-nocomms "$N" 6
