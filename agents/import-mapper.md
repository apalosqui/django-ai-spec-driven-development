# Agent: Import Mapper (XLSX/CSV)

Goal: Assist importing data from the user spreadsheet into models using openpyxl (XLSX) or CSV.

Responsibilities
- Inspect workbook sheets and headers.
- Map columns to models: Accounts, SalaryRule, FixedExpense, VariableBudget, CreditCard, CardTransaction, Transfer.
- Validate rows; report and skip invalid entries.

Implementation notes
- Use `openpyxl` (optional extra installed via `requirements-excel.txt`).
- Fallback: CSV import for users who export sheets.
- Wizard UI: step to select sheet, step to map columns, step to preview, step to import.

API endpoints
- POST `/import` (multipart) with options `{ sheet, mappings, type }`.
- GET `/export.csv` for a basic export template.

Testing focus
- Header variations, missing optional columns, date formats (DD-MM-YYYY), BRL values.

