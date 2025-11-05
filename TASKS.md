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
- [x] Horizonte por mês completo (fim no último dia do mês alvo)
- [x] Janeiro: não somar dezembro inexistente (carry-over seguro)
- [x] Onboarding: dias anteriores ao onboarding sem valores (respeita D0)
- [x] Considerar: salários, fixos, variável/dia, faturas, transferências; timezone `America/Sao_Paulo`
- [ ] Performance aceitável em dados de exemplo; memoization onde útil
- [ ] Docs/algoritmo atualizados
- Aceite: série diária coerente e com eventos do dia

## Sprint 4 (1–2 semanas)
- [x] Atualizar landing/home para MVP (pivot DRF + projeção)
- [x] Incluir CTA e seção de demonstração da projeção (GET `/api/projection/`)
- [x] Texto e visual alinhados ao PRD (pt-BR, BRL, datas DD-MM-YYYY)
- [x] Aceite: home comunica valor e permite testar projeção (se logado)

## Sprint 5 (1–2 semanas)
- [x] Export template CSV e endpoint GET `/api/export.csv`
- [x] Relatório CSV consolidado por período (cliente)
- [ ] Docs (guia de exportação) e exemplos
- Aceite: exporta relatório CSV válido e coerente

## Sprint 6 (1–2 semanas)
- [x] Tabela diária compatível com planilha: Data, Entrada, Saída, Diário, Saldo
- [x] Indicadores de risco (saldo futuro negativo)
- [x] Alinhamento com design system; acessibilidade básica
- [ ] Docs (prints e instruções)
- Aceite: visual consistente e informativo para próximos 30 dias

## Ajustes pendentes
- [x] Projeção (MVP): garantir carry-over exibido na tabela do mês (saldo no dia 01 deve herdar saldo do último dia do mês anterior; onboarding = zero).

### Novos itens
- [ ] Onboarding: garantir que D0/saldo inicial, SalaryRule, FixedExpenses e VariableBudget reflitam imediatamente no dashboard (sessão + endpoint; validação visual).
- [ ] Resumo do mês: revisar agregação dos cards (Receitas, Despesas, Performance) após onboarding e eventos; padronizar formatação BRL e precisão.
- [ ] Dashboard (UX): reposicionar botão “Adicionar evento” para junto da tabela e melhorar UX do modal (atalhos de tipo, validação, mensagens, loading e retorno de sucesso).

## Sprint 7 — Polish, Cleanup & Testing Foundation (1–2 semanas)
**Objetivo**: Estabilizar funcionalidades atuais, limpar débito técnico, baseline de testes

### Tarefas
- [ ] Code cleanup
  - [ ] Remove unused imports (core/views.py: Sum, tx_selectors, Transaction)
  - [ ] Remove unused variable prev_end_balance
  - [ ] Fix Pylance warnings
- [ ] Merge onboarding work
  - [ ] Commit current changes on feat/pivot-prd-agents-readme
  - [ ] Review and merge to main
- [ ] Testing infrastructure
  - [ ] Setup pytest + pytest-django
  - [ ] Test: projection carry-over between months
  - [ ] Test: invoice calculation edge cases
  - [ ] Test: user isolation (no data leakage)
  - [ ] Test: onboarding seeds validation
  - [ ] Test: January without December (edge case)
- [ ] Documentation
  - [ ] Document projection algorithm in PRD (detailed pseudocode)
  - [ ] Document onboarding flow in README
  - [ ] Document `?onboarding=` parameter behavior
  - [ ] Add algorithm examples to PRD
- [ ] Performance baseline
  - [ ] Measure projection time for 24 months with typical data
  - [ ] Log baseline metrics for Sprint 9 comparison
- [ ] UTF-8 validation
  - [ ] Check all templates for encoding consistency
  - [ ] Fix any remaining mojibake

**Aceite**: Warnings resolvidos, branch mergeado, ≥5 testes passando, algoritmo documentado, baseline registrado

---

## Sprint 8 — XLSX/CSV Import Wizard (2 semanas)
**Objetivo**: Implementar o import mapper (PRD RF alta prioridade)

### Tarefas
- [ ] Backend: importer app
  - [ ] Create `importer/` Django app
  - [ ] Service: `import_mapper.py` with parse_xlsx(), parse_csv(), validate_mapping()
  - [ ] Model: `ImportSession` (track upload state)
  - [ ] API endpoints:
    - [ ] `POST /api/import/upload/` → preview
    - [ ] `POST /api/import/confirm/` → persist
- [ ] Frontend: wizard UI
  - [ ] Step 1: Upload file (XLSX/CSV)
  - [ ] Step 2: Map columns (dropdown matching)
  - [ ] Step 3: Preview & confirm (show what will be created)
  - [ ] Template: `templates/importer/wizard.html`
  - [ ] Smart column detection (name similarity matching)
- [ ] Validation & error handling
  - [ ] Required fields validation
  - [ ] Date format validation (DD-MM-YYYY, YYYY-MM-DD)
  - [ ] Amount validation (numeric, positive where required)
  - [ ] Duplicate detection
  - [ ] Error messages in pt-BR
- [ ] Template download
  - [ ] CSV template with example data
  - [ ] Download link on wizard page
- [ ] Testing
  - [ ] Test: happy path (valid file imports correctly)
  - [ ] Test: validation errors (malformed file)
  - [ ] Test: column mapping edge cases
  - [ ] Test: large file handling (1000+ rows)
- [ ] Documentation
  - [ ] User guide: how to prepare import file
  - [ ] API documentation for import endpoints

**Aceite**: Wizard funcional, upload → map → confirm, entidades criadas corretamente, template disponível, testes cobrem happy path + erros

---

## Sprint 9 — Performance Optimization & Cache Strategy (1–2 semanas)
**Objetivo**: Implementar cache incremental para escalar com datasets grandes

### Tarefas
- [ ] ProjectionSnapshot caching
  - [ ] Design cache schema (monthly aggregations)
  - [ ] Implement cache write (after projection calculation)
  - [ ] Implement cache read (check before calculation)
  - [ ] Invalidation logic (detect affected months)
  - [ ] Selective recalculation (only dirty months)
- [ ] Cache management API
  - [ ] `POST /api/projection/invalidate/?start=YYYY-MM&end=YYYY-MM`
  - [ ] `GET /api/projection/cache-status/` (diagnostics: hit/miss rates)
- [ ] Projection engine optimization
  - [ ] Memoize daily variable calculations
  - [ ] Batch query all entities at start (avoid N+1)
  - [ ] Profile with django-debug-toolbar
  - [ ] Optimize timezone conversions
- [ ] Monthly summary endpoint
  - [ ] `GET /api/projection/monthly/?year=2025` → 12 aggregated records
  - [ ] Reduce payload for dashboard (use monthly instead of daily)
- [ ] Performance testing
  - [ ] Test: 24-month projection with 50+ entities < 2s
  - [ ] Test: cache hit reduces time by ≥3x
  - [ ] Test: invalidation updates correct months
- [ ] Documentation
  - [ ] Cache architecture in PRD
  - [ ] Cache invalidation rules
  - [ ] Performance benchmarks

**Aceite**: Cache funcional, projeção com cache ≥3x mais rápida, invalidação correta, endpoint mensal reduz payload, performance < 2s para 24 meses

---

## Próximas ações sugeridas (pós-Sprint 9)
- [ ] Endpoint de projeção mensal: aceitar `year`/`month` e retornar apenas o intervalo do mês (server-side) para reduzir payload
- [ ] Regras de "adiantar para dia útil anterior" (business days logic)
- [ ] Ajustes de categoria/mês (override variable budgets per month)
- [ ] Melhorias no Quick Event (editar eventos, múltiplos eventos no mesmo dia)
- [ ] Dashboard widgets (receitas vs despesas, trends)
- [ ] Mobile responsiveness improvements
- [ ] Metas de economia por subconta
