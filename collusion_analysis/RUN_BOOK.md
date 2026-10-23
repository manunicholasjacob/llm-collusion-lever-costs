# Run-book: AI Collusion Sprint (Track 1, Q1.5 + Q1.4 stretch)
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

## 3. Stage 2: only with Manu's approval of about +$27
```bash
BUDGET_USD=77 bash collusion_analysis/run_sprint.sh monitor 10 3   # H2
```

## 4. Analysis
```bash
G='data/*_base-*/ data/*_oversight-*/ data/*_boss_pressure-*/ results/*_sp-*/'
env/Scripts/python.exe -X utf8 -I collusion_analysis/run_stats.py "results/*_sp-*/"
env/Scripts/python.exe -X utf8 -I collusion_analysis/frontier.py figs/frontier_primary.png --metric collusion_index_2nd_half $G
env/Scripts/python.exe -X utf8 -I collusion_analysis/frontier.py figs/frontier_wholerun.png $G
# add --pool only if the H5 drift check passes (SPRINT_PROTOCOL.md section 2)
```

## 5. Stretch (no API cost): detectors on real trajectories
Discretize each seller's asks with `discretize_asks(asks, n_bins=3)`. Then:
- compute `pairwise_scores` with `shift_null_pvalue`, and `net_influence` with the state set to the previous-round mean-ask bin
- compute the AUC for comms vs no-comms runs and the Spearman correlation with `collusion_metrics.json` `seller_N_coordination_score`
