"""AI FinOps core: usage normalization, cost attribution and budget enforcement."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Usage: service:str; tokens_in:int; tokens_out:int; rate_in:float; rate_out:float; tenant:str
def cost(u):
 if min(u.tokens_in,u.tokens_out,u.rate_in,u.rate_out)<0:raise ValueError("negative usage");return u.tokens_in*u.rate_in+u.tokens_out*u.rate_out
class Budget:
 def __init__(self,limit):self.limit=limit;self.spent={}
 def charge(self,u):
  n=self.spent.get(u.tenant,0)+cost(u)
  if n>self.limit:raise RuntimeError("budget exceeded")
  self.spent[u.tenant]=n;return n
