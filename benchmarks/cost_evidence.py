import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cost_domain import Usage, Price, attribute, cost, within_budget

p = Price(0.01, 0.02, 0.1)
u = Usage("tenant-a", "model", 1000, 500, 2)
amount = cost(u, p)
totals = attribute([u], {"model": p})
report = {
    "cost": amount,
    "tenant_total": totals["tenant-a"],
    "within_0_05": within_budget(amount, 0.05),
    "within_0_1": within_budget(amount, 0.1),
}
if abs(report["cost"] - 0.22) > 1e-9 or abs(report["tenant_total"] - 0.22) > 1e-9:
    raise SystemExit(report)
if report["within_0_1"] or report["within_0_05"]:
    raise SystemExit(report)
print(json.dumps(report, sort_keys=True))
