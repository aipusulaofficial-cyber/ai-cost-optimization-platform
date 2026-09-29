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
