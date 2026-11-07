from __future__ import annotations
import json, random, re
from dataclasses import asdict
from . import llm
from .sandbox import make_sandbox
from .scenarios import SYSTEM, task

MAX_TURNS = 5


def parse_action(text: str) -> dict | None:
    """First balanced-looking JSON object in the reply; None if unparseable."""
    for m in re.finditer(r"\{", text):
        depth = 0
        for j in range(m.start(), len(text)):
            depth += text[j] == "{"
            depth -= text[j] == "}"
            if depth == 0:
                try:
                    obj = json.loads(text[m.start():j + 1])
                    if isinstance(obj, dict):
                        return obj
                except ValueError:
                    pass
                break
    return None


def run_session(kind: str, k: int, seed: int, agent_model: str) -> dict:
    rng = random.Random(f"{kind}-{k}-{seed}")
    sid = f"sess-{kind[:2]}{k}-{seed}"
    sb = make_sandbox(rng, sid)
    parse_fail = 0
    for i in range(k):
        agent = f"agent{i}"
        msgs = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": task(kind, i, k)}]
        for step in range(MAX_TURNS):
            reply = llm.chat(agent_model, msgs, max_tokens=300, temperature=0.0)
            act = parse_action(reply)
            if act is None:
                parse_fail += 1
                msgs += [{"role": "assistant", "content": reply},
                         {"role": "user", "content": "Reply with one JSON object only."}]
                continue
            if "done" in act:
                break
            res = sb.call(agent, step, str(act.get("tool", "")), act.get("args") or {})
            msgs += [{"role": "assistant", "content": json.dumps(act)},
                     {"role": "user", "content": f"Tool result: {res}"}]
    return {"session": sid, "kind": kind, "k": k, "seed": seed, "canary": sb.canary,
            "label": sb.exfiltrated(), "parse_fail": parse_fail,
            "events": [asdict(e) for e in sb.events]}
