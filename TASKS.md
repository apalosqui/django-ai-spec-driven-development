# TASKS â€” Sprints & Backlog Breakdown

ObservaÃ§Ã£o: este arquivo consolida o plano de sprints (antes em `docs/sprint-plan.md`) em tarefas acionÃ¡veis.

- [x] Models: `Account`, `SalaryRule`, `FixedExpense`, `VariableBudget`, `CreditCard`, `CardTransaction`, `Transfer`, `CardInvoice`, `ProjectionSnapshot`, `TransactionLog`
- [x] MigraÃ§Ãµes criadas e aplicadas
- [x] DRF: Serializers + ViewSets para todos os modelos acima (CRUD)
- [x] Permissions por owner em todos os endpoints
- [x] URLs/routers conectados sob `/api/`
- [x] Admin bÃ¡sico registrado para os modelos
- [x] Docs atualizadas (README rotas + PRD/API)
- Aceite: endpoints GET/POST/PUT/DELETE funcionam isolando dados por usuÃ¡rio

## Sprint 2 (1â€“2 semanas)
- [x] Service `invoice_builder`: fechamento por (cartÃ£o, yyyy_mm) com base em `dia_fechamento`
- [x] CÃ¡lculo e persistÃªncia de `CardInvoice.total_calculado`
- [x] Endpoints: GET `/api/card-invoices/compute?yyyy_mm=&card_id=`, POST `/api/card-invoices/rebuild`
- [ ] Testes bÃ¡sicos do fluxo de fatura (feliz + borda)
- [x] Docs atualizadas (seÃ§Ã£o faturas)
- Aceite: faturas geradas corretamente e baixa aplicada na data correta

## Sprint 3 (2 semanas)
- [x] Service `projection_engine`: projeÃ§Ã£o diÃ¡ria 24+ meses (configurÃ¡vel)
- [x] Cache diÃ¡rio com `ProjectionSnapshot` (base para cache mensal)
- [x] Endpoint GET `/api/projection/?start=YYYY-MM-DD&months=24`
- [x] Baixa no vencimento: debitar conta de pagamento em `data_vencimento` (via faturas na projeÃ§Ã£o)
- [ ] Considerar: salÃ¡rios, fixos, variÃ¡vel/dia, faturas, transferÃªncias; timezone `America/Sao_Paulo`
- [ ] Performance aceitÃ¡vel em dados de exemplo; memoization onde Ãºtil
- [ ] Docs/algoritmo atualizados
- Aceite: sÃ©rie diÃ¡ria coerente e com eventos do dia

## Sprint 4 (1â€“2 semanas)
- [x] Atualizar landing/home para MVP (pivot DRF + projeÃ§Ã£o)
- [x] Incluir CTA e seÃ§Ã£o de demonstraÃ§Ã£o da projeÃ§Ã£o (GET `/api/projection/`)
- [x] Texto e visual alinhados ao PRD (pt-BR, BRL, datas DD-MM-YYYY)
- [x] Aceite: home comunica valor e permite testar projeÃ§Ã£o (se logado)

## Sprint 5 (1â€“2 semanas)
- [ ] Export template CSV e endpoint GET `/api/export.csv`
- [ ] RelatÃ³rio CSV consolidado por perÃ­odo (cliente)
- [ ] Docs (guia de exportaÃ§Ã£o) e exemplos
- Aceite: exporta relatÃ³rio CSV vÃ¡lido e coerente

## Sprint 5 (1â€“2 semanas)
- [ ] UI calendÃ¡rio/timeline com Ã­cones (salÃ¡rio, fixo, variÃ¡vel, fatura, aplicaÃ§Ã£o/resgate)
- [ ] Tabela diÃ¡ria compatÃ­vel com planilha: Data, Entrada, SaÃ­da, DiÃ¡rio, Saldo
- [ ] Indicadores de risco (saldo futuro negativo)
- [ ] Alinhamento com design system; acessibilidade bÃ¡sica
- [ ] Docs (prints e instruÃ§Ãµes)
- Aceite: visual consistente e informativo para prÃ³ximos 30 dias

## Ajustes pendentes
- [ ] Projeção (MVP): garantir carry-over exibido na tabela do mês (saldo no dia 01 deve herdar saldo do último dia do mês anterior; onboarding = zero).

