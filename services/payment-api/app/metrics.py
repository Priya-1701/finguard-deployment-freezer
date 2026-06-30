from prometheus_client import Counter, Gauge, Histogram

HTTP_REQUESTS_TOTAL = Counter(
    "finguard_http_requests_total",
    "Total HTTP requests received by the payment API",
    ["method", "path", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "finguard_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)

PAYMENT_REQUESTS_TOTAL = Counter(
    "finguard_payment_requests_total",
    "Total payment requests processed by status",
    ["status"],
)

PAYMENT_AMOUNT_TOTAL = Counter(
    "finguard_payment_amount_total",
    "Total approved payment amount by currency",
    ["currency"],
)

PAYMENT_ERRORS_TOTAL = Counter(
    "finguard_payment_errors_total",
    "Total simulated or real payment API errors",
    ["error_type"],
)

PAYMENT_STORE_SIZE = Gauge(
    "finguard_payment_store_size",
    "Number of payments currently stored in memory",
)
