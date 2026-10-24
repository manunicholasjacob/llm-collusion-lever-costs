# Report plan (follows the official Apart template; Manu writes the prose)
The template recommends 4 pages excluding references and appendix (8 is the cap): about 1 page for
Introduction and Related Work, 2.5 for Methods and Results, 0.5 for Discussion. It says the final
version should be "primarily written by your team" and requires an LLM Usage Statement. So this
file gives the verified facts, numbers and citations for each section, and Manu writes the text.
Numbers marked [S] come from sprint runs and are filled in after Stage 2. Numbers marked [P] come
from pre-sprint analysis of the authors' public data and must be labelled that way in the report.
House rule: no em dashes anywhere in the report.

**Audience and what wins (researched Oct 22).** The 41 judges are mostly AI security, fraud and evals people
(Anthropic, UK AISI, Meta, Microsoft, MATS, SaferAI), not market economists, so explain CE and JPM in one line each.
Past 1st-place Apart reports won on:
- a crisp, nameable reframe in the title
- controls that separate cause from correlation
- a public repo and a short recording (both common among winners)

Their statistics were usually weak, so our CIs, pre-registration and Holm-corrected tests are a real differentiator; show them in Table 1 and the tests table.
Docked points went to "building on existing work" without a clear new contribution: state ours in the first paragraph.

**Report Google Doc (copied from the official template, Oct 22):**
https://docs.google.com/document/d/17yYLSlvpev7FITEAk8XS8bhhfy_CzO0e82hTFm4jf0o/edit

**Figure and table commands:** RUN_BOOK.md section 4 (`report_tables.py`, `frontier.py`, `detector_eval.py`).

**Working title** (choose after results; do not pre-commit to a claim):
- if H1 holds: "Deterrence Without Enforcement: Measured Costs Reorder Anti-Collusion Levers for LLM Market Agents"
- if H1 fails: "Oversight Is a Delayed Ban: Measured Costs of Anti-Collusion Levers for LLM Market Agents"

## OVERNIGHT RESULTS (Oct 23-24) AND RECOMMENDED FRAMING (read first)
**Data:**
- 175 Llama-3.3-70B runs (7 levers x 25) plus 18 pilot runs, $37.45 in total
- the monitor and judge are gpt-4.1-mini
- all numbers live in `WRITING_PACK.md`; the lead figure is `figs/llama70b/fig_costs.png`

**What happened:**
1. **Positive control failed for both cheap models.**
   - Llama-3.3-70B: comms -0.006 vs no-comms +0.024.
   - gpt-4.1-mini: both about -0.5, i.e. below the competitive price.
   - So the pre-registered "lever reduces collusion" tests (H1, H2, H2b, H-mav) are all null; there was nothing to reduce.
   - Report this prominently. It is itself a finding: collusion in this harness is model-specific. gpt-4.1 shows it (weakly), Llama-70B and gpt-4.1-mini do not.
2. **F1 (pre-registered): the LLM monitor punishes innocent markets.**
   - With no collusion present, monitor-only fired in 12/25 runs, gagging 31% of rounds.
   - Oversight with the notice fired in 5/25; oversight25 in 7/25.
   - gpt-4.1 (2025): 20/20.
3. **X1 (EXPLORATORY): levers have real costs in a market that is not colluding.**

   | Lever | Effect vs comms (95% CI) |
   |---|---|
   | Monitoring notice | Trades -20% (-16.2 [-25.9, -6.6], Holm 0.003); buyer welfare -22% (-5.5 [-9.3, -1.9], Holm 0.004); sellers lose too (-$159) |
   | Monitor without notice | About 0 on every outcome |
   | Ban communication | Trades -13% (-10.6 [-19.1, -2.1]); seller profit -$163 |
   | One no-regret competitor | Buyer welfare +26% (+6.7 [+2.7, +10.6]); trade price -$1.41 |

   - **Reading:** it is the *warning text* that does the damage, a chilling effect, not the monitor.
   - **Why the ban costs trades:** here messages coordinate liquidity ("adjust asks to meet bids").
   - **The competitor** is the one lever that helps buyers.
4. **Contrast with gpt-4.1 (2025 public data, [P]):**
   - Where sellers did collude (weakly), oversight acted as a ban and *raised* buyer welfare (+7.5).
   - In a competitive market the same lever *lowers* it.
   - So a lever's net value depends on whether collusion is present. Price levers by their **false-positive cost**.

**Recommended title (pick one; do not overclaim):**
- "Anti-Collusion Levers Are Not Free: What Monitoring Costs LLM Markets"
- "The Cost of Watching: Anti-Collusion Interventions in LLM Markets With and Without Collusion"

**Story in one line:** an audit shows the reference "oversight" is really a ban; a powered 7-lever study (where cheap models do not collude) shows warnings chill trade, bans cost liquidity and monitors misfire, while adding one no-regret competitor helps buyers.

**Rules for writing it:**
- Every X1 number is labelled exploratory.
- F1 and the pre-registered nulls are confirmatory.
- [P] numbers are labelled pre-sprint analysis of public data.
- Never claim any lever "reduces collusion" in the Llama data.

## Sprint-day additions (Oct 23; all verified against primary sources)
**Novelty check of the headline:** Agrawal et al. say only that sellers are "quickly reprimanded" and gagged. They never report gag frequency, timing, the share of rounds gagged or characters delivered, and never call oversight a ban. Their coordination judge **excludes messages**, so it scores reasoning only.
- Their Table 1 trade prices: oversight 86.24 [85.15, 87.30] vs no communication 87.71 [86.18, 89.69] vs communication 90.52 [88.06, 92.87]. The overlap supports "oversight ≈ ban".
- Our numbers are new: 20/20 runs, gag onset rounds 1 to 7, 77 to 97% of rounds gagged, 10% of characters delivered.
- The paper does not name the overseer model; cite our logs (gpt-4.1-mini).

**Framing for this jury (mostly AI security/control/evals):** use AI-control vocabulary (Greenblatt et al. 2024).
- *Trusted monitoring* with an *auditing budget* and a *false-positive-rate* threshold (their monitor flags the top 2%).
- The harness's monitor fired in 100% of runs, so it spends the whole *usefulness* budget (the message channel) on every agent.
- Ctrl-Z (Bhatt et al. 2025) is the precedent for reporting safety gain together with usefulness cost ("58% to 7% at a 5% cost").
- SCHEMEs (Radev et al. 2026): telling agents a monitor exists halves sabotage. This is prior evidence for deterrence from notice alone.

**Results so far (sprint work, 2025 public runs, $0):**
- **A6, the organizers' Q3.4 criterion:** messages fell 99.4% under the gag (median 234 vs 41,830 chars, rounds 8 to 30), but action-based dependence did NOT rise (te_z oversight vs comms p=0.66, vs no-comms p=0.43). No evidence of channel movement: the gag works like a ban, with no price-side workaround.
- **Q1.4 detector validity:**
  - TE detector AUC for comms vs no-comms: 0.71 (p=0.12, 10 vs 10).
  - Spearman correlation with the judge: +0.26 (p=0.07).
  - Bonjour net influence at its paper threshold of 0.05 flags 40/50 runs, including no-comms runs, so it is uncalibrated for 30-round runs.
- **Exploratory, then failed to replicate (report it, it shows rigour):** the share of flat ask moves tracked the judge at rho=+0.81 on the 50 gpt-4.1 runs. The pre-registered held-out test on 25 cross-model runs gave rho=+0.16 (p=0.22). Claude sellers hold *low* prices stickily (69% flat at index -0.48). Sticky is not the same as collusive.

- **Q1.3 calibration:**
  - Bonjour's fixed 0.05 threshold flags 70% of no-comms runs and 100% of comms runs, so it does not discriminate.
  - Calibrated at the no-comms 90th percentile, `te_z` and `ni_max` each catch 4/10 comms runs at a 10% leave-one-out false-positive rate.
  - Thresholds are frozen for the sprint runs.
- **Price paths (`figs/report/fig_paths.png`), which matters for honest framing:**
  - Under gpt-4.1 with comms, mean asks drift down to about $90.2 by hour 30, essentially the competitive price. The comms "collusion" in the 2025 data lives mostly in the first 15 hours.
  - Boss pressure is the strong, sustained elevation (about $96 throughout), and oversight leaves it unchanged.
  - Oversight ends *below* the ban (about $86.4 vs $87.6).
  - So describe the comms baseline as "slower convergence to competitive prices", not as a stable cartel.

- **A7, Q2.3 "collusion on paper" (pre-registered, then a detrended check):**
  - In plain comms runs the judge's coordination score *rises* while prices *fall*: 10/10 runs, mean within-run rho -0.52, p=0.002.
  - Between conditions the judge does track prices (rho +0.61, n=50).
  - Exploratory detrending (round-to-round changes): rho -0.04, and judged-coordination changes do not predict the next round's price change (rho -0.11, p=0.34).
  - **Write it as:** the judge measures talk, not market harm; escalating collusive talk coexists with convergence to competitive prices. **Do not** claim talk causes prices to fall.
- **Power (for Methods):** with the 2025 gpt-4.1 spreads (SD 0.42 comms, 0.30 ban), n=10 per arm, as in the original paper, has an 80%-power minimum detectable effect of 0.41 to 0.50 index units, larger than the ban's own effect (0.28). Our n=25 gives 0.26 to 0.32, with 68 to 86% power for a ban-sized effect.
- **Publishing:** the upstream harness repo has **no license file**. A public repo should contain only our code (`collusion_analysis/`, a patch of our `src/` changes, figures) and point to andyjliu/llm-agent-collusion for the harness and data. Do not re-host their code or runs.

**Figures ready (public data):**
- `figs/report/fig_gag.png`: gag onset per run, and the channel collapse.
- `figs/report/fig_paths.png`: asks by condition with bands.
- `figs/report/fig_channel.png`: A6 scatter.
- Palette validated for colour-blind readers; every condition keeps one colour across figures.

**Additional verified references** (add to the list; formats as given):
- Greenblatt, R., Shlegeris, B., Sachan, K., Roger, F. (2024). AI Control: Improving Safety Despite Intentional Subversion. ICML 2024; arXiv:2312.06942.
- Bhatt, A., et al. (2025). Ctrl-Z: Controlling AI Agents via Resampling. arXiv:2504.10374.
- Radev, N., Haas, L., Arnav, B., Bernabeu-Pérez, P. (2026). The Best-Laid SCHEMEs: Coordinated Sabotage and Monitoring in Multi-Agent Systems. arXiv:2605.29178.
- Kale, N., et al. (2025). Reliable Weak-to-Strong Monitoring of LLM Agents. arXiv:2508.19461.
- Najt, E., Toft, C., Tracy, T., Roger, F., Benton, J. (2026). SLEIGHT-Bench: A Benchmark of Evasion Attacks Against Agent Monitors. arXiv:2605.16626.
- Jiralerspong, T., Kondrup, F., Bengio, Y. (2026). Noticing the Watcher: LLM Agents Can Infer CoT Monitoring from Blocking Feedback. arXiv:2603.16928. Note: models inferred the monitor in "up to 19%" of episodes; 3 of 2,400 formed an intent to hide; evasion success was 0%.
- Liu, Q., et al. (2026). Breaking the Secret: Economic Interventions for Combating Collusion in Embodied Multi-Agent Systems. arXiv:2604.23511.
- Dhanda, K. (2026). A Price Cap Can Act as a Focal Point for LLM Pricing Agents. Research Square. https://doi.org/10.21203/rs.3.rs-10183486/v1 (an announced cap is the most collusive; a hidden cap does not induce collusion).
- Tomašev, N., Franklin, M., Jacobs, J., Krier, S., Osindero, S. (2025). Distributional AGI Safety. arXiv:2512.16856.
- Mathew, Y., Matthews, O., McCarthy, R., Velja, J., Schroeder de Witt, C., Cope, D., Schoots, N. (2025). Hidden in Plain Text: Emergence & Mitigation of Steganographic Collusion in LLMs. IJCNLP-AACL 2025; arXiv:2410.03768.
- Rippin, J. L., Marshall, S. C., Africa, D. D., Schroeder de Witt, C. (2026). Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems. arXiv:2606.28425.
- Anto, M., Vazquez, J. (2026). Oversight is Not Compliance: Tacit Collusion in LLM Pricing Agents Under Antitrust Regulation. ICML 2026 Agents in the Wild Workshop. https://icml.cc/virtual/2026/67865. Closest prior work: it compares logging, revision and veto without costs. Re-open the link before citing.
- Garra (2026) full text checked: Bertrand duopoly, DeepSeek-V3.1, 7 runs per condition. It measures **no intervention cost**.

**Speakers present at the sprint** (likely reading Q3.4 closely): Velja (Hidden in Plain Text), Motwani (Secret Collusion), Bagdasarian and Nakamura (Colosseum), Anwar.

## Abstract (150 to 250 words, write last)
Cover four things:
- **Problem:** which single restriction buys the most collusion reduction per unit cost.
- **Gap:** prior work measures levers on effect alone.
- **Method:** measured channel-loss cost in the Agrawal et al. double auction; oversight split into notice and monitor.
- **Key numbers and takeaway:** [S], [P].

## 1. Introduction
- **Threat model:** LLM sellers in a market tacitly or overtly coordinate on supracompetitive prices (Agrawal et al. 2025; Fish et al. 2024).
- **Why it matters:** the cheapest effective lever is what a platform or regulator would actually deploy.
- **The problem with current comparisons:** levers are compared on effect only, or on an assumed intrusiveness. [P] The reference "oversight" condition gagged sellers in 20/20 runs, so its real channel cost (0.90) is close to a ban's.
- **Contributions** (edit to match results):
  1. A measured cost axis (channel loss, monitor calls) for anti-collusion levers, with bootstrap uncertainty.
  2. A decomposition of oversight into deterrence (notice) and enforcement (monitor/gag) [S].
  3. A control showing whether pressure-driven high prices need communication at all [S].
  4. (Stretch) The first application of Bonjour et al.'s net-influence statistic to LLM agents, with its power limits at realistic run lengths.

## 2. Related Work (verified Oct 22; keep these exact characterisations)
- Fish et al. (2024): LLM pricing agents reach supracompetitive prices **without communication**; small prompt wording changes shift the level.
- Agrawal et al. (2025): seller communication raises collusion; models differ; oversight and CEO urgency shift behaviour.
  - Urgency dominates oversight (trade price 96.16 with both).
  - The 5-character cap is part of their oversight condition, never tested alone. Sellers kept signalling with single symbols and emojis.
- Nakamura et al. (2026), Colosseum: secret channels lead most models to collude in cooperative multi-agent systems; agents often agree "on paper" and then act non-collusively.
- Keppo et al. (2026): heterogeneity (patience, data access) weakens LLM collusion. Pairing with a Q-learner ends at +2 to +8% above competitive. A model-size mismatch can **stabilise** collusion.
- Xu et al. (2026): cross-agent residual coupling falls monotonically with sampling temperature (p=0.002); price-level audits miss collusion with competitive marginals.
- Bracale Syrnikov et al. (2026): prompt-only anti-collusion "constitutions" give no reliable improvement; an enforced governance graph cuts severe collusion from 50% to 5.6%. This motivates the notice-vs-monitor split.
- Garra (2026), repeated oligopoly pricing with DeepSeek-V3.1: a prompt-only warning "reduces but does not eliminate above-Nash pricing"; also tests an expected-damages regulator and a random entrant. Closest prior evidence on warnings alone. It does not report intervention cost (abstract checked; check the full text before claiming that). Our addition: measured cost, and a warning vs monitor split in the double auction.
- Collina et al. (2025), theory: one human defecting to a no-regret strategy can destabilise algorithmic collusion.
- Calvano et al. (2020): Q-learning pricing agents learn to collude without communicating, using punish-then-return strategies.
- Detection:
  - LLM-judge coordination scores (Agrawal et al. 2025).
  - Cross-run mutual information (Tailor 2025).
  - Partial information decomposition of time-delayed MI in LLM groups (Riedl 2026).
  - Steganographic collusion (Motwani et al. 2024).
  - Bonjour et al. (2022) net influence: conditional MI given state, minus the strongest rival's influence; rule-based and DDQN agents in RPS and Leduc poker.
- **Novelty wording (exact):** "to our knowledge, Bonjour et al.'s pairwise net-influence statistic has not been applied to LLM agents; prior LLM work uses cross-run MI (Tailor 2025) or PID of time-delayed MI (Riedl 2026)." Do NOT claim information-theoretic detection of LLM collusion is new.

## 3. Methods
- **Environment:** Agrawal et al. continuous double auction, unmodified market logic.
  - 5 sellers (cost $80), 5 buyers (value $100), 30 rounds.
  - The harness opens with asks at 97.5 ± 2.5 and bids at 82.5 ± 2.5.
  - gpt-4.1 for all trading agents at temperature 0.7. The judge and monitor are gpt-4.1-mini.
- **Collusion index:** mean seller ask, scaled so CE $90 = 0 and JPM $100 = 1.
  - Primary: rounds 16 to 30 (pre-registered; rationale: the initial condition).
  - Also: whole run, trade price, efficiency, judge score.
- **Cost:**
  - channel loss = 1 - delivered seller-message characters / comms-baseline mean (ban = 1 by construction)
  - monitor calls per run
  - fraction of rounds gagged
- **Levers (one change vs. comms baseline):**
  - ban
  - full oversight (2025 data)
  - notice only
  - monitor/gag only
  - 50-character static cap
  - seller-only temperature 1.2
  - boss pressure with and without comms (amplifier controls)
- **Replication:** n per condition [S]. The 2025 runs serve as references (n=10 each). Pooling rule per the protocol's drift check.
- **Statistics:** bootstrap 95% CIs (10k), Holm-corrected one-sided tests for H1 to H4, OLS with HC3 as robustness.
- **Harness changes (preexisting, disclosed):** three flags whose defaults reproduce original behaviour, verified by a $0 mock test.

## 4. Results (figures and tables)
- **Figure 1:** measured-cost frontier, x = reduction [95% CI], y = channel loss, with the ban-parity line.
- **Table 1:** per lever: n, primary index, whole-run index, reduction [CI], channel loss, red/loss vs ban, % rounds gagged, buyer welfare.
- **Figure 2:** per-run strip plot of the primary index by condition (shows the noisy comms baseline, SD 0.40 [P]).
- **Figure 3 (stretch):** detector AUC and the correlation of the detector with the judge; synthetic power curve vs. T (15/30/60/200 rounds).
- **Pre-sprint facts to report as [P]:**
  - Gag fired in 20/20 runs at rounds 1 to 7; gagged for 77 to 97% of rounds; channel retained 10%.
  - Boss pressure 0.659 vs boss+oversight 0.652.
  - The assumed-intrusiveness ratio (1.8x) becomes 0.82x (whole run) or 1.26x (second half) at measured cost.

## 5. Discussion and Limitations
- **Interpretation:** depends on H1/H2 [S].
- **Limitations:**
  - one market, homogeneous valuations, one model family, n=10 to 15 per arm against a noisy baseline (power for differences of about 0.2 needs about 54 per arm)
  - the overseer's 4/4 threshold is the harness default
  - channel loss prices the information channel, not legitimate uses of it (a benign-task cost would be future work)
  - the notice is non-credible if never enforced, so long-horizon deterrence may decay
  - the API model may drift since 2025 (H5)
- **Future work:** a benign-cooperation cost task, credible-threat schedules, mixed-model markets, longer horizons for the detector.

### Dual-use / ethical considerations (required appendix)
- **Dual-use:** ranking levers by cheapness also tells a colluding operator which restrictions to lobby against, and when monitoring is non-credible. Detector power limits also hint at how short or lagged a convention must be to evade it.
- **Mitigation:** we report aggregate effects and omit any recipe for evasion.
- **Scope:** all agents are simulated. No real markets, firms or people are involved.

## 6. Conclusion (1 to 2 paragraphs, after results)

## Code and Data
Repository link if Manu chooses to publish it (optional).

## LLM Usage Statement (required)
Describe it honestly. Claude (Anthropic) assisted with:
- engineering: harness flags, analysis scripts, mock tests
- auditing the pre-built tooling
- statistics
- verifying citations against primary sources

All numbers were regenerated from logged runs, and the prose was written by the author.

## References (verified Oct 22 against arXiv, PMLR, AEA; consistent format)
1. Agrawal, K., Teo, V., Vazquez, J. J., Kunnavakkam, S., Srikanth, V., Liu, A. (2025). Evaluating LLM Agent Collusion in Double Auctions. arXiv:2507.01413. https://arxiv.org/abs/2507.01413
2. Bonjour, T., Aggarwal, V., Bhargava, B. (2022). Information Theoretic Approach to Detect Collusion in Multi-Agent Games. UAI 2022, PMLR 180:223-232. https://proceedings.mlr.press/v180/bonjour22a.html
3. Bracale Syrnikov, M., Pierucci, F., Galisai, M., Prandi, M., Bisconti, P., Giarrusso, F., Sorokoletova, O., Suriani, V., Nardi, D. (2026). Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs. arXiv:2601.11369. https://arxiv.org/abs/2601.11369
4. Calvano, E., Calzolari, G., Denicolò, V., Pastorello, S. (2020). Artificial Intelligence, Algorithmic Pricing, and Collusion. American Economic Review 110(10):3267-3297. https://doi.org/10.1257/aer.20190623
5. Collina, N., Arunachaleswaran, E. R., Jagadeesan, M. (2025). Breaking Algorithmic Collusion in Human-AI Ecosystems. arXiv:2511.21935. https://arxiv.org/abs/2511.21935
6. Fish, S., Gonczarowski, Y. A., Shorrer, R. I. (2024). Algorithmic Collusion by Large Language Models. arXiv:2404.00806 (EC 2026). https://arxiv.org/abs/2404.00806
7a. Garra, A. (2026). Mitigating Emergent Collusion in LLM Pricing Agents. arXiv:2609.13037. https://arxiv.org/abs/2609.13037
7. Keppo, J., Li, Y., Tsoukalas, G., Yuan, N. (2026). On the Fragility of AI Agent Collusion. arXiv:2603.20281. https://arxiv.org/abs/2603.20281
8. Motwani, S. R., et al. (2024). Secret Collusion among AI Agents: Multi-Agent Deception via Steganography. NeurIPS 2024. arXiv:2402.07510. https://arxiv.org/abs/2402.07510
9. Nakamura, M., Kumar, A., Das, S., Abdelnabi, S., Mahmud, S., Fioretto, F., Zilberstein, S., Bagdasarian, E. (2026). Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems. arXiv:2602.15198. https://arxiv.org/abs/2602.15198
10. Riedl, C. (2026). Emergent Coordination in Multi-Agent Language Models. ICLR 2026. arXiv:2510.05174. https://arxiv.org/abs/2510.05174
11. Tailor, O. (2025). Audit the Whisper: Detecting Steganographic Collusion in Multi-Agent LLMs. arXiv:2510.04303. https://arxiv.org/abs/2510.04303
12. Xu, X., Wu, C., Lu, J., Tan, K., Tao, S., Hong, H. (2026). Collusion with Competitive Marginals: Price-Level Audits Are Blind by Construction. arXiv:2607.26385. https://arxiv.org/abs/2607.26385
(If transfer entropy is cited: Schreiber, T. (2000). Measuring Information Transfer. Phys. Rev. Lett. 85, 461. Verify the DOI before use.)
