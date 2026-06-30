import asyncio
import time

from fastapi import FastAPI, HTTPException, Query, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.config import settings
from app.metrics import (
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_TOTAL,
    PAYMENT_AMOUNT_TOTAL,
    PAYMENT_ERRORS_TOTAL,
    PAYMENT_REQUESTS_TOTAL,
    PAYMENT_STORE_SIZE,
)
from app.models import (
    HealthResponse,
    PaymentRequest,
    PaymentResponse,
    PaymentStatus,
    build_payment_response,
)
from app.store import payment_store

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FinTech-style payment API for FinGuard Deployment Freezer.",
)


@app.middleware("http")
async def collect_http_metrics(request: Request, call_next):
    """
    Middleware that records request count and request duration.

    This helps us later calculate error rate and latency SLOs.
    """
    start_time = time.perf_counter()
    path = request.url.path

    try:
        response = await call_next(request)
        status_code = str(response.status_code)
        return response
    except Exception:
        status_code = "500"
        PAYMENT_ERRORS_TOTAL.labels(error_type="unhandled_exception").inc()
        raise
    finally:
        duration = time.perf_counter() - start_time
        HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            path=path,
            status_code=status_code,
        ).inc()
        HTTP_REQUEST_DURATION_SECONDS.labels(
            method=request.method,
            path=path,
        ).observe(duration)


@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "message": "FinGuard Payment API is running",
    }


@app.get("/health", response_model=HealthResponse)
def health():
    """
    Liveness endpoint.

    Kubernetes will later use this to check whether the container is alive.
    """
    return HealthResponse(
        service=settings.app_name,
        status="healthy",
        version=settings.app_version,
        environment=settings.app_env,
    )


@app.get("/ready", response_model=HealthResponse)
def ready():
    """
    Readiness endpoint.

    Kubernetes will later use this to check whether the service is ready
    to receive traffic.
    """
    return HealthResponse(
        service=settings.app_name,
        status=settings.readiness_status,
        version=settings.app_version,
        environment=settings.app_env,
    )


@app.post("/pay", response_model=PaymentResponse)
def create_payment(request: PaymentRequest):
    """
    Simulates a fintech payment authorization.

    Current Phase 1 behavior:
    - Amount must be greater than zero.
    - Very large payments are declined.
    - Valid payments are approved and stored in memory.
    """

    if request.amount > settings.max_single_payment_amount:
        payment = build_payment_response(
            request=request,
            status=PaymentStatus.DECLINED,
            message="Payment declined because amount exceeds single payment limit",
        )
        payment_store.save(payment)
        PAYMENT_REQUESTS_TOTAL.labels(status=payment.status.value).inc()
        PAYMENT_STORE_SIZE.set(payment_store.count())
        return payment

    payment = build_payment_response(
        request=request,
        status=PaymentStatus.APPROVED,
        message="Payment approved",
    )

    payment_store.save(payment)

    PAYMENT_REQUESTS_TOTAL.labels(status=payment.status.value).inc()
    PAYMENT_AMOUNT_TOTAL.labels(currency=payment.currency).inc(payment.amount)
    PAYMENT_STORE_SIZE.set(payment_store.count())

    return payment


@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: str):
    payment = payment_store.get(payment_id)

    if payment is None:
        PAYMENT_ERRORS_TOTAL.labels(error_type="payment_not_found").inc()
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment


@app.get("/simulate/error")
def simulate_error():
    """
    Simulates a payment API failure.

    This will be used later to burn error budget and test deployment freeze logic.
    """
    PAYMENT_ERRORS_TOTAL.labels(error_type="simulated_error").inc()
    raise HTTPException(status_code=500, detail="Simulated payment API failure")


@app.get("/simulate/latency")
async def simulate_latency(
    delay_ms: int = Query(default=1000, ge=0, le=10000),
):
    """
    Simulates slow payment processing.

    This will be used later to test p95 latency alerts and canary rollback.
    """
    await asyncio.sleep(delay_ms / 1000)

    return {
        "message": "Simulated latency completed",
        "delay_ms": delay_ms,
    }


@app.get("/metrics")
def metrics():
    """
    Prometheus metrics endpoint.

    Prometheus will scrape this endpoint in a later phase.
    """
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
