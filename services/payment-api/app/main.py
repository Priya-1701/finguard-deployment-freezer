import asyncio
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import create_db_and_tables, get_db
from app.metrics import (
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_TOTAL,
    PAYMENT_AMOUNT_TOTAL,
    PAYMENT_ERRORS_TOTAL,
    PAYMENT_REQUESTS_TOTAL,
    PAYMENT_STORE_SIZE,
)
from app.models import (
    DatabaseHealthResponse,
    HealthResponse,
    PaymentRequest,
    PaymentResponse,
    PaymentStatus,
    PaymentWithLedgerResponse,
)
from app.repository import (
    count_payments,
    create_payment_transaction,
    get_payment_by_id,
    get_payment_with_ledger,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FinTech-style payment API for FinGuard Deployment Freezer.",
    lifespan=lifespan,
)


@app.middleware("http")
async def collect_http_metrics(request: Request, call_next):
    """
    Middleware that records request count and request duration.

    This helps us later calculate error rate and latency SLOs.
    """
    start_time = time.perf_counter()
    path = request.url.path
    status_code = "500"

    try:
        response = await call_next(request)
        status_code = str(response.status_code)
        return response
    except Exception:
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
    return HealthResponse(
        service=settings.app_name,
        status="healthy",
        version=settings.app_version,
        environment=settings.app_env,
    )


@app.get("/ready", response_model=HealthResponse)
def ready():
    return HealthResponse(
        service=settings.app_name,
        status=settings.readiness_status,
        version=settings.app_version,
        environment=settings.app_env,
    )


@app.get("/db/health", response_model=DatabaseHealthResponse)
def database_health(db: Session = Depends(get_db)):
    """
    Confirms that the API can communicate with the database.
    """
    try:
        db.execute(text("SELECT 1"))
        return DatabaseHealthResponse(
            service=settings.app_name,
            database="postgresql" if "postgresql" in settings.database_url else "sqlite",
            status="healthy",
            details="Database connection successful",
        )
    except Exception as exc:
        PAYMENT_ERRORS_TOTAL.labels(error_type="database_health_check_failed").inc()
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {exc}",
        ) from exc


@app.post("/pay", response_model=PaymentWithLedgerResponse)
def create_payment(
    request: PaymentRequest,
    db: Session = Depends(get_db),
):
    """
    Simulates a fintech payment authorization.

    Phase 3 behavior:
    - Saves payment transaction in the database.
    - Creates ledger entries for approved payments.
    - Stores declined payment decision without ledger entries.
    """

    result = create_payment_transaction(
        db=db,
        request=request,
        max_single_payment_amount=settings.max_single_payment_amount,
    )

    PAYMENT_REQUESTS_TOTAL.labels(status=result.payment.status.value).inc()

    if result.payment.status == PaymentStatus.APPROVED:
        PAYMENT_AMOUNT_TOTAL.labels(currency=result.payment.currency).inc(result.payment.amount)

    PAYMENT_STORE_SIZE.set(count_payments(db))

    return result


@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: str,
    db: Session = Depends(get_db),
):
    payment = get_payment_by_id(db, payment_id)

    if payment is None:
        PAYMENT_ERRORS_TOTAL.labels(error_type="payment_not_found").inc()
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment


@app.get("/payments/{payment_id}/ledger", response_model=PaymentWithLedgerResponse)
def get_payment_ledger(
    payment_id: str,
    db: Session = Depends(get_db),
):
    result = get_payment_with_ledger(db, payment_id)

    if result is None:
        PAYMENT_ERRORS_TOTAL.labels(error_type="payment_not_found").inc()
        raise HTTPException(status_code=404, detail="Payment not found")

    return result


@app.get("/simulate/error")
def simulate_error():
    PAYMENT_ERRORS_TOTAL.labels(error_type="simulated_error").inc()
    raise HTTPException(status_code=500, detail="Simulated payment API failure")


@app.get("/simulate/latency")
async def simulate_latency(
    delay_ms: int = Query(default=1000, ge=0, le=10000),
):
    await asyncio.sleep(delay_ms / 1000)

    return {
        "message": "Simulated latency completed",
        "delay_ms": delay_ms,
    }


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
