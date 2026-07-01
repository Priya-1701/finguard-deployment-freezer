from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FinGuard Deployment Freezer Controller"
    app_version: str = "1.0.0"
    app_env: str = "local"

    prometheus_url: str = "http://127.0.0.1:9090"
    query_window: str = "5m"

    slo_availability_target_percent: float = 99.9

    max_error_rate_percent: float = 1.0
    max_p95_latency_ms: float = 500.0
    max_error_budget_burn_percent: float = 100.0

    manual_review_error_budget_burn_percent: float = 80.0

    rollback_error_rate_percent: float = 10.0
    rollback_p95_latency_ms: float = 2000.0

    max_critical_alerts: int = 0
    max_warning_alerts: int = 2

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
