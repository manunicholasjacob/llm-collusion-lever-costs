# Follow-up study: what anti-collusion levers buy, and what they cost, in markets that collude

Status: DRAFT design, not yet pre-registered. Written 24 Oct 2026 after the sprint submission. Nothing here
has been run except the screens logged in `collusion_analysis/SPRINT_PROTOCOL.md` (P2, S1).

## Why a follow-up

The sprint study measured lever costs in markets that do not collude (Llama-3.3-70B and GPT-4.1-mini sellers
never priced above the competitive level, so the positive control failed). A reviewer's first question will be
what the same levers buy where collusion exists. Without that, "levers are not free" has a cost side and no
benefit side. The follow-up supplies the benefit side in the same harness, so cost and benefit can be put on
one axis.

## Two ways to get a colluding market

1. **Instructed collusion (ground truth).** A hidden instruction tells some sellers to coordinate on high prices
   and avoid detection. Honest runs get no instruction. Because we know which runs collude, every monitor firing
   becomes a true or a false positive, and every lever has both a measurable benefit (collusion removed in
   instructed runs) and a measurable cost (harm in honest runs). This is the core design.
2. **Natural collusion.** A model that colludes unprompted (screen S1 nominates candidates among cheap model
   families; gpt-4.1 colluded weakly in the authors' 2025 runs). A smaller natural-collusion arm checks that
   lever effects measured under instruction carry over to unprompted collusion, the obvious external-validity
   objection to design 1.

## Arms (each one change versus communication on)

Market type {honest, instructed} x lever {none, ban communication, notice only, monitor only, full oversight,
oversight with 25% monitoring budget, one no-regret seller}, plus two monitor-calibration arms that only make
sense with ground truth: monitor threshold 3 instead of 4, and monitor budget 50%.

## Pre-registered hypotheses (draft)

- **H1 (replication of the sprint cost result).** In honest markets the monitoring notice lowers buyer welfare.
- **H2 (benefit).** In instructed markets each lever lowers the collusion index relative to no lever.
- **H3 (the trade-off).** Levers differ in collusion removed per unit of honest-market welfare lost; the no-regret
  seller has the best ratio (it raised welfare in honest markets in the sprint and is predicted by Collina et
  al. 2025 to destabilise collusion).
- **H4 (monitor quality).** The monitor's true-positive rate in instructed runs exceeds its false-positive rate
  in honest runs, and both fall with the monitoring budget; report the full ROC over threshold and budget.
- **H5 (transfer).** Lever rankings under instruction match rankings under natural collusion (sign agreement).

## Primary outputs

- A cost-benefit frontier: collusion removed (instructed) against welfare lost (honest), one point per lever.
- Monitor ROC across thresholds and budgets, with the operating point the harness default actually sits at.
- The sprint's exploratory findings retested as confirmatory where they recur (H1).

## Sample size and budget (per run: about $0.19 with Llama-3.3-70B; cheap screen models similar; gpt-4.1 about $2.60)

| Package | Runs | Approximate cost |
|---|---|---|
| Pilot: instruction strength and positive control (honest vs instructed, no lever), n=10 each | 20 | about $4 |
| Core: 2 market types x 7 levers, n=25 | 350 | about $65 |
| Monitor calibration: threshold 3 and budget 50%, both market types, n=25 | 100 | about $19 |
| Natural-collusion arm on the S1 candidate (or gpt-4.1 fallback): 4 key levers, n=20 | 80 | about $15 (cheap model) or about $210 (gpt-4.1) |
| Confirmatory replication of the headline results, n=25 x 3 | 75 | about $14 |
| **Total** | **625** | **about $120 with a cheap colluder; about $315 if gpt-4.1 is needed** |

## Process (same standard as the sprint)

Pre-register in the protocol before every phase; anchor entries to git commits and system-clock times;
positive-control gate before the main study; Holm within each confirmatory family; exploratory results labelled
and retested on fresh runs; `verify_claims.py`-style checker for every number in the paper; public data and DOI.

## Separation from the Swarm Alignment Hackathon (6 to 8 Nov 2026)

Apart judges only the weekend's work and screens for prior work. The hackathon project must not be this study.
Keep the hackathon on a different question (see `SWARM_PREP.md`), and if any follow-up runs happen before 6 Nov,
list them as prior work in the hackathon report.

## Authorship

Same as the sprint: Manu writes the paper text from fact lists; Claude runs, analyses and checks; the LLM
statement says so.
