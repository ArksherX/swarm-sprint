#!/usr/bin/env python3
"""Upload SFT data to Adaption and start an AutoScientist training run.

Usage:
    cd ~/swarm-sprint
    set -a && . .env && set +a
    .venv-adaption/bin/python tools/train_adaption.py

Reads ADAPTION_API_KEY from the environment.
"""
import json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from adaption import Adaption

SFT_FILE = "results/sft_monitor.jsonl"
STATE_FILE = "results/adaption_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {}

def save_state(s):
    json.dump(s, open(STATE_FILE, "w"), indent=2)

client = Adaption()
state = load_state()

# Step 1: Upload dataset
if "dataset_id" not in state:
    print("Uploading dataset...")
    ds = client.datasets.upload_file(
        SFT_FILE,
        processing_mode="raw",
        column_mapping={"prompt": "prompt", "completion": "completion"},
    )
    state["dataset_id"] = ds.dataset_id
    save_state(state)
    print(f"Dataset created: {ds.dataset_id}")
else:
    print(f"Dataset already uploaded: {state['dataset_id']}")

# Step 2: Wait for ingestion
dataset_id = state["dataset_id"]
print("Waiting for ingestion...")
for _ in range(120):
    status = client.datasets.get_status(dataset_id)
    if status.status == "failed":
        err = getattr(status, "error_data", None)
        msg = (err and getattr(err, "message", None)) or "unknown error"
        raise RuntimeError(f"Ingestion failed: {msg}")
    if status.row_count is not None:
        print(f"Ingested {status.row_count} rows")
        break
    time.sleep(5)
else:
    raise RuntimeError("Ingestion timed out after 10 minutes")

# Step 3: Start AutoScientist
if "run_id" not in state:
    print("Starting AutoScientist run...")
    run = client.autoscientist.create(
        dataset_id=dataset_id,
        model="Qwen/Qwen3.5-4B",
        training_method="instruction",
        
    )
    state["run_id"] = run.run_id
    save_state(state)
    print(f"AutoScientist run started: {run.run_id}")
else:
    print(f"AutoScientist run already started: {state['run_id']}")

print(f"\nState saved to {STATE_FILE}")
print("Monitor progress: .venv-adaption/bin/python tools/check_adaption.py")
