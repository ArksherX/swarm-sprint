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
| per_agent | 0.99 [0.98, 1.00] | 0.95 [0.90, 1.00] | 0.014 |
| session_thread | 0.98 [0.96, 1.00] | 0.87 [0.00, 1.00] | 0.035 |
| window_thread | 0.72 [0.65, 0.78] | 0.15 [0.00, 0.30] | 0.035 |
| window_nothread | 0.83 [0.77, 0.89] | 0.09 [0.00, 0.20] | 0.035 |
| taint_session | 0.99 [0.98, 1.00] | 1.00 [1.00, 1.00] | 0.012 |

## Hard case: exfiltration vs sessions where the secret was read but not leaked

n positives = 40, n negatives = 42

| monitor | AUROC [95% CI] | TPR @ 5% FPR (split-avg) | realised FPR |
|---|---|---|---|
| rules_per_agent | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] | 0.000 |
| per_agent | 0.99 [0.98, 1.00] | 0.95 [0.90, 1.00] | 0.000 |
| session_thread | 0.98 [0.94, 1.00] | 0.77 [0.00, 1.00] | 0.049 |
| window_thread | 0.74 [0.65, 0.82] | 0.18 [0.05, 0.30] | 0.024 |
| window_nothread | 0.77 [0.68, 0.85] | 0.08 [0.00, 0.20] | 0.048 |
| taint_session | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.000 |

## Team size k=2

n positives = 13, n negatives = 29

| monitor | AUROC [95% CI] | TPR @ 5% FPR (split-avg) | realised FPR |
|---|---|---|---|
| rules_per_agent | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] | 0.000 |
| per_agent | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.044 |
| session_thread | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.055 |
| window_thread | 0.86 [0.73, 0.97] | 0.13 [0.00, 0.43] | 0.044 |
| window_nothread | 0.93 [0.83, 0.99] | 0.37 [0.00, 1.00] | 0.033 |
| taint_session | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.000 |

## Team size k=4

n positives = 14, n negatives = 28

| monitor | AUROC [95% CI] | TPR @ 5% FPR (split-avg) | realised FPR |
|---|---|---|---|
| rules_per_agent | 0.55 [0.50, 0.61] | 0.00 [0.00, 0.00] | 0.000 |
| per_agent | 0.98 [0.94, 1.00] | 0.93 [0.86, 1.00] | 0.000 |
| session_thread | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.000 |
| window_thread | 0.61 [0.52, 0.70] | 0.00 [0.00, 0.00] | 0.037 |
| window_nothread | 0.73 [0.62, 0.86] | 0.00 [0.00, 0.00] | 0.028 |
| taint_session | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.000 |

## Team size k=6

n positives = 13, n negatives = 29

| monitor | AUROC [95% CI] | TPR @ 5% FPR (split-avg) | realised FPR |
|---|---|---|---|
| rules_per_agent | 0.50 [0.50, 0.50] | 0.00 [0.00, 0.00] | 0.000 |
| per_agent | 0.98 [0.95, 1.00] | 0.57 [0.00, 1.00] | 0.036 |
| session_thread | 0.95 [0.90, 1.00] | 0.10 [0.00, 1.00] | 0.019 |
| window_thread | 0.67 [0.55, 0.80] | 0.15 [0.00, 0.43] | 0.034 |
| window_nothread | 0.86 [0.77, 0.94] | 0.16 [0.00, 0.43] | 0.034 |
| taint_session | 0.98 [0.95, 1.00] | 0.48 [0.00, 1.00] | 0.032 |

## Paired AUROC differences (bootstrap over sessions)

- session_thread-per_agent: -0.01 [95% CI -0.03, +0.01]
- window_thread-window_nothread: -0.11 [95% CI -0.17, -0.05]
