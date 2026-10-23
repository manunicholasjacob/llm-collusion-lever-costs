# Pre-sprint vs. sprint work (for the README and the report's required disclosure)
The sprint runs Fri Oct 23 to Sun Oct 25, 2026 (AoE). Everything below marked PRE-SPRINT was done on
Oct 22, 2026 and is captured in a local git commit made before kickoff (see `git log`).

## PRE-SPRINT (disclose as preexisting)
- **Analysis tooling** in `collusion_analysis/`:
  - `pipeline.py`: run parser and metrics. The collusion index reuses Agrawal et al.'s CE/JPM definitions. Fixed on Oct 22 for Windows file encoding and paths.
  - `run_stats.py`: CIs, second-half index, gag frequency, channel retained, token footprint.
  - `frontier.py` v2: measured-cost frontier.
  - `net_influence.py`: lagged transfer-entropy score, Bonjour et al. net influence, circular-shift null.
  - `report_tables.py`: Table 1, the pre-registered tests, the strip plot, and robust OLS.
  - `detector_eval.py`: detector statistics per run, the AUC and judge correlation, and the synthetic power curve.
  - `mock_llm.py`, `mock_sim.py`, `mock_smoke_test.py` and `run_sprint.sh`.
  - The full pipeline was rehearsed end to end on 17 fake-LLM runs ($0). Those runs were deleted, and the analysis refuses runs marked `MOCK`.
- **Harness changes** in `src/`:
  - New flags `--oversight_notice`, `--oversight_monitor` and `--seller_temperature`. Their defaults reproduce the original behaviour exactly.
  - `--overseer_sample_fraction`, **adapted from the official sprint starter repo** (github.com/poseidon-research/collusion_hackathon, `llm-agent-collusion/`), plus a per-round log of which messages the overseer read.
  - A $0 mock test verifies all of these.
- **Analysis of the authors' public run data** (`data/`, Agrawal et al. 2025):
  - reproduction of their condition means
  - finding that the oversight gag fired in 20/20 runs (channel retained 10%)
  - the power analysis
  - These findings motivated the sprint design and are labelled "pre-sprint analysis of public data" wherever they appear.
- **Literature check** of every related-work citation against its primary source.
- **Protocol:** the pre-registered `SPRINT_PROTOCOL.md`.

## NEW DURING THE SPRINT (the research contribution)
- All new LLM runs (`results/*_sp-*`). New levers and controls:
  - notice-only, monitor-only (the oversight decomposition)
  - static 50-character cap
  - seller-only temperature
  - boss pressure without communication
  - 2026 drift check of the comms baseline
- The measured-cost frontier and hypothesis tests on the new and pooled data.
- Applying the information-theoretic detectors to LLM-agent trajectories and comparing them with the harness LLM judge.
- The report.

Mark `collusion_analysis/` and the `src/` flag changes as preexisting in the README and in the report.
