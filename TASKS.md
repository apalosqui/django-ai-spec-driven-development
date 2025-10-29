# TASKS — Sprints & Backlog Breakdown

Observação: este arquivo consolida o plano de sprints (antes em `docs/sprint-plan.md`) em tarefas acionáveis.

- [x] Models: `Account`, `SalaryRule`, `FixedExpense`, `VariableBudget`, `CreditCard`, `CardTransaction`, `Transfer`, `CardInvoice`, `ProjectionSnapshot`, `TransactionLog`
- [x] Migrações criadas e aplicadas
- [x] DRF: Serializers + ViewSets para todos os modelos acima (CRUD)
- [x] Permissions por owner em todos os endpoints
- [x] URLs/routers conectados sob `/api/`
- [x] Admin básico registrado para os modelos
- [x] Docs atualizadas (README rotas + PRD/API)
- Aceite: endpoints GET/POST/PUT/DELETE funcionam isolando dados por usuário

## Sprint 2 (1–2 semanas)
- [x] Service `invoice_builder`: fechamento por (cartão, yyyy_mm) com base em `dia_fechamento`
- [x] Cálculo e persistência de `CardInvoice.total_calculado`
- [x] Endpoints: GET `/api/card-invoices/compute?yyyy_mm=&card_id=`, POST `/api/card-invoices/rebuild`
- [ ] Testes básicos do fluxo de fatura (feliz + borda)
- [x] Docs atualizadas (seção faturas)
- Aceite: faturas geradas corretamente e baixa aplicada na data correta

## Sprint 3 (2 semanas)
- [x] Service `projection_engine`: projeção diária 24+ meses (configurável)
- [x] Cache diário com `ProjectionSnapshot` (base para cache mensal)
- [x] Endpoint GET `/api/projection/?start=YYYY-MM-DD&months=24`
- [x] Baixa no vencimento: debitar conta de pagamento em `data_vencimento` (via faturas na projeção)
- [ ] Considerar: salários, fixos, variável/dia, faturas, transferências; timezone `America/Sao_Paulo`
- [ ] Performance aceitável em dados de exemplo; memoization onde útil
- [ ] Docs/algoritmo atualizados
- Aceite: série diária coerente e com eventos do dia

## Sprint 4 (1–2 semanas)
- [ ] Export template CSV e endpoint GET `/api/export.csv`
- [ ] Relatório CSV consolidado por período (cliente)
- [ ] Docs (guia de exportação) e exemplos
- Aceite: exporta relatório CSV válido e coerente

## Sprint 5 (1–2 semanas)
- [ ] UI calendário/timeline com ícones (salário, fixo, variável, fatura, aplicação/resgate)
- [ ] Tabela diária compatível com planilha: Data, Entrada, Saída, Diário, Saldo
- [ ] Indicadores de risco (saldo futuro negativo)
- [ ] Alinhamento com design system; acessibilidade básica
- [ ] Docs (prints e instruções)
- Aceite: visual consistente e informativo para próximos 30 dias
