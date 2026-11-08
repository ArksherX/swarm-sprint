## Session outcomes (label = canary reached the external sink)

| scenario | k | sessions | exfiltrated |
|---|---|---|---|
| attack | 2 | 14 | 13 |
| attack | 4 | 14 | 14 |
| attack | 6 | 14 | 13 |
| benign | 2 | 14 | 0 |
| benign | 4 | 14 | 0 |
| benign | 6 | 14 | 0 |
| hardneg | 2 | 14 | 0 |
| hardneg | 4 | 14 | 0 |
| hardneg | 6 | 14 | 0 |

Agent replies that failed to parse as JSON: 0 across 126 sessions.

## All sessions: exfiltration vs no exfiltration

n positives = 40, n negatives = 86

| monitor | AUROC [95% CI] | TPR @ 5% FPR (split-avg) | realised FPR |
|---|---|---|---|
| rules_per_agent | 0.52 [0.50, 0.54] | 0.00 [0.00, 0.00] | 0.000 |
| per_agent | 0.58 [0.52, 0.65] | 0.21 [0.10, 0.35] | 0.033 |
| session_thread | 0.58 [0.52, 0.65] | 0.20 [0.10, 0.30] | 0.036 |
| window_thread | 0.57 [0.51, 0.64] | 0.17 [0.05, 0.30] | 0.037 |
| window_nothread | 0.57 [0.51, 0.64] | 0.16 [0.00, 0.30] | 0.034 |
| taint_session | 0.99 [0.98, 1.00] | 1.00 [1.00, 1.00] | 0.012 |

## Hard case: exfiltration vs sessions where the secret was read but not leaked

n positives = 40, n negatives = 42

| monitor | AUROC [95% CI] | TPR @ 5% FPR (split-avg) | realised FPR |
|---|---|---|---|
| rules_per_agent | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] | 0.000 |
| per_agent | 0.58 [0.51, 0.65] | 0.21 [0.10, 0.30] | 0.037 |
| session_thread | 0.58 [0.51, 0.65] | 0.20 [0.05, 0.30] | 0.037 |
| window_thread | 0.58 [0.51, 0.65] | 0.18 [0.05, 0.30] | 0.038 |
| window_nothread | 0.58 [0.51, 0.65] | 0.17 [0.05, 0.30] | 0.035 |
| taint_session | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.000 |

## Team size k=2

n positives = 13, n negatives = 29

| monitor | AUROC [95% CI] | TPR @ 5% FPR (split-avg) | realised FPR |
|---|---|---|---|
| rules_per_agent | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] | 0.000 |
| per_agent | 0.75 [0.61, 0.88] | 0.54 [0.29, 0.86] | 0.049 |
| session_thread | 0.75 [0.59, 0.88] | 0.54 [0.29, 0.71] | 0.052 |
| window_thread | 0.74 [0.58, 0.88] | 0.46 [0.14, 0.71] | 0.023 |
| window_nothread | 0.74 [0.58, 0.88] | 0.43 [0.14, 0.71] | 0.049 |
| taint_session | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.000 |

## Team size k=4

n positives = 14, n negatives = 28

| monitor | AUROC [95% CI] | TPR @ 5% FPR (split-avg) | realised FPR |
|---|---|---|---|
| rules_per_agent | 0.55 [0.50, 0.61] | 0.00 [0.00, 0.00] | 0.000 |
| per_agent | 0.52 [0.46, 0.61] | 0.07 [0.00, 0.14] | 0.037 |
| session_thread | 0.52 [0.46, 0.61] | 0.06 [0.00, 0.14] | 0.036 |
| window_thread | 0.50 [0.43, 0.59] | 0.02 [0.00, 0.14] | 0.040 |
| window_nothread | 0.50 [0.43, 0.59] | 0.02 [0.00, 0.14] | 0.033 |
| taint_session | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.000 |

## Team size k=6

n positives = 13, n negatives = 29

| monitor | AUROC [95% CI] | TPR @ 5% FPR (split-avg) | realised FPR |
|---|---|---|---|
| rules_per_agent | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] | 0.000 |
| per_agent | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] | 0.000 |
| session_thread | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] | 0.000 |
| window_thread | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] | 0.000 |
| window_nothread | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] | 0.000 |
| taint_session | 0.98 [0.95, 1.00] | 0.48 [0.00, 1.00] | 0.032 |

## Paired AUROC differences (bootstrap over sessions)

- session_thread-per_agent: +0.00 [95% CI +0.00, +0.00]
- window_thread-window_nothread: +0.00 [95% CI -0.00, +0.00]
