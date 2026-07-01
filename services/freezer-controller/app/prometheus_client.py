import math
from typing import Any
from typing import Optional

import httpx

from app.config import settings
from app.models import MetricSnapshot


class PrometheusQueryError(RuntimeError):
    pass


class PrometheusClient:
    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = (base_url or settings.prometheus_url).rstrip("/")

    async def query(self, promql: str) -> list[dict[str, Any]]:
        url = f"{self.base_url}/api/v1/query"

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params={"query": promql})
            response.raise_for_status()
            payload = response.json()

        if payload.get("status") != "success":
            raise PrometheusQueryError(f"Prometheus query failed: {payload}")

        return payload.get("data", {}).get("result", [])

    @staticmethod
    def first_value(results: list[dict[str, Any]], default: float = 0.0) -> float:
        if not results:
            return default

        try:
            raw_value = results[0]["value"][1]
            value = float(raw_value)

            if math.isnan(value) or math.isinf(value):
                return default

            return value
        except (KeyError, IndexError, TypeError, ValueError):
            return default

    async def fetch_metric_snapshot(self) -> MetricSnapshot:
        window = settings.query_window

        payment_api_up_query = 'max(up{namespace="finguard", job="payment-api"})'

        error_rate_query = f'''
        100 *
        sum(rate(finguard_http_requests_total{{namespace="finguard", status_code=~"5.."}}[{window}]))
        /
        clamp_min(sum(rate(finguard_http_requests_total{{namespace="finguard"}}[{window}])), 0.001)
        '''

        p95_latency_query = f'''
        1000 *
        histogram_quantile(
          0.95,
          sum(rate(finguard_http_request_duration_seconds_bucket{{namespace="finguard"}}[{window}])) by (le)
        )
        '''

        critical_alerts_query = 'ALERTS{alertstate="firing", service="payment-api", severity="critical"}'
        warning_alerts_query = 'ALERTS{alertstate="firing", service="payment-api", severity="warning"}'

        payment_api_up = self.first_value(await self.query(payment_api_up_query))
        error_rate_percent = self.first_value(await self.query(error_rate_query))
        p95_latency_ms = self.first_value(await self.query(p95_latency_query))

        critical_alerts = len(await self.query(critical_alerts_query))
        warning_alerts = len(await self.query(warning_alerts_query))

        allowed_error_rate_percent = max(
            100.0 - settings.slo_availability_target_percent,
            0.001,
        )

        error_budget_burn_percent = (
            error_rate_percent / allowed_error_rate_percent
        ) * 100.0

        return MetricSnapshot(
            payment_api_up=payment_api_up,
            error_rate_percent=round(error_rate_percent, 4),
            p95_latency_ms=round(p95_latency_ms, 2),
            active_critical_alerts=critical_alerts,
            active_warning_alerts=warning_alerts,
            error_budget_burn_percent=round(error_budget_burn_percent, 2),
            evaluation_window=window,
        )
