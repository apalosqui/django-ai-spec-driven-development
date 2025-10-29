# Plano de Sprints

Sprint 1 (1-2 semanas)
- Objetivos: modelos base + CRUD DRF para Accounts, SalaryRule, FixedExpense, VariableBudget, CreditCard, CardTransaction, Transfer.
- DoD: endpoints GET/POST/PUT/DELETE com permissions por owner; migrações e docs atualizadas.
- Riscos: definição de regras de datas (DD-MM-YYYY) e timezone.

Sprint 2 (1-2 semanas)
- Objetivos: invoice_builder (fechamento/baixa), CardInvoice endpoints.
- DoD: faturamento por período com fechamento e baixa no vencimento; testes básicos.

Sprint 3 (2 semanas)
- Objetivos: projection_engine (24+ meses, cache mensal), endpoint `/api/projection/`.
- DoD: série diária com eventos; performance aceitável com caching.

Sprint 4 (1-2 semanas)
- Objetivos: importador XLSX/CSV (openpyxl), export template, UI wizard.
- DoD: importar amostras da planilha-base com validação e logs.

Sprint 5 (1-2 semanas)
- Objetivos: UI calendário/timeline + tabela diária, alertas de risco.
- DoD: visual consistente com design system e colunas compatíveis com planilha.

