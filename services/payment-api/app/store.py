from typing import Dict, Optional

from app.models import PaymentResponse


class PaymentStore:
    """
    Simple in-memory payment store.

    For Phase 1, we are not using a database yet.
    This store keeps payments in memory while the application is running.
    Later, this can be replaced with PostgreSQL, DynamoDB, Redis, or another real datastore.
    """

    def __init__(self):
        self.payments: Dict[str, PaymentResponse] = {}

    def save(self, payment: PaymentResponse) -> PaymentResponse:
        """
        Save a payment response using payment_id as the key.
        """
        self.payments[payment.payment_id] = payment
        return payment

    def get(self, payment_id: str) -> Optional[PaymentResponse]:
        """
        Get a payment by payment_id.
        Returns None if the payment does not exist.
        """
        return self.payments.get(payment_id)

    def count(self) -> int:
        """
        Return total number of payments currently stored.
        """
        return len(self.payments)

    def clear(self) -> None:
        """
        Clear all payments from memory.
        Useful for tests.
        """
        self.payments.clear()


payment_store = PaymentStore()
