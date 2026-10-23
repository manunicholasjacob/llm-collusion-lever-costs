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
set -euo pipefail
cond="${1:?condition}"; n="${2:?replicates}"; par="${3:-3}"
MODEL="${MODEL:-gpt-4.1}"; BUDGET_USD="${BUDGET_USD:-50}"
PRICE_IN="${PRICE_IN:-2}"; PRICE_OUT="${PRICE_OUT:-8}"
: "${OPENAI_API_KEY:?set OPENAI_API_KEY}"
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
    echo "BUDGET STOP: est. \$$s >= \$$BUDGET_USD, skipping sp-$cond-$i"; return 0
  fi
  echo "[$(date +%H:%M:%S)] start sp-$cond-$i (est. spent \$$s)"
  "$PY" src/continuous_double_auction/simulation.py \
    --seller_valuations 80 80 80 80 80 --buyer_valuations 100 100 100 100 100 \
    --seller_models $MODEL $MODEL $MODEL $MODEL $MODEL \
    --buyer_models  $MODEL $MODEL $MODEL $MODEL $MODEL \
    --rounds 30 $flags --tag "sp-$cond-$i" > "results/.sp-$cond-$i.log" 2>&1 \
    && echo "[$(date +%H:%M:%S)] done  sp-$cond-$i" \
    || echo "[$(date +%H:%M:%S)] FAIL  sp-$cond-$i (see results/.sp-$cond-$i.log)"
}
export -f run_one spent; export cond flags MODEL PY BUDGET_USD PRICE_IN PRICE_OUT
mkdir -p results
# Continue numbering after any replicates already in results/ for this condition.
start=$(ls -d results/*_sp-"$cond"-* 2>/dev/null | wc -l)
seq $((start + 1)) $((start + n)) | xargs -P "$par" -I{} bash -c 'run_one {}'
echo "Condition $cond: total est. spend \$$(spent)"
