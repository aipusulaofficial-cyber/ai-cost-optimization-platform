from cost_platform import *
import pytest
def test_cost_and_attribution():
 b=Budget(1);assert b.charge(Usage("llm",100,50,.001,.002,"team-a"))==.2
def test_budget_enforced():
 b=Budget(.1)
 with pytest.raises(RuntimeError):b.charge(Usage("llm",100,0,.002,0,"a"))
def test_negative_usage():
 with pytest.raises(ValueError):cost(Usage("x",-1,0,1,1,"a"))
