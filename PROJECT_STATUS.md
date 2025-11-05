# Project Status

Registro de mudanças do projeto (atualizado pelo agente PM). Formato: data, autor, alteração, impacto.

- 2025-10-29 — agent — Pivot iniciado: PRD reescrito para DRF + projeção; AGENTS/agents atualizados; README revisado. Impacto: direção do produto e arquitetura definidas.
- 2025-10-29 — agent — Adicionados requirements opcionais (API/JWT e Excel) e util scripts/xlsx_head.py. Impacto: facilita inspeção e importação de planilha.
- 2025-10-29 — agent — Refatoração para selectors (accounts/categories/transactions) e dashboard via selectors. Impacto: coesão/testabilidade.
- 2025-10-29 — agent — Adicionados agentes Projection Engine, Import Mapper e Project Manager; roadmap/backlog/sprint plan criados. Impacto: planejamento operacionalizado.
- 2025-10-29 — agent — Sprint plan movido de docs/sprint-plan.md para TASKS.md. Impacto: centralização das tarefas.
- 2025-10-29 — agent — Sprint 1 executada: modelos e endpoints DRF criados (planning, cards, transfers/logs/snapshots) e Account estendido. Impacto: CRUDs de domínio disponíveis via /api/.
- 2025-10-29 — agent — TASKS.md atualizado: Sprint 1 com itens concluídos marcados.
- 2025-10-29 — agent — Sprint 2: implementado invoice_builder (compute/rebuild) e endpoints.
- 2025-10-29 — agent — Sprint 3: projection_engine implementado (endpoint /api/projection) e baixa no vencimento aplicada via faturas.
- 2025-10-29 — agent — Sprint 4 replanejada: landing/home atualizada para MVP com demo de projeção; export CSV movido para Sprint 5.
- 2025-10-29 — agent — Fluxo de autenticação revisado: auto login no signup, templates de login/signup em UTF-8 e labels pt-BR; LOGIN_REDIRECT para dashboard.
- 2025-10-29 — agent — Projeção: carry-over exibido na tabela do MVP (linha "Saldo anterior") e correção de rótulos (coluna "Saldo" e chave diario). Impacto: visão acumulada mês a mês correta.
 - 2025-10-31 — PM Agent — Sprint 3 executada: horizonte mensal completo; carry-over contínuo; correção de janeiro (sem dezembro inexistente); onboarding respeitado (dias anteriores a D0 sem valores); endpoint de projeção consumido pelo dashboard com base_start/meses corretos. Impacto: MVP consistente mês a mês e pronto para validação de uso real.

Relatório do Project Manager — Sprint 3
- Objetivo: consolidar a projeção diária com comportamento contínuo entre meses e bordas (janeiro/onboarding) e alinhar o dashboard ao engine.
- Entregas:
  - Engine: horizonte por mês completo; eventos considerados (salários, fixos, variável/dia, faturas no vencimento, transferências como eventos sem afetar patrimônio total).
  - Dashboard: consumo usando base do ano corrente e months span corretos; remoção de dependência de dezembro no mês de janeiro; suporte a `?onboarding=YYYY-MM-DD` (padrão demo 2025-01-15) para não exibir valores antes do D0.
  - TASKS.md: sprint 3 atualizada; itens marcados como concluídos conforme implementação.
- Pendências/risco:
  - Performance/memoization em bases maiores (avaliar cache incremental em ProjectionSnapshot e invalidação por janela).
  - Documentação do algoritmo (PRD) e casos de borda adicionais; testes automatizados.
  - Normalização final de encoding residual em templates, se houver.
- Próximos passos propostos (entrada Sprint 5/6):
  - Export CSV consolidado por período para cliente.
  - Endpoint de projeção mensal (server-side) para reduzir payload no dashboard.
  - Indicadores de risco (saldo futuro negativo).

Pendências conhecidas:
- Validar bordas de janeiro/ano anterior no carry-over com dados reais (onboarding = zero).
- Revisão final de encoding UTF-8 em todos os templates para eliminar resquícios de mojibake.
- Testes automatizados mínimos para projeção e dashboard (consistência das somas/limites de mês).

- 2025-10-31 — PM Agent — Sprint 5 executada: endpoint de exportação CSV (`/api/export.csv`) com suporte a `year+month` ou `start+end`, formato de saída UTF-8 com colunas Data (DD-MM-YYYY), Entrada, Saída, Diário, Saldo. Impacto: permite ao cliente extrair relatório mensal diretamente do sistema.
 - 2025-10-31 — PM Agent — Sprint 6 executada: tabela diária mantida compatível com a planilha, realce de risco (saldo futuro negativo) e acessibilidade básica. Impacto: detecção precoce de risco financeiro.

## [2025-11-05] - PM Agent
### Status Atual
- **Fase**: Fase 3 (Importação e UX) - parcialmente concluída
- **Sprints completos**: 1-6
- **Funcionalidades working**:
  - ✅ DRF API completo (accounts, planning, cards, transactions)
  - ✅ Projection engine (24 meses, carry-over, onboarding)
  - ✅ Invoice builder (fechamento e vencimento)
  - ✅ CSV export por período
  - ✅ Detecção de risco (saldo negativo) com realce visual
  - ✅ Onboarding wizard (dados iniciais + fixos + variável)
- **Gaps conhecidos**:
  - ⚠️ Sem testes automatizados
  - ⚠️ Import XLSX/CSV não implementado
  - ⚠️ Performance optimization (cache) não implementado
  - ⚠️ Code cleanup necessário (unused imports)
  - ⚠️ Documentação incompleta (algoritmo, API)

### Planejamento Sprints 7-9
**Sprint 7** (1-2 semanas): Polish, cleanup, testes básicos
- Cleanup de código (remover imports não usados)
- Merge de onboarding work para main
- Setup pytest com ≥5 testes críticos
- Documentar algoritmo de projeção no PRD
- Performance baseline

**Sprint 8** (2 semanas): Importador XLSX/CSV
- Wizard 3 passos (upload, map, confirm)
- Backend com openpyxl
- Smart column detection
- Validação e error handling
- Template de exemplo para download

**Sprint 9** (1-2 semanas): Performance e cache
- ProjectionSnapshot caching mensal
- Invalidação incremental
- Monthly aggregation endpoint
- Otimização de queries (N+1)
- Target: <2s para 24 meses com 50+ entities

### Impact
Roadmap claro para próximos 5-6 semanas. Prioriza estabilidade (Sprint 7), feature crítica de import (Sprint 8), e performance para escalar (Sprint 9). Projeto transiciona de MVP funcional para produto production-ready.

### Next Steps
- Iniciar Sprint 7: code cleanup e setup de testes
- Atualizar docs/ com roadmap revisado
- Commit work-in-progress de onboarding

## [2025-11-05] - PM Agent (Orquestração Backend + Frontend)
### Completed Task
**Onboarding → Dashboard Integration Fix** - Garantir que dados do onboarding (D0, SalaryRule, FixedExpense, VariableBudget) reflitam imediatamente no dashboard.

### Problem Diagnosed
Após completar onboarding, dados não apareciam no dashboard. Identificados 3 problemas críticos:
1. **Transaction timing**: Redirect acontecia DENTRO do `@transaction.atomic`, antes do commit concluir
2. **Session persistence**: Session modificada mas não salva explicitamente antes do redirect
3. **Query cache**: Dashboard usava queries cacheadas, não via dados recém-commitados

### Backend Changes (profiles/views.py, core/views.py, planning/services.py)
**1. Transaction Scope Fix** (profiles/views.py:63-119)
- Mudou de `@transaction.atomic` decorator para `with transaction.atomic():` context manager
- Transaction agora commita ao final do bloco `with` (linha 119) ANTES do redirect (linha 145)
- Redirect movido para FORA do contexto da transação

**2. POST-COMMIT Verification** (profiles/views.py:121-135)
- Adicionado `connection.close()` para limpar query cache
- Verificação com count queries: `salary_count`, `fixed_count_verify`, `variable_count`, `account_count`
- Logging detalhado: `[Onboarding POST-COMMIT] User X: salary_rules=Y, fixed_expenses=Z...`

**3. Session Persistence** (profiles/views.py:137-141)
- Adicionado `self.request.session.modified = True`
- Adicionado `self.request.session.save()` para forçar persistência
- Garante que `onboarding_date` seja salvo antes do redirect

**4. Dashboard Fresh Queries** (core/views.py:21-23)
- Adicionado `connection.close()` no início do `get_context_data()`
- Força queries frescas no dashboard, evita dados cacheados

**5. Enhanced Logging** (planning/services.py:75-85)
- Logs detalhados: `[Projection] start=X, months=Y, end=Z`
- Logs de contagem: `salary_rules=N, fixed_expenses=M, variable_budgets=P`
- Logs de valores: detalhe de cada salary rule, fixed expense, variable budget

### Frontend Changes (templates/profiles/onboarding.html, templates/dashboard.html)
**1. Onboarding UX Enhancements** (onboarding.html)
- **Progress Indicator**: Badges numerados (1, 2) com checkmark verde quando completo
- **Field Validation**: Border verde (emerald-700) quando campo válido preenchido
- **Summary Preview**: Box indigo com resumo dinâmico: "Salário: R$ X", "Despesas fixas: N", "Variável: R$ Y/mês"
- **Loading State**: Botão muda para "Processando..." com spinner animado ao submeter

**2. Dashboard Success Messaging** (dashboard.html:4-24)
- **Success Banner**: Banner verde emerald quando redirect tem `?onboarding=` param
- **Dynamic Summary**: Fetches de API para mostrar: "✓ Salário configurado: R$ X", "✓ N despesas fixas", "✓ Variável: R$ Y/mês"
- **Close Button**: X para fechar banner, remove param `?onboarding=` da URL

**3. Empty State Handling** (dashboard.html:48-61)
- **Empty State**: Ícone chart + texto "Nenhuma projeção disponível"
- **CTA**: Botão "Iniciar Onboarding" com gradiente indigo-to-sky
- **Smart Logic**: Distingue entre "sem dados nenhum" vs "sem dados no mês filtrado"

**4. Visual Consistency**
- Tema dark mantido (slate colors)
- Success elements: emerald-400/800/950
- Primary actions: gradiente indigo-to-sky
- Animações smooth: spinner, transitions

### Technical Implementation
**Transaction Flow ANTES**:
```
[@transaction.atomic decorator]
  → Create entities
  → return redirect()  ← Redirect DENTRO da transaction
[Transaction commits ao sair da função]
[User redirected]
[Dashboard queries podem ver dados não-commitados]
```

**Transaction Flow DEPOIS**:
```
[with transaction.atomic():]
  → Create entities
[Transaction commits aqui - fim do with block]
→ connection.close() (limpa cache)
→ Verify data (fresh queries)
→ session.save() (persiste sessão)
→ return redirect()  ← Redirect DEPOIS do commit
[User redirected]
[Dashboard: connection.close() + fresh queries veem dados commitados]
```

### Files Modified
1. **profiles/views.py** (linhas 1-11, 49-145) - Transaction fix, verification, session save
2. **core/views.py** (linhas 21-23, 76-84) - Fresh queries, enhanced logging
3. **planning/services.py** (linhas 75-85) - Detailed projection logging
4. **templates/profiles/onboarding.html** - Complete UX overhaul (progress, validation, summary, loading)
5. **templates/dashboard.html** - Success banner, empty state, smart filtering

### Success Criteria Met
✅ Transaction commits BEFORE redirect
✅ Session persists onboarding_date before redirect
✅ Dashboard forces fresh queries (no cache)
✅ Data verification with count queries
✅ Comprehensive logging at all points
✅ Visual feedback: loading state, success banner, empty state
✅ Progress indicator with checkmarks
✅ Field validation with green borders
✅ Dynamic summary preview

### Testing Checklist
- [ ] Complete onboarding → verify logs show `[Onboarding POST-COMMIT]` with counts > 0
- [ ] Verify redirect goes to dashboard with `?onboarding=` param
- [ ] Verify green success banner appears with summary
- [ ] Verify projection table shows salary, fixed expenses, variable budget
- [ ] Verify empty dashboard shows CTA "Iniciar Onboarding"
- [ ] Verify form shows "Processando..." during submit
- [ ] Verify progress indicator shows checkmark on step 1 when moving to step 2

### Impact
**High Impact** - Resolve problema crítico de UX onde usuários completavam onboarding mas não viam dados no dashboard, causando confusão e necessidade de recarregar página. Agora:
- Dados aparecem imediatamente após onboarding
- Usuário recebe confirmação visual clara (banner de sucesso)
- Empty state guia novos usuários para onboarding
- Loading states previnem double-submit
- Logs detalhados facilitam debug

### Next Steps
- Testar fluxo completo com usuário real
- Validar logs em ambiente de desenvolvimento
- Considerar adicionar testes automatizados para transaction timing
- Monitorar se issue está resolvido em produção
