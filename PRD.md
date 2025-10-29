# PRD — Finanpy (Pivot DRF + Projeção)

Contexto BR: moeda BRL, timezone America/Sao_Paulo, datas DD-MM-YYYY.

## 1) Objetivo do Produto
Criar um app web que centraliza receitas, gastos fixos/variáveis, cartões de crédito e economias (reservas/projetos) e projeta diariamente o saldo futuro por pelo menos 24 meses (configurável). A projeção considera salários, fixos, variáveis (distribuição diária), faturas de cartão e transferências entre caixa e economias, com visualizações em calendário/tabela e indicadores de risco.

## 2) Glossário
- Caixa: saldo de liquidez imediata (espelha “saldo” da planilha).
- Economias: subcontas de poupança/projetos/reserva.
- Fixo: despesa recorrente em data específica (ex.: aluguel dia 05).
- Variável: orçamento mensal distribuído uniformemente por dia.
- Compra no cartão: não impacta caixa no dia da compra; impacta no vencimento da fatura.
- Aplicação/Resgate: transferências entre caixa e economias (tags de cor distintas).

## 3) Requisitos Funcionais (RF)
- RF-01 Contas: “Caixa” (obrigatória) e N contas de Economias.
- RF-02 Salários: valor e regras de recebimento (ex.: dia 5 e 20; “último dia útil”).
- RF-03 Fixos: valor, periodicidade (mensal/anual), vencimento e conta pagadora.
- RF-04 Variáveis (orçamentos): valor mensal → distribuição diária uniforme na projeção.
- RF-05 Cartões: múltiplos cartões com dia de fechamento e vencimento.
- RF-06 Transações do cartão: compras (data, valor, categoria, cartão); compõem fatura; baixa no vencimento debitando Caixa.
- RF-07 Transferências: Aplicação (Caixa→Economia) e Resgate (Economia→Caixa) com status visual.
- RF-08 Projeção diária por N meses (default 24): receitas − fixos − variável por dia − faturas no vencimento; saldo cumulativo dia a dia.
- RF-09 Visões: calendário diário (heatmap/ícones), tabela diária (data, saldo projetado, lançamentos), mês consolidado.
- RF-11 Autenticação: e-mail/senha.
- RF-12 Permissões: dados isolados por usuário.
- RF-13 Auditoria: created_at/updated_at, quem criou/alterou.
- RF-14 Configurações: N meses de projeção, formato de data, moeda BRL e timezone America/Sao_Paulo.
- RF-15 Desempenho: projeção incremental (recalcular apenas janelas afetadas).
- RF-16 Anotações de cor: aplicações/resgates com cores conforme planilha.

## 4) Regras de Negócio (RN)
- RN-01 Salários: múltiplos por mês; se cair em feriado/fim de semana, opção “adiantar para dia útil anterior”.
- RN-02 Variáveis: cota_dia = valor_mensal / dias_do_mês; replicar meses futuros com possibilidade de ajustes por categoria/mês.
- RN-03 Fixos: lançar no vencimento; “pagar adiantado” move para dia útil anterior.
- RN-04 Cartão: fechamento define o ciclo; vencimento debita Caixa com total por cartão; múltiplos cartões → múltiplas baixas.
- RN-05 Aplicação/Resgate: não alteram patrimônio total; apenas distribuição entre Caixa/Economias; aparecem na timeline.
- RN-06 Projeção: saldo_dia = saldo_(dia-1) + receitas_dia − fixos_dia − variáveis_dia − faturas_dia ± transferências_dia.
- RN-07 Consistência: nenhuma transação sem conta/cartão; validações fortes.

## 5) Modelos de Dados (ORM Django — proposta)
- User (Django)
- Account (tipo: CAIXA|ECONOMIA; nome; cor_tag; saldo_inicial; owner)
- SalaryRule (user, valor, regra: {dias=[5,20]} ou {ultimo_dia_util=true})
- FixedExpense (user, nome, valor, dia_vencimento, periodicidade: MENSAL|ANUAL, conta_pagadora=Account)
- VariableBudget (user, categoria, valor_mensal, ativo_bool)
- CreditCard (user, nome, dia_fechamento, dia_vencimento, conta_pagamento=Account)
- CardTransaction (cartao, data_compra, descricao, categoria, valor, parcelas_opc)
- CardInvoice (cartao, referencia_yyyy_mm, data_fechamento, data_vencimento, total_calculado, status: ABERTA|PAGA)
- Transfer (user, origem=Account, destino=Account, valor, data, tipo: APLICACAO|RESGATE)
- TransactionLog (user, data, tipo: SALARIO|FIXO|VARIAVEL|FATURA|TRANSFER, ref_id, valor)
- ProjectionSnapshot (user, data, saldo_projetado, meta_info_json) [opcional cache]

Observação: “Variável” não é lançada como transação unitária; é gerada na projeção a partir de VariableBudget.

## 6) Projeção — Algoritmo (alto nível)
Entrada: start_date=today, horizonte=N meses. Inicialize saldos por conta = saldos iniciais. Para cada dia d até o horizonte: some salários e resgates; subtraia fixos com vencimento em d; subtraia a cota variável diária (soma de valor_mensal/dias_do_mês por categoria ativa); subtraia faturas que vencem em d; aplique transferências Caixa↔Economias de d. Atualize saldos por conta e saldo projetado do dia. Persistir ProjectionSnapshot (opcional) e expor via API. Fatura: calcule CardInvoice por (cartão, mês de referência) com base em CardTransaction entre (fechamento_prev+1, fechamento_atual); debitar somente no vencimento.

## 7) API (OpenAPI — esqueleto)
- POST /auth/register, POST /auth/login
- GET/POST/PUT/DELETE /accounts/
- GET/POST/PUT/DELETE /salary-rules/
- GET/POST/PUT/DELETE /fixed-expenses/
- GET/POST/PUT/DELETE /variable-budgets/
- GET/POST/PUT/DELETE /credit-cards/
- GET/POST/PUT/DELETE /card-transactions/
- GET /card-invoices/?yyyy_mm=&card_id= (recalcula on-the-fly); POST /card-invoices/rebuild
- GET/POST /transfers/
- GET /projection/?start=YYYY-MM-DD&months=24 → retorna lista diária {date, saldo, eventos:[...]}
- POST /import (XLSX/CSV com mapeamento assistido)
- GET /export.csv

## 8) UI (MVP)
- Dashboard: saldo atual de Caixa e Economias; próximos 30 dias (cards por dia); alertas de saldo negativo futuro.
- Calendário/Timeline: visão diária com ícones (salário, fixo, variável, fatura, aplicação/resgate).
- Cartões: lista de faturas (aberta/próxima), total e datas; detalhe da fatura.
- Economias: subcontas, extrato de aplicações/resgates; cores: tag-apply (aplicação) e tag-redeem (resgate).
- Importador: wizard para mapear colunas da planilha para os modelos.

## 9) Tarefas Técnicas (Backlog inicial)
- Adotar DRF (djangorestframework), autenticação (SimpleJWT), i18n pt-BR, timezone America/Sao_Paulo.
- Models e migrações (Seção 5).
- Serviços: invoice_builder, projection_engine (cache incremental), import_mapper (XLSX/CSV via openpyxl).
- APIs REST (Seção 7) e documentação OpenAPI.
- Seeds e fixtures de exemplo.
- Testes automatizados (pytest + pytest-django) [posterior].

## 10) Performance & Escalabilidade
- Cache de projeção por janela (ex.: mês) invalidado somente quando entidades daquele período mudarem.
- Cálculo da variável diária com memoization; paginação e filtros nas listas.

## 11) Segurança e Qualidade
- Autorização por owner em todas as queries; validações de datas/valores; CSRF nas views HTML.

## 12) Stack
- Backend: Django 5.x, Django REST Framework; SQLite em dev, Postgres recomendado em produção.
- Importação: openpyxl (XLSX), CSV nativo.
- Frontend: DTL + Tailwind (CDN) no MVP; opcional HTMX.

