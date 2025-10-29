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

Pendências conhecidas:
- Validar bordas de janeiro/ano anterior no carry-over com dados reais (onboarding = zero).
- Revisão final de encoding UTF-8 em todos os templates para eliminar resquícios de mojibake.
- Testes automatizados mínimos para projeção e dashboard (consistência das somas/limites de mês).
