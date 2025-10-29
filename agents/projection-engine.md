# Agent: Projection Engine

Goal: Implement and maintain the daily balance projection for N months (default 24), honoring rules for salaries, fixed expenses, variable budgets, credit card invoices, and transfers.

Key responsibilities
- Compute daily projection given start date and horizon.
- Build card invoices per (card, yyyy_mm) based on closing day; apply on due dates.
- Cache by window (e.g., month) and invalidate incrementally.

Inputs
- Accounts (CAIXA/ECONOMIA) with opening balances.
- SalaryRule, FixedExpense, VariableBudget.
- CreditCard, CardTransaction; computed CardInvoice.
- Transfer (APLICACAO/RESGATE).

Algorithm outline
1) Initialize per-account balances from opening balances.
2) For each day d in [start, start + months]:
   - Add salaries (with business-day advance rule when configured).
   - Subtract fixed expenses due on d (advance if pay-early is set).
   - Subtract variable daily quota: sum(valor_mensal / dias_do_mes(d)).
   - Subtract invoices due on d (per card).
   - Apply transfers (APLICACAO negative on CAIXA, positive on ECONOMIA; RESGATE inverse).
   - Persist optional snapshot and emit events for UI.

API
- GET `/projection/?start=YYYY-MM-DD&months=24` → `[ { date, saldo, eventos: [...] } ]`

Testing focus
- Deterministic scenarios per month with fixtures.
- Edge cases: month length, weekends/holidays, multiple cards, multiple salaries.

