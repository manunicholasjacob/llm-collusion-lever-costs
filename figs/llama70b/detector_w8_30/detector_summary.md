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
