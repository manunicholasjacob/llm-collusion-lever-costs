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
export BUDGET_USD=150 MODEL=gpt-4.1   # runner refuses new runs past the cap
```

## 2. Stage 0 canary, then Stage 1 (Friday)
```bash
bash collusion_analysis/run_sprint.sh comms 1 1          # canary (~10 min, ~$2.40)
env/Scripts/python.exe -X utf8 -I collusion_analysis/run_stats.py "results/*_sp-*/"   # sanity + real token count
bash collusion_analysis/run_sprint.sh comms 4 3          # H5 drift (n=5 total)
bash collusion_analysis/run_sprint.sh notice 10 3        # H1
bash collusion_analysis/run_sprint.sh boss-nocomms 5 3   # H4
```

## 3. Stage 2 (Saturday)
```bash
bash collusion_analysis/run_sprint.sh monitor 10 3       # H2
bash collusion_analysis/run_sprint.sh cap50 10 3         # H3
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
