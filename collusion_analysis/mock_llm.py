"""Scripted fake LLM for $0 tests and rehearsals (PRE-SPRINT, built Oct 22).
install() swaps every client the harness builds for FakeClient. Asks drift with a little
noise so trades and the analysis code see realistic shapes; the numbers mean nothing."""
import json, random
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
            "scratch_pad_update": "s", "coordination_score": random.randint(1, 4), "coordination": "no", "type": None,
        })


def fake_get_client(model, temperature, **kw):
    return FakeClient(model, temperature, **kw)


def install():
    # Patch the defining module too, so a later `from ...misc import get_client` (e.g. simulation.py
    # re-executed by runpy) also gets the fake.
    from src.continuous_double_auction.util import misc
    misc.get_client = fake_get_client
    from src.continuous_double_auction import simulation
    from src.continuous_double_auction.evaluation import evaluate
    simulation.get_client = fake_get_client
    evaluate.get_client = fake_get_client
    return simulation
