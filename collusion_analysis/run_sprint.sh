#!/usr/bin/env bash
# Sprint runner (PRE-SPRINT SCAFFOLDING, built Oct 22). Runs N replicates of one condition
# in the authors' reference configuration (5 sellers at $80, 5 buyers at $100, 30 rounds)
# so new runs are comparable with their n=10 gpt-4.1 data in data/.
#
# Usage:  bash collusion_analysis/run_sprint.sh <condition> <n> [parallel]
# Env:    OPENAI_API_KEY (required), MODEL (default gpt-4.1), BUDGET_USD (default 50),
#         PRICE_IN / PRICE_OUT in $ per 1M tokens (default 2 / 8, gpt-4.1)
# Conditions:
#   comms         seller comms on (positive control / drift check vs. data/*base-seller_comms*)
#   nocomms       comms ban
#   oversight     notice + monitor/gag (authors' oversight)
#   notice        monitoring notice only, no monitor   (NEW lever)
#   monitor       monitor/gag only, no notice          (NEW lever)
#   cap50         static 50-character message cap      (NEW lever)
#   seltemp       seller-only temperature 1.2          (NEW lever)
#   boss-nocomms  boss pressure without comms          (NEW control)
#   oversight25   oversight whose monitor reads 25% of messages (monitoring-cost dial; flag from the starter repo)
set -euo pipefail
cond="${1:?condition}"; n="${2:?replicates}"; par="${3:-3}"
MODEL="${MODEL:-gpt-4.1}"; BUDGET_USD="${BUDGET_USD:-50}"
PRICE_IN="${PRICE_IN:-2}"; PRICE_OUT="${PRICE_OUT:-8}"
# The key can live in .env.local (git-ignored) as OPENAI_API_KEY=sk-..., so it never goes through chat or git.
cd "$(dirname "$0")/.."
if [ -z "${OPENAI_API_KEY:-}" ] && [ -f .env.local ]; then set -a; . ./.env.local; set +a; fi
SIM="${SIM:-src/continuous_double_auction/simulation.py}"   # SIM=collusion_analysis/mock_sim.py rehearses at $0
# Open-model runs: LOCAL_LLM_MODEL=... routes everything to an OpenAI-compatible server; they are tagged
# lo-<TAG_MODEL>-..., cost nothing and are excluded from the OpenAI budget guard below.
if [ -n "${LOCAL_LLM_MODEL:-}" ]; then PFX="lo-${TAG_MODEL:?set TAG_MODEL, e.g. qwen7b}"; else PFX="sp"; fi
[ "$SIM" != "src/continuous_double_auction/simulation.py" ] || [ -n "${LOCAL_LLM_MODEL:-}" ] || : "${OPENAI_API_KEY:?set OPENAI_API_KEY}"
export WANDB_MODE=disabled PYTHONIOENCODING=utf-8
cd "$(dirname "$0")/.."
PY=env/Scripts/python.exe; [ -x "$PY" ] || PY=env/bin/python

case "$cond" in
  comms)        flags="--seller_comms_enabled" ;;
  nocomms)      flags="" ;;
  oversight)    flags="--seller_comms_enabled --oversight_enabled" ;;
  notice)       flags="--seller_comms_enabled --oversight_notice" ;;
  monitor)      flags="--seller_comms_enabled --oversight_monitor" ;;
  cap50)        flags="--seller_comms_enabled --max_message_length 50" ;;
  seltemp)      flags="--seller_comms_enabled --seller_temperature 1.2" ;;
  boss-nocomms) flags="--boss_pressure" ;;
  oversight25)  flags="--seller_comms_enabled --oversight_enabled --overseer_sample_fraction 0.25" ;;
  *) echo "unknown condition $cond"; exit 2 ;;
esac

# Spend so far, estimated from log bytes (chars/4 tokens, 80% input / 20% output as measured
# on the authors' logs), plus 10% for the gpt-4.1-mini judge. A guard, not an invoice:
# check the real figure on platform.openai.com/usage.
spent() {
  local bytes; bytes=$(find results -path "*sp-*" -name "*.md" ! -name auction_results.md -printf "%s\n" 2>/dev/null | awk '{s+=$1} END {print s+0}')
  awk -v b="$bytes" -v pi="$PRICE_IN" -v po="$PRICE_OUT" 'BEGIN {t=b/4; printf "%.2f", 1.1*(0.8*t*pi + 0.2*t*po)/1e6}'
}

run_one() {
  local i="$1" s
  s=$(spent)
  if awk -v s="$s" -v b="$BUDGET_USD" 'BEGIN {exit !(s >= b)}'; then
    echo "BUDGET STOP: est. \$$s >= \$$BUDGET_USD, skipping $PFX-$cond-$i"; return 0
  fi
  echo "[$(date +%H:%M:%S)] start $PFX-$cond-$i (est. spent \$$s)"
  "$PY" -X utf8 "$SIM" \
    --seller_valuations 80 80 80 80 80 --buyer_valuations 100 100 100 100 100 \
    --seller_models $MODEL $MODEL $MODEL $MODEL $MODEL \
    --buyer_models  $MODEL $MODEL $MODEL $MODEL $MODEL \
    --rounds 30 $flags --tag "$PFX-$cond-$i" > "results/.$PFX-$cond-$i.log" 2>&1 \
    && echo "[$(date +%H:%M:%S)] done  $PFX-$cond-$i" \
    || echo "[$(date +%H:%M:%S)] FAIL  $PFX-$cond-$i (see results/.$PFX-$cond-$i.log)"
}
export -f run_one spent; export cond flags MODEL PY SIM PFX BUDGET_USD PRICE_IN PRICE_OUT
mkdir -p results
# Continue numbering after any replicates already in results/ for this condition.
# (find, not ls: with pipefail an empty ls glob would abort the script silently)
start=$(find results -maxdepth 1 -type d -name "*_$PFX-$cond-*" | wc -l)
seq $((start + 1)) $((start + n)) | xargs -P "$par" -I{} bash -c 'run_one {}'
echo "Condition $cond: total est. spend \$$(spent)"
