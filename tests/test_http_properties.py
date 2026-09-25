from hypothesis import given,strategies as st
from fastapi.testclient import TestClient
from service import app
c=TestClient(app)
def test_contract(): assert c.get("/health/live").status_code==200
@given(st.text(min_size=1,max_size=32))
def test_property(v):
 assert c.post("/v1/cost",json={"key":v,"payload":{"model":"m","tenant":"t","input_tokens":1,"output_tokens":1,"compute_seconds":1,"input_per_1k":1,"output_per_1k":1,"compute_per_s":1}}).status_code==200
