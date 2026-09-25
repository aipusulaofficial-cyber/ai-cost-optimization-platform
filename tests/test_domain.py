from cost_domain import *
def test_cost():
 u=Usage("t","m",1000,500,2);p=Price(1,2,.5);assert cost(u,p)==3