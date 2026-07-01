from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.config import settings
from app.evaluator import build_policy, evaluate_deployment
from app.metrics import (
    FREEZER_ACTIVE_CRITICAL_ALERTS,
    FREEZER_ACTIVE_WARNING_ALERTS,
    FREEZER_DEPLOYMENT_ALLOWED,
    FREEZER_ERROR_BUDGET_BURN_PERCENT,
    FREEZER_ERROR_RATE_PERCENT,
    FREEZER_EVALUATIONS_TOTAL,
    FREEZER_P95_LATENCY_MS,
)
from app.models import (
    DeploymentDecision,
    EvaluationResult,
    HealthResponse,
    MetricSnapshot,
)
from app.prometheus_client import PrometheusClient


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Error-budget-aware deployment freezer controller for FinGuard.",
)


@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "message": "FinGuard Deployment Freezer Controller is running",
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
        status="ready",
        version=settings.app_version,
        environment=settings.app_env,
    )


@app.get("/policy")
def policy():
    return build_policy()


@app.get("/decision", response_model=EvaluationResult)
async def decision():
    prometheus = PrometheusClient()

    try:
        snapshot = await prometheus.fetch_metric_snapshot()
        result = evaluate_deployment(snapshot)
    except Exception as exc:
        snapshot = MetricSnapshot()
        result = EvaluationResult(
            decision=DeploymentDecision.MANUAL_REVIEW_REQUIRED,
            allowed=False,
            reason=f"Could not evaluate Prometheus metrics. Manual review required. Error: {exc}",
            violated_rules=["Prometheus query failed"],
            metrics=snapshot,
            policy=build_policy(),
        )

    FREEZER_EVALUATIONS_TOTAL.labels(decision=result.decision.value).inc()
    FREEZER_DEPLOYMENT_ALLOWED.set(1 if result.allowed else 0)
    FREEZER_ERROR_RATE_PERCENT.set(result.metrics.error_rate_percent)
    FREEZER_P95_LATENCY_MS.set(result.metrics.p95_latency_ms)
    FREEZER_ERROR_BUDGET_BURN_PERCENT.set(result.metrics.error_budget_burn_percent)
    FREEZER_ACTIVE_CRITICAL_ALERTS.set(result.metrics.active_critical_alerts)
    FREEZER_ACTIVE_WARNING_ALERTS.set(result.metrics.active_warning_alerts)

    return result


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
