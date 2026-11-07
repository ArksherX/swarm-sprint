"""Log-tampering matrix -> results/tamper.json plus a printed table."""
import json
from harness.tamper import matrix, SCHEMES, ATTACKS

m = matrix()
json.dump(m, open("results/tamper.json", "w"), indent=1)
cols = [(s, k) for s in SCHEMES for k in ([False, True] if s == "line_mac" else [False])]
name = lambda s, k: s + ("+key" if k else "")
print(f"{'attack':<20}" + "".join(f"{name(s, k):>14}" for s, k in cols))
for a in ATTACKS:
    print(f"{a:<20}" + "".join(f"{m[name(s, k) + '|' + a]['detect']:>14.2f}" for s, k in cols))
