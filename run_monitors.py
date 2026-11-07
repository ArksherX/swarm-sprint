"""Score every recorded session with every monitor. Resumable. Writes results/scores.jsonl."""
from __future__ import annotations
import json, os
from concurrent.futures import ThreadPoolExecutor
from harness.llm_monitors import llm_scores, rule_scores
from harness import llm

SESS, OUT = "results/sessions.jsonl", "results/scores.jsonl"
sessions = [json.loads(l) for l in open(SESS)]
done = {json.loads(l)["session"] for l in open(OUT)} if os.path.exists(OUT) else set()
todo = [s for s in sessions if s["session"] not in done]
print(f"{len(todo)} sessions to score ({len(done)} done)")


def one(s):
    return {"session": s["session"], "kind": s["kind"], "k": s["k"], "label": s["label"],
            **llm_scores(s, sessions), **rule_scores(s)}


with ThreadPoolExecutor(2) as ex, open(OUT, "a") as f:
    for n, r in enumerate(ex.map(one, todo), 1):
        f.write(json.dumps(r) + "\n"); f.flush()
        if n % 10 == 0 or n == len(todo):
            print(f"  {n}/{len(todo)} llm={llm.stats}")
