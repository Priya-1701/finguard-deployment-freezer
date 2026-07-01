from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings for the payment API.

    Phase 3 adds DATABASE_URL so the API can persist payments
    and ledger entries in PostgreSQL.
    """

    app_name: str = "FinGuard Payment API"
    app_version: str = "1.2.0-risky"
    app_env: str = "local"

    max_single_payment_amount: float = 100000.00
    readiness_status: str = "ready"

    database_url: str = "sqlite:///./payment_api_local.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
