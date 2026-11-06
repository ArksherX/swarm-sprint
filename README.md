# swarm-sprint

Submission for Apart's Swarm Alignment Hackathon (Nov 2026). Solo.
Question: do monitors that see one agent at a time miss attacks split across agents,
and does a shared session identity recover detection at a fixed false-positive rate?

    python3 -m pytest -q tests
    python3 run_pilot.py --n 400 --seed 1       # writes results/pilot_seed1.json
    python3 tools/check_refs.py refs.tsv        # verify citations (needs network)

Status: simulated event streams only. Not yet driven by real LLM agents.
See PRIOR_WORK.md for what pre-dates the sprint.
