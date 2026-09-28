from cost_domain import Price, Usage, attribute, cost, within_budget


def test_cost_calculation_and_budget():
    usage = Usage("tenant-a", "model-a", 1000, 500, 2.0)
    price = Price(0.01, 0.02, 0.005)
    amount = cost(usage, price)
    assert amount == 0.03
    assert within_budget(amount, 0.03) is True
    assert within_budget(amount, 0.02) is False


def test_cost_attribution_is_grouped_by_tenant():
    prices = {"model-a": Price(0.01, 0.02, 0.0)}
    usages = [Usage("a", "model-a", 1000, 0, 0), Usage("a", "model-a", 0, 500, 0)]
    assert attribute(usages, prices) == {"a": 0.02}
