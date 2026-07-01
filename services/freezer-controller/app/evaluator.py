from app.config import settings
from typing import Optional
from app.models import (
    DeploymentDecision,
    EvaluationResult,
    FreezerPolicy,
    MetricSnapshot,
)


def build_policy() -> FreezerPolicy:
    return FreezerPolicy(
        slo_availability_target_percent=settings.slo_availability_target_percent,
        max_error_rate_percent=settings.max_error_rate_percent,
        max_p95_latency_ms=settings.max_p95_latency_ms,
        max_error_budget_burn_percent=settings.max_error_budget_burn_percent,
        manual_review_error_budget_burn_percent=settings.manual_review_error_budget_burn_percent,
        rollback_error_rate_percent=settings.rollback_error_rate_percent,
        rollback_p95_latency_ms=settings.rollback_p95_latency_ms,
        max_critical_alerts=settings.max_critical_alerts,
        max_warning_alerts=settings.max_warning_alerts,
    )


def evaluate_deployment(
    metrics: MetricSnapshot,
    policy: Optional[FreezerPolicy] = None,
) -> EvaluationResult:
    policy = policy or build_policy()
    violated_rules: list[str] = []

    if metrics.payment_api_up < 1:
        violated_rules.append("Payment API target is down")

    if metrics.active_critical_alerts > policy.max_critical_alerts:
        violated_rules.append("Critical alerts are firing")

    if metrics.error_rate_percent >= policy.rollback_error_rate_percent:
        violated_rules.append("Error rate crossed rollback threshold")

    if metrics.p95_latency_ms >= policy.rollback_p95_latency_ms:
        violated_rules.append("p95 latency crossed rollback threshold")

    if violated_rules:
        return EvaluationResult(
            decision=DeploymentDecision.ROLLBACK_REQUIRED,
            allowed=False,
            reason="Severe reliability risk detected. Rollback is recommended.",
            violated_rules=violated_rules,
            metrics=metrics,
            policy=policy,
        )

    if metrics.error_rate_percent > policy.max_error_rate_percent:
        violated_rules.append("Error rate crossed deployment freeze threshold")

    if metrics.p95_latency_ms > policy.max_p95_latency_ms:
        violated_rules.append("p95 latency crossed deployment freeze threshold")

    if metrics.error_budget_burn_percent >= policy.max_error_budget_burn_percent:
        violated_rules.append("Error budget exhausted")

    if metrics.active_warning_alerts > policy.max_warning_alerts:
        violated_rules.append("Too many warning alerts are firing")

    if violated_rules:
        return EvaluationResult(
            decision=DeploymentDecision.FREEZE_DEPLOYMENT,
            allowed=False,
            reason="Deployment freeze required because reliability policy is violated.",
            violated_rules=violated_rules,
            metrics=metrics,
            policy=policy,
        )

    if metrics.error_budget_burn_percent >= policy.manual_review_error_budget_burn_percent:
        return EvaluationResult(
            decision=DeploymentDecision.MANUAL_REVIEW_REQUIRED,
            allowed=False,
            reason="Error budget burn is high. Manual approval is required before deployment.",
            violated_rules=["Error budget burn crossed manual review threshold"],
            metrics=metrics,
            policy=policy,
        )

    return EvaluationResult(
        decision=DeploymentDecision.ALLOW_DEPLOYMENT,
        allowed=True,
        reason="All reliability checks are within policy. Deployment is allowed.",
        violated_rules=[],
        metrics=metrics,
        policy=policy,
    )
