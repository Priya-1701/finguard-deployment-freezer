from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings for the payment API.

    These values can be overridden later using environment variables.
    For Phase 1, defaults are enough for local development.
    """

    app_name: str = "FinGuard Payment API"
    app_version: str = "1.0.0"
    app_env: str = "local"

    max_single_payment_amount: float = 100000.00
    readiness_status: str = "ready"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
