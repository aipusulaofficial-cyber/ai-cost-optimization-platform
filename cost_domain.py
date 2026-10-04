import math
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Usage:
    tenant: str
    model: str
    input_tokens: int
    output_tokens: int
    compute_seconds: float

    def __post_init__(self) -> None:
        if not self.tenant.strip() or not self.model.strip():
            raise ValueError("tenant and model are required")
        if (
            isinstance(self.input_tokens, bool)
            or not isinstance(self.input_tokens, int)
            or isinstance(self.output_tokens, bool)
            or not isinstance(self.output_tokens, int)
            or self.input_tokens < 0
            or self.output_tokens < 0
            or isinstance(self.compute_seconds, bool)
            or not isinstance(self.compute_seconds, (int, float))
            or not math.isfinite(self.compute_seconds)
            or self.compute_seconds < 0
        ):
            raise ValueError("usage must be finite and non-negative")


@dataclass(frozen=True)
class Price:
    input_per_1k: float
    output_per_1k: float
    compute_per_s: float

    def __post_init__(self) -> None:
        for value in (self.input_per_1k, self.output_per_1k, self.compute_per_s):
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or value < 0
            ):
                raise ValueError("pricing must be finite and non-negative")


def cost(u: Usage, p: Price) -> float:
    amount = (
        u.input_tokens * p.input_per_1k / 1000
        + u.output_tokens * p.output_per_1k / 1000
        + u.compute_seconds * p.compute_per_s
    )
    if not math.isfinite(amount):
        raise ValueError("cost must be finite")
    return round(amount, 6)


def attribute(usages: list[Usage], prices: dict[str, Price]) -> dict[str, float]:
    totals = defaultdict(float)
    for u in usages:
        totals[u.tenant] += cost(u, prices[u.model])
    return dict(totals)


def within_budget(amount: float, budget: float) -> bool:
    if (
        isinstance(amount, bool)
        or not isinstance(amount, (int, float))
        or not math.isfinite(amount)
        or isinstance(budget, bool)
        or not isinstance(budget, (int, float))
        or not math.isfinite(budget)
        or amount < 0
        or budget < 0
    ):
        raise ValueError("amount and budget must be finite and non-negative")
    return amount <= budget
