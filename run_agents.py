"""Generate sessions with real LLM agents. Writes results/sessions.jsonl (append, resumable).
    NVIDIA_API_KEY=... python3 run_agents.py --per-cell 12 --workers 8
"""
from __future__ import annotations
import argparse, json, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from harness.runner import run_session
from harness import llm

AGENT_MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"
OUT = "results/sessions.jsonl"

ap = argparse.ArgumentParser()
ap.add_argument("--per-cell", type=int, default=12)
ap.add_argument("--ks", default="2,4,6")
ap.add_argument("--workers", type=int, default=8)
a = ap.parse_args()
os.makedirs("results", exist_ok=True)
done = set()
if os.path.exists(OUT):
    done = {json.loads(l)["session"] for l in open(OUT)}
jobs = [(kind, k, s) for k in map(int, a.ks.split(",")) for kind in ("attack", "benign", "hardneg")
        for s in range(a.per_cell) if f"sess-{kind[:2]}{k}-{s}" not in done]
print(f"{len(jobs)} sessions to run ({len(done)} already done)")
with ThreadPoolExecutor(a.workers) as ex, open(OUT, "a") as f:
    futs = {ex.submit(run_session, kd, k, s, AGENT_MODEL): (kd, k, s) for kd, k, s in jobs}
    for n, fu in enumerate(as_completed(futs), 1):
        try:
            r = fu.result()
        except Exception as e:  # noqa: BLE001
            print("FAILED", futs[fu], e); continue
        f.write(json.dumps(r) + "\n"); f.flush()
        if n % 10 == 0 or n == len(jobs):
            print(f"  {n}/{len(jobs)}  llm={llm.stats}")
