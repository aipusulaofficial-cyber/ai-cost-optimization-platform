from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True)
class Usage:
    tenant:str; model:str; input_tokens:int; output_tokens:int; compute_seconds:float

@dataclass(frozen=True)
class Price:
    input_per_1k:float; output_per_1k:float; compute_per_s:float

def cost(u:Usage,p:Price)->float:
    if min(u.input_tokens,u.output_tokens)<0 or u.compute_seconds<0:raise ValueError("negative usage")
    return round(u.input_tokens*p.input_per_1k/1000+u.output_tokens*p.output_per_1k/1000+u.compute_seconds*p.compute_per_s,6)

def attribute(usages:list[Usage],prices:dict[str,Price])->dict[str,float]:
    totals=defaultdict(float)
    for u in usages:totals[u.tenant]+=cost(u,prices[u.model])
    return dict(totals)

def within_budget(amount:float,budget:float)->bool:return amount<=budget
