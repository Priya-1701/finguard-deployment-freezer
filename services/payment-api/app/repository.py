from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import LedgerEntry, PaymentTransaction
from app.models import (
    LedgerEntryResponse,
    PaymentRequest,
    PaymentResponse,
    PaymentStatus,
    PaymentWithLedgerResponse,
)


def _payment_to_response(payment: PaymentTransaction) -> PaymentResponse:
    return PaymentResponse(
        payment_id=payment.payment_id,
        status=PaymentStatus(payment.status),
        amount=payment.amount,
        currency=payment.currency,
        merchant_id=payment.merchant_id,
        customer_id=payment.customer_id,
        message=payment.message,
        created_at=payment.created_at,
    )


def _ledger_to_response(entry: LedgerEntry) -> LedgerEntryResponse:
    return LedgerEntryResponse(
        ledger_entry_id=entry.ledger_entry_id,
        payment_id=entry.payment_id,
        entry_type=entry.entry_type,
        account_ref=entry.account_ref,
        amount=entry.amount,
        currency=entry.currency,
        created_at=entry.created_at,
    )


def create_payment_transaction(
    db: Session,
    request: PaymentRequest,
    max_single_payment_amount: float,
) -> PaymentWithLedgerResponse:
    currency = request.currency.upper()

    if request.amount > max_single_payment_amount:
        payment = PaymentTransaction(
            status=PaymentStatus.DECLINED.value,
            amount=request.amount,
            currency=currency,
            merchant_id=request.merchant_id,
            customer_id=request.customer_id,
            idempotency_key=request.idempotency_key,
            message="Payment declined because amount exceeds single payment limit",
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return PaymentWithLedgerResponse(
            payment=_payment_to_response(payment),
            ledger_entries=[],
        )

    payment = PaymentTransaction(
        status=PaymentStatus.APPROVED.value,
        amount=request.amount,
        currency=currency,
        merchant_id=request.merchant_id,
        customer_id=request.customer_id,
        idempotency_key=request.idempotency_key,
        message="Payment approved",
    )

    db.add(payment)
    db.flush()

    debit_customer = LedgerEntry(
        payment_id=payment.payment_id,
        entry_type="DEBIT_CUSTOMER",
        account_ref=request.customer_id,
        amount=request.amount,
        currency=currency,
    )

    credit_merchant = LedgerEntry(
        payment_id=payment.payment_id,
        entry_type="CREDIT_MERCHANT",
        account_ref=request.merchant_id,
        amount=request.amount,
        currency=currency,
    )

    db.add_all([debit_customer, credit_merchant])
    db.commit()

    db.refresh(payment)
    db.refresh(debit_customer)
    db.refresh(credit_merchant)

    return PaymentWithLedgerResponse(
        payment=_payment_to_response(payment),
        ledger_entries=[
            _ledger_to_response(debit_customer),
            _ledger_to_response(credit_merchant),
        ],
    )


def get_payment_by_id(db: Session, payment_id: str) -> Optional[PaymentResponse]:
    payment = db.get(PaymentTransaction, payment_id)

    if payment is None:
        return None

    return _payment_to_response(payment)


def get_payment_with_ledger(
    db: Session,
    payment_id: str,
) -> Optional[PaymentWithLedgerResponse]:
    payment = db.get(PaymentTransaction, payment_id)

    if payment is None:
        return None

    ledger_entries = db.scalars(
        select(LedgerEntry).where(LedgerEntry.payment_id == payment_id)
    ).all()

    return PaymentWithLedgerResponse(
        payment=_payment_to_response(payment),
        ledger_entries=[_ledger_to_response(entry) for entry in ledger_entries],
    )


def count_payments(db: Session) -> int:
    return len(db.scalars(select(PaymentTransaction)).all())
