# Phase 3 Interview Explanation

In Phase 3, I enhanced the FinGuard Payment API by replacing the temporary in-memory store with PostgreSQL-backed persistence.

I added SQLAlchemy as the ORM layer and created two core database tables: `payment_transactions` and `ledger_entries`.

The `payment_transactions` table stores the final payment decision, including approved and declined transactions. The `ledger_entries` table stores accounting-style records for approved payments. For each approved payment, the system creates a debit entry for the customer and a credit entry for the merchant. Declined payments are stored as decisions but do not create ledger movement records.

I also added a `/db/health` endpoint so the API can expose database connectivity status. This becomes important later for Kubernetes readiness, monitoring, alerting, and release-freezer decisions.

I updated Docker Compose so the local stack runs both the Payment API and PostgreSQL. This allows the project to behave more like a real fintech platform where service health and database health both matter.

This phase is important because deployment governance should not only look at whether the API process is running. It should also consider whether critical dependencies like the database are healthy.
