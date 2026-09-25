from fastapi import FastAPI, HTTPException
from fastapi import Request as FastAPIRequest
from opentelemetry import trace
from pydantic import BaseModel, Field

from cost_domain import Price, Usage, cost, within_budget

try:
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    provider = TracerProvider(
        resource=Resource.create({"service.name": "ai-cost-optimization-platform"})
    )
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
except (ImportError, RuntimeError) as exc:
    import logging
    logging.getLogger(__name__).warning("OpenTelemetry setup unavailable: %s", exc)

app = FastAPI(title="ai-cost-optimization-platform", version="1.0.0")
tracer = trace.get_tracer("ai-cost-optimization-platform")


@app.middleware("http")
async def observability_headers(request: FastAPIRequest, call_next):
    import time
    import uuid
    started = time.perf_counter()
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    correlation_id = request.headers.get("x-correlation-id") or request_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    response.headers["x-correlation-id"] = correlation_id
    response.headers["x-latency-ms"] = f"{(time.perf_counter() - started) * 1000:.3f}"
    return response


class Request(BaseModel):
    key: str
    payload: dict = Field(default_factory=dict)


@app.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/v1/cost")
def handle(r: Request) -> dict[str, float | str | bool]:
    with tracer.start_as_current_span("ai-cost-optimization-platform.domain"):
        try:
            usage = Usage(
                r.payload.get("tenant", r.key),
                r.payload.get("model", "default"),
                int(r.payload.get("input_tokens", 0)),
                int(r.payload.get("output_tokens", 0)),
                float(r.payload.get("compute_seconds", 0)),
            )
            price = Price(
                float(r.payload.get("input_per_1k", 0)),
                float(r.payload.get("output_per_1k", 0)),
                float(r.payload.get("compute_per_s", 0)),
            )
            amount = cost(usage, price)
            return {
                "tenant": usage.tenant,
                "cost": amount,
                "within_budget": within_budget(
                    amount,
                    float(r.payload.get("budget", float("inf"))),
                ),
            }
        except (ValueError, KeyError, RuntimeError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
