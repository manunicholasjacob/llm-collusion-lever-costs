"""Assemble WRITING_PACK.md after run_all.sh: every number, table, figure and verified fact Manu needs,
in the order of the official Apart template, so writing is prose-only. Pulls live outputs; nothing typed in.
Usage: python -X utf8 -I collusion_analysis/writing_pack.py [OUT.md]"""
import glob, os, re, sys

out = sys.argv[1] if len(sys.argv) > 1 else "WRITING_PACK.md"


def read(path, default="(not produced yet)"):
    return open(path, encoding="utf-8").read().strip() if os.path.exists(path) else default


gate = read("results/pilot_gate.txt")
chosen = (re.search(r"^CHOSEN (\S+)", gate, re.M) or [None, None])[1]
second = (re.search(r"^SECOND (\S+)", gate, re.M) or [None, "none"])[1]
usage = re.findall(r"^FINAL_USAGE ([0-9.]+)", read("results/run_all.log", ""), re.M)
runs = {t: len(glob.glob(f"results/*_lo-{t}-*/collusion_metrics.json")) for t in [chosen, second] if t and t != "none"}

sec = []
sec.append("# Writing pack (generated; all numbers come from the run outputs)\n"
           "Write in your own words; the template expects the final text to be primarily the team's. No em dashes.\n"
           "Each section lists what it must contain. [P] = pre-sprint analysis of the authors' public data (label it so).")
sec.append("## Run facts\n"
           f"- Gate and models:\n```\n{gate}\n```\n"
           f"- Completed runs per model: {runs}\n"
           f"- Real OpenRouter spend at end: ${usage[-1] if usage else '?'}")
if chosen:
    for tag in filter(lambda t: t and t != "none", [chosen, second]):
        sec.append(f"## Results for {tag}\n### Table 1\n{read(f'figs/{tag}/table1.md')}\n\n"
                   f"### Pre-registered tests\n{read(f'figs/{tag}/tests.md')}\n\n"
                   f"### Robustness (OLS, HC3)\n{read(f'figs/{tag}/ols_hc3.md')}\n\n"
                   f"### Detector (whole runs)\n```\n{read(f'figs/{tag}/detector_whole/detector_summary.md')}\n```\n"
                   f"### Channel movement A6 (hours 8-30)\n```\n{read(f'figs/{tag}/detector_w8_30/detector_summary.md')}\n```\n"
                   f"Figures: `figs/{tag}/frontier_primary.png`, `figs/{tag}/strip_primary.png`")
sec.append("## Section-by-section checklist (template order)\n"
           "1. **Title + abstract (150-250 words, write last):** problem, approach (measured cost, oversight split, "
           "maverick), the headline numbers from the tests table, one-sentence takeaway.\n"
           "2. **Introduction (~0.5 p):** threat model; why the cheapest effective lever matters; [P] the 20/20 gag "
           "finding (`figs/report/fig_gag.png`); 3-4 numbered contributions.\n"
           "3. **Related work (~0.5 p):** use REPORT_SKELETON.md wording verbatim in substance (verified); exact novelty "
           "sentence for net influence; cite Garra 2026, Anto & Vazquez 2026 as closest.\n"
           "4. **Methods (~1 p):** environment; levers; primary metric and why (second half; LLM-only for maverick); "
           "measured costs; pilot gate; n per arm; stats (bootstrap, Holm over H1/H2/H2b/H-mav); disclosure of "
           "preexisting code; deviation log.\n"
           "5. **Results (~1.5 p):** Figure 1 frontier; Table 1; tests table; positive control (comms vs ban) first; "
           "price paths [P] (`figs/report/fig_paths.png`); A6 [P + sprint] (`figs/report/fig_channel.png`); detector "
           "calibration (Q1.3); the failed stickiness replication.\n"
           "6. **Discussion + limitations (~0.5 p):** what the levers' costs mean for AI control (auditing budget, "
           "usefulness cost); limitations list from REPORT_SKELETON.md.\n"
           "7. **Required appendix:** Limitations and Dual-Use / Ethical Considerations (text in REPORT_SKELETON.md).\n"
           "8. **LLM usage statement (required):** Claude helped with engineering, statistics, citation checks; you "
           "wrote the prose; all numbers regenerated from logs.\n"
           "9. **Code and data:** repo link if published; `SPRINT_README.md` marks preexisting vs sprint work.")
sec.append("## Verified facts, references and framing\nSee `collusion_analysis/REPORT_SKELETON.md` (sprint-day additions "
           "and the verified reference list); copy references from there only.")
open(out, "w", encoding="utf-8").write("\n\n".join(sec) + "\n")
print("wrote", out)
