#!/usr/bin/env bash
# Unattended sprint run (SPRINT_PROTOCOL.md, commits 2040915 and 677ed76). No human decisions inside;
# every branch is pre-registered. Phase P pilot + gate -> Phase O (7 levers, balanced batches) ->
# Phase G (if both pilot models pass) -> Phase J judge subset -> analysis and figures.
# Usage: bash collusion_analysis/run_all.sh     (needs LOCAL_LLM_BASE_URL + LOCAL_LLM_API_KEY in .env.local)
# Env overrides (for testing): N_LLAMA N_MINI N_O N_G K_J BATCH BUDGET_USD
set -uo pipefail
cd "$(dirname "$0")/.."
if [ -f .env.local ]; then set -a; . ./.env.local; set +a; fi
: "${LOCAL_LLM_API_KEY:?put LOCAL_LLM_API_KEY in .env.local}"
mkdir -p results figs
LOG=results/run_all.log
exec > >(tee -a "$LOG") 2>&1
PY=env/Scripts/python.exe; [ -x "$PY" ] || PY=env/bin/python
export BUDGET_USD="${BUDGET_USD:-46}" SKIP_LLM_JUDGE=1 WANDB_MODE=disabled
N_O="${N_O:-25}"; N_G="${N_G:-6}"; K_J="${K_J:-4}"; BATCH="${BATCH:-1}"
declare -A MODEL=([llama70b]=meta-llama/llama-3.3-70b-instruct [mini41]=openai/gpt-4.1-mini)
LEVERS_O="comms nocomms oversight notice monitor oversight25 maverick"
LEVERS_G="comms nocomms notice maverick"
step() { echo; echo "===== [$(date '+%a %H:%M')] $* ====="; }
usage() { curl -s -H "Authorization: Bearer $LOCAL_LLM_API_KEY" "${USAGE_URL:-$LOCAL_LLM_BASE_URL/key}" \
          | "$PY" -c "import json,sys; print('%.2f' % float(json.load(sys.stdin)['data']['usage']))" 2>/dev/null || echo "?"; }
route() { export TAG_MODEL="$1" LLM_MODEL_MAP="gpt-4.1=${MODEL[$1]},gpt-4.1-mini=openai/gpt-4.1-mini"; }

# Balanced batches: each batch starts BATCH runs of every lever concurrently, so if the budget runs
# out the levers stay balanced instead of the last ones getting nothing.
balanced() {  # tag levers total
  local tag="$1" levers="$2" total="$3" done=0
  route "$tag"
  while [ "$done" -lt "$total" ]; do
    local b=$(( total - done < BATCH ? total - done : BATCH ))
    # Wait on these PIDs only: a bare `wait` (bash >= 5.1) also waits on the `tee` process
    # substitution that logs this script, which never exits, so it would hang forever.
    local pids=()
    for lv in $levers; do bash collusion_analysis/run_sprint.sh "$lv" "$b" "$b" & pids+=($!); done
    wait "${pids[@]}"; done=$((done + b))
    echo "[$(date +%H:%M)] $tag: $done/$total per lever done; key usage \$$(usage)"
    if [ "$(usage)" != "?" ] && awk -v s="$(usage)" -v b="$BUDGET_USD" 'BEGIN {exit !(s >= b)}'; then
      echo "BUDGET reached; stopping $tag after $done per lever"; break; fi
  done
}

step "Phase P: pilot + gate (usage \$$(usage))"
bash collusion_analysis/run_pilot.sh
CHOSEN=$(awk '/^CHOSEN/ {print $2}' results/pilot_gate.txt)
SECOND=$(awk '/^SECOND/ {print $2}' results/pilot_gate.txt)
[ -n "$CHOSEN" ] || { echo "No gate decision; stopping."; exit 1; }

step "Phase O: $CHOSEN, $N_O per lever x 7 levers (usage \$$(usage))"
balanced "$CHOSEN" "$LEVERS_O" "$N_O"

if [ "$SECOND" != "none" ]; then
  step "Phase G: $SECOND, $N_G per lever on key levers (usage \$$(usage))"
  balanced "$SECOND" "$LEVERS_G" "$N_G"
else
  step "Phase G skipped (only one model passed or none did)"
fi

step "Phase J: judge on up to $K_J runs per lever for $CHOSEN (usage \$$(usage))"
route "$CHOSEN"; "$PY" -X utf8 -I collusion_analysis/judge_subset.py "$CHOSEN" "$K_J"

step "Analysis (\$0)"
for tag in "$CHOSEN" $( [ "$SECOND" != none ] && echo "$SECOND" ); do
  G="results/*_lo-$tag-*/"
  "$PY" -X utf8 -I collusion_analysis/report_tables.py "figs/$tag" --suffix "$tag" $G
  "$PY" -X utf8 -I collusion_analysis/frontier.py "figs/$tag/frontier_primary.png" --suffix "$tag" --metric collusion_index_2nd_half_llm $G
  "$PY" -X utf8 -I collusion_analysis/detector_eval.py "figs/$tag/detector_whole" $G
  "$PY" -X utf8 -I collusion_analysis/detector_eval.py --window 8 30 "figs/$tag/detector_w8_30" $G
done
git diff 2bb2a7e -- src > collusion_analysis/harness_changes.patch  # our src changes only (upstream has no license; never re-host theirs)
echo "FINAL_USAGE $(usage)"
"$PY" -X utf8 -I collusion_analysis/writing_pack.py WRITING_PACK.md
step "DONE. Final key usage \$$(usage). Start here: WRITING_PACK.md (gate, tables, tests, figures, checklist)"
