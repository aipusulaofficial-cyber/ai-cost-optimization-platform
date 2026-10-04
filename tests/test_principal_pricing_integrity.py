import math

import pytest

from pricing_store import PricingStore


@pytest.mark.parametrize("price", [math.nan, math.inf, -math.inf, -0.01, "1", True])
def test_rejects_invalid_price(tmp_path, price):
    store = PricingStore(tmp_path / "pricing.db")
    with pytest.raises(ValueError):
        store.put("provider", "model", price, 1.0)


def test_rejects_blank_identity(tmp_path):
    store = PricingStore(tmp_path / "pricing.db")
    with pytest.raises(ValueError):
        store.put("", "model", 0.5, 0.5)
    with pytest.raises(ValueError):
        store.put("provider", "", 0.5, 0.5)
