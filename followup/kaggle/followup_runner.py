"""Follow-up runner for Kaggle's free GPUs: serve an open model with vLLM (Ollama as a fallback), point the
Agrawal et al. harness at it through its OpenAI-compatible local backend, and run the jobs in plan.json.
Results are packed into /kaggle/working/results.tar.gz. No paid API is used: every model call goes to localhost."""
import glob, json, os, shutil, subprocess, sys, tarfile, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

T0 = time.time()
PLAN_FILE = "plan.json"  # each kernel copy names its own plan file
DATA = glob.glob(f"/kaggle/input/**/{PLAN_FILE}", recursive=True)[0].rsplit("/", 1)[0]
PLAN = json.load(open(f"{DATA}/{PLAN_FILE}"))
WORK = "/kaggle/working/h"
LOG = open("/kaggle/working/runner.log", "a", buffering=1)


def log(*a):
    msg = f"[{time.time() - T0:7.0f}s] " + " ".join(str(x) for x in a)
    print(msg, flush=True); LOG.write(msg + "\n")


def sh(cmd, **kw):
    log("$", cmd)
    return subprocess.run(cmd, shell=True, **kw)


def up(port, timeout, proc=None):
    t = time.time()
    while time.time() - t < timeout:
        if proc is not None and proc.poll() is not None:
            log(f"server on {port} exited with code {proc.returncode}")
            return False
        try:
            urllib.request.urlopen(f"http://localhost:{port}/v1/models", timeout=5).read()
            return True
        except Exception:
            time.sleep(10)
    return False


def smoke(port, name):
    body = json.dumps({"model": name, "temperature": 0.7, "max_tokens": 120, "response_format": {"type": "json_object"},
                       "messages": [{"role": "user", "content": 'You are a seller with cost 80. Reply only with JSON {"ask": <number>, "message": "<short>"}.'}]}).encode()
    req = urllib.request.Request(f"http://localhost:{port}/v1/chat/completions", body, {"Content-Type": "application/json"})
    out = json.loads(urllib.request.urlopen(req, timeout=300).read())["choices"][0]["message"]["content"]
    log(f"smoke {port}:", out[:120]); json.loads(out)


log("plan:", PLAN.get("phase"), "| prefix", PLAN["prefix"], "|", sum(a["n"] for a in PLAN["arms"]), "jobs")
sh("nvidia-smi --query-gpu=name,memory.total --format=csv")
ngpu = int(subprocess.run("nvidia-smi -L | wc -l", shell=True, capture_output=True, text=True).stdout.strip() or 0)
shutil.copytree(DATA, WORK, dirs_exist_ok=True)
os.chdir(WORK)
sh("pip install -q backoff anthropic wandb 2>&1 | tail -2")
if subprocess.run([sys.executable, "-c", "import google.api_core.exceptions"]).returncode != 0:
    os.makedirs("stubs/google/api_core", exist_ok=True)
    open("stubs/google/__init__.py", "w").close(); open("stubs/google/api_core/__init__.py", "w").close()
    open("stubs/google/api_core/exceptions.py", "w").write("class GoogleAPIError(Exception):\n    pass\nclass ResourceExhausted(GoogleAPIError):\n    pass\n")

M = PLAN["model"]; NAME = PLAN["served_name"]
ports = [8000 + i for i in range(max(1, ngpu))]
backend = None
sh("pip install -q vllm 2>&1 | tail -2")
# vllm pulls a torch built for a newer CUDA than the image's torchaudio, and transformers imports torchaudio
# when present (run 1 crashed on exactly that); nothing here needs audio.
sh("pip uninstall -y -q torchaudio 2>&1 | tail -1")
sh(f"{sys.executable} -c 'import torch; print(torch.__version__, torch.version.cuda, torch.cuda.get_device_capability(0))'")
procs = []
for i, p in enumerate(ports):
    cmd = (f"exec {sys.executable} -m vllm.entrypoints.openai.api_server --model {M['vllm']} "
           f"--served-model-name {NAME} --port {p} --dtype half --max-model-len {PLAN.get('max_model_len', 8192)} "
           f"--gpu-memory-utilization 0.90 --enable-prefix-caching > /kaggle/working/vllm_{p}.log 2>&1")
    log("$", cmd)
    procs.append(subprocess.Popen(cmd, shell=True, env=dict(os.environ, CUDA_VISIBLE_DEVICES=str(i))))
if all(up(p, 1500, pr) for p, pr in zip(ports, procs)):
    backend = "vllm"
else:
    log("vLLM did not come up; tail of its log follows, then Ollama fallback")
    sh(f"tail -30 /kaggle/working/vllm_{ports[0]}.log")
    sh("pkill -f vllm.entrypoints || true")
    sh("apt-get install -y -qq zstd > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq zstd)")
    sh("curl -fsSL https://ollama.com/install.sh | sh > /kaggle/working/ollama_install.log 2>&1")
    for i, p in enumerate(ports):
        sh(f"CUDA_VISIBLE_DEVICES={i} OLLAMA_HOST=127.0.0.1:{p} OLLAMA_NUM_PARALLEL={PLAN['par_per_gpu']} "
           f"OLLAMA_KEEP_ALIVE=-1 OLLAMA_CONTEXT_LENGTH={PLAN.get('max_model_len', 8192)} nohup ollama serve > /kaggle/working/ollama_{p}.log 2>&1 &")
    time.sleep(15)
    for p in ports:
        sh(f"OLLAMA_HOST=127.0.0.1:{p} ollama pull {M['ollama']} > /dev/null 2>&1; "
           f"OLLAMA_HOST=127.0.0.1:{p} ollama cp {M['ollama']} {NAME}")
    backend = "ollama" if all(up(p, 600) for p in ports) else None
if backend is None:
    raise SystemExit("no backend came up")
log("backend:", backend, "ports:", ports)
for p in ports:
    smoke(p, NAME)

jobs = []
for arm in PLAN["arms"]:
    start = arm.get("start", 1)  # top-ups continue an earlier phase's numbering
    for i in range(start, start + arm["n"]):
        jobs.append((f"{arm.get('prefix', PLAN['prefix'])}-{arm['name']}-{i}", arm["flags"]))
# top-ups (arms with "start" > 1) first, then interleave the rest so a time stop leaves balanced arms
topups = {f"{a.get('prefix', PLAN['prefix'])}-{a['name']}" for a in PLAN["arms"] if a.get("start", 1) > 1}
jobs.sort(key=lambda j: (j[0].rsplit("-", 1)[0] not in topups, int(j[0].rsplit("-", 1)[1]), j[0]))
seller = " ".join(["gpt-4.1"] * 5)
deadline = T0 + PLAN.get("max_hours", 11) * 3600


def pack(final=False):
    """Write results.tar.gz with every finished run so far, so a session cut short keeps its completed runs."""
    tmp = "/kaggle/working/results.tar.gz.tmp"
    with tarfile.open(tmp, "w:gz") as tf:
        prefixes = {a.get("prefix", PLAN["prefix"]) for a in PLAN["arms"]}
        for d in [d for p in prefixes for d in glob.glob(f"results/*_{p}-*")]:
            if not os.path.exists(f"{d}/experiment_metadata.json"):
                continue
            for f in ("experiment_metadata.json", "auction_results.md", "collusion_metrics.json", "unified.log", "Overseer.md"):
                if os.path.exists(f"{d}/{f}"):
                    tf.add(f"{d}/{f}")
            for f in glob.glob(f"{d}/Seller*.md"):
                tf.add(f)
        if final:
            tf.add("results/fu_summary.json")
    os.replace(tmp, "/kaggle/working/results.tar.gz")


import threading
PACK_LOCK = threading.Lock()


def run(idx_job):
    idx, (tag, flags) = idx_job
    if time.time() > deadline:
        log("TIME STOP, skipping", tag); return tag, "skipped"
    port = ports[idx % len(ports)]
    env = dict(os.environ, LOCAL_LLM_BASE_URL=f"http://localhost:{port}/v1", LOCAL_LLM_API_KEY="local",
               LLM_MODEL_MAP=f"gpt-4.1={NAME},gpt-4.1-mini={NAME}", SKIP_LLM_JUDGE="1", WANDB_MODE="disabled",
               PYTHONPATH=f"{WORK}/stubs:{WORK}", PYTHONUTF8="1")
    sellers = seller if "--maverick" not in flags else " ".join(["gpt-4.1"] * 4 + ["noregret"])
    flags = flags.replace("--maverick", "")
    cmd = (f"{sys.executable} -X utf8 src/continuous_double_auction/simulation.py --seller_valuations 80 80 80 80 80 "
           f"--buyer_valuations 100 100 100 100 100 --seller_models {sellers} --buyer_models {seller} "
           f"--rounds 30 {flags} --tag {tag}")
    t = time.time()
    r = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
    status = "done" if r.returncode == 0 else "FAIL"
    log(status, tag, f"{time.time() - t:.0f}s", "" if r.returncode == 0 else r.stderr[-400:])
    with PACK_LOCK:
        pack()
    return tag, status


with ThreadPoolExecutor(PLAN["par_per_gpu"] * len(ports)) as ex:
    res = list(ex.map(run, enumerate(jobs)))
json.dump({"backend": backend, "model": M, "ngpu": ngpu, "results": res, "hours": (time.time() - T0) / 3600},
          open("results/fu_summary.json", "w"), indent=1)
pack(final=True)
log("packed", len(res), "jobs;", sum(s == "done" for _, s in res), "done")
