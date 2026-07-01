from app.evaluator import evaluate_deployment
from app.models import DeploymentDecision, FreezerPolicy, MetricSnapshot


policy = FreezerPolicy(
    slo_availability_target_percent=99.9,
    max_error_rate_percent=1.0,
    max_p95_latency_ms=500.0,
    max_error_budget_burn_percent=100.0,
    manual_review_error_budget_burn_percent=80.0,
    rollback_error_rate_percent=10.0,
    rollback_p95_latency_ms=2000.0,
    max_critical_alerts=0,
    max_warning_alerts=2,
)


def test_allows_deployment_when_metrics_are_healthy():
    metrics = MetricSnapshot(
        payment_api_up=1,
        error_rate_percent=0.0,
        p95_latency_ms=120,
        active_critical_alerts=0,
        active_warning_alerts=0,
        error_budget_burn_percent=10,
    )

    result = evaluate_deployment(metrics, policy)

    assert result.decision == DeploymentDecision.ALLOW_DEPLOYMENT
    assert result.allowed is True


def test_requires_manual_review_when_error_budget_burn_is_high():
    metrics = MetricSnapshot(
        payment_api_up=1,
        error_rate_percent=0.05,
        p95_latency_ms=120,
        active_critical_alerts=0,
        active_warning_alerts=0,
        error_budget_burn_percent=85,
    )

    result = evaluate_deployment(metrics, policy)

    assert result.decision == DeploymentDecision.MANUAL_REVIEW_REQUIRED
    assert result.allowed is False


def test_freezes_deployment_when_error_rate_is_high():
    metrics = MetricSnapshot(
        payment_api_up=1,
        error_rate_percent=2.0,
        p95_latency_ms=120,
        active_critical_alerts=0,
        active_warning_alerts=0,
        error_budget_burn_percent=40,
    )

    result = evaluate_deployment(metrics, policy)

    assert result.decision == DeploymentDecision.FREEZE_DEPLOYMENT
    assert result.allowed is False


def test_freezes_deployment_when_latency_is_high():
    metrics = MetricSnapshot(
        payment_api_up=1,
        error_rate_percent=0.0,
        p95_latency_ms=800,
        active_critical_alerts=0,
        active_warning_alerts=0,
        error_budget_burn_percent=20,
    )

    result = evaluate_deployment(metrics, policy)

    assert result.decision == DeploymentDecision.FREEZE_DEPLOYMENT
    assert result.allowed is False


def test_requires_rollback_when_payment_api_is_down():
    metrics = MetricSnapshot(
        payment_api_up=0,
        error_rate_percent=0.0,
        p95_latency_ms=120,
        active_critical_alerts=0,
        active_warning_alerts=0,
        error_budget_burn_percent=0,
    )

    result = evaluate_deployment(metrics, policy)

    assert result.decision == DeploymentDecision.ROLLBACK_REQUIRED
    assert result.allowed is False


def test_requires_rollback_when_critical_alert_is_firing():
    metrics = MetricSnapshot(
        payment_api_up=1,
        error_rate_percent=0.0,
        p95_latency_ms=120,
        active_critical_alerts=1,
        active_warning_alerts=0,
        error_budget_burn_percent=0,
    )

    result = evaluate_deployment(metrics, policy)

    assert result.decision == DeploymentDecision.ROLLBACK_REQUIRED
    assert result.allowed is False
