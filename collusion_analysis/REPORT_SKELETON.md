# Report plan (follows the official Apart template; Manu writes the prose)
The template recommends 4 pages excluding references and appendix (8 is the cap): about 1 page for
Introduction and Related Work, 2.5 for Methods and Results, 0.5 for Discussion. It says the final
version should be "primarily written by your team" and requires an LLM Usage Statement. So this
file gives the verified facts, numbers and citations for each section, and Manu writes the text.
Numbers marked [S] come from sprint runs and are filled in after Stage 2. Numbers marked [P] come
from pre-sprint analysis of the authors' public data and must be labelled that way in the report.
House rule: no em dashes anywhere in the report.

**Working title** (choose after results; do not pre-commit to a claim):
- if H1 holds: "Deterrence Without Enforcement: Measured Costs Reorder Anti-Collusion Levers for LLM Market Agents"
- if H1 fails: "Oversight Is a Delayed Ban: Measured Costs of Anti-Collusion Levers for LLM Market Agents"

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
7. Keppo, J., Li, Y., Tsoukalas, G., Yuan, N. (2026). On the Fragility of AI Agent Collusion. arXiv:2603.20281. https://arxiv.org/abs/2603.20281
8. Motwani, S. R., et al. (2024). Secret Collusion among AI Agents: Multi-Agent Deception via Steganography. NeurIPS 2024. arXiv:2402.07510. https://arxiv.org/abs/2402.07510
9. Nakamura, M., Kumar, A., Das, S., Abdelnabi, S., Mahmud, S., Fioretto, F., Zilberstein, S., Bagdasarian, E. (2026). Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems. arXiv:2602.15198. https://arxiv.org/abs/2602.15198
10. Riedl, C. (2026). Emergent Coordination in Multi-Agent Language Models. ICLR 2026. arXiv:2510.05174. https://arxiv.org/abs/2510.05174
11. Tailor, O. (2025). Audit the Whisper: Detecting Steganographic Collusion in Multi-Agent LLMs. arXiv:2510.04303. https://arxiv.org/abs/2510.04303
12. Xu, X., Wu, C., Lu, J., Tan, K., Tao, S., Hong, H. (2026). Collusion with Competitive Marginals: Price-Level Audits Are Blind by Construction. arXiv:2607.26385. https://arxiv.org/abs/2607.26385
(If transfer entropy is cited: Schreiber, T. (2000). Measuring Information Transfer. Phys. Rev. Lett. 85, 461. Verify the DOI before use.)
