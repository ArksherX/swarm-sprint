# Prior work disclosure

Required by the Swarm Alignment Hackathon rules. Everything below existed BEFORE the
sprint started (kickoff Fri 6 Nov 2026). Nothing in this repository imports it.

## Pre-existing (not part of this submission's contribution)

ARTO suite (Tessera, VerityFlux, Vestigia), repo `ArksherX/ARTO`, local checkout
`ml-redteam`, pinned at commit `80b90bc2d5426cc55c4fafac6a11f4c54512225e` (2026-11-05).
BSL 1.1, (c) ARTONexa Ltd.

Relevant earlier components:
- Tessera: scoped, depth-limited delegation (identity).
- VerityFlux: tool-call and trajectory scoring, multi-turn detectors.
- Vestigia: hash-chained append-only ledger, correlation endpoints.
- W3C trace-context + baggage `session.id` propagation across the three tools:
  commits `8c682ea`, `c12e11d`, `01e1290`, `80b90bc` (all 2026-11-05, the day before kickoff).
- Prior multi-turn escalation corpus and its figures (~0% per-message vs ~44% trajectory
  detection at ~8% FPR). Measured on that corpus only; not re-measured here.

## New during the sprint (everything under this repo)

`harness/`, `tools/`, `tests/`, `results/`, and the report. Commit history of this repo
is the record; the first commit is the scaffold made on 2026-11-06.

## Rule for this repo

If any code or data from the prior work is copied in, list file and source commit here
before it is committed.
