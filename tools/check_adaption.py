#!/usr/bin/env python3
"""Check AutoScientist training status."""
import json, os
from adaption import Adaption

STATE_FILE = "results/adaption_state.json"
state = json.load(open(STATE_FILE))
client = Adaption()

run = client.autoscientist.get(state["run_id"])
print(f"Run:      {state['run_id']}")
print(f"Status:   {run.status}")
print(f"Model:    {run.model}")
if run.win_rate is not None:
    print(f"Win rate: {run.win_rate}")
if hasattr(run, 'error') and run.error:
    print(f"Error:    {run.error}")
