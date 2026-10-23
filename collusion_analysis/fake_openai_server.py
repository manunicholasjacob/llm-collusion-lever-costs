"""Fake OpenAI-compatible server for $0 tests of the routed backend (built Oct 23, sprint tooling).
POST /v1/chat/completions: records the request body (JSON lines) and answers by role.
GET  /v1/key: OpenRouter-style usage, rising by COST_PER_CALL per completion, to test the budget stop.
Usage: python -X utf8 -I collusion_analysis/fake_openai_server.py PORT RECORD.jsonl"""
import json, random, sys, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT, RECORD = int(sys.argv[1]), sys.argv[2]
COST_PER_CALL = 0.001
calls, lock = [0], threading.Lock()


def answer(prompt):
    if "expert overseer" in prompt:
        return {"evidence": [], "coordination": "yes", "coordination_score": 4, "type": "overt"}
    return {"reflection": "r", "plan_for_this_hour": "p", "ask": f"{random.uniform(88, 99):.2f}",
            "bid": random.uniform(82, 95), "new_memory": "m", "plan_for_message": "pm",
            "message_to_sellers": "hold at 98", "scratch_pad_update": "s"}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, obj):
        body = json.dumps(obj).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        if self.path.endswith("/key"):
            self._send({"data": {"usage": round(calls[0] * COST_PER_CALL, 6), "limit": None}})
        else:
            self.send_error(404)

    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        with lock:
            calls[0] += 1
            with open(RECORD, "a", encoding="utf-8") as f:
                f.write(json.dumps({k: v for k, v in req.items() if k != "messages"}
                                   | {"prompt_head": req["messages"][-1]["content"][:80]}) + "\n")
        self._send({"id": "x", "object": "chat.completion", "model": req["model"], "created": 0,
                    "choices": [{"index": 0, "finish_reason": "stop",
                                 "message": {"role": "assistant", "content": json.dumps(answer(req["messages"][-1]["content"]))}}],
                    "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}})


ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
