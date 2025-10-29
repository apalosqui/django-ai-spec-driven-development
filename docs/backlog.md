# Backlog (priorizado)

Alta
- Projeção diária (service + endpoint) considerando salários, fixos, variável/dia, faturas, transferências.
- Fechamento de faturas (invoice_builder) e baixa no vencimento.
- CRUDs essenciais (Accounts, SalaryRule, FixedExpense, VariableBudget, CreditCard, CardTransaction, Transfer).

Média
- Importador XLSX/CSV com openpyxl (wizard + mapeamento).
- UI calendário/linha do tempo e tabela diária (Data/Entrada/Saída/Diário/Saldo).
- ProjectionSnapshot cache mensal com invalidação incremental.

Baixa
- Export CSV e template de importação.
- Alertas (saldo negativo previsto; faturas acima da média).
- Metas de economia por subconta.

Refinamento contínuo
- Regras de “adiantar para dia útil anterior” e ajustes por categoria/mês.
- Formatações BR (datas DD-MM-YYYY, moeda BRL) consistentes na API e UI.
