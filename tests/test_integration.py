from fastapi.testclient import TestClient
from service import app
def test_http_contract_and_domain():
 c=TestClient(app);assert c.get("/health/live").status_code==200
 r=c.post("/v1/cost",json={"key":"integration","payload":{"model":"m","tenant":"t","input_tokens":10,"output_tokens":5,"compute_seconds":1,"input_per_1k":1,"output_per_1k":1,"compute_per_s":1}});assert r.status_code==200,r.text
