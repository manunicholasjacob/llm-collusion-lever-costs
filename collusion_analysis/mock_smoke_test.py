"""
Zero-cost smoke test of the harness flags (PRE-SPRINT, built Oct 22).
Replaces every LLM client with a scripted fake, runs each sprint condition for
a few rounds, and checks that each lever does what it claims:
  notice-only  -> notice text in seller prompts, no Overseer.md
  monitor-only -> Overseer.md written, gag text appears, no notice text
  full         -> both
  msgcap 50    -> no delivered seller message longer than 50 chars
  seller temp  -> sellers and buyers get different temperatures
Usage (from the harness root): WANDB_MODE=disabled python -X utf8 collusion_analysis/mock_smoke_test.py
"""
import glob, json, os, random, shutil, sys
sys.path.insert(0, os.getcwd())
os.environ["WANDB_MODE"] = "disabled"

from src.continuous_double_auction import simulation
from src.continuous_double_auction.evaluation import evaluate
from src.continuous_double_auction.cda_types import ExperimentParams
from src.resources.model_wrappers import ModelWrapper

TEMPS = []


class FakeClient(ModelWrapper):
    def __init__(self, model, temperature, **kw):
        super().__init__(model, temperature=temperature)
        self.model = model
        TEMPS.append((model, temperature))

    def batch_generate(self, batch):
        return [self.generate(m) for m in batch]

    def generate(self, messages):
        p = messages[-1]["content"]
        if "expert overseer" in p:
            return json.dumps({"evidence": [], "coordination": "yes", "coordination_score": 4, "type": "overt"})
        return json.dumps({
            "reflection": "r", "plan_for_this_hour": "p",
            "ask": round(random.uniform(88, 99), 2), "bid": round(random.uniform(82, 95), 2),
            "new_memory": "m", "plan_for_message": "pm",
            "message_to_sellers": "Let us all hold our asks at 98 for the rest of the session and never undercut. " * 3,
            "scratch_pad_update": "s", "coordination_score": 2, "coordination": "no", "type": None,
        })


def fake_get_client(model, temperature, **kw):
    return FakeClient(model, temperature, **kw)


simulation.get_client = fake_get_client
evaluate.get_client = fake_get_client

BASE = dict(seller_valuations=[80.0] * 3, buyer_valuations=[100.0] * 2,
            seller_models=["gpt-4.1"] * 3, buyer_models=["gpt-4.1"] * 2, rounds=4)
CASES = {
    "notice": dict(seller_comms_enabled=True, oversight_notice=True),
    "monitor": dict(seller_comms_enabled=True, oversight_monitor=True),
    "full": dict(seller_comms_enabled=True, oversight_enabled=True),
    "msgcap": dict(seller_comms_enabled=True, max_message_length=50),
    "selltemp": dict(seller_comms_enabled=True, seller_temperature=1.2),
    "boss-nocomms": dict(boss_pressure=True),
}
NOTICE = "new oversight system to monitor seller communications"
GAG = "all sellers are gagged"


def latest_dir(tag):
    return sorted(glob.glob(os.path.join("results", f"*_mock-{tag}")))[-1]


def check(tag, d):
    seller_txt = "".join(open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(d, "Seller *.md")))
    has_over = os.path.exists(os.path.join(d, "Overseer.md"))
    meta = json.load(open(os.path.join(d, "experiment_metadata.json"), encoding="utf-8"))["auction_config"]
    rounds = open(os.path.join(d, "auction_results.md"), encoding="utf-8").read()
    msgs = [m for blk in rounds.split("seller_messages")[1:] for m in blk.split('"')[3:4]]
    checks = {
        "notice": (NOTICE in seller_txt) == bool(meta["oversight_notice"]),
        "monitor": has_over == bool(meta["oversight_monitor"]),
        "gag": (GAG in seller_txt) == bool(meta["oversight_monitor"]),
    }
    if tag == "msgcap":
        cfg_rounds = [json.loads(b.split("````")[0]) for b in rounds.split("````json")[1:]]
        longest = max((len(m) for r in cfg_rounds for m in r["seller_messages"].values()), default=0)
        checks["cap<=50"] = longest <= 50
    return checks, meta


ok = True
for tag, extra in CASES.items():
    TEMPS.clear()
    simulation.run_simulation(ExperimentParams(**BASE, **extra, tag=f"mock-{tag}"))
    d = latest_dir(tag)
    checks, meta = check(tag, d)
    if tag == "selltemp":
        temps = {t for m, t in TEMPS if m == "gpt-4.1"}
        checks["seller!=buyer temp"] = temps == {0.7, 1.2}
    good = all(checks.values())
    ok &= good
    print(f"{'PASS' if good else 'FAIL'} {tag:<13} notice={meta['oversight_notice']} monitor={meta['oversight_monitor']} {checks}")

# Mock runs stay in results/*_mock-* (log handles are open until exit on Windows); delete them afterwards.
print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
