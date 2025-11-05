# Backlog (priorizado)

## Concluídos ✅
- ✅ Projeção diária (service + endpoint) considerando salários, fixos, variável/dia, faturas, transferências
- ✅ Fechamento de faturas (invoice_builder) e baixa no vencimento
- ✅ CRUDs essenciais (Accounts, SalaryRule, FixedExpense, VariableBudget, CreditCard, CardTransaction, Transfer)
- ✅ Tabela diária de projeção (Data/Entrada/Saída/Diário/Saldo)
- ✅ Export CSV e template de exportação
- ✅ Alertas (saldo negativo previsto) com realce visual
- ✅ Onboarding wizard (salary + fixed + variable)

## Alta prioridade 🔴
- **Testes automatizados básicos** (Sprint 7)
  - Projection carry-over
  - Invoice calculation edge cases
  - User isolation validation
  - Onboarding seeds verification
- **Code cleanup** (Sprint 7)
  - Remove unused imports
  - Fix diagnostics warnings
  - UTF-8 consistency
- **Importador XLSX/CSV** (Sprint 8)
  - Wizard com openpyxl (3 steps: upload, map, confirm)
  - Column mapping assistant
  - Bulk entity creation
  - Validation and error handling

## Média prioridade 🟡
- **Performance optimization** (Sprint 9)
  - ProjectionSnapshot cache mensal com invalidação incremental
  - Memoization de cálculos variáveis
  - Monthly aggregation endpoint (`/api/projection/monthly/`)
  - Query optimization (N+1 elimination)
- **Documentação completa**
  - Projection algorithm pseudocode in PRD
  - API documentation (OpenAPI/Swagger)
  - Onboarding flow documentation
  - Cache architecture documentation

## Baixa prioridade 🟢
- **Melhorias no Quick Event** (UX)
  - Função de editar eventos existentes
  - Suporte para múltiplos eventos no mesmo dia (soma valores)
  - Histórico de eventos com filtros por tipo e data
  - Confirmação visual de eventos adicionados
- Metas de economia por subconta
- Dashboard widgets (receitas vs despesas, trends)
- Mobile responsiveness improvements
- Export template download (XLSX with example data)
- Faturas acima da média (alertas adicionais)

## Refinamento contínuo 🔄
- Regras de "adiantar para dia útil anterior" (business days logic)
- Ajustes de categoria/mês (override variable budgets per month)
- Formatações BR (datas DD-MM-YYYY, moeda BRL) - validação contínua
- Accessibility (a11y) improvements
- Error messages in pt-BR
