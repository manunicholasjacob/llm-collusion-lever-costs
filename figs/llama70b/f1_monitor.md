F1: monitor firing per arm. For llama70b the positive control failed (no collusion), so every firing is a false positive.

| Model | Arm | n | Runs where monitor fired | Median first-fire hour | Rounds gagged (mean) | Channel retained vs comms |
|---|---|---|---|---|---|---|
| gpt-4.1 (2025) | oversight | 10 | 10/10 (100%) | 4 | 85% | 10% |
| gpt-4.1 (2025) | boss + oversight | 10 | 10/10 (100%) | 3 | 90% | 6% |
| llama70b | oversight | 25 | 5/25 (20%) | 25 | 7% | 93% |
| llama70b | monitor only | 25 | 12/25 (48%) | 7 | 31% | 69% |
| llama70b | oversight, 25% sampling | 25 | 7/25 (28%) | 8 | 20% | 79% |
