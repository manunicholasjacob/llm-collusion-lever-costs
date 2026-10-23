# collusion_analysis: sprint tooling (PREEXISTING, built Oct 22, 2026, before the sprint)
Analysis and run tooling for the Apart AI Collusion Research Sprint (Track 1, Q1.5 + Q1.4), on top of
the Agrawal et al. (2025) double-auction harness. See DISCLOSURE.md for pre-sprint vs. sprint work.

- `pipeline.py`: parse runs into the collusion index (CE=0, JPM=1), allocative efficiency, welfare and volatility
- `run_stats.py`: per-run stats, bootstrap CIs, second-half index, measured costs (channel retained, gag rounds), token footprint
- `frontier.py`: measured-cost frontier plot and table (`OUT.png [--pool] [--metric M] GLOB...`)
- `net_influence.py`: lagged TE score, Bonjour et al. (2022) net influence, circular-shift null; RPS validation
- `mock_smoke_test.py`: $0 end-to-end test of every sprint condition with a scripted fake LLM
- `run_sprint.sh`: run N replicates of a condition with a budget guard
- `RUN_BOOK.md`: exact commands. `SPRINT_PROTOCOL.md`: pre-registered design. `REPORT_SKELETON.md`: report plan

Always run Python with `-X utf8` on Windows. New runs land in `results/`; the authors' runs are in `data/`.
