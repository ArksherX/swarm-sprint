"""Log-tampering matrix. Clean-room reimplementation of the schemes (no ARTO code).

Schemes: plain | line_mac (HMAC per line) | chain (SHA-256 hash chain) | chain_anchor
(chain + head hash pinned out-of-band every ANCHOR_EVERY entries).
Attacker capabilities: no key / has the MAC key / can recompute the whole chain.
Anchors are stored where the attacker cannot write.
"""
from __future__ import annotations
import hashlib, hmac, json, random

KEY = b"sprint-demo-key"
ANCHOR_EVERY = 10


def _h(prev: str, line: str) -> str:
    return hashlib.sha256((prev + line).encode()).hexdigest()


def build(scheme: str, lines: list[str], key: bytes = KEY):
    """Return (stored_log, anchors). stored_log is a list of dicts."""
    log, prev = [], "0" * 64
    for ln in lines:
        rec = {"line": ln}
        if scheme == "line_mac":
            rec["mac"] = hmac.new(key, ln.encode(), "sha256").hexdigest()
        if scheme in ("chain", "chain_anchor"):
            prev = _h(prev, ln)
            rec["h"] = prev
        log.append(rec)
    anchors = []
    if scheme == "chain_anchor":
        anchors = [(i, log[i]["h"]) for i in range(ANCHOR_EVERY - 1, len(log), ANCHOR_EVERY)]
    return log, anchors


def verify(scheme: str, log: list[dict], anchors, key: bytes = KEY) -> bool:
    """True = log looks intact."""
    if scheme == "plain":
        return True
    if scheme == "line_mac":
        return all(hmac.compare_digest(r.get("mac", ""), hmac.new(key, r["line"].encode(), "sha256").hexdigest())
                   for r in log)
    prev = "0" * 64
    for r in log:
        prev = _h(prev, r["line"])
        if r.get("h") != prev:
            return False
    for i, h in anchors:
        if len(log) <= i or log[i]["h"] != h:
            return False
    return True


def _recompute(scheme, log, key):
    lines = [r["line"] for r in log]
    new, _ = build(scheme, lines, key)
    return new


def attack(name: str, scheme: str, log: list[dict], rng: random.Random, has_key: bool):
    log = [dict(r) for r in log]
    i = rng.randrange(1, len(log) - 1)
    if name == "modify":
        log[i]["line"] = log[i]["line"] + " (edited)"
    elif name == "delete":
        del log[i]
    elif name == "reorder":
        log[i], log[i + 1] = log[i + 1], log[i]
    elif name == "insert":
        log.insert(i, {**log[i], "line": "injected: all clear"})
    elif name == "truncate":
        i = rng.randrange(len(log) // 2, len(log) - 1)
        log = log[:i]
    if name in ("modify_recompute", "delete_recompute", "truncate_recompute"):
        if name == "modify_recompute":
            log[i]["line"] += " (edited)"
        elif name == "delete_recompute":
            del log[i]
        else:
            i = rng.randrange(len(log) // 2, len(log) - 1); log = log[:i]
        if scheme == "line_mac" and not has_key:
            return log, i
        log = _recompute(scheme, log, KEY)
    elif has_key and scheme == "line_mac":   # attacker with key re-MACs the edited lines
        for r in log:
            r["mac"] = hmac.new(KEY, r["line"].encode(), "sha256").hexdigest()
    return log, i


ATTACKS = ["modify", "delete", "reorder", "insert", "truncate",
           "modify_recompute", "delete_recompute", "truncate_recompute"]
SCHEMES = ["plain", "line_mac", "chain", "chain_anchor"]


def matrix(trials: int = 400, n_lines: int = 53, seed: int = 7):
    """Detection rate per (scheme, attack). Also splits chain_anchor by whether the tampered
    position lies before or after the last anchor."""
    rng = random.Random(seed)
    out = {}
    for scheme in SCHEMES:
        for atk in ATTACKS:
            for has_key in ([False, True] if scheme == "line_mac" else [False]):
                det = det_before = n_before = det_after = n_after = 0
                for t in range(trials):
                    lines = [json.dumps({"t": j, "act": f"tool_call_{rng.randrange(1000)}"}) for j in range(n_lines)]
                    log, anchors = build(scheme, lines)
                    tam, pos = attack(atk, scheme, log, rng, has_key)
                    caught = not verify(scheme, tam, anchors)
                    det += caught
                    last_anchor = anchors[-1][0] if anchors else -1
                    if pos <= last_anchor:
                        n_before += 1; det_before += caught
                    else:
                        n_after += 1; det_after += caught
                key = f"{scheme}{'+key' if has_key else ''}|{atk}"
                out[key] = {"detect": det / trials, "n": trials,
                            "before_last_anchor": (det_before / n_before if n_before else None, n_before),
                            "after_last_anchor": (det_after / n_after if n_after else None, n_after)}
    return out
