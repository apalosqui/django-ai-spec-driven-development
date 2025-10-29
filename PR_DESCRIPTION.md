# PR: Refactor to SOLID + Django-friendly Patterns

## Summary
Refactors code toward SOLID and pragmatic Design Patterns:
- Extracts reusable selectors per app (accounts, categories, transactions).
- Delegates CBVs to selectors (Template Method) for cleaner orchestration.
- Adds Excel util with openpyxl (optional extra) to support reading cached formula values.
- Centralizes dashboard totals and recent queries via selectors.
- Documents best practices (SOLID/Patterns) and Excel usage.

No functional behavior is intended to change, only structure and cohesion.

## Scope
- accounts: selectors + views using them
- categories: selectors + views using them
- transactions: selectors (filters, totals, recent) + views using them
- core: dashboard now uses selectors
- core/utils: excel util with ead_sheet_as_dicts
- docs: best-practices guide + readme extras (Excel and util usage)
- dependencies: optional equirements-excel.txt for openpyxl

## Rationale
- SRP: Views orchestrate; queries live in selectors; utilities isolated.
- OCP/LSP: CBVs extended via conventional hooks without breaking contracts.
- DIP: Views depend on simple abstractions (selectors) instead of raw queries.
- Testability: selectors/services are easy to test in isolation when tests arrive.

## How to test
- Accounts/Categories lists and CRUDs still load for the signed-in user.
- Transactions list filters (ccount, category, date_from, date_to, q) continue working.
- Dashboard totals/balance and recent transactions render as before.

## Notes
- openpyxl is optional: pip install -r requirements.txt -r requirements-excel.txt.
- ead_sheet_as_dicts returns cached formula results (data_only=True).

## Screenshots
N/A (no UI changes).