from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from opentelemetry import trace
from cost_domain import *
try:
 from opentelemetry.sdk.resources import Resource
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
 p=TracerProvider(resource=Resource.create({"service.name":"ai-cost-optimization-platform"}));p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()));trace.set_tracer_provider(p)
except Exception: pass
app=FastAPI(title="ai-cost-optimization-platform",version="1.0.0");tracer=trace.get_tracer("ai-cost-optimization-platform")
class Request(BaseModel): key:str; payload:dict={}
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/cost")
def handle(r:Request):
 with tracer.start_as_current_span("ai-cost-optimization-platform.domain"):
  try: u=Usage(r.payload.get("tenant",r.key),r.payload.get("model","default"),int(r.payload.get("input_tokens",0)),int(r.payload.get("output_tokens",0)),float(r.payload.get("compute_seconds",0)));p=Price(float(r.payload.get("input_per_1k",0)),float(r.payload.get("output_per_1k",0)),float(r.payload.get("compute_per_s",0)));amount=cost(u,p);return {"tenant":u.tenant,"cost":amount,"within_budget":within_budget(amount,float(r.payload.get("budget",float("inf"))))}
  except (ValueError,KeyError,RuntimeError) as e: raise HTTPException(status_code=400,detail=str(e)) from e
