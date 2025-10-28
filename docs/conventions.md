# Convenções e padrões

Estilo de código
- PEP 8, indentação de 4 espaços, usar aspas simples sempre que possível.
- Código em inglês; textos da interface em português brasileiro.

Arquitetura
- Django full‑stack, DTL nos templates.
- Separação por domínio: `users`, `profiles`, `accounts`, `categories`, `transactions`.
- Preferir Class Based Views e recursos nativos do Django.
- Se houver signals, manter em `signals.py` do app e importar no `apps.py`.

Modelos
- Cada model deverá conter `created_at` e `updated_at` (padrão do projeto).

Commits e PRs
- Mensagens concisas no imperativo. Sugestão de padrão: Conventional Commits (ex.: `feat(accounts): add list view`).
- PRs com descrição objetiva, escopo claro e itens de verificação (migrations, rota, template quando aplicável).

Referências
- Guia geral: `AGENTS.md`.
- Escopo e metas do produto: `PRD.md`.
