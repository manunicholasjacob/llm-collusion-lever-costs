# Measured costs of anti-collusion levers for LLM market agents
Apart Research AI Collusion Research Sprint, Oct 23-25, 2026. Track 1 (Q1.5, Q1.3, Q1.4) and Track 3 (Q3.4).
Built on the double-auction harness of Agrawal et al. (2025), "Evaluating LLM Agent Collusion in Double
Auctions" (arXiv:2507.01413, https://github.com/andyjliu/llm-agent-collusion); their code and their
`data/` runs are theirs, and their README follows below this section.

## What is preexisting and what was done during the sprint
- **Preexisting (built Oct 22, before the sprint; git commit 6078dab and earlier on branch `sprint-prep`):**
  - the `collusion_analysis/` tooling (parser, statistics, frontier, detectors, runners, mock tests)
  - harness flags `--oversight_notice`, `--oversight_monitor` and `--seller_temperature`
  - `--overseer_sample_fraction`, adapted from the official sprint starter repo (poseidon-research/collusion_hackathon)
  - the pre-registered protocol
  - a pre-sprint analysis of the authors' public runs (the oversight monitor fired in 20/20 runs)
- **During the sprint (Oct 23-25):**
  - all new LLM runs (`results/`)
  - the no-regret maverick seller lever
  - per-role model routing
  - robustness fixes (string prices, rounds without bids)
  - every analysis in the deviation log of `collusion_analysis/SPRINT_PROTOCOL.md`: channel movement, detector validity and calibration, the measured-cost frontier and the hypothesis tests
  - figures and the report

See `collusion_analysis/DISCLOSURE.md` and the timestamped deviation log in `collusion_analysis/SPRINT_PROTOCOL.md`.

## Reproduce
```bash
# environment (Python 3.12)
uv venv --python 3.12 env && uv pip install --python env/Scripts/python.exe -r requirements.txt && uv pip install --python env/Scripts/python.exe -e .
env/Scripts/python.exe -X utf8 collusion_analysis/mock_smoke_test.py          # $0 check of every lever (fake LLM)
# results on the authors' public runs ($0)
env/Scripts/python.exe -X utf8 -I collusion_analysis/run_stats.py "data/*/"
env/Scripts/python.exe -X utf8 -I collusion_analysis/detector_eval.py --window 8 30 figs/detector_w8_30 data/*_base-[0-9]*/ data/*_base-seller_comms-*/ data/*_oversight-*/ data/*_boss_pressure-*/
env/Scripts/python.exe -X utf8 -I collusion_analysis/report_figs.py figs/report
# new runs: put LOCAL_LLM_BASE_URL and LOCAL_LLM_API_KEY (an OpenRouter key) in .env.local, then
bash collusion_analysis/run_pilot.sh                                            # pilot and positive-control gate
```
The exact commands for every stage are in `collusion_analysis/RUN_BOOK.md`.

## Dual use
Ranking anti-collusion levers by cost also tells a colluding operator which levers to resist. Detector
power limits hint at what evades detection. We report aggregate effects only, and all agents are simulated.

---
