# Roadmap (Pivot DRF + Projeção)

Fase 0 — Pivot e alinhamento (concluída)
- Atualizar PRD, AGENTS e README; criar agentes (projection-engine, import-mapper, PM).
- Confirmar estrutura da planilha base (XLSX) e alinhar UI com Data/Entrada/Saída/Diário/Saldo.

Fase 1 — Fundamentos do domínio (Sprint 1–2)
- Modelos: Account, SalaryRule, FixedExpense, VariableBudget, CreditCard, CardTransaction, CardInvoice, Transfer, ProjectionSnapshot, TransactionLog.
- Serializers/ViewSets básicos (CRUD) com permissions por owner.

Fase 2 — Projeção e faturas (Sprint 3–4)
- Service projection_engine (cálculo diário 24+ meses, cache mensal, timezone BR).
- Service invoice_builder (fechamento por ciclo e baixa no vencimento).
- Endpoint `/api/projection/`.

Fase 3 — Importação e UX (Sprint 5–6)
- Importador XLSX/CSV (wizard + openpyxl), export template.
- UI: calendário/timeline, tabela diária, indicadores de risco.

Fase 4 — Performance e qualidade (Sprint 7)
- Cache incremental e invalidação dirigida.
- Seeds/fixtures, smoke tests, documentação de API.

