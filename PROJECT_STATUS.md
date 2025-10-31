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
  - UI timeline e indicadores de risco (saldo futuro negativo).

Pendências conhecidas:
- Validar bordas de janeiro/ano anterior no carry-over com dados reais (onboarding = zero).
- Revisão final de encoding UTF-8 em todos os templates para eliminar resquícios de mojibake.
- Testes automatizados mínimos para projeção e dashboard (consistência das somas/limites de mês).

- 2025-10-31 — PM Agent — Sprint 5 executada: endpoint de exportação CSV (`/api/export.csv`) com suporte a `year+month` ou `start+end`, formato de saída UTF-8 com colunas Data (DD-MM-YYYY), Entrada, Saída, Diário, Saldo. Impacto: permite ao cliente extrair relatório mensal diretamente do sistema.
 - 2025-10-31 — PM Agent — Sprint 6 executada: adicionada Timeline do mês com ícones (💼 salário, 🧾 fixo, 📊 variável, 💳 fatura, 🔁 transferência), realce de risco (saldo futuro negativo) e acessibilidade básica (rótulos e aria). Tabela diária mantida compatível com a planilha. Impacto: melhor compreensão visual e detecção precoce de risco financeiro.
