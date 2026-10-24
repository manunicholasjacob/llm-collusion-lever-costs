# Anti-Collusion Levers Are Not Free: Measuring What Monitoring Costs LLM Markets

**Manu Nicholas Jacob**, Independent Researcher. With Apart Research.

Track 1 (Markets and Collusion: Q1.5, Q1.3, Q1.4) and Track 3 (Q3.4).

## Abstract

The question behind this study is straightforward: which intervention can reduce collusion between LLM pricing agents at the lowest cost to the market? Previous work has mainly compared interventions by how much collusion they prevent, without measuring what those interventions cost when there is no collusion to prevent. We use the continuous double auction from Agrawal et al. (2025) to investigate this trade-off. First, we audited the authors' public runs and found that the LLM monitor triggered in 20 of 20 oversight runs, within seven rounds, restricting sellers to five-character messages for 77 to 97% of each run. In practice, this makes oversight behave more like a delayed communication ban than light-touch monitoring. We then compared seven interventions in a pre-registered study with 25 runs each, using Llama-3.3-70B sellers. Neither Llama-3.3-70B nor GPT-4.1-mini sellers colluded when communication was allowed, meaning there was no collusion for the interventions to reduce. Instead, we measured their costs in a non-colluding market. The monitor punished innocent markets in up to 48% of runs, the monitoring notice reduced buyer welfare by 22%, and banning communication cost 13% of trades. In contrast, adding one no-regret competitor increased buyer welfare by 26%. A further 75 pre-registered runs confirmed both welfare effects, although the notice's effect on trade volume did not replicate. These findings show why the costs of false positives must be measured alongside the benefits of anti-collusion interventions.

## 1. Introduction

LLM pricing agents can sustain supracompetitive prices, both with and without direct communication (Fish et al., 2024; Agrawal et al., 2025). This creates a practical problem for platforms and regulators: how should they intervene? They could ban communication, introduce an automated monitor, warn agents that they are being monitored, or change the market by introducing a different type of competitor. In practice, the preferred option will depend not only on whether it reduces collusion, but also on what it costs.

Existing studies have compared interventions based on their ability to reduce collusion (Agrawal et al., 2025; Bracale Syrnikov et al., 2026; Garra, 2026; Anto and Vazquez, 2026). However, an important question remains unanswered: what happens when an intervention is applied to a market that is not colluding in the first place? A monitor can flag legitimate behaviour, a warning can change how agents make decisions, and a communication ban can prevent sellers from coordinating on prices that allow trades to happen. These costs matter just as much when evaluating whether an intervention is worthwhile.

This problem also connects to AI control, where monitoring systems are evaluated in terms of false positives, auditing budgets, and the usefulness they sacrifice to maintain oversight (Greenblatt et al., 2024; Bhatt et al., 2025). Anti-collusion interventions should be evaluated using the same principle.

This study makes four contributions:
1. We audit the reference oversight mechanism and find that it triggered in 20/20 public runs, removing about 90% of seller message text. This makes it closer to a delayed communication ban than ordinary monitoring.
2. We conduct a pre-registered comparison of seven interventions (n=25 each), separating a monitoring warning from enforcement, varying the monitoring budget, and testing a no-regret competitor.
3. We measure the costs of these interventions in non-colluding markets and find that warnings can harm buyers and monitors misfire on innocent markets, while a no-regret competitor improves buyer welfare. Both welfare effects hold in fresh, pre-registered runs.
4. We evaluate information-theoretic detection and LLM-based coordination judging, finding important limitations in what each measure captures.

## 2. Related Work

**LLM collusion.** Research has shown that LLM pricing agents can produce supracompetitive prices even without direct communication, with small changes to prompts sometimes producing substantial behavioural differences (Fish et al., 2024). In continuous double auctions, seller communication can increase collusion, while oversight and urgency can change agent behaviour (Agrawal et al., 2025). However, the oversight mechanism in that work combines a warning with an LLM monitor that restricts messages. Other work finds that agent heterogeneity can weaken collusion (Keppo et al., 2026), while reinforcement-learning pricing agents can collude without communication (Calvano et al., 2020). More recent studies examine governance mechanisms, prompt-based warnings, and different forms of oversight, with results varying across interventions and models (Bracale Syrnikov et al., 2026; Garra, 2026; Anto and Vazquez, 2026). Collina et al. (2025) also show theoretically how a single participant using a no-regret strategy can destabilise algorithmic collusion.

**Interventions.** Existing work explores interventions ranging from governance structures to changes in agent behaviour. A warning that a monitor is present can reduce coordinated sabotage in non-market settings (Radev et al., 2026). However, these results do not establish what such interventions cost when applied to a market that is already behaving competitively.

**Monitoring and detection.** AI-control research highlights the importance of monitoring budgets, false-positive rates, and the usefulness sacrificed to maintain oversight (Greenblatt et al., 2024; Bhatt et al., 2025). For collusion detection, Bonjour et al. (2022) propose pairwise net influence for small multi-agent games. LLM-specific approaches have since explored cross-run mutual information (Tailor, 2025) and partial information decomposition (Riedl, 2026). Nakamura et al. (2026) further examine cases where agents agree to collude in text but do not follow through in their actions. Despite this progress, existing work has not measured the costs of anti-collusion interventions or separated the effect of a warning from that of the monitor enforcing it.

## 3. Methods

**Environment.** We use the Agrawal et al. (2025) continuous double auction unchanged in its market logic: 5 sellers (cost $80), 5 buyers (value $100), 30 hourly rounds, initial asks near $97.5. Sellers may send each other messages each round. In the oversight condition an LLM monitor scores seller messages from 1 to 4 and, after the first 4, limits all sellers to five-character messages for the rest of the run.

**Models.** Trading agents are Llama-3.3-70B-Instruct (via OpenRouter) in the new runs; the monitor and the judge are GPT-4.1-mini in every arm, so the measuring instruments are constant. The 2025 audit uses the authors' public gpt-4.1 runs (10 per condition). All agents use the harness's prompt templates unchanged (the notice arm shows the template's own oversight warning) at temperature 0.7. The harness sets no random seed, so every run is an independent sample, and we report run-to-run variation through bootstrap intervals.

**Levers (one change each, versus communication on).** Ban communication; monitoring notice only (the warning text, no monitor); monitor only (monitor and gag, no warning); full oversight (both); oversight with a monitor that reads a random 25% of messages; and one no-regret seller (Hedge over asks $80.5 to $100 with full-information counterfactual payoffs) replacing one LLM seller.

**Outcomes and costs.** The primary collusion index is the mean seller ask over hours 16 to 30, scaled so the competitive price ($90) is 0 and the joint-profit price ($100) is 1 (for the no-regret lever, LLM sellers only). Costs: messages delivered (channel loss), monitor firing, completed trades, allocative efficiency, buyer welfare and seller profit.

**Design and statistics.** A pilot (6 plus 6 runs of Llama-3.3-70B, 3 plus 3 of GPT-4.1-mini) applied a pre-registered positive-control gate before the main study (25 runs per lever). Hypothesis tests use one-sided bootstrap differences (10,000 resamples) with Holm correction; exploratory comparisons use two-sided bootstrap intervals and are labelled as such. The exploratory effects of the notice and the no-regret seller were then tested in a confirmatory replication, pre-registered before any of its 75 fresh runs (25 each of communication, notice and no-regret seller), with Holm correction over its three tests. Every design decision, deviation and runtime fix is timestamped in a protocol committed to git before the analysis it governs. With the 2025 gpt-4.1 spread (SD 0.42), the original 10 runs per arm could detect only effects of 0.42 to 0.49 index units at 80% power (one-sided), larger than the communication ban's own effect (0.28); 25 runs per arm detects 0.26 to 0.30.

## 4. Results

**4.1 The reference oversight is a delayed ban (pre-sprint analysis of public data).** In the authors' runs the monitor fired in 10/10 oversight runs and 10/10 runs combining oversight with profit pressure, first at hours 1 to 7, gagging sellers for 77 to 97% of the run; only 10% of message characters were delivered relative to the communication baseline (Figure 1). Priced at this measured cost, oversight is 0.82 to 1.26 times as cost-effective as a ban depending on the metric, with overlapping confidence intervals, rather than the "nearly free" lever an assumed cost suggests.

[Figure 1: figs/report/fig_gag.png. Caption: Left, the hour at which the monitor first fired and the gagged span, for all 20 gpt-4.1 oversight runs. Right, seller message characters delivered per hour, communication baseline versus oversight (mean of 10 runs).]

**4.2 The positive control failed.** With communication, Llama-3.3-70B sellers did not price above the no-communication arm (index -0.006 versus +0.024, n=6 each), and GPT-4.1-mini sellers priced below the competitive level in both arms (-0.54 versus -0.48, n=3 each). In the main study the Llama communication baseline sits at the competitive price (index -0.00, 95% CI [-0.09, 0.08]). Following the pre-registered rule, the main study ran on Llama-3.3-70B. In the pre-registered tests (H1 notice, H2 monitor, H2b 25% monitor, H-mav competitor) no lever reduced collusion (all Holm p > 0.8): there was no collusion to reduce.

**4.3 The monitor punishes innocent markets.** Because no Llama market colluded, every monitor firing is a false positive. The monitor alone fired in 12 of 25 runs and gagged 31% of rounds; with the warning in place it fired in 5 of 25 (7% of rounds), and reading 25% of messages it fired in 7 of 25 (20% of rounds) (Figure 2, right).

**4.4 What levers cost a market that is not colluding (exploratory).** Compared with the communication baseline (81 trades per run, buyer welfare 25.3 per round):

| Lever | Trades per run | Buyer welfare per round | Seller profit |
|---|---|---|---|
| Monitoring notice only | -16.2 [-25.9, -6.6], Holm p=0.003 | -5.5 [-9.3, -1.9], Holm p=0.004 | -$159 [-309, -12] |
| Monitor only | -5.3 [-13.7, +3.0] | -0.3 [-4.2, +3.7] | -$97 [-224, +18] |
| Full oversight | -10.1 [-20.8, +0.5] | -4.8 [-8.4, -1.1], Holm p=0.022 | -$59 [-211, +85] |
| Ban communication | -10.6 [-19.1, -2.1] | -1.6 [-5.3, +2.0] | -$163 [-295, -37] |
| One no-regret seller | +8.0 [-1.6, +17.5] | +6.7 [+2.7, +10.6] | -$41 [-187, +104] |

The results suggest that the warning itself causes most of the harm, rather than the monitor. Markets exposed to the notice experienced lower buyer welfare, and the notice alone also reduced the number of trades. By contrast, the monitor without the warning had no detectable effect. Warned sellers changed how they communicated, with 28% of their messages mentioning monitoring or regulation, compared with 3% without the notice, and they maintained slightly higher asks. Banning communication also came at a cost: sellers appeared to use messages to converge on prices that allowed trades to happen. Of the interventions tested, only the no-regret competitor helped buyers, lowering the mean trade price by $1.41. Although the notice's effect on trade volume was also supported by a rank test (median 60 versus 82 trades, Mann-Whitney p=0.005), this result did not hold in the replication.

[Figure 2: figs/llama70b/fig_costs.png. Caption: Differences from the communication baseline in trades per run and buyer welfare per round, with 95% bootstrap intervals (Llama-3.3-70B sellers, 25 runs per lever), and the share of runs in which the monitor fired, all false positives because no market colluded.]

**4.5 Confirmatory replication.** We pre-registered three tests of the exploratory results and ran them on 75 fresh runs:

| Pre-registered test (fresh runs, n=25 per arm) | Difference [95% CI] | Holm p | Result |
|---|---|---|---|
| Notice lowers trades per run | +0.96 [-8.56, +10.28] | 0.59 | Not confirmed |
| Notice lowers buyer welfare per round | -3.73 [-7.43, -0.19] | 0.040 | Confirmed |
| No-regret seller raises buyer welfare per round | +10.00 [+5.73, +14.26] | <0.001 | Confirmed |

The replication supports the main welfare findings, even though the precise way the warning affected the market changed between samples. Buyer welfare under the notice remained similar across the two samples, at 19.7 and 19.1, while the no-regret competitor produced welfare of 32.0 and 32.8. The communication baseline differed between samples (25.3 and 22.8), suggesting that the original trade-volume reduction was partly influenced by an unusually busy baseline. In the replication, the warning hurt buyers through higher prices rather than fewer trades, with mean trade prices of $91.88 versus $90.49. Warned sellers again discussed monitoring and regulation more often (17% versus 8% of messages). Taken together, the findings suggest that warnings can reduce buyer welfare even when their specific effects vary, while a single no-regret competitor consistently improves buyer outcomes.

**4.6 Evidence standards.** (i) Detection (Q1.3, Q1.4): on the gpt-4.1 runs, Bonjour et al.'s net influence at its published threshold flags 70% of no-communication runs; calibrated at the 90th percentile of no-communication runs, net influence and a transfer-entropy statistic each detect 4 of 10 communication runs at a 10% false-positive rate. (ii) Judges (Q2.3): within communication runs, the LLM judge's coordination score rose while prices fell in 10 of 10 runs (mean within-run rho -0.52, sign test p=0.002); on round-to-round changes the correlation vanishes (rho -0.04). The judge measures talk, not market outcomes. (iii) Channel movement (Q3.4): under the gag, gpt-4.1 messages fell by 99.4% but price-path dependence did not rise, so we find no evidence that coordination moved into prices.

## 5. Discussion and Limitations

The main takeaway is that an intervention cannot be judged by how well it works against collusion alone. Its costs depend on the market it is applied to. In the gpt-4.1 data, where sellers colluded weakly, oversight effectively acted as a communication ban and increased buyer welfare (27.2 versus 19.8 per round). In the Llama markets, where sellers did not collude, the warning attached to oversight reduced buyer welfare by 16 to 22%, and the monitor triggered falsely in up to half of runs. The same intervention can therefore help in one setting and cause harm in another.

For platforms and regulators, this means that measuring false-positive costs should be part of evaluating any anti-collusion intervention. A monitor that fires easily and imposes a permanent penalty can spend much of its usefulness budget restricting legitimate behaviour. Even the warning that announces monitoring can change seller behaviour and harm buyers even when no monitor is present. Among the options tested here, a no-regret competitor appears more attractive than additional enforcement: it requires neither communication restrictions nor monitoring and improves buyer outcomes. The goal should not be to abandon oversight, but to measure its costs and calibrate it to the behaviour it is intended to prevent.

### Limitations
- One market environment with homogeneous costs and values; one main model family for the new runs; the failed positive control means we could not test lever benefits on the same model.
- Collusion in this harness is model-specific: gpt-4.1 shows weak communication-driven collusion, Llama-3.3-70B and GPT-4.1-mini do not.
- The cost results in Section 4.4 were found after inspecting the data. Of the three we then tested on fresh pre-registered runs, the two welfare effects replicated and the trade-volume effect did not, and the route by which the warning hurts buyers (fewer trades in one sample, higher prices in the other) is not stable.
- The monitor's threshold and permanent gag are the harness defaults; other thresholds would change false-positive rates.
- Buyer welfare and trades are in-market costs; costs outside the market (for example, lost legitimate coordination) are not measured.
- Thirty rounds limit the power of information-theoretic detectors.

### Future Work

Future work should test these interventions in a model that colludes reliably, allowing their benefits and costs to be measured in the same setting. Other priorities include calibrating monitor thresholds and budgets, comparing credible and non-credible warnings, and testing mixed-model markets with multiple no-regret competitors.

## 6. Conclusion

Anti-collusion interventions in LLM markets should be evaluated by their costs as well as their effectiveness. In the reference environment, oversight behaved like a delayed communication ban. In markets that did not collude, monitors produced false positives, warnings reduced buyer welfare, and communication bans cost liquidity. A single no-regret competitor improved buyer welfare, and both welfare effects held in a pre-registered replication. Measuring these false-positive costs should be a standard part of evaluating interventions against AI collusion.

## Code and Data
- Code and data: https://github.com/manunicholasjacob/llm-collusion-lever-costs, archived at https://doi.org/10.5281/zenodo.23622463. It holds the analysis code, our harness changes as a patch against the original repository, all 268 sprint runs (market logs and monitor scores; per-agent transcripts on request), the timestamped protocol, and a script that recomputes this report's numbers from the runs.
- Original runs and harness: Agrawal et al.'s public repository (https://github.com/andyjliu/llm-agent-collusion), which is not redistributed.
- Pre-sprint work (disclosed): analysis tooling and harness flags were built on 22 October 2026, before the sprint; all new runs and analyses were done during the sprint. The repository's DISCLOSURE.md separates the two, and every step is timestamped in the protocol file.

## Author Contributions

M.N.J. selected the study and sprint questions, made the go/no-go and budget decisions at each stage, wrote the abstract, introduction, related work, results interpretation paragraphs, discussion, and conclusion, and reviewed the full manuscript. Claude wrote the analysis and experiment code, ran the experiments, conducted the statistical analysis, and drafted the Methods, Results, and appendices.

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

Claude (Anthropic) was used to write and test the analysis and experiment tooling, run experiments under the pre-registered protocol, conduct statistical analyses, check citations against their sources, and draft the Methods, Results, and appendices. M.N.J. wrote the abstract, introduction, related work, results interpretation paragraphs, discussion, and conclusion. All numerical results were regenerated from the logged runs and checked by script against the outputs in the public repository.
