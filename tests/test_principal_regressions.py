import pytest

from pricing_store import PricingStore


@pytest.mark.parametrize("rate", [float("nan"), float("inf"), -1.0])
def test_invalid_rates_rejected(tmp_path, rate):
    store = PricingStore(tmp_path / "pricing.db")
    with pytest.raises(ValueError):
        store.put("provider", "model", rate, 0.1)


def test_valid_rate_persists(tmp_path):
    store = PricingStore(tmp_path / "pricing.db")
    store.put("provider", "model", 0.1, 0.2)
    assert store.get("provider", "model")[2:] == (0.1, 0.2)


def test_production_cost_domain_rejects_nonfinite_values():
    from cost_domain import Price, Usage, within_budget
    with pytest.raises(ValueError):
        Price(float("nan"), 0.0, 0.0)
    with pytest.raises(ValueError):
        Usage("tenant", "model", 1, 1, float("inf"))
    with pytest.raises(ValueError):
        within_budget(1.0, float("inf"))
