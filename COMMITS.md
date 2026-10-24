# Commit map

This repository's history was produced from the private working repository by removing every file that belongs to
the upstream harness (`src/`, `data/` and the rest of andyjliu/llm-agent-collusion) and the harness patch, with
`git filter-branch`. Author and commit dates are unchanged; hashes changed. `SPRINT_PROTOCOL.md` cites the
original hashes, so this table maps them. Times are US Central (CDT, UTC-5). The sprint opened Fri 23 Oct 2026,
00:00 AoE, which is 07:00 CDT.

| Original (cited in SPRINT_PROTOCOL.md) | This repository | Date (CDT) | Subject |
|---|---|---|---|
| 6078dab | b2ebdc7 | 2026-10-22 19:29 | Pre-sprint state for the Apart AI Collusion Research Sprint (Oct 23-25,  |
| 06f7ecd | 454e92f | 2026-10-22 19:40 | Amend protocol before kickoff: approved $50 cap, 17-run funded design |
| 2f4a0d1 | 818ab30 | 2026-10-22 20:12 | Pre-sprint: rehearsed pipeline, report tooling, overseer sampling flag |
| aedbf59 | ab67463 | 2026-10-23 07:43 | Sprint day 1: detector results on public runs, open-model backend, robus |
| 2040915 | 84a51dd | 2026-10-23 08:05 | Maverick no-regret seller, per-role model routing, judge skip; $50 all-p |
| 11dfa4f | 17ba0a9 | 2026-10-23 08:19 | Sprint: OpenRouter hardening, pilot+gate, report figures, Q1.3 calibrati |
| 5636a9f | b07b747 | 2026-10-23 08:20 | Deviation log: anchor every entry to its git commit; correct estimated c |
| 677ed76 | bc4ebe1 | 2026-10-23 08:28 | Protocol: pilot/main data separation and unattended run order (logged be |
| 363d1be | 6212802 | 2026-10-23 08:44 | Unattended overnight orchestrator, judge subset, writing pack; rehearsal |
| 872bd5f | 14ace69 | 2026-10-23 13:06 | Protocol: pre-register A7 talk-vs-prices test (Q2.3) before computing |
| 44d5875 | 86bc5bb | 2026-10-23 13:07 | A7 results: collusion on paper descriptively (9/9 runs), detrended null  |
| 4f8942b | 92ff62b | 2026-10-23 13:08 | Report plan: A7 + power analysis + licensing note; export harness_change |
| 8888cdf | f9c9c04 | 2026-10-23 21:44 | Final $40 budget: BUDGET_USD=39, judge before replication, N_G=3 (logged |
| 1c51d89 | 85ffc4e | 2026-10-23 21:44 | Overnight launcher: block idle sleep only while the run is going; $40 se |
| d4b5f5a | 1b125ea | 2026-10-23 21:52 | Real-environment Python: envw on uv Python 3.12; PY override in run scri |
| 45ce6ad | e5d83e6 | 2026-10-23 22:29 | Phase P: positive control failed for both models; Phase O on llama70b pe |
| 523737c | ca2819a | 2026-10-23 22:30 | F1 monitor false-positive analysis script (tested on 2025 arms) |
| 6c0c203 | 6343b44 | 2026-10-23 22:38 | Skip W&B logging when disabled: overseer sampling made a per-round list  |
| d759473 | 3d19b0c | 2026-10-23 22:52 | Coerce agent messages to text: Llama sent a bare number under the gag an |
| ddc8771 | 4ce2fa3 | 2026-10-24 02:15 | Phase O results logged (pre-registered family null; F1 monitor false pos |
| 4ce0cda | 1e9e372 | 2026-10-24 02:17 | Overnight results: Phase O (llama70b, 7x25), F1, exploratory X1 costs, f |
| 77e63d6 | 8e96484 | 2026-10-24 02:19 | X1 robustness (rank tests) and mechanism (compliance talk) logged as exp |
| ea5facd | c93516c | 2026-10-24 06:32 | Pre-register confirmatory replication C2 (notice chills trade/welfare; m |
| 82ae9ce | c12d528 | 2026-10-24 06:34 | C2 runner/analysis/launcher (tested on fake server, real usage unchanged |
| 8cc4552 | c15f9cc | 2026-10-24 06:41 | Report: full draft in the official template (python-docx build from the  |
| cacd452 | b051142 | 2026-10-24 08:36 | C2 results: notice lowers buyer welfare (confirmed), maverick raises it  |
| cb46a6e | 6c4c52a | 2026-10-24 08:38 | Final report v1: confirmatory results integrated; PDF + docx from the of |
| 0c464b3 | 92297f3 | 2026-10-24 08:38 | Report metadata: real title and author |
| 3e1bf5a | 1ea1b98 | 2026-10-24 08:53 | Final verification pass: correct report numbers, add claim checker |
| 9ddf84d | 5ef2ef3 | 2026-10-24 11:28 | Correct pilot sizes and power range in the report; add power.py |
