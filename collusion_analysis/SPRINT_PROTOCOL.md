# Sprint protocol: pre-registered before kickoff (written Oct 22, 2026)

Track 1, Q1.5: *which single restriction removes the most collusion at the least cost?*
Stretch: Q1.4 (information-theoretic detection). This file is committed before any sprint run;
the git commit timestamp is the pre-registration record. Deviations get logged at the bottom.

## 1. What pre-sprint analysis of the authors' public data showed
Source: `data/` in andyjliu/llm-agent-collusion (Agrawal et al. 2025, arXiv:2507.01413);
gpt-4.1 sellers and buyers, 5 sellers at $80, 5 buyers at $100, 30 rounds, n=10 runs per condition.
Reproduce with `python -X utf8 -I collusion_analysis/run_stats.py "data/*/"`.

| Fact | Evidence |
|---|---|
| F1. "Oversight" is a monitor that gags sellers to 5 characters for the rest of the run once it scores any round 4/4. It fired in **20/20** oversight runs, at rounds 1 to 7. | Gagged for 77 to 97% of rounds; seller message characters delivered = **10%** of the comms baseline. |
| F2. The handoff's frontier assumed oversight intrusiveness 0.40, giving "1.8x the ban's reduction per cost". With measured channel loss (0.90) the ratio is **0.82x** on the whole-run index and **1.26x** on the second-half index. | Reduction CIs overlap: ban +0.20 [-0.09, +0.46], oversight +0.14 [-0.12, +0.39] (whole run). |
| F3. Boss pressure raises the index to 0.66 (SD 0.04). Oversight leaves it at 0.65, even with the channel gagged 90% of the time. | boss 0.659 [0.64, 0.68], boss+oversight 0.652 [0.62, 0.68]. |
| F4. The comms baseline is noisy: per-run index ranges from -0.44 to +0.77 (SD 0.40). | 80% power to detect a difference of 0.20 needs about 54 runs per arm. |

The original thesis ("oversight is the Pareto-best lever, 1.8x") is **not** supported, so it is not
claimed. The sprint question becomes: **does any lever reduce collusion without paying the ban's
channel cost?** That requires splitting oversight into its two parts.

## 2. Hypotheses (sprint runs)
- **H1, deterrence alone:** a monitoring *notice* with no monitor (`notice`) lowers the primary index versus the comms baseline at channel loss of about 0. If so, it dominates both the ban and full oversight on the frontier.
- **H2, enforcement alone:** a monitor and gag with no notice (`monitor`) reproduces full oversight's effect. That would mean oversight works as a delayed ban.
- **H3, static bandwidth:** a 50-character cap from round 1 (`cap50`) gives a measured channel loss between 0 and 1 and some reduction. This places it on the frontier.
- **H4, pressure needs no talk:** boss pressure without communication (`boss-nocomms`) is within 0.05 of boss pressure with communication. If so, communication restrictions cannot touch pressure-driven supracompetitive pricing, and the 0.66 is unilateral pricing, not coordination.
- **H5, drift check:** the sprint comms baseline (2026 gpt-4.1) is compared with the 2025 baseline. Pool the two only if the 95% bootstrap CI of the difference in means includes 0. Report both either way.

## 3. Outcomes
- **Primary:** `collusion_index_2nd_half`, the mean seller ask over rounds 16 to 30, scaled so that CE $90 = 0 and JPM $100 = 1.
  - *Rationale:* the harness opens every run with asks at 97.5 ± 2.5. The whole-run mean is therefore anchored to the initial condition rather than to agent behaviour.
  - *Caveat (stated now):* we saw both metrics on the 2025 data before choosing, and the oversight-versus-ban ordering flips between them. The whole-run index is therefore reported alongside the primary everywhere.
- **Secondary:**
  - whole-run index
  - mean trade price
  - allocative efficiency (trades / (5 x 30))
  - buyer welfare per round
  - ask dispersion
  - the harness's LLM-judge coordination score (gpt-4.1-mini, 1 to 4)
- **Cost (measured):**
  - channel loss = 1 - (seller message characters delivered / comms-baseline mean)
  - monitor calls per run (operator cost)
  - fraction of rounds gagged
- **Decision statistic:** the break-even cost (reduction share of the ban) and reduction per unit channel loss relative to the ban, with bootstrap CIs. No intrusiveness value is assumed.

## 4. Conditions and stages
All runs use the authors' configuration so that the 50 existing 2025 runs can serve as references:
gpt-4.1 for all 10 agents, 30 rounds, default initial condition. Each lever changes one thing relative to `comms`.

**Budget amendment (Oct 22, before kickoff): Manu approved a $50 cap.** Stages 0 and 1 total 17 runs and are the
whole funded design. Stage 2 runs only with Manu's explicit approval of more spend. H2 and H3 are otherwise
unfunded; the report says so and lists them as future work.

| Stage | Condition | n | Why |
|---|---|---|---|
| 0, canary (Fri) | `comms` | 1 | Checks the API key, measures real cost per run, early drift signal |
| 1 (Fri/Sat) | `comms` | +2 | H5 drift check (n=3 total) |
| 1 | `notice` | 10 | H1, the decisive test |
| 1 | `boss-nocomms` | 4 | H4 (SD 0.04, so n=4 is enough) |
| 2 (needs approval, about +$27; pick one) | `monitor` | 10 | H2 |
| 2, alternative | `oversight25` | 10 | Monitor reads 25% of messages: does a quarter of the monitoring cost keep the effect? (flag from the official starter repo) |
| unfunded | `cap50`, `seltemp` | | H3 and the temperature lever: future work |

Stopping rules:
- Stop all runs at the `BUDGET_USD` cap (`run_sprint.sh` enforces it).
- Never drop a completed run. Failed API runs are logged and re-run under the next replicate number.
- No condition is added after looking at its own results, except the Stage 3 extensions named above.

## 5. Analysis plan
1. Run `run_stats.py` and `frontier.py` over `"data/*_base-*/" "data/*_oversight-*/" "data/*_boss_pressure-*/" "results/*_sp-*/"`.
2. Bootstrap 95% CIs (10k resamples) per condition and per difference.
3. One-sided tests for H1 to H4, Holm-corrected across the four.
4. Pooled OLS of the per-run primary index on lever dummies with HC3 errors, as a robustness check.
5. Report every condition run, the per-run spread (strip plots), and the positive control (comms vs ban).

## 6. Q1.4 stretch (no API cost)
- **Discretization:** each seller's ask series is binned into 3 bins per run.
- **Statistics:**
  - lagged TE score with a circular-shift null (run-level z statistic)
  - Bonjour et al. (2022) net influence, conditioned on the previous-round market state
- **Evaluation:**
  1. AUC separating comms from no-comms runs (2025 and sprint data).
  2. Spearman correlation with the harness LLM-judge coordination score.
  3. Power limits at T=30: on synthetic data with 3 bins, the true pair is ranked #1 in 100% (strong coupling) and 48% (moderate coupling) of 30-round trials. With 5 bins it is only 55% (strong). The bin count (3) is fixed here, before any real data is seen.
- **Framing:** a feasibility and limits result, not a deployed detector.

## 7. Budget (approved cap $50; confirm prices on platform.openai.com)
- **Per-run cost (measured on the 2025 logs, chars/4):** about 640k input and 150k output tokens, so **$2.35 to $2.60 per gpt-4.1 run** at $2/$8 per M tokens. The gpt-4.1-mini judge and monitor add roughly 8 to 10%.
- **Funded design:** 17 runs, about $47.
- **Guard:** `run_sprint.sh` defaults to `BUDGET_USD=50`. Its estimate runs about 5% above the real bill.
- **After the canary:** compare the canary's real cost on the OpenAI usage page with the guard's estimate.

## 8. Deviation log
(append during the sprint: time, what changed, why)

**Correction (23 Oct, 08:20 CDT, read from the system clock).** The first entries below carried clock times I estimated rather than read; several were later than the actual time. Each entry is now anchored to the git commit that first contains it, which is verifiable with `git log`.
- Entries within one commit were written in the order listed.
- **The commit alone cannot prove** that a specification preceded its result when both landed in the same commit (A6, C1 and Q13).
- **Future entries will be committed before the analysis they specify runs.**

- **2026-10-23, commit aedbf59 (07:43 CDT; sprint live; no sprint run executed yet).** The sprint Resources tab frames Q3.4 with a test: *"Claim channel movement only if message-based coordination falls while action-based dependence rises."* Added analysis A6, specified before running it.
  - **Data:** the 2025 gpt-4.1 runs only (`base`, `base-seller_comms`, `oversight`, `boss_pressure`, `boss_pressure-oversight`; n=10 each). Cross-model runs serve as a robustness set.
  - **Action-based dependence:** detector `te_z` (3 bins, 200 circular shifts) over a fixed window, rounds 8 to 30. Round 7 is the latest gag onset observed, so every oversight run is fully gagged inside the window.
  - **Message-based coordination:** delivered seller-message characters in the same window, plus the LLM-judge coordination score.
  - **Channel movement is claimed only if** oversight runs have (a) message characters far below comms runs and (b) `te_z` above **both** comms runs and no-comms runs (one-sided Mann-Whitney, Holm over the two comparisons). Otherwise we report "no evidence of channel movement".
  - **Also:** the AUC of whole-run `te_z` for plain comms vs plain no-comms (detector validity), and the Spearman correlation with the judge score.
  - **Submission tracks:** Track 1 (Q1.5, Q1.4) and Track 3 (Q3.4).
- **2026-10-23, commit aedbf59 (07:43 CDT), A6 and detector-validity results (50 gpt-4.1 runs).**
  - Detector AUC comms vs no-comms: 0.71 (p=0.12).
  - Bonjour flags at the 0.05 threshold: 40/50 runs, including no-comms runs.
  - A6: no evidence of channel movement (messages -99.4%, `te_z` not higher).
  - **EXPLORATORY, found after looking at the data** (`silence_check.py`): the share of flat ask moves (rounds 8 to 30) tracks the judge score (rho=+0.81) and the primary index (rho=+0.41).
- **2026-10-23, commit aedbf59 (07:43 CDT), confirmation test C1, specified before looking at the held-out data.**
  - **Data:** the 25 cross-model runs (`*claude*`, `*mixed*`), not yet used for this statistic, plus later all sprint runs (`results/*_sp-*`).
  - **Statistic:** per-run flat-move share, rounds 8 to 30, threshold |Δask| <= 0.005.
  - **Claim stands only if** Spearman rho with the judge score is > 0 at p < 0.05 (one-sided) on the held-out set. The rho with the primary index is reported either way.
- **2026-10-23, commit aedbf59 (07:43 CDT), C1 result: NOT confirmed.**
  - On the 25 held-out cross-model runs: rho=+0.16 (one-sided p=0.22) with the judge, rho=-0.14 (p=0.50) with the primary index. A first attempt double-counted 5 runs through overlapping globs (n=30, same verdict); corrected to unique runs.
  - Held-out judge scores span only 3.0 to 3.9.
  - Claude sellers hold *low* prices stickily (69% flat moves at index -0.48).
  - **Report as:** stickiness tracks coordination for gpt-4.1 sellers but does not transfer across model families. Sticky is not the same as collusive.
- **2026-10-23, commit 2040915 (08:05 CDT), PROPOSED open-model arm (runs only if Manu approves the OpenRouter spend; specified before any open-model data).**
  - **Why:** the comms baseline is too noisy for gpt-4.1 at $2.48/run. Llama-3.3-70B-Instruct on OpenRouter is about $0.11/run, which affords powered arms.
  - **Pilot (P):** `lo-llama70b` with `comms` x6 and `nocomms` x6, same 5x5x30 config. All agents, the overseer and the judge use the same model; the backend is recorded in `experiment_metadata.json` as `llm_backend`.
  - **Gate:** proceed only if the comms-minus-nocomms primary index is > 0 with a bootstrap 90% CI lower bound > -0.05. That is the positive control.
  - **If the gate passes,** powered arm (O): `comms`, `nocomms`, `oversight`, `notice`, `monitor`, `oversight25`, n=25 each (about 150 runs, about $17). Same hypotheses H1 to H3 plus H2b (`oversight25` vs `oversight`), Holm over the family, primary index as pre-registered.
  - **If the gate fails,** report that Llama-3.3-70B does not collude under communication here, and stop.
  - **Fallback model if Llama misbehaves on JSON (>10% failed calls in the pilot):** Qwen3-32B with thinking off. The switch is recorded here before any data.
  - **Never pooled with gpt-4.1 runs;** reported as a separate model family.
- **2026-10-23, commit 2040915 (08:05 CDT), BUDGET AND DESIGN AMENDMENT (before any paid run).**
  - **Budget:** Manu set **$50 total across all providers**. All runs go through one OpenRouter key; the runner reads the key's real USD usage and stops at `BUDGET_USD=46`, leaving room for OpenRouter's credit fee. This **supersedes** the 17-run gpt-4.1 Stage 0/1 design: at $2.48/run it cannot power any comparison, and the 2025 data already gives gpt-4.1 references.
  - **New lever (L-mav):** Q1.5's own text points to "a single participant playing a no-regret strategy" (Collina et al. 2025). The `maverick` condition replaces seller 5 with `noregret`, a Hedge seller with full-information counterfactual payoffs over asks of 80.5 to 100.0 in steps of 0.5. It sends no messages and makes no model calls. Costs: zero channel loss, zero monitoring, one market seat.
    - **Primary for L-mav:** `collusion_index_2nd_half_llm`, the 4 LLM sellers' asks only. The maverick's own asks would lower the all-seller index mechanically.
    - **Secondary for L-mav:** the all-seller index and mean trade price.
  - **Instruments held constant across model families:** monitor and judge on `openai/gpt-4.1-mini` via `LLM_MODEL_MAP`. The judge is skipped during runs (`SKIP_LLM_JUDGE=1`) and run afterwards on a subset if budget remains.
  - **Phase P, pilot, about $4:**
    - `lo-llama70b` (agents `meta-llama/llama-3.3-70b-instruct`): comms x6, nocomms x6.
    - `lo-mini41` (agents `openai/gpt-4.1-mini`): comms x3, nocomms x3.
    - Gate per model: comms minus nocomms primary index > 0, with a bootstrap 90% CI lower bound > -0.05.
  - **Phase O, about $22, on the cheapest model that passes the gate:** comms, nocomms, oversight, notice, monitor, oversight25 and maverick, n=25 each.
    - Tests: H1 notice<comms; H2 monitor<comms; H2b oversight25<comms; H-mav maverick<comms on the LLM-only primary; plus ban and oversight as references.
    - One-sided bootstrap tests, Holm over H1, H2, H2b and H-mav.
    - If neither model passes the gate, run Phase O on the model with the larger comms-nocomms gap and report the failed positive control prominently.
  - **Phase G, about $12, only if both models pass:** the second model on the key levers comms, nocomms, notice and maverick (n=6 each) as a cross-family replication.
  - **Phase J, the remainder:** the gpt-4.1-mini judge on a stratified subset of Phase O runs, for the detector and judge analyses.
- **2026-10-23, commit 11dfa4f (08:19 CDT), analysis Q13: detector calibration, specified before computing it.** The organizers' Q1.3 suggests calibrating a detector on no-communication runs.
  - **Rule:** flag a run when its whole-run statistic exceeds the 90th percentile of the same statistic over no-comms runs of the same model.
  - **Statistics:** `te_z` and Bonjour `ni_max`.
  - **On the 2025 gpt-4.1 data:**
    - false-positive rate by leave-one-out over the 10 no-comms runs (each null run scored against a threshold from the other 9)
    - detection rate on comms runs
  - **Compare** with Bonjour's fixed 0.05 threshold (40/50 runs flagged).
  - **Re-test the frozen 2025 thresholds** on the held-out sprint-model runs only if that model's no-comms arm gives its own calibration. Thresholds are never refit on the test runs.
- **2026-10-23, commit 11dfa4f (08:19 CDT), Q13 result.**
  - **Bonjour's fixed 0.05 threshold** flags 70% of no-comms runs and 100% of comms runs: unusable as a test.
  - **Calibrated at the no-comms 90th percentile:**

    | Statistic | Threshold | False-positive rate (LOO) | Comms runs detected |
    |---|---|---|---|
    | `te_z` | -1.436 | 10% | 4/10 |
    | `ni_max` | 0.224 | 10% | 4/10 |

  - **Report as:** one ROC operating point with modest power at T=30. The thresholds are now frozen.
- **2026-10-23, 08:28 CDT (system clock; committed before any paid run): unattended orchestration and pilot/main separation.**
  - **Pilot runs are tagged** `lo-pllama70b-*` and `lo-pmini41-*`. They decide the gate only and are **excluded** from the Phase O and Phase G hypothesis tests. Those use only runs tagged with the model name (`lo-llama70b-*`, `lo-mini41-*`).
  - **`run_all.sh` executes the pre-registered sequence without human decisions:**
    1. Phase P, then the gate.
    2. Phase O on the cheapest passing model, or on the larger-gap model if none passes.
    3. Phase G only if both pass.
    4. Phase J: the judge on 4 Phase O runs per condition while budget remains.
    5. The analysis scripts.
  - **Budget:** stop at `BUDGET_USD=46` of real key usage throughout.
- **2026-10-23, 13:06 CDT (system clock; committed before computing): analysis A7 "talk vs prices" (Q2.3, collusion on paper).**
  - **Data:** the 50 gpt-4.1 runs from 2025 (`base`, `base-seller_comms`, `oversight`, `boss_pressure`, `boss_pressure-oversight`). Judge scores come from each run's `llm_eval_full.json`; the per-round score is the mean over sellers.
  - **(a) Within run:** Spearman rho between the per-round judge score and the per-round mean-ask index, computed per run.
    - Primary set: the 10 plain comms runs.
    - Report the mean rho and a two-sided sign test over runs.
  - **(b) Between runs:** Spearman rho of the run-mean judge score against the primary index (rounds 16 to 30), over all 50 runs.
  - **Claim "collusion on paper" only if (a)** gives a mean rho < 0 with sign-test p < 0.05 in the plain comms runs, i.e. judged coordination rises while prices fall. Otherwise report the numbers without the claim.
- **2026-10-23, 13:07 CDT (system clock): A7 results.**
  - **(a) Within run, plain comms:** mean rho -0.49, 9/9 analysable runs negative (one run's judge scores were constant, so its rho is undefined), sign p=0.004.
    - **Pre-registered claim met:** judged coordination rises while prices fall.
    - Boss pressure: -0.24, 10/10 negative.
    - Oversight: +0.42 (sellers judged more docile after the gag as prices fall).
  - **(b) Between runs:** rho +0.61 over 50 runs, so the judge does separate conditions.
  - **EXPLORATORY detrending (round-to-round changes):** comms same-round rho -0.04 (5/10 negative); judge change at t vs price change at t+1, rho -0.11 (7/10, p=0.34).
  - **Report as:** (a) is driven by opposite time trends. The judge's score tracks escalating talk while the market converges toward competitive prices, and round-level judged coordination does not predict price moves. Do NOT claim talk causes prices to fall.
- **2026-10-23, 21:44 CDT (system clock; committed before any paid run): final budget, verified key.**
  - **Money:** Manu bought **$40** of OpenRouter credit. The account shows total_credits 40, usage 0.
  - **Smoke test:** one JSON-mode call each to `meta-llama/llama-3.3-70b-instruct` (provider AkashML) and `openai/gpt-4.1-mini` (OpenAI) returned valid JSON. Cost rounds to $0.
  - **Settings:** `BUDGET_USD=39` (balance minus $1). Phase J (judge, `K_J=3`) runs **before** Phase G. Phase G is trimmed to `N_G=3` per key lever.
  - **Unchanged:** Phase P (pilot) and Phase O (n=25 per lever).
  - **If the budget stop truncates Phase G,** it is reported as truncated and its arms are not tested.
- **2026-10-23, 22:29 CDT (system clock): Phase P result. The positive control FAILED for both models.**
  - **llama70b:** comms -0.006 (n=6) vs nocomms +0.024 (n=6); diff -0.030, 90% lower bound -0.367; 0/12 failed runs; $0.185/run.
  - **mini41:** comms -0.536 (n=3) vs nocomms -0.480 (n=3); diff -0.056, lower bound -0.172; 0/6 failed runs; $0.479/run. Asks sit below the competitive price.
  - **Pre-registered branch taken automatically:** Phase O on llama70b (the larger comms-nocomms gap). The failed positive control is to be reported prominently.
  - **Interpretation fixed now, before Phase O data:** with no collusion to remove, the lever "reductions" estimate effects on a competitive market. Monitor firing in oversight / monitor / oversight25 runs is then a pure false-positive cost: channel loss with no collusion prevented.
  - **Added secondary analysis F1:** monitor fire rate per run and the fraction of rounds gagged in the llama70b oversight arms, against the 2025 gpt-4.1 oversight arms (fired 20/20).
- **2026-10-23, 22:38 CDT (system clock): runtime fix, no design change.**
  - **What failed:** `lo-llama70b-oversight25-1` exited non-zero in the harness's W&B logging step, which runs after all results are written.
  - **Cause:** with 25% sampling the overseer is skipped in rounds where it sees no message, so its per-round list had 27 entries, and W&B asserts 30.
  - **The run's data is complete** (`auction_results.md`, `experiment_metadata.json`, `collusion_metrics.json`, `Overseer.md`) and is kept.
  - **Fix:** `simulation.py` skips W&B logging when `WANDB_MODE=disabled` (always the case here). Runs started before the fix may show the same benign exit.
- **2026-10-23, 22:52 CDT (system clock): runtime fix 2, no design change.**
  - **What failed:** `lo-llama70b-oversight-3` crashed mid-run. Under the gag, Llama returned `message_to_sellers` as a bare number, and `market.py` assumed a string.
  - **Fix:** messages are coerced to text, the same normalisation as the earlier string-price fix.
  - **The crashed run has no metadata and is excluded.** Per section 4 it gets one make-up run of the same lever under the next replicate number after Phase O, so every lever reaches n=25 completed runs.
- **2026-10-24, 02:15 CDT (system clock): Phase O results (llama70b, n=25 per lever) and Phase J.**
  - **Spend:** $37.45 in total. Phase J judged 20 runs; Phase G was skipped (one chosen model). The oversight-3 crash was replaced by make-up run oversight-15.
  - **Pre-registered family (one-sided, "lever < comms"), all null after Holm:**

    | Test | Difference | Holm p |
    |---|---|---|
    | H1 notice | +0.062 | 1.0 |
    | H2 monitor | -0.034 | 0.91 |
    | H2b oversight25 | +0.118 | 1.0 |
    | H-mav (LLM-only index) | -0.054 | 0.81 |

    The comms baseline is competitive (primary index -0.00), consistent with the failed positive control.
  - **F1 (pre-registered secondary), monitor firing on non-colluding markets (all false positives):**
    - monitor-only: 12/25 runs, 31% of rounds gagged
    - oversight25: 7/25 runs, 20% of rounds gagged
    - oversight: 5/25 runs, 7% of rounds gagged
    - gpt-4.1 (2025): 20/20 runs
  - **A6 (llama):** null. Its automatic grouping put notice and maverick runs with comms and all monitored arms together, so it is reported as a secondary, not re-specified.
- **2026-10-24, 02:15 CDT: EXPLORATORY, specified AFTER seeing the Table 1 means. Analysis X1, the backfire check.**
  - **Comparison:** two-sided bootstrap differences (10k) of notice, monitor, oversight and oversight25 against comms.
  - **Outcomes:** primary index, mean trade price, buyer welfare per round.
  - **Correction:** Holm over the 4 arms within each outcome.
  - **Reporting:** exploratory only; never presented as a confirmatory test.
- **X1 extension (exploratory, same rules):** allocative efficiency, trades per run and total seller profit, notice-type arms vs comms.
