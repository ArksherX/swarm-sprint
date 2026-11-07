"""Minimal OpenAI-compatible chat client for NVIDIA NIM with an on-disk cache.

Reads NVIDIA_API_KEY from the environment only. The cache key is the full request, so
re-running an experiment is reproducible and free; delete results/cache to force fresh calls.
"""
from __future__ import annotations
import hashlib, json, os, threading, time, urllib.error, urllib.request

URL = "https://integrate.api.nvidia.com/v1/chat/completions"
CACHE = os.path.join(os.path.dirname(__file__), "..", "results", "cache")
_lock = threading.Lock()
_rate_lock = threading.Lock()
_next_slot = [0.0]
RPM = int(os.environ.get("SWARM_RPM", "30"))


def _throttle():
    """Global pacing so parallel workers stay under the provider's request limit."""
    with _rate_lock:
        now = time.monotonic()
        wait = max(0.0, _next_slot[0] - now)
        _next_slot[0] = max(now, _next_slot[0]) + 60.0 / RPM
    if wait:
        time.sleep(wait)
stats = {"calls": 0, "cache_hits": 0, "errors": 0}


def chat(model: str, messages: list[dict], max_tokens: int = 400, temperature: float = 0.0,
         timeout: int = 90, retries: int = 8) -> str:
    body = {"model": model, "messages": messages, "max_tokens": max_tokens,
            "temperature": temperature,
            "chat_template_kwargs": {"enable_thinking": False}}  # reasoning models otherwise spend max_tokens thinking
    key = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
    path = os.path.join(CACHE, key + ".json")
    if os.path.exists(path):
        with _lock:
            stats["cache_hits"] += 1
        return json.load(open(path))["text"]
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY not set")
    last = None
    for attempt in range(retries):
        try:
            _throttle()
            req = urllib.request.Request(
                URL, data=json.dumps(body).encode(), method="POST",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                text = json.load(r)["choices"][0]["message"].get("content") or ""
            os.makedirs(CACHE, exist_ok=True)
            json.dump({"model": model, "text": text}, open(path, "w"))
            with _lock:
                stats["calls"] += 1
            return text
        except (urllib.error.URLError, TimeoutError, OSError, KeyError, ValueError) as e:
            last = e
            with _lock:
                stats["errors"] += 1
            ra = getattr(e, "headers", None) and e.headers.get("Retry-After")
            time.sleep(min(60, float(ra)) if ra and str(ra).isdigit() else min(120, 8 * 2 ** attempt))
    raise RuntimeError(f"LLM call failed after {retries} tries: {last}")
