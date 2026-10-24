# Anti-Collusion Levers Are Not Free: Measuring What Monitoring Costs LLM Markets

**Manu Nicholas Jacob**, Independent Researcher. With Apart Research.

Track 1 (Markets and Collusion: Q1.5, Q1.3, Q1.4) and Track 3 (Q3.4).

## Abstract

Which single restriction removes the most LLM-agent collusion at the least cost? Prior work compares anti-collusion levers by their effect alone; we also price them. In the continuous double auction of Agrawal et al. (2025) we first audit the reference "oversight" lever in the authors' public runs: its LLM monitor fired in 20 of 20 runs within seven rounds and limited sellers to five-character messages for 77 to 97% of each run, so it acts as a delayed communication ban rather than light-touch monitoring. We then run a pre-registered, powered study of seven levers (25 runs each) with Llama-3.3-70B sellers, separating a monitoring notice from the monitor, varying the monitoring budget, and adding a single no-regret competitor seller. Our positive control failed: neither Llama-3.3-70B nor GPT-4.1-mini sellers colluded when allowed to communicate, so no lever could reduce collusion, and the study measures what levers cost a market that is not colluding. The monitor punished innocent markets in up to 48% of runs. A monitoring notice lowered buyer welfare by 22% while the monitor without the notice had no detectable effect, and banning communication cost 13% of trades. One no-regret seller raised buyer welfare by 27%. A replication on 75 fresh runs, pre-registered before it ran, confirmed both welfare effects (notice -16%, competitor +44%) but not the notice's effect on trade volume. Anti-collusion levers carry false-positive costs that should be measured alongside their benefits.

## 1. Introduction

LLM agents that set prices can sustain prices above the competitive level, with or without talking to each other (Fish et al., 2024; Agrawal et al., 2025). A platform or regulator facing this risk will deploy the cheapest lever that works: a communication ban, a monitor, a warning, or a change to who is in the market. Existing studies compare such levers by how much collusion they remove (Agrawal et al., 2025; Bracale Syrnikov et al., 2026; Garra, 2026; Anto and Vazquez, 2026), but none measures what a lever costs, and in particular what it costs when there is no collusion to remove. In AI-control terms, a monitor has a false-positive rate and spends a usefulness budget (Greenblatt et al., 2024; Bhatt et al., 2025); anti-collusion levers should be priced the same way.

**Our main contributions are:**
1. An audit of the reference oversight lever in the Agrawal et al. harness: in the authors' public gpt-4.1 runs, its monitor fired in 20/20 runs and removed about 90% of seller messages, so "oversight" in that environment is a delayed ban. The original paper does not report this.
2. A pre-registered, powered comparison of seven levers (n=25 each) that splits deterrence (a monitoring notice) from enforcement (a monitor that gags sellers), varies the monitoring budget, and tests a no-regret competitor, the lever singled out in the sprint's Q1.5.
3. Evidence that levers are costly where there is no collusion: a monitor that misfires on innocent markets, a warning that lowers buyer welfare and a communication ban that costs liquidity, while a single competitor raises buyer welfare. Both welfare effects replicated on fresh runs pre-registered before they ran.
4. Evidence-standard results for Q1.3 and Q2.3: an information-theoretic detector calibrated against no-communication runs, and an LLM judge whose coordination score tracks talk rather than prices.

## 2. Related Work

**LLM collusion.** Fish et al. (2024) show LLM pricing agents reaching supracompetitive prices without any communication, with large effects from small prompt changes. Agrawal et al. (2025) find that seller communication raises collusion in a double auction and that oversight and urgency shift behaviour; their oversight condition combines a warning with a message cap that is triggered by an LLM monitor. Keppo et al. (2026) find that heterogeneity among agents weakens collusion, and Calvano et al. (2020) show reinforcement-learning pricing agents colluding without communication.

**Interventions.** Bracale Syrnikov et al. (2026) find that a prompt-only anti-collusion instruction gives no reliable improvement while an enforced governance graph sharply reduces severe collusion. Garra (2026) finds that a prompt-only warning reduces but does not eliminate above-Nash pricing. Anto and Vazquez (2026) compare passive logging, revision and veto oversight and find that the best mode depends on the model. Collina et al. (2025) show theoretically that a single participant playing a no-regret strategy can destabilise algorithmic collusion. None of these studies measures the cost of an intervention, and none separates a warning from the monitor that backs it. Radev et al. (2026) report that telling agents a monitor is present halves coordinated sabotage, a deterrence effect in a non-market setting.

**Monitoring and detection.** AI-control work frames monitors in terms of auditing budgets, false-positive rates and usefulness costs (Greenblatt et al., 2024; Bhatt et al., 2025). For collusion detection, Bonjour et al. (2022) define pairwise net influence for small games; to our knowledge it has not been applied to LLM agents, while prior LLM work uses cross-run mutual information (Tailor, 2025) or partial information decomposition (Riedl, 2026). Nakamura et al. (2026) observe "collusion on paper": agents that agree to collude in text but act otherwise.

## 3. Methods

**Environment.** We use the Agrawal et al. (2025) continuous double auction unchanged in its market logic: 5 sellers (cost $80), 5 buyers (value $100), 30 hourly rounds, initial asks near $97.5. Sellers may send each other messages each round. In the oversight condition an LLM monitor scores seller messages from 1 to 4 and, after the first 4, limits all sellers to five-character messages for the rest of the run.

**Models.** Trading agents are Llama-3.3-70B-Instruct (via OpenRouter) in the new runs; the monitor and the judge are GPT-4.1-mini in every arm, so the measuring instruments are constant. The 2025 audit uses the authors' public gpt-4.1 runs (10 per condition).

**Levers (one change each, versus communication on).** Ban communication; monitoring notice only (the warning text, no monitor); monitor only (monitor and gag, no warning); full oversight (both); oversight with a monitor that reads a random 25% of messages; and one no-regret seller (Hedge over asks $80.5 to $100 with full-information counterfactual payoffs) replacing one LLM seller.

**Outcomes and costs.** The primary collusion index is the mean seller ask over hours 16 to 30, scaled so the competitive price ($90) is 0 and the joint-profit price ($100) is 1 (for the no-regret lever, LLM sellers only). Costs: messages delivered (channel loss), monitor firing, completed trades, allocative efficiency, buyer welfare and seller profit.

**Design and statistics.** A pilot (6 plus 6 runs per model) applied a pre-registered positive-control gate before the main study (25 runs per lever). Hypothesis tests use one-sided bootstrap differences (10,000 resamples) with Holm correction; exploratory comparisons use two-sided bootstrap intervals and are labelled as such. The exploratory effects of the notice and the no-regret seller were then tested in a confirmatory replication, pre-registered before any of its 75 fresh runs (25 each of communication, notice and no-regret seller), with Holm correction over its three tests. Every design decision, deviation and runtime fix is timestamped in a protocol committed to git before the analysis it governs. With the 2025 gpt-4.1 spread (SD 0.42), the original 10 runs per arm could detect only effects of 0.41 to 0.50 index units at 80% power, larger than the communication ban's own effect (0.28); 25 runs per arm detects 0.26 to 0.32.

## 4. Results

**4.1 The reference oversight is a delayed ban (pre-sprint analysis of public data).** In the authors' runs the monitor fired in 10/10 oversight runs and 10/10 runs combining oversight with profit pressure, first at hours 1 to 7, gagging sellers for 77 to 97% of the run; only 10% of message characters were delivered relative to the communication baseline (Figure 1). Priced at this measured cost, oversight is 0.82 to 1.26 times as cost-effective as a ban depending on the metric, with overlapping confidence intervals, rather than the "nearly free" lever an assumed cost suggests.

[Figure 1: figs/report/fig_gag.png. Caption: Left, the hour at which the monitor first fired and the gagged span, for all 20 gpt-4.1 oversight runs. Right, seller message characters delivered per hour, communication baseline versus oversight (mean of 10 runs).]

**4.2 The positive control failed.** With communication, Llama-3.3-70B sellers did not price above the no-communication arm (index -0.006 versus +0.024, n=6 each), and GPT-4.1-mini sellers priced below the competitive level in both arms (-0.54 versus -0.48). In the main study the Llama communication baseline sits at the competitive price (index -0.00, 95% CI [-0.09, 0.08]). Following the pre-registered rule, the main study ran on Llama-3.3-70B. In the pre-registered tests (H1 notice, H2 monitor, H2b 25% monitor, H-mav competitor) no lever reduced collusion (all Holm p > 0.8): there was no collusion to reduce.

**4.3 The monitor punishes innocent markets.** Because no Llama market colluded, every monitor firing is a false positive. The monitor alone fired in 12 of 25 runs and gagged 31% of rounds; with the warning in place it fired in 5 of 25 (7% of rounds), and reading 25% of messages it fired in 7 of 25 (20% of rounds) (Figure 2, right).

**4.4 What levers cost a market that is not colluding (exploratory).** Compared with the communication baseline (81 trades per run, buyer welfare 25.3 per round):

| Lever | Trades per run | Buyer welfare per round | Seller profit |
|---|---|---|---|
| Monitoring notice only | -16.2 [-25.9, -6.6], Holm p=0.003 | -5.5 [-9.3, -1.9], Holm p=0.004 | -$159 [-309, -12] |
| Monitor only | -5.3 [-14.0, +3.3] | -0.3 [-4.3, +3.6] | -$97 [-225, +24] |
| Full oversight | -10.1 [-20.5, +0.1] | -4.8 [-8.4, -1.1], Holm p=0.025 | -$59 [-209, +83] |
| Ban communication | -10.6 [-19.1, -2.1] | -1.6 [-5.3, +2.0] | -$163 [-295, -37] |
| One no-regret seller | +8.0 [-1.6, +17.5] | +6.7 [+2.7, +10.6] | -$41 [-187, +106] |

The warning, not the monitor, does the damage: arms that include the notice lose buyer welfare (and, in this sample, trades), while the monitor without the notice does not. Warned sellers turned their messages toward compliance (28% of messages mention monitoring or regulation, against 3% without the notice) and held slightly higher asks. A communication ban costs liquidity because these sellers used messages to converge on tradable prices. The no-regret seller is the only lever that helps buyers, lowering mean trade prices by $1.41. In this sample the trade effect also survives a rank test (median 60 versus 82 trades, Mann-Whitney p=0.005), but it did not replicate (Section 4.5).

[Figure 2: figs/llama70b/fig_costs.png. Caption: Differences from the communication baseline in trades per run and buyer welfare per round, with 95% bootstrap intervals (Llama-3.3-70B sellers, 25 runs per lever), and the share of runs in which the monitor fired, all false positives because no market colluded.]

**4.5 Confirmatory replication.** We pre-registered three tests of the exploratory results and ran them on 75 fresh runs:

| Pre-registered test (fresh runs, n=25 per arm) | Difference [95% CI] | Holm p | Result |
|---|---|---|---|
| Notice lowers trades per run | +0.96 [-8.56, +10.28] | 0.59 | Not confirmed |
| Notice lowers buyer welfare per round | -3.73 [-7.43, -0.19] | 0.040 | Confirmed |
| No-regret seller raises buyer welfare per round | +10.00 [+5.73, +14.26] | <0.001 | Confirmed |

The arms themselves were stable across the two samples (buyer welfare under the notice 19.7 and 19.1; under the no-regret seller 32.0 and 32.8), while the communication baseline varied (25.3 and 22.8), so part of the original trade gap reflected an unusually busy baseline. In the replication the notice hurt buyers through higher prices rather than fewer trades (mean trade price $91.88 versus $90.49), and warned sellers again talked more about monitoring and regulation (17% versus 8% of messages). The robust conclusions are therefore that a monitoring warning lowers buyer welfare in markets that are not colluding, by a route that varies, and that a single no-regret competitor raises it.

**4.6 Evidence standards.** (i) Detection (Q1.3, Q1.4): on the gpt-4.1 runs, Bonjour et al.'s net influence at its published threshold flags 70% of no-communication runs; calibrated at the 90th percentile of no-communication runs, net influence and a transfer-entropy statistic each detect 4 of 10 communication runs at a 10% false-positive rate. (ii) Judges (Q2.3): within communication runs, the LLM judge's coordination score rose while prices fell in 9 of 9 runs (mean within-run rho -0.49, sign test p=0.004); on round-to-round changes the correlation vanishes (rho -0.04). The judge measures talk, not market outcomes. (iii) Channel movement (Q3.4): under the gag, gpt-4.1 messages fell by 99.4% but price-path dependence did not rise, so we find no evidence that coordination moved into prices.

## 5. Discussion and Limitations

The same lever can help or hurt depending on whether collusion is present. In the gpt-4.1 data, where sellers colluded weakly, oversight acted as a ban and raised buyer welfare (27.2 versus 19.8 per round). In Llama markets that did not collude, the warning attached to oversight lowered buyer welfare by about a fifth and the monitor misfired in up to half of runs. A platform therefore cannot judge a lever by its effect on colluding markets alone; it should also measure its false-positive cost, the harm to the many markets that are behaving competitively. By that standard the most attractive lever we tested is a competitor rather than a cop: a single no-regret seller costs no communication and no monitoring and improved buyer outcomes. For AI-control practice, a monitor with a hair-trigger, permanent penalty spends its whole usefulness budget on false positives, and the warning that announces it can impose costs by itself.

### Limitations
- One market environment with homogeneous costs and values; one main model family for the new runs; the failed positive control means we could not test lever benefits on the same model.
- Collusion in this harness is model-specific: gpt-4.1 shows weak communication-driven collusion, Llama-3.3-70B and GPT-4.1-mini do not.
- The cost results in Section 4.4 were found after inspecting the data. Of the three we then tested on fresh pre-registered runs, the two welfare effects replicated and the trade-volume effect did not, and the route by which the warning hurts buyers (fewer trades in one sample, higher prices in the other) is not stable.
- The monitor's threshold and permanent gag are the harness defaults; other thresholds would change false-positive rates.
- Buyer welfare and trades are in-market costs; costs outside the market (for example, lost legitimate coordination) are not measured.
- Thirty rounds limit the power of information-theoretic detectors.

### Future Work
A model that colludes reliably, to measure lever benefits and costs in the same model; calibrated monitor thresholds and budgets; credible versus non-credible warnings; mixed-model markets; and multiple competitor sellers.

## 6. Conclusion

Anti-collusion levers for LLM markets should be priced, not just scored. In the reference environment, "oversight" is a delayed ban. In markets where agents do not collude, monitors misfire, warnings lower buyer welfare and bans cost liquidity, while a single no-regret competitor helps buyers; both welfare effects held up in a pre-registered replication. Measuring false-positive costs should be part of evaluating any intervention against AI collusion.

## Code and Data
- Code: analysis, runners and harness changes (as a patch against the original repository), with a README marking pre-sprint and sprint work; available from the author on request.
- Data: the original runs are in Agrawal et al.'s public repository (https://github.com/andyjliu/llm-agent-collusion); our 268 sprint runs (all logs) are available from the author on request.
- Pre-sprint work (disclosed): analysis tooling and harness flags were built on 22 October 2026, before the sprint; all new runs and analyses were done during the sprint. Every step is timestamped in the protocol file.

## Author Contributions
M.N.J. designed the study, made the decisions at each stage and reviewed the manuscript. Analysis code, runs and the first draft were produced with Claude (see the LLM Usage Statement).

## References
1. Agrawal, K., Teo, V., Vazquez, J. J., Kunnavakkam, S., Srikanth, V., Liu, A. (2025). Evaluating LLM Agent Collusion in Double Auctions. arXiv:2507.01413. https://arxiv.org/abs/2507.01413
2. Anto, M., Vazquez, J. (2026). Oversight is Not Compliance: Tacit Collusion in LLM Pricing Agents Under Antitrust Regulation. ICML 2026 Workshop on Agents in the Wild. https://icml.cc/virtual/2026/67865
3. Bhatt, A., et al. (2025). Ctrl-Z: Controlling AI Agents via Resampling. arXiv:2504.10374. https://arxiv.org/abs/2504.10374
4. Bonjour, T., Aggarwal, V., Bhargava, B. (2022). Information Theoretic Approach to Detect Collusion in Multi-Agent Games. UAI 2022, PMLR 180:223-232. https://proceedings.mlr.press/v180/bonjour22a.html
5. Bracale Syrnikov, M., et al. (2026). Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs. arXiv:2601.11369. https://arxiv.org/abs/2601.11369
6. Calvano, E., Calzolari, G., Denicolò, V., Pastorello, S. (2020). Artificial Intelligence, Algorithmic Pricing, and Collusion. American Economic Review 110(10):3267-3297. https://doi.org/10.1257/aer.20190623
7. Collina, N., Arunachaleswaran, E. R., Jagadeesan, M. (2025). Breaking Algorithmic Collusion in Human-AI Ecosystems. arXiv:2511.21935. https://arxiv.org/abs/2511.21935
8. Fish, S., Gonczarowski, Y. A., Shorrer, R. I. (2024). Algorithmic Collusion by Large Language Models. arXiv:2404.00806. https://arxiv.org/abs/2404.00806
9. Garra, A. (2026). Mitigating Emergent Collusion in LLM Pricing Agents. arXiv:2609.13037. https://arxiv.org/abs/2609.13037
10. Greenblatt, R., Shlegeris, B., Sachan, K., Roger, F. (2024). AI Control: Improving Safety Despite Intentional Subversion. ICML 2024; arXiv:2312.06942. https://arxiv.org/abs/2312.06942
11. Keppo, J., Li, Y., Tsoukalas, G., Yuan, N. (2026). On the Fragility of AI Agent Collusion. arXiv:2603.20281. https://arxiv.org/abs/2603.20281
12. Nakamura, M., et al. (2026). Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems. arXiv:2602.15198. https://arxiv.org/abs/2602.15198
13. Radev, N., Haas, L., Arnav, B., Bernabeu-Pérez, P. (2026). The Best-Laid SCHEMEs: Coordinated Sabotage and Monitoring in Multi-Agent Systems. arXiv:2605.29178. https://arxiv.org/abs/2605.29178
14. Riedl, C. (2026). Emergent Coordination in Multi-Agent Language Models. ICLR 2026; arXiv:2510.05174. https://arxiv.org/abs/2510.05174
15. Tailor, O. (2025). Audit the Whisper: Detecting Steganographic Collusion in Multi-Agent LLMs. arXiv:2510.04303. https://arxiv.org/abs/2510.04303

## Appendix A. Limitations and Dual-Use / Ethical Considerations
**What our results do and do not establish.** We establish, for one simulated double auction, that the reference oversight lever behaves as a delayed ban, that an LLM monitor misfires on non-colluding markets, and, in a pre-registered replication on fresh runs, that a monitoring warning lowers buyer welfare and a single no-regret seller raises it where no collusion is present. We do not establish that any lever reduces collusion in Llama-3.3-70B markets, because those markets did not collude, nor that these magnitudes transfer to real markets, other models, or other market designs.

**Dual use.** Ranking levers by cost also tells a colluding operator which restrictions are cheapest to resist or to lobby against, and showing that a warning can be costly could be used to argue against oversight in general; our results argue for measuring and calibrating oversight, not for removing it. Detector power limits indicate how short or noisy coordination must be to evade a statistical monitor. We report aggregate effects only and provide no method for evading monitors. All agents are simulated; no real market, firm or person is involved.

## Appendix B. Additional results

**Table B1. Pre-registered tests (Llama-3.3-70B, 25 runs per arm; one-sided bootstrap, Holm over the family).**

| Test | Claim | Difference [95% CI] | Holm p |
|---|---|---|---|
| H1 | Notice lowers the collusion index | +0.062 [-0.057, +0.183] | 1.00 |
| H2 | Monitor lowers the collusion index | -0.034 [-0.162, +0.091] | 0.91 |
| H2b | 25% monitor lowers the collusion index | +0.118 [+0.002, +0.235] | 1.00 |
| H-mav | No-regret seller lowers the LLM sellers' index | -0.054 [-0.181, +0.070] | 0.81 |

**Table B2. Monitor firing. For Llama-3.3-70B no market colluded, so every firing is a false positive.**

| Model | Arm | Runs where monitor fired | Rounds gagged (mean) | Message channel kept |
|---|---|---|---|---|
| gpt-4.1 (2025 public runs) | Oversight | 10/10 | 85% | 10% |
| gpt-4.1 (2025 public runs) | Profit pressure + oversight | 10/10 | 90% | 6% |
| Llama-3.3-70B | Oversight | 5/25 | 7% | 93% |
| Llama-3.3-70B | Monitor only | 12/25 | 31% | 69% |
| Llama-3.3-70B | Oversight, monitor reads 25% | 7/25 | 20% | 79% |

**Table B3. Per-lever means (Llama-3.3-70B, 25 runs each; index in brackets is the 95% bootstrap interval; the no-regret row's index includes its own asks).**

| Lever | Collusion index (hours 16-30) | Mean trade price | Allocative efficiency | Buyer welfare per round |
|---|---|---|---|---|
| Communication baseline | -0.00 [-0.09, 0.08] | $90.54 | 0.54 | 25.27 |
| Ban communication | 0.03 [-0.03, 0.10] | $89.91 | 0.47 | 23.63 |
| Monitoring notice only | 0.06 [-0.02, 0.15] | $90.68 | 0.43 | 19.73 |
| Monitor only | -0.03 [-0.13, 0.06] | $90.20 | 0.50 | 24.96 |
| Full oversight | 0.12 [0.06, 0.17] | $91.20 | 0.47 | 20.51 |
| Oversight, monitor reads 25% | 0.12 [0.04, 0.20] | $91.49 | 0.45 | 19.29 |
| One no-regret seller | -0.13 [-0.21, -0.06] | $89.12 | 0.59 | 31.97 |

[Figure B1: figs/report/fig_paths.png. Caption: Mean seller ask by hour in the 2025 gpt-4.1 public runs (10 per condition) with 95% bootstrap bands. With communication, asks drift back toward the competitive price by hour 30; profit pressure keeps them near $96 with or without oversight.]

[Figure B2: figs/report/fig_channel.png. Caption: Per-run seller message characters (hours 8-30, log scale) against price-path dependence (transfer-entropy z) in the 2025 gpt-4.1 runs. Under the gag, messages fall by 99% without any rise in action dependence.]

**Negative result.** An exploratory signal (the share of rounds in which sellers leave their ask unchanged tracked the judge's coordination score, rho=+0.81 in the gpt-4.1 runs) failed a pre-registered replication on 25 held-out cross-model runs (rho=+0.16, p=0.22): Claude sellers hold low prices just as stickily.

## LLM Usage Statement
Claude (Anthropic) assisted throughout: it wrote and tested the analysis and run tooling, ran the experiments under a pre-registered protocol, performed the statistical analysis, verified every citation against its primary source, and drafted this report. The author defined the goals, approved each design decision and budget, and reviewed and edited the text. All numbers were regenerated from the logged runs, and every claim was checked against the outputs in the accompanying repository.
