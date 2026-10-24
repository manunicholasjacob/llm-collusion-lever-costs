#!/usr/bin/env bash
# Phase P pilot (SPRINT_PROTOCOL.md amendment in commit 2040915): two candidate seller models through
# OpenRouter, monitor/judge pinned to gpt-4.1-mini, judge deferred. Records real USD per run per model
# from the key's usage, then applies the pre-registered gate (gate.py).
# Usage: bash collusion_analysis/run_pilot.sh      (needs LOCAL_LLM_BASE_URL + LOCAL_LLM_API_KEY in .env.local)
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -f .env.local ]; then set -a; . ./.env.local; set +a; fi
: "${LOCAL_LLM_API_KEY:?put LOCAL_LLM_API_KEY in .env.local}"
export SKIP_LLM_JUDGE=1 BUDGET_USD="${BUDGET_USD:-46}"
PY="${PY:-env/Scripts/python.exe}"; [ -x "$PY" ] || PY=env/bin/python  # PY overrides (real-terminal env: envw)
usage() { curl -s -H "Authorization: Bearer $LOCAL_LLM_API_KEY" "${USAGE_URL:-$LOCAL_LLM_BASE_URL/key}" \
          | "$PY" -c "import json,sys; print(json.load(sys.stdin)['data']['usage'])"; }
COSTS=results/pilot_costs.json; mkdir -p results; [ -f "$COSTS" ] || echo '{}' > "$COSTS"

pilot() {  # tag agent_model n_each parallel  (runs tagged lo-p<tag>: gate only, excluded from Phase O/G tests)
  local tag="$1" model="$2" n="$3" par="$4" u0 u1
  export TAG_MODEL="p$tag" LLM_MODEL_MAP="gpt-4.1=$model,gpt-4.1-mini=openai/gpt-4.1-mini"
  u0=$(usage)
  bash collusion_analysis/run_sprint.sh comms "$n" "$par"
  bash collusion_analysis/run_sprint.sh nocomms "$n" "$par"
  u1=$(usage)
  "$PY" -c "import json,sys; f=sys.argv[1]; d=json.load(open(f)); d[sys.argv[2]]=(float(sys.argv[4])-float(sys.argv[3]))/(2*int(sys.argv[5])); json.dump(d,open(f,'w'))" \
        "$COSTS" "$tag" "$u0" "$u1" "$n"
  echo "[$tag] spent \$$("$PY" -c "print(round(float('$u1')-float('$u0'),3))") on $((2 * n)) runs"
}

pilot llama70b meta-llama/llama-3.3-70b-instruct "${N_LLAMA:-6}" 6
pilot mini41   openai/gpt-4.1-mini               "${N_MINI:-3}"  3
"$PY" -X utf8 -I collusion_analysis/gate.py "$COSTS" | tee results/pilot_gate.txt
