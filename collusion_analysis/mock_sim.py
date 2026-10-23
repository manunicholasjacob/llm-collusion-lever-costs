"""Drop-in for simulation.py that runs with the fake LLM (PRE-SPRINT, built Oct 22).
Rehearse the real runner at $0:  SIM=collusion_analysis/mock_sim.py bash collusion_analysis/run_sprint.sh notice 2 2"""
import glob, os, runpy, sys
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.dirname(__file__))
os.environ["WANDB_MODE"] = "disabled"
import mock_llm

mock_llm.install()
try:
    # install() patched util.misc, so simulation.py's own import picks up the fake client.
    runpy.run_path("src/continuous_double_auction/simulation.py", run_name="__main__")
finally:
    # Mark the run as fake so run_stats.py refuses it unless ALLOW_MOCK=1.
    tag = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else ""
    runs = sorted(glob.glob(os.path.join("results", f"*_{tag}")))
    if runs:
        open(os.path.join(runs[-1], "MOCK"), "w").close()
