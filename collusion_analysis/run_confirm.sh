#!/usr/bin/env bash
# Confirmatory replication C2 (SPRINT_PROTOCOL.md section 9, commit ea5facd): fresh llama70b runs of comms,
# notice and maverick, n=25 completed each, balanced batches, make-ups for crashed runs, budget = live
# OpenRouter balance minus $1 unless BUDGET_USD is set. Then the pre-registered analysis (c2_confirm.py).
set -uo pipefail
cd "$(dirname "$0")/.."
if [ -z "${LOCAL_LLM_API_KEY:-}" ] && [ -f .env.local ]; then set -a; . ./.env.local; set +a; fi  # never override an explicit (e.g. test) backend
: "${LOCAL_LLM_API_KEY:?put LOCAL_LLM_API_KEY in .env.local}"
mkdir -p results figs/llamaR
exec > >(tee -a results/run_confirm.log) 2>&1
PY="${PY:-env/Scripts/python.exe}"; [ -x "$PY" ] || PY=env/bin/python
export PY SKIP_LLM_JUDGE=1 WANDB_MODE=disabled TAG_MODEL=llamaR
export LLM_MODEL_MAP="gpt-4.1=meta-llama/llama-3.3-70b-instruct,gpt-4.1-mini=openai/gpt-4.1-mini"
usage() { curl -s -H "Authorization: Bearer $LOCAL_LLM_API_KEY" "${USAGE_URL:-$LOCAL_LLM_BASE_URL/key}" \
          | "$PY" -c "import json,sys; print('%.2f' % float(json.load(sys.stdin)['data']['usage']))" 2>/dev/null || echo "?"; }
if [ -z "${BUDGET_USD:-}" ]; then
  BUDGET_USD=$(curl -s -H "Authorization: Bearer $LOCAL_LLM_API_KEY" "$LOCAL_LLM_BASE_URL/credits" \
    | "$PY" -c "import json,sys; print('%.2f' % (float(json.load(sys.stdin)['data']['total_credits']) - 1))")
fi
export BUDGET_USD
N="${N:-25}"; BATCH="${BATCH:-2}"; LEVERS="comms notice maverick"
done_n() { find results -maxdepth 2 -path "*_lo-llamaR-$1-*" -name experiment_metadata.json | wc -l; }
over_budget() { local u; u=$(usage); [ "$u" != "?" ] && awk -v s="$u" -v b="$BUDGET_USD" 'BEGIN {exit !(s >= b)}'; }
echo "===== [$(date '+%a %H:%M')] C2 start: n=$N per arm, batch $BATCH, budget \$$BUDGET_USD, usage \$$(usage) ====="
# Balanced batches, then make-ups, until every arm has N completed runs (or the budget stops it).
for attempt in $(seq 1 40); do
  pids=(); started=0
  for lv in $LEVERS; do
    need=$(( N - $(done_n "$lv") )); [ "$need" -le 0 ] && continue
    b=$(( need < BATCH ? need : BATCH ))
    bash collusion_analysis/run_sprint.sh "$lv" "$b" "$b" & pids+=($!); started=1
  done
  [ "$started" -eq 0 ] && break
  wait "${pids[@]}"   # PIDs only: a bare wait would also wait on the tee above (bash >= 5.1)
  echo "[$(date +%H:%M)] completed: comms $(done_n comms), notice $(done_n notice), maverick $(done_n maverick); usage \$$(usage)"
  if over_budget; then echo "BUDGET reached (\$$BUDGET_USD); stopping"; break; fi
done
echo "===== [$(date '+%a %H:%M')] C2 analysis ====="
"$PY" -X utf8 -I collusion_analysis/c2_confirm.py figs/llamaR/c2_confirm.md
echo "===== [$(date '+%a %H:%M')] C2 DONE. Final usage \$$(usage). Results: figs/llamaR/c2_confirm.md ====="
