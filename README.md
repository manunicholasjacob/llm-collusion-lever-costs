# Anti-Collusion Levers Are Not Free: Measuring What Monitoring Costs LLM Markets

Code, run data and pre-registration log for a study submitted to the Apart Research AI Collusion Research Sprint
(23 to 25 October 2026; Track 1, Q1.5, Q1.3, Q1.4, and Track 3, Q3.4).

Manu Nicholas Jacob, Independent Researcher.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23622463.svg)](https://doi.org/10.5281/zenodo.23622463)

**Report:** [`report/Apart_Collusion_Sprint_Report_Manu_Nicholas_Jacob.pdf`](report/Apart_Collusion_Sprint_Report_Manu_Nicholas_Jacob.pdf)

> **Submitted version:** release [v1.1.0](https://github.com/manunicholasjacob/llm-collusion-lever-costs/releases/tag/v1.1.0) (Zenodo [10.5281/zenodo.23624191](https://doi.org/10.5281/zenodo.23624191)) is exactly what was submitted to the sprint on 24 Oct 2026. Everything added after it (`results_postsprint/`, `followup/`, `results_followup/`, and protocol sections 10 onward) is later follow-up work, not part of the submission.

## What the study found

The study uses the continuous double auction of Agrawal et al. (2025), *Evaluating LLM Agent Collusion in Double
Auctions* ([arXiv:2507.01413](https://arxiv.org/abs/2507.01413), [code and data](https://github.com/andyjliu/llm-agent-collusion)).

- **Audit of the reference "oversight" lever (the authors' public gpt-4.1 runs).** The LLM monitor fired in 20 of 20
  oversight runs, first at hours 1 to 7, and limited sellers to five-character messages for 77 to 97% of each run.
  In that environment oversight is a delayed communication ban.
- **Positive control failed.** Neither Llama-3.3-70B nor GPT-4.1-mini sellers colluded when allowed to communicate,
  so the pre-registered tests of collusion reduction are null. The study therefore measures what levers cost a
  market that is not colluding.
- **Costs (seven levers, 25 runs each, Llama-3.3-70B sellers).** The monitor fired on innocent markets in up to 48% of
  runs. A monitoring notice lowered buyer welfare by 22% while the monitor without the notice had no detectable
  effect. Banning communication cost 13% of trades. One no-regret (Hedge) seller raised buyer welfare by 26%.
- **Confirmatory replication (75 fresh runs, pre-registered before they ran).** Both welfare effects held (16% lower
  under the notice, 44% higher with the no-regret seller); the notice's effect on trade volume did not.

## Pre-sprint and sprint work

The sprint opened 23 Oct 2026, 00:00 AoE. **Preexisting (built 22 Oct 2026, before the sprint):** the core analysis
tooling (`pipeline.py`, `run_stats.py`, `frontier.py`, `net_influence.py`, `report_tables.py`, `detector_eval.py`,
`run_sprint.sh`, the mock tests), the harness flags `--oversight_notice`, `--oversight_monitor`,
`--seller_temperature` and `--overseer_sample_fraction` (the last adapted from the official starter repository),
the analysis of the authors' public runs, and the protocol. **New during the sprint:** the no-regret seller and
model routing, every run in `results/`, and every analysis and figure in the report. Details and commits:
[`collusion_analysis/DISCLOSURE.md`](collusion_analysis/DISCLOSURE.md); the git history keeps the original dates.

## Contents

| Path | What it is |
|---|---|
| `report/` | The report (PDF, DOCX, Markdown source), the DOCX builder, and `verify_claims.py`, which recomputes the report's hand-typed numbers from the runs |
| `collusion_analysis/` | Analysis and run tooling: run parser and metrics (`pipeline.py`, `run_stats.py`), lever costs (`x1_costs.py`), monitor false positives (`f1_monitor.py`), the confirmatory tests (`c2_confirm.py`), pre-registered tests and tables (`report_tables.py`), detectors (`net_influence.py`, `detector_eval.py`), power (`power.py`), figures, runners and $0 mock tests |
| `collusion_analysis/SPRINT_PROTOCOL.md` | Pre-registration and timestamped deviation log, including every correction |
| `collusion_analysis/harness_changes.patch` | Our changes to the upstream harness (new lever flags, the no-regret seller, OpenAI-compatible routing, robustness fixes), as a zero-context patch |
| `results/` | All 269 sprint run directories (268 complete; `20261023_224813_lo-llama70b-oversight-3` crashed and has no metadata, so the analysis skips it) |
| `figs/` | Analysis outputs and figures used in the report |
| `results_postsprint/` | Post-sprint runs, **not part of the submission**: pilot P2 (12 runs, profit pressure; protocol section 10) and screen S1 (9 runs, three cheap model families; section 11) |
| `followup/`, `results_followup/` | Follow-up study (not part of the submission): design, free-GPU runner and pilot F0 (20 runs; a hidden instruction to collude raises the second-half index from -0.90 to +0.47; protocol sections 12-13) |
| `collusion_analysis/DISCLOSURE.md` | What was built before the sprint and what during it |
| `COMMITS.md` | Map from the commit hashes cited in the protocol to this repository's hashes |

Each run directory holds `experiment_metadata.json` (configuration and model routing), `auction_results.md` (every
round's asks, bids, trades and messages), `collusion_metrics.json`, `unified.log`, `llm_eval_full.json` (LLM-judge
scores, where the judge was run) and, for arms with a monitor, `Overseer.md` (the monitor's scores). The per-agent
transcripts (856 MB, and they contain the upstream prompt templates) are not included; they are available from the
author on request. Run names: `pllama70b`/`pmini41` = pilot, `llama70b` = main study, `llamaR` = confirmatory
replication. Agents were `meta-llama/llama-3.3-70b-instruct`; the monitor and judge were `openai/gpt-4.1-mini`,
both through OpenRouter.

## Reproduce the numbers

The upstream repository has no license file, so this repository does not include its code or its 2025 runs. Lay
this repository over a checkout of it:

```bash
git clone https://github.com/andyjliu/llm-agent-collusion
cd llm-agent-collusion
git checkout 2bb2a7e
cp -r ../llm-collusion-lever-costs/{collusion_analysis,report,results,figs} .
pip install numpy scipy matplotlib
python -X utf8 report/verify_claims.py
```

`verify_claims.py` should print `34 claims checked, 0 failed`. To regenerate the analysis outputs (each is
byte-identical to the committed file):

```bash
mkdir -p out
python -X utf8 collusion_analysis/x1_costs.py out/x1_costs.md
python -X utf8 collusion_analysis/f1_monitor.py out/f1_monitor.md
python -X utf8 collusion_analysis/c2_confirm.py out/c2_confirm.md
python -X utf8 collusion_analysis/report_tables.py out/llama70b --suffix llama70b "results/*_lo-llama70b-*/"
python -X utf8 collusion_analysis/detector_eval.py out/detector_whole "data/*_base-[0-9]*/" "data/*_base-seller_comms-*/" "data/*_oversight-*/" "data/*_boss_pressure*/"
python -X utf8 collusion_analysis/power.py
```

The detector's transfer-entropy null uses one seeded random stream across runs, so its z-scores depend on the
order of the globs above. Across 11 seeds the calibrated transfer-entropy detector finds 4 of 10 communication runs
in 10 seeds and 5 of 10 in one; net influence is deterministic.

## Run new experiments

Apply the patch to the upstream checkout (`git apply --unidiff-zero collusion_analysis/harness_changes.patch`) and
install the upstream requirements. The runners route every model through one OpenAI-compatible endpoint set in
`.env.local` (`LOCAL_LLM_BASE_URL`, `LOCAL_LLM_API_KEY`) with `LLM_MODEL_MAP` mapping harness model names to
provider models; see `collusion_analysis/run_all.sh` and `run_confirm.sh`. `mock_smoke_test.py` exercises every
condition at no cost with a scripted fake model.

## Citation

See `CITATION.cff`. Please also cite Agrawal et al. (2025), whose harness and data this work builds on.

## License

MIT for the contents of this repository. The upstream harness and its data are not covered and are not included.
The analysis code, runs and first draft of the report were produced with Claude (Anthropic); see the report's LLM
Usage Statement.
