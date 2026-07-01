from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class DeploymentDecision(str, Enum):
    ALLOW_DEPLOYMENT = "ALLOW_DEPLOYMENT"
    FREEZE_DEPLOYMENT = "FREEZE_DEPLOYMENT"
    ROLLBACK_REQUIRED = "ROLLBACK_REQUIRED"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"


class FreezerPolicy(BaseModel):
    slo_availability_target_percent: float
    max_error_rate_percent: float
    max_p95_latency_ms: float
    max_error_budget_burn_percent: float
    manual_review_error_budget_burn_percent: float
    rollback_error_rate_percent: float
    rollback_p95_latency_ms: float
    max_critical_alerts: int
    max_warning_alerts: int


class MetricSnapshot(BaseModel):
    payment_api_up: float = 0
    error_rate_percent: float = 0
    p95_latency_ms: float = 0
    active_critical_alerts: int = 0
    active_warning_alerts: int = 0
    error_budget_burn_percent: float = 0
    evaluation_window: str = "5m"


class EvaluationResult(BaseModel):
    decision: DeploymentDecision
    allowed: bool
    reason: str
    violated_rules: list[str] = Field(default_factory=list)
    metrics: MetricSnapshot
    policy: FreezerPolicy
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HealthResponse(BaseModel):
    service: str
    status: str
    version: str
    environment: str
