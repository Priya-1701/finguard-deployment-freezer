from datetime import datetime
from enum import Enum
from typing import Optional

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


class LedgerEntryResponse(BaseModel):
    ledger_entry_id: str
    payment_id: str
    entry_type: str
    account_ref: str
    amount: float
    currency: str
    created_at: datetime


class PaymentWithLedgerResponse(BaseModel):
    payment: PaymentResponse
    ledger_entries: list[LedgerEntryResponse]


class HealthResponse(BaseModel):
    service: str
    status: str
    version: str
    environment: str


class DatabaseHealthResponse(BaseModel):
    service: str
    database: str
    status: str
    details: str
