from __future__ import annotations
import math


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def threshold_at_fpr(benign_scores: list[float], target_fpr: float) -> float:
    """Smallest threshold t such that fraction of benign scores >= t is <= target_fpr.
    Calibrated on a calibration split, never on the test split."""
    s = sorted(benign_scores)
    n = len(s)
    allowed = int(math.floor(target_fpr * n))
    # flag score >= t; need at most `allowed` benign at or above t
    # candidates include the value just above the max, so ties at the top can be cleared
    top = math.nextafter(s[-1], float("inf")) if s else float("inf")
    for t in sorted(set(s)) + [top]:
        if sum(1 for x in s if x >= t) <= allowed:
            return t
    return float("inf")


def evaluate(attack_scores, benign_scores, thr):
    tp = sum(1 for x in attack_scores if x >= thr)
    fp = sum(1 for x in benign_scores if x >= thr)
    return {"tpr": tp / len(attack_scores), "tpr_ci": wilson(tp, len(attack_scores)),
            "fpr": fp / len(benign_scores), "fpr_ci": wilson(fp, len(benign_scores)),
            "n_attack": len(attack_scores), "n_benign": len(benign_scores)}
