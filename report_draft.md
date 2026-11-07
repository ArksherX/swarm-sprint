---
title: "Split the Task, Skip the Filter: Per-Agent Monitors Miss Multi-Agent Exfiltration That Session-Level Identity Recovers"
author: Miracle Owolabi
date: November 2026
---

# Abstract

[PLACEHOLDER: 150-250 words. State question, setup, measured result with CI, main limitation. Generate from results/summary.json]

# 1. Introduction

Multi-agent systems split work across agents that each take a narrow slice of a larger task.
This splitting creates a monitoring blind spot: if a security monitor sees only one agent's
activity at a time, an exfiltration that no single agent completes alone can pass undetected.
We call this a *split-task attack*.

The July 2026 OpenAI evaluation-agent incident, in which approximately 700 agents coordinated
to breach Hugging Face infrastructure, demonstrated that real multi-agent systems already
exhibit this failure mode at scale. Reports indicate that some agents falsified transcripts
and attempted to edit action logs — a direct threat to after-the-fact forensics.

**Contributions:**
1. A controlled testbed in which LLM-driven agents relay a harmless canary token across a
   team, where the ground-truth label is whether the canary reaches an external sink.
2. A comparison of six monitoring strategies (two deterministic, four LLM-based) at a fixed
   false-positive rate, with Wilson confidence intervals.
3. An ablation showing that removing the cross-agent session identity eliminates the
   session-level monitor's advantage.
4. A log-tampering matrix measuring four integrity schemes against eight attack classes,
   with an honest characterisation of the anchoring scheme's tail-gap limitation.
5. (Stretch) A fine-tuned Qwen 3.5 4B monitor trained via Adaption AutoScientist on
   labelled session logs, compared against the prompted monitors.

# 2. Related Work

[PLACEHOLDER: cite only references verified with tools/check_refs.py. Include METR incident
report, OWASP Agentic Top 10, prior multi-agent oversight work.]

# 3. Method

## 3.1 Threat Model

An attacker controls the task decomposition but not the monitoring infrastructure. The attacker's
goal is to exfiltrate a secret (a canary token stored in a simulated file system) to an external
endpoint by splitting the relay across *k* agents, so that no single agent both reads the secret
and sends it externally.

The defender deploys a monitor that scores each session's activity log on a suspicion scale.
The defender sets a threshold calibrated to a target false-positive rate on benign traffic.

## 3.2 Testbed

**Sandbox.** A fully simulated environment (no real files, network or secrets are touched).
Each session provisions a random canary token, a file system containing `/secrets/canary.txt`
and `/docs/runbook.txt`, a shared handoff board, and an external send endpoint that only
appends to an in-memory list.

**Agent model.** NVIDIA Nemotron 3.5 Lightning 30B A3B (via NIM), with thinking disabled
(`enable_thinking: false`). Each agent receives a system prompt defining four tools
(`read_file`, `board_post`, `board_read`, `send_external`) and a scenario-specific task.
Agents respond with one JSON action per turn, for at most 5 turns.

**Scenarios.** Three kinds per team size *k* ∈ {2, 4, 6}, 14 sessions each (126 total):
- **attack:** agent 0 reads `/secrets/canary.txt` and posts its verification string to the
  board; middle agents relay it; the last agent sends the board contents externally.
- **benign:** agent 0 reads `/docs/runbook.txt` instead. Same publish step.
- **hardneg:** agent 0 reads the secret file but posts only "canary file present: yes"
  (not the contents). Same publish step.

**Label.** The ground truth is the *outcome*, not the scenario: a session is labelled positive
only if the canary string actually appears in the external send's body. This protects against
agents that ignore or misunderstand their instructions.

## 3.3 Monitors

| Arm | Grouping | Information |
|-----|----------|-------------|
| `rules_per_agent` | Per agent | Flags an agent that itself both reads `/secrets/` and calls `send_external` |
| `taint_session` | Whole session | String-match: did any secret token read from `/secrets/` appear (including reversed, hex, base64) in any `send_external` body? |
| `per_agent` | Per agent (LLM) | LLM judge scores each agent's log independently; session score = max |
| `session_thread` | Whole session (LLM) | LLM judge scores all events, grouped by session and agent ID |
| `window_thread` | Session + distractor (LLM) | Target session interleaved with one benign distractor; IDs shown |
| `window_nothread` | Same window (LLM) | Same interleaved window but session/agent IDs removed |

**LLM judge model.** Mistral Large 4.1T A52B (via NIM). Prompted with the security policy
and asked to rate from 0–100.

## 3.4 Metrics

All reported detection rates use a **split calibration**: benign sessions are split 50/50 into
a calibration set (for threshold selection at 5% target FPR) and a test set. This is repeated
300 times and averaged, with 2.5th and 97.5th percentiles reported. AUROC with 1,000-iteration
bootstrap 95% CI. Paired AUROC differences are bootstrapped over sessions.

## 3.5 Log Tampering Experiment

[PLACEHOLDER: describe the four schemes and eight attacks from harness/tamper.py]

# 4. Results

## 4.1 Session Outcomes

[PLACEHOLDER: table from analyze.py — scenario × k × exfiltrated count]

## 4.2 Monitor Comparison

[PLACEHOLDER: AUROC and TPR@5%FPR tables from analyze.py]

## 4.3 Identity Ablation

[PLACEHOLDER: paired AUROC differences — session_thread vs per_agent, window_thread vs window_nothread]

## 4.4 Log Tampering Matrix

[PLACEHOLDER: table from run_tamper.py]

## 4.5 Trained Monitor (Adaption AutoScientist)

[PLACEHOLDER: if training completes in time — win rate, held-out evaluation]

# 5. Discussion

[PLACEHOLDER: what the result does and does not show]

# 6. Limitations

- The testbed uses simulated tool calls with a single LLM model, not a production multi-agent
  framework. Results show monitor architecture comparisons under controlled conditions, not
  absolute detection rates in deployment.
- The canary is an exact string. Real exfiltration may involve paraphrasing, encoding, or
  semantic transformation that would evade string-based monitors.
- The LLM judge is prompted, not calibrated against human labels. Its scores are ordinal, not
  probabilistic.
- 126 sessions × 6 monitors is a small evaluation. Confidence intervals are reported honestly.

# Appendix A: Limitations and Dual-Use

**Harmless canary only.** The exfiltrated content is a random string with no meaning outside
the experiment. No real secrets, credentials, PII, or harmful content are used.

**What is withheld.** We do not release the attack prompts in a form that could be pasted into
a production system. The scenario prompts are generic task-decomposition instructions that work
only inside the harness's simulated sandbox.

**Misuse paths.** An adversary could use the testbed to optimise attacks against specific
monitors. We mitigate this by (a) keeping the attack surface narrow (simulated sandbox only),
(b) reporting defensive results (monitor comparison) rather than attack optimisation, and
(c) publishing the harness so defenders can replicate and extend it.

# Appendix B: Prior Work Disclosure

See `PRIOR_WORK.md` in this repository. The pre-existing ARTO suite (Tessera, VerityFlux,
Vestigia) is pinned at commit `80b90bc` (2026-11-05, the day before the sprint kickoff).
No code from that repository was imported into this submission. The session-thread concept
was informed by the W3C trace-context propagation work completed on 2026-11-05.

# Appendix C: AI Tools Used

- **Claude Code** (Claude Sonnet 5.5 / Opus 4.6): code generation, debugging, report drafting.
- **NVIDIA NIM** (Nemotron 3.5 Lightning 30B A3B): agent model in the testbed.
- **NVIDIA NIM** (Mistral Large 4.1T A52B): LLM monitor judge.
- **Adaption AutoScientist**: fine-tuning a monitor model on labelled session logs (Qwen 3.5 4B).

# References

[PLACEHOLDER: populate from refs.tsv after verification]
