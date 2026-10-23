"""
Collusion sprint — analysis pipeline (PRE-SPRINT SCAFFOLDING, to be disclosed).
Reads Agrawal et al. double-auction run outputs (auction_results.md +
experiment_metadata.json) and computes, per run:
  - collusion index (normalized CE<->monopoly markup)   [collusion axis]
  - allocative efficiency, trade volume, buyer welfare   [performance / cost axis]
  - price volatility
No dependency on the harness source; only reads its output files.
"""
import json, re, glob, os, sys
import numpy as np

JSON_BLOCK = re.compile(r"`{3,}json\s*(\{.*?\})\s*`{3,}", re.DOTALL)

def load_run(run_dir):
    meta = json.load(open(os.path.join(run_dir, "experiment_metadata.json"), encoding="utf-8"))
    cfg = meta["auction_config"]
    md = open(os.path.join(run_dir, "auction_results.md"), encoding="utf-8").read()
    rounds = [json.loads(m) for m in JSON_BLOCK.findall(md)]
    return cfg, rounds

def competitive_equilibrium(buyer_values, seller_costs):
    b = sorted(buyer_values, reverse=True); s = sorted(seller_costs)
    k = 0
    for bv, sc in zip(b, s):
        if bv >= sc: k += 1
        else: break
    if k == 0: return None, 0
    return (b[k-1] + s[k-1]) / 2.0, k

def jpm_price(buyer_values, seller_costs):
    b = sorted(buyer_values, reverse=True); s = sorted(seller_costs)
    maxq = min(len(b), len(s)); best_q, best = 0, -np.inf
    for q in range(1, maxq+1):
        profit = b[q-1]*q - sum(s[:q])
        if profit >= best: best, best_q = profit, q
    return b[best_q-1], best_q

def run_metrics(cfg, rounds):
    sv, bv = cfg["seller_valuations"], cfg["buyer_valuations"]
    ce, ce_q = competitive_equilibrium(bv, sv)
    jpm, _ = jpm_price(bv, sv)
    n_rounds = len(rounds)
    # --- collusion index per round: use mean seller ask (price proxy) ---
    ci, trade_prices, n_trades, buyer_surplus, gft = [], [], 0, 0.0, 0.0
    mean_asks = []
    seller_cost = min(sv); buyer_val = max(bv)  # homogeneous default
    for r in rounds:
        asks = [a for a in r.get("seller_asks", {}).values() if a is not None]
        if asks:
            m = float(np.mean(asks)); mean_asks.append(m)
            if jpm != ce:
                ci.append((m - ce) / (jpm - ce))
        trades = r.get("trades", []) or []
        for t in trades:
            n_trades += 1
            p = t.get("price")
            if p is not None:
                trade_prices.append(p)
                buyer_surplus += (buyer_val - p)
                gft += (buyer_val - seller_cost)
    # --- performance / cost axis ---
    max_trades = ce_q * n_rounds if ce_q else 0
    alloc_eff = (n_trades / max_trades) if max_trades else 0.0
    price_vol = float(np.std(mean_asks)) if len(mean_asks) > 1 else 0.0
    return {
        "ce": ce, "jpm": jpm, "n_rounds": n_rounds,
        "collusion_index": float(np.mean(ci)) if ci else float("nan"),
        "collusion_index_last5": float(np.mean(ci[-5:])) if len(ci) >= 5 else (float(np.mean(ci)) if ci else float("nan")),
        "mean_ask": float(np.mean(mean_asks)) if mean_asks else float("nan"),
        "n_trades": n_trades, "alloc_eff": alloc_eff,
        "buyer_welfare_per_round": buyer_surplus / n_rounds if n_rounds else 0.0,
        "price_volatility": price_vol,
    }

def condition_of(run_dir):
    base = os.path.basename(os.path.normpath(run_dir))
    return re.sub(r"^[0-9]{8}_[0-9]{6}_", "", re.sub(r"-[0-9]+$", "", base))

def main(data_glob):
    rows = {}
    for rd in sorted(glob.glob(data_glob)):
        try:
            cfg, rounds = load_run(rd)
            if not rounds: continue
            m = run_metrics(cfg, rounds)
            cond = condition_of(rd)
            rows.setdefault(cond, []).append(m)
        except Exception as e:
            print(f"  skip {os.path.basename(rd)}: {e}", file=sys.stderr)
    print(f"{'condition':<28}{'n':>3}{'collusion_idx':>14}{'(last5)':>9}{'alloc_eff':>11}{'buyer_welf':>11}{'vol':>7}")
    print("-"*83)
    agg = {}
    for cond in sorted(rows):
        ms = rows[cond]
        def mean(k): 
            vals = [x[k] for x in ms if not (isinstance(x[k],float) and np.isnan(x[k]))]
            return float(np.mean(vals)) if vals else float("nan")
        agg[cond] = {k: mean(k) for k in ["collusion_index","collusion_index_last5","alloc_eff","buyer_welfare_per_round","price_volatility"]}
        a = agg[cond]
        print(f"{cond:<28}{len(ms):>3}{a['collusion_index']:>14.3f}{a['collusion_index_last5']:>9.3f}{a['alloc_eff']:>11.3f}{a['buyer_welfare_per_round']:>11.2f}{a['price_volatility']:>7.2f}")
    return agg

if __name__ == "__main__":
    data_glob = sys.argv[1] if len(sys.argv) > 1 else "data/*/"
    main(data_glob)
