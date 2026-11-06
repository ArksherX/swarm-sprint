"""Pilot: per-agent vs session-level vs session-level with the identity thread stripped.

Every number in results/ is written by this script. Do not hand-type results into the report.
    python3 run_pilot.py --n 400 --seed 1
"""
from __future__ import annotations
import argparse
import json
import random
from harness.sim import make_session
from harness.monitors import per_agent, session_level
from harness.metrics import threshold_at_fpr, evaluate

ARMS = {"per_agent": (per_agent, False),
        "session_level": (session_level, False),
        "session_level_no_thread": (session_level, True)}


def run(n: int, seed: int, target_fpr: float, obfuscate: float):
    out = {"config": {"n_per_cell": n, "seed": seed, "target_fpr": target_fpr,
                      "obfuscate": obfuscate}, "cells": []}
    for k in (2, 4, 8):
        for arm, (fn, strip) in ARMS.items():
            rng = random.Random(f"{seed}-{k}-{arm}")
            def gen(attack):
                return [fn(make_session(rng, k, attack, strip_identity=strip,
                                        obfuscate=obfuscate)) for _ in range(n)]
            cal_benign = gen(False)                 # calibration split
            thr = threshold_at_fpr(cal_benign, target_fpr)
            res = evaluate(gen(True), gen(False), thr)   # fresh test split
            out["cells"].append({"agents": k, "arm": arm, "threshold": thr, **res})
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--fpr", type=float, default=0.05)
    ap.add_argument("--obfuscate", type=float, default=0.3)
    a = ap.parse_args()
    r = run(a.n, a.seed, a.fpr, a.obfuscate)
    path = f"results/pilot_seed{a.seed}.json"
    json.dump(r, open(path, "w"), indent=1, default=str)
    for c in r["cells"]:
        print(f"{c['agents']} agents  {c['arm']:<24} TPR {c['tpr']:.2f} "
              f"[{c['tpr_ci'][0]:.2f},{c['tpr_ci'][1]:.2f}]  FPR {c['fpr']:.3f}")
    print("wrote", path)
