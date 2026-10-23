# Run-book: AI Collusion Sprint (Track 1, Q1.5 + Q1.4 stretch)

## CURRENT: one unattended command (plan v3, $50 total via OpenRouter)
1. Put two lines in `.env.local` (git-ignored):
   ```
   LOCAL_LLM_BASE_URL=https://openrouter.ai/api/v1
   LOCAL_LLM_API_KEY=sk-or-...
   ```
2. **The laptop must stay on, awake and online:**
   - plugged in
   - Settings > Power: sleep "Never" while plugged in
   - lid open, or "closing the lid does nothing"
   - postpone Windows Update restarts
3. Start it:
   ```bash
   bash collusion_analysis/run_all.sh
   ```
   It runs the pilot, the gate, Phase O (7 levers x 25, balanced batches), Phase G (only if both pilot models pass), the judge subset and all analysis. It has no human decision points, and it stops at $46 of real key usage.
4. **Progress:** `results/run_all.log`.
   **Outputs:**
   - the gate: `results/pilot_gate.txt`
   - per-model results: `figs/<model>/` (`table1.md`, `tests.md`, `ols_hc3.md`, `strip_primary.png`, `frontier_primary.png`, detector summaries)
5. **Expected wall time:** about 4 to 7 hours. Measured median run is 7.6 min (authors' gpt-4.1 logs); 7 runs execute concurrently per batch.

Sections below are the earlier gpt-4.1 plan, kept for the record.
Corrected Oct 22. The v1 run-book had five defects:
- it globbed `data/`, but new runs land in `results/`
- it never disabled W&B, so every run would crash at the end
- it used `python3`, which on Windows is the Store stub
- it promised "matched seeds", but the harness has no seed control
- its 3x3x15 design is too short for the detector

The design is in SPRINT_PROTOCOL.md. All paths are relative to the harness root `C:\dev\collusion-sprint\llm-agent-collusion`.

## 0. Setup (already done on Oct 22)
```bash
cd /c/dev/collusion-sprint/llm-agent-collusion
env/Scripts/python.exe -X utf8 collusion_analysis/mock_smoke_test.py   # $0; expect ALL PASS
rm -rf results/*_mock-*
```

## 1. Key and budget (Manu)
```bash
export OPENAI_API_KEY=sk-...          # never commit; paste only in the terminal
export BUDGET_USD=50 MODEL=gpt-4.1    # approved cap; runner refuses new runs past it
```

## 2. Stage 0 canary, then Stage 1 (after kickoff Friday; 17 runs, about $47)
```bash
bash collusion_analysis/run_sprint.sh comms 1 1          # canary (~10 min, ~$2.60); check the OpenAI usage page
env/Scripts/python.exe -X utf8 -I collusion_analysis/run_stats.py "results/*_sp-*/"   # sanity + real token count
bash collusion_analysis/run_sprint.sh notice 10 3        # H1, the decisive test, first
bash collusion_analysis/run_sprint.sh boss-nocomms 4 3   # H4
bash collusion_analysis/run_sprint.sh comms 2 2          # H5 drift (n=3 total)
```

## 3. Stage 2: only with Manu's approval of about +$27 (pick one)
```bash
BUDGET_USD=77 bash collusion_analysis/run_sprint.sh monitor 10 3       # A: H2, enforcement without the notice
BUDGET_USD=77 bash collusion_analysis/run_sprint.sh oversight25 10 3   # B: monitor reads 25% of messages (monitoring-cost dial)
```

## 4. Analysis (rehearsed end to end on fake runs, Oct 22)
```bash
G='data/*_base-*/ data/*_oversight-*/ data/*_boss_pressure-*/ results/*_sp-*/'
env/Scripts/python.exe -X utf8 -I collusion_analysis/report_tables.py figs --pool $G   # Table 1, tests (H1-H5), strip plot, OLS
env/Scripts/python.exe -X utf8 -I collusion_analysis/frontier.py figs/frontier_primary.png --pool --metric collusion_index_2nd_half $G
env/Scripts/python.exe -X utf8 -I collusion_analysis/frontier.py figs/frontier_wholerun.png --pool $G
# Drop --pool (and report sprint and 2025 baselines separately) if tests.md says H5 "do NOT pool".
```

## 5. Stretch (no API cost): detectors on real trajectories
```bash
env/Scripts/python.exe -X utf8 -I collusion_analysis/detector_eval.py figs/detector $G   # AUC, judge correlation, power curve
```
Bins are fixed at 3 (pre-registered). Never pass `ALLOW_MOCK=1` on sprint day.
