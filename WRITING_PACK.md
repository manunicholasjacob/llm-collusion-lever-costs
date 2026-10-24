# Writing pack (generated; all numbers come from the run outputs)
Write in your own words; the template expects the final text to be primarily the team's. No em dashes.
Each section lists what it must contain. [P] = pre-sprint analysis of the authors' public data (label it so).

## Run facts
- Gate and models:
```
FAIL  llama70b     comms -0.006 (n=6) vs nocomms +0.024 (n=6): diff -0.030, 90% CI lower -0.367; failed runs 0/12; cost/run $0.185
FAIL  mini41       comms -0.536 (n=3) vs nocomms -0.480 (n=3): diff -0.056, 90% CI lower -0.172; failed runs 0/6; cost/run $0.479
GATE: no model passed. Per protocol, Phase O runs on 'llama70b' (larger comms-nocomms gap); report the failed positive control prominently.
CHOSEN llama70b
SECOND none
```
- Completed runs per model: {'llama70b': 175}
- Real OpenRouter spend at end: $37.45

## Results for llama70b
### Table 1
Table 1. Mean [95% bootstrap CI] per condition.

| Condition | n | Primary index (rounds 16-30) | Whole-run index | Mean trade price | Allocative eff. | Buyer welfare/round | Judge score (1-4) | Rounds gagged | Channel loss |
|---|---|---|---|---|---|---|---|---|---|
| Comms baseline (llama70b) | 25 | -0.00 [-0.09, 0.08] | 0.12 [0.06, 0.18] | 90.54 [89.79, 91.30] | 0.54 [0.49, 0.58] | 25.27 [22.61, 28.03] | 1.11 [1.05, 1.21] | 0.00 [0.00, 0.00] | 0.00 |
| One no-regret seller (maverick) (llama70b) | 25 | -0.13 [-0.21, -0.06] | -0.03 [-0.09, 0.02] | 89.12 [88.51, 89.78] | 0.59 [0.55, 0.64] | 31.97 [29.14, 34.89] | 1.43 [1.03, 2.08] | 0.00 [0.00, 0.00] | 0.19 |
| Monitor/gag only (llama70b) | 25 | -0.03 [-0.13, 0.06] | 0.11 [0.05, 0.16] | 90.20 [89.50, 90.89] | 0.50 [0.47, 0.54] | 24.96 [22.21, 27.91] | 1.99 [1.81, 2.18] | 0.31 [0.17, 0.46] | 0.31 |
| Ban communication (llama70b) | 25 | 0.03 [-0.03, 0.10] | 0.08 [0.01, 0.14] | 89.91 [89.22, 90.57] | 0.47 [0.43, 0.50] | 23.63 [21.15, 26.15] | 1.12 [1.09, 1.17] | 0.00 [0.00, 0.00] | 1.00 |
| Monitoring notice only (llama70b) | 25 | 0.06 [-0.02, 0.15] | 0.16 [0.11, 0.22] | 90.68 [89.95, 91.51] | 0.43 [0.38, 0.48] | 19.73 [17.27, 22.20] | 1.15 [1.09, 1.23] | 0.00 [0.00, 0.00] | 0.00 |
| Oversight (notice + monitor/gag) (llama70b) | 25 | 0.12 [0.06, 0.17] | 0.20 [0.16, 0.24] | 91.20 [90.73, 91.70] | 0.47 [0.42, 0.52] | 20.51 [18.12, 22.94] | 1.62 [1.42, 1.85] | 0.07 [0.00, 0.16] | 0.07 |
| Oversight, monitor reads 25% (llama70b) | 25 | 0.12 [0.04, 0.20] | 0.22 [0.17, 0.28] | 91.49 [90.79, 92.20] | 0.45 [0.41, 0.50] | 19.29 [16.98, 21.58] | 1.17 [1.07, 1.31] | 0.20 [0.08, 0.33] | 0.21 |

### Pre-registered tests
Pre-registered tests (difference of means [95% bootstrap CI]; one-sided bootstrap p; Holm over the family H1, H2, H2b, H-mav per commit 2040915; H-mav uses the LLM-sellers-only index).

| Test | Claim | Difference | p | Holm p / decision |
|---|---|---|---|---|
| H1 | notice < comms | +0.062 [-0.057, +0.183] | 0.8407 | 1.0000 |
| H2 | monitor < comms | -0.034 [-0.162, +0.091] | 0.3044 | 0.9132 |
| H2b | oversight25 < comms | +0.118 [+0.002, +0.235] | 0.9771 | 1.0000 |
| H-mav | maverick < comms (LLM sellers only) | -0.054 [-0.181, +0.070] | 0.2031 | 0.8124 |
| H3 | cap50 < comms (outside family) | not run | | |
| H4 | boss-nocomms within 0.05 of boss (outside family) | not run | | |

### Robustness (OLS, HC3)
Robustness: pooled OLS of the primary index on condition dummies, n=175 runs.

| Term | Coef | HC3 SE | 95% CI |
|---|---|---|---|
| (intercept) comms (llama70b) | -0.000 | 0.046 | [-0.089, +0.089] |
| maverick (llama70b) | -0.130 | 0.062 | [-0.250, -0.009] |
| monitor (llama70b) | -0.034 | 0.068 | [-0.167, +0.099] |
| nocomms (llama70b) | +0.032 | 0.057 | [-0.080, +0.145] |
| notice (llama70b) | +0.062 | 0.064 | [-0.063, +0.187] |
| oversight (llama70b) | +0.116 | 0.055 | [+0.009, +0.223] |
| oversight25 (llama70b) | +0.118 | 0.062 | [-0.004, +0.239] |

### Detector (whole runs)
```
runs: 175  (AUC groups: plain comms 75; plain no-comms 25)
AUC te_z comms vs no-comms: 0.460  (Mann-Whitney p=0.5505)
Spearman te_z vs LLM-judge score: rho=+0.129 p=0.2323 (n=87)
Spearman ni_max vs LLM-judge score: rho=+0.060 p=0.5828 (n=87)
Spearman te_z vs primary collusion index: rho=+0.130 p=0.0867
runs with te_p<0.05: 4/175; runs with >=1 Bonjour flag: 126/175
```
### Channel movement A6 (hours 8-30)
```
window: rounds 8-30
runs: 175  (AUC groups: plain comms 75; plain no-comms 25)
AUC te_z comms vs no-comms: 0.563  (Mann-Whitney p=0.3517)
Spearman te_z vs LLM-judge score: rho=-0.018 p=0.8650 (n=87)
Spearman ni_max vs LLM-judge score: rho=-0.131 p=0.2275 (n=87)
Spearman te_z vs primary collusion index: rho=+0.158 p=0.0373
runs with te_p<0.05: 2/175; runs with >=1 Bonjour flag: 128/175
comms      n=75  median te_z=-1.45  median message chars=13,312
oversight  n=75  median te_z=-2.02  median message chars=13,446
nocomms    n=25  median te_z=-1.90  median message chars=0
oversight te_z > comms: p=0.9567 (Holm 1.0000); > no-comms: p=0.6369 (Holm 1.0000)
A6 verdict: no evidence of channel movement under the pre-registered rule
```
### F1 monitor firing (pre-registered secondary; all false positives if the positive control failed)
F1: monitor firing per arm. For llama70b the positive control failed (no collusion), so every firing is a false positive.

| Model | Arm | n | Runs where monitor fired | Median first-fire hour | Rounds gagged (mean) | Channel retained vs comms |
|---|---|---|---|---|---|---|
| gpt-4.1 (2025) | oversight | 10 | 10/10 (100%) | 4 | 85% | 10% |
| gpt-4.1 (2025) | boss + oversight | 10 | 10/10 (100%) | 3 | 90% | 6% |
| llama70b | oversight | 25 | 5/25 (20%) | 25 | 7% | 93% |
| llama70b | monitor only | 25 | 12/25 (48%) | 7 | 31% | 69% |
| llama70b | oversight, 25% sampling | 25 | 7/25 (28%) | 8 | 20% | 79% |

### X1 costs of levers (EXPLORATORY; label it so in the report)
X1 (EXPLORATORY): lever minus comms baseline, llama70b markets (no collusion present). Difference [95% bootstrap CI], two-sided p; Holm over the 4 monitoring arms (notice, monitor, oversight, oversight25) per outcome. n per arm: {'comms': 25, 'nocomms': 25, 'notice': 25, 'monitor': 25, 'oversight': 25, 'oversight25': 25, 'maverick': 25}


**Primary index (hours 16-30)** (comms mean -0.000)

| Lever | Difference | 95% CI | p (two-sided) | Holm (monitoring arms) |
|---|---|---|---|---|
| nocomms | +0.032 | [-0.076, +0.141] | 0.5444 | n/a |
| notice | +0.062 | [-0.057, +0.181] | 0.3024 | 0.6048 |
| monitor | -0.034 | [-0.160, +0.091] | 0.6236 | 0.6236 |
| oversight | +0.116 | [+0.014, +0.218] | 0.0258 | 0.1032 |
| oversight25 | +0.118 | [+0.003, +0.236] | 0.0456 | 0.1368 |
| maverick | -0.130 | [-0.245, -0.014] | 0.0232 | n/a |

**Mean trade price ($)** (comms mean 90.537)

| Lever | Difference | 95% CI | p (two-sided) | Holm (monitoring arms) |
|---|---|---|---|---|
| nocomms | -0.625 | [-1.664, +0.382] | 0.2200 | n/a |
| notice | +0.142 | [-0.931, +1.222] | 0.8052 | 1.0000 |
| monitor | -0.335 | [-1.350, +0.688] | 0.5130 | 1.0000 |
| oversight | +0.667 | [-0.222, +1.562] | 0.1416 | 0.4248 |
| oversight25 | +0.949 | [-0.104, +2.004] | 0.0820 | 0.3280 |
| maverick | -1.414 | [-2.386, -0.416] | 0.0064 | n/a |

**Trades per run** (comms mean 80.760)

| Lever | Difference | 95% CI | p (two-sided) | Holm (monitoring arms) |
|---|---|---|---|---|
| nocomms | -10.640 | [-19.120, -2.120] | 0.0156 | n/a |
| notice | -16.240 | [-25.881, -6.560] | 0.0008 | 0.0032 |
| monitor | -5.320 | [-13.680, +3.001] | 0.2172 | 0.2172 |
| oversight | -10.080 | [-20.801, +0.480] | 0.0608 | 0.1216 |
| oversight25 | -12.760 | [-22.040, -3.000] | 0.0076 | 0.0228 |
| maverick | +8.000 | [-1.560, +17.521] | 0.0992 | n/a |

**Allocative efficiency** (comms mean 0.538)

| Lever | Difference | 95% CI | p (two-sided) | Holm (monitoring arms) |
|---|---|---|---|---|
| nocomms | -0.071 | [-0.129, -0.013] | 0.0170 | n/a |
| notice | -0.108 | [-0.174, -0.044] | 0.0008 | 0.0032 |
| monitor | -0.035 | [-0.092, +0.021] | 0.2070 | 0.2070 |
| oversight | -0.067 | [-0.137, +0.001] | 0.0542 | 0.1084 |
| oversight25 | -0.085 | [-0.147, -0.020] | 0.0100 | 0.0300 |
| maverick | +0.053 | [-0.011, +0.117] | 0.1010 | n/a |

**Buyer welfare per round** (comms mean 25.274)

| Lever | Difference | 95% CI | p (two-sided) | Holm (monitoring arms) |
|---|---|---|---|---|
| nocomms | -1.646 | [-5.342, +1.994] | 0.3820 | n/a |
| notice | -5.542 | [-9.316, -1.859] | 0.0014 | 0.0042 |
| monitor | -0.314 | [-4.234, +3.684] | 0.8792 | 0.8792 |
| oversight | -4.763 | [-8.414, -1.130] | 0.0110 | 0.0220 |
| oversight25 | -5.982 | [-9.524, -2.368] | 0.0008 | 0.0032 |
| maverick | +6.692 | [+2.748, +10.598] | 0.0018 | n/a |

**Total seller profit ($)** (comms mean 856.995)

| Lever | Difference | 95% CI | p (two-sided) | Holm (monitoring arms) |
|---|---|---|---|---|
| nocomms | -163.427 | [-295.017, -36.960] | 0.0096 | n/a |
| notice | -158.554 | [-308.949, -11.923] | 0.0316 | 0.1264 |
| monitor | -96.978 | [-224.147, +18.238] | 0.1078 | 0.3234 |
| oversight | -58.697 | [-211.469, +84.573] | 0.4438 | 0.5916 |
| oversight25 | -75.748 | [-217.496, +66.573] | 0.2958 | 0.5916 |
| maverick | -40.747 | [-186.793, +104.120] | 0.5870 | n/a |

Figures: `figs/llama70b/fig_costs.png` (lead figure), `figs/llama70b/frontier_primary.png`, `figs/llama70b/strip_primary.png`

## Section-by-section checklist (template order)
1. **Title + abstract (150-250 words, write last):** problem, approach (measured cost, oversight split, maverick), the headline numbers from the tests table, one-sentence takeaway.
2. **Introduction (~0.5 p):** threat model; why the cheapest effective lever matters; [P] the 20/20 gag finding (`figs/report/fig_gag.png`); 3-4 numbered contributions.
3. **Related work (~0.5 p):** use REPORT_SKELETON.md wording verbatim in substance (verified); exact novelty sentence for net influence; cite Garra 2026, Anto & Vazquez 2026 as closest.
4. **Methods (~1 p):** environment; levers; primary metric and why (second half; LLM-only for maverick); measured costs; pilot gate; n per arm; stats (bootstrap, Holm over H1/H2/H2b/H-mav); disclosure of preexisting code; deviation log.
5. **Results (~1.5 p):** Figure 1 frontier; Table 1; tests table; positive control (comms vs ban) first; price paths [P] (`figs/report/fig_paths.png`); A6 [P + sprint] (`figs/report/fig_channel.png`); detector calibration (Q1.3); the failed stickiness replication.
6. **Discussion + limitations (~0.5 p):** what the levers' costs mean for AI control (auditing budget, usefulness cost); limitations list from REPORT_SKELETON.md.
7. **Required appendix:** Limitations and Dual-Use / Ethical Considerations (text in REPORT_SKELETON.md).
8. **LLM usage statement (required):** Claude helped with engineering, statistics, citation checks; you wrote the prose; all numbers regenerated from logs.
9. **Code and data:** repo link if published; `SPRINT_README.md` marks preexisting vs sprint work.

## Verified facts, references and framing
See `collusion_analysis/REPORT_SKELETON.md` (sprint-day additions and the verified reference list); copy references from there only.
