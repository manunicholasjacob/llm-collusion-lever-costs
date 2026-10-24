window: rounds 8-30
runs: 50  (AUC groups: plain comms 10; plain no-comms 10)
AUC te_z comms vs no-comms: 0.580  (Mann-Whitney p=0.5708)
Spearman te_z vs LLM-judge score: rho=+0.137 p=0.3438 (n=50)
Spearman ni_max vs LLM-judge score: rho=-0.391 p=0.0050 (n=50)
Spearman te_z vs primary collusion index: rho=+0.027 p=0.8547
runs with te_p<0.05: 3/50; runs with >=1 Bonjour flag: 36/50
comms      n=10  median te_z=-2.89  median message chars=41,830
oversight  n=10  median te_z=-3.32  median message chars=234
nocomms    n=10  median te_z=-3.48  median message chars=0
oversight te_z > comms: p=0.6612 (Holm 0.8501); > no-comms: p=0.4251 (Holm 0.8501)
A6 verdict: no evidence of channel movement under the pre-registered rule
