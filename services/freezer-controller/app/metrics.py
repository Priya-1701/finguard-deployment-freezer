from prometheus_client import Counter, Gauge

FREEZER_EVALUATIONS_TOTAL = Counter(
    "finguard_freezer_evaluations_total",
    "Total deployment freezer evaluations by decision",
    ["decision"],
)

FREEZER_DEPLOYMENT_ALLOWED = Gauge(
    "finguard_freezer_deployment_allowed",
    "Whether deployment is currently allowed. 1 means allowed, 0 means blocked.",
)

FREEZER_ERROR_RATE_PERCENT = Gauge(
    "finguard_freezer_error_rate_percent",
    "Latest observed Payment API 5xx error rate percent.",
)

FREEZER_P95_LATENCY_MS = Gauge(
    "finguard_freezer_p95_latency_ms",
    "Latest observed Payment API p95 latency in milliseconds.",
)

FREEZER_ERROR_BUDGET_BURN_PERCENT = Gauge(
    "finguard_freezer_error_budget_burn_percent",
    "Latest approximate error budget burn percentage.",
)

FREEZER_ACTIVE_CRITICAL_ALERTS = Gauge(
    "finguard_freezer_active_critical_alerts",
    "Latest number of active critical alerts affecting Payment API.",
)

FREEZER_ACTIVE_WARNING_ALERTS = Gauge(
    "finguard_freezer_active_warning_alerts",
    "Latest number of active warning alerts affecting Payment API.",
)
