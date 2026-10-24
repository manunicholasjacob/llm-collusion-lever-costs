# Pre-sprint and sprint work

The sprint opened Fri 23 Oct 2026, 00:00 AoE (07:00 CDT). Commit dates in this repository are the original ones;
`COMMITS.md` maps the hashes cited in `SPRINT_PROTOCOL.md` to this repository's hashes.

This file replaces an earlier version written before the sprint. That version listed planned arms (a static
50-character cap, seller-only temperature, a boss-pressure arm and a drift check) that were dropped when the design
was amended on 23 Oct (see the protocol's deviation log); none of them was run.

## Before the sprint (22 Oct 2026; original commits 6078dab, 06f7ecd, 2f4a0d1)

- Analysis tooling in `collusion_analysis/`: `pipeline.py`, `run_stats.py`, `frontier.py`, `net_influence.py`,
  `report_tables.py`, `detector_eval.py`, `run_sprint.sh`, and the $0 mock tests (`mock_llm.py`, `mock_sim.py`,
  `mock_smoke_test.py`). The pipeline was rehearsed end to end on fake-model runs, which were then deleted; the
  analysis refuses runs marked as mock.
- Harness flags (in the patch): `--oversight_notice`, `--oversight_monitor`, `--seller_temperature`, and
  `--overseer_sample_fraction`, adapted from the official sprint starter repository
  (github.com/poseidon-research/collusion_hackathon). Their defaults reproduce the original behaviour.
- Analysis of the authors' public 2025 runs: the oversight monitor fired in 20 of 20 runs, and a power analysis.
  The report labels these results "pre-sprint analysis of public data".
- The pre-registered protocol, `SPRINT_PROTOCOL.md`.

## During the sprint (from 23 Oct 2026, 07:43 CDT)

- Harness additions (in the patch): the no-regret Hedge seller (`NoRegretSeller`), routing of each role's model
  through an OpenAI-compatible endpoint (`OpenAICompatibleClient`, `local_backend`, `routed_model`), price
  normalisation, and runtime fixes logged in the protocol.
- Detector results and calibration on the public runs (Q1.3, Q1.4), the channel-movement test (Q3.4) and the
  judge test (Q2.3).
- All 268 new runs in `results/`: the pilot and positive-control gate, the main study (seven levers, 25 runs each)
  and the confirmatory replication (75 runs), with the runners, gate and orchestration scripts.
- The analyses of monitor false positives (`f1_monitor.py`), lever costs (`x1_costs.py`), the confirmatory tests
  (`c2_confirm.py`), `power.py`, the figures and the report.
