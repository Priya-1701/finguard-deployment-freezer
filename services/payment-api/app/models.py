from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class PaymentStatus(str, Enum):
    APPROVED = "APPROVED"
    DECLINED = "DECLINED"


class PaymentRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Payment amount must be greater than zero")
    currency: str = Field(default="INR", min_length=3, max_length=3)
    merchant_id: str = Field(..., min_length=3)
    customer_id: str = Field(..., min_length=3)
    idempotency_key: Optional[str] = Field(default=None)


class PaymentResponse(BaseModel):
    payment_id: str
    status: PaymentStatus
    amount: float
    currency: str
    merchant_id: str
    customer_id: str
    message: str
    created_at: datetime


class HealthResponse(BaseModel):
    service: str
    status: str
    version: str
    environment: str


def build_payment_response(
    request: PaymentRequest,
    status: PaymentStatus,
    message: str,
) -> PaymentResponse:
    return PaymentResponse(
        payment_id=str(uuid4()),
        status=status,
        amount=request.amount,
        currency=request.currency.upper(),
        merchant_id=request.merchant_id,
        customer_id=request.customer_id,
        message=message,
        created_at=datetime.now(timezone.utc),
    )
