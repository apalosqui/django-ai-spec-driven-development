# PR: Dashboard monthly carry-over + MVP projection

## Summary
- Compute projection from a safe base period to ensure carry-over into the selected month.
- Cards show only the month aggregate; table shows the accumulated daily balance (with carry-over).
- Add deterministic seed and checker to validate carry-over math.
- Rename card label to Performance (Receitas - Despesas do mês).

## Details
- core/views.py
  - Define base_start (start-of-year or previous year if January) and months_span for cards.
  - Define prev_first_day (first day of previous month) for the table request (months=2).
  - Compute monthly income/expense/performance and the month-end balance from projection.
- templates/dashboard.html
  - Selector for month/year (GET + apply).
  - Box: Resumo financeiro do mês (Receitas, Despesas, Performance).
  - MVP table auto-loads projection from prev_first_day (months=2) and filters to the month.
- planning/services.py (prior work): separates Saída (fixos/faturas) vs Diário (variável/dia) with positive values only.
- users/management/commands
  - seed_carry_demo: 2000 salary, 500 fixed (25), 500 variable, start at 2025-01-15.
  - check_carryover: print end-of-month saldo and delta to verify +1000 monthly.
- TASKS.md: add pending task to ensure carry-over display in table is consistent.
- PROJECT_STATUS.md: note outstanding task and rename of card.

## How to validate
- python manage.py seed_carry_demo
- python manage.py check_carryover --email carry@demo.com --start 2025-01-01 --months 12
- Login carry@demo.com / demo12345, navigate to /dashboard, select months and verify:
  - Cards reflect only the selected month.
  - Table shows daily balances with carry-over (day 01 carries previous month end).

## Notes
- If the client has no prior data (onboarding), carry-over is zero.
