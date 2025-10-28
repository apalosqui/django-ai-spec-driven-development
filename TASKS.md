## Lista de tarefas (Sprints)

### Sprint 1 — Fundações e Auth
- [X] Criar projeto e apps (`core`, `users`, `profiles`, `accounts`, `categories`, `transactions`).
- [X] Configurar templates, static e Tailwind CDN no `base.html`.
- [X] Custom User por e-mail e login via e-mail.
- [X] Signals: auto-criar `Profile` após usuário.
- [X] Landing pública + rotas de cadastro/login/logout.

### Sprint 2 — Modelos e CRUDs
- [X] Modelos com `created_at`/`updated_at` em todas as tabelas.
- [X] CRUD `Account` (List/Create/Update/Delete) com CBVs.
- [X] CRUD `Category` com tipo receita/depesa.
- [X] CRUD `Transaction` com filtro por período/conta/categoria.
- [X] Dashboard com saldo, totals e últimas transações.

### Sprint 3 — UX e Polimento
- [ ] Aplicar design system unificado (navbar, cards, botões, formulários).
- [ ] Mensagens de feedback (success/erro) e estados vazios.
- [ ] Acessibilidade básica (foco/contraste) e responsividade.

### Sprint 4 — Perfil do Usuário
- [X] Página de perfil (visualizar e editar).
- [X] Criar CBVs: `ProfileDetailView` e `ProfileUpdateView`.
- [X] Formulário de perfil (campo: nome completo).
- [X] URLs do app `profiles` (`profiles/urls.py`).
- [X] Templates: `profiles/detail.html` e `profiles/form.html`.
- [X] Proteger acesso (LoginRequired; apenas o próprio usuário).
- [X] Link para perfil na navbar e no dashboard.
- [X] Mensagem de sucesso após salvar.
- [X] Incluir rotas de `profiles` em `core/urls.py`.

- [X] Sprint concluída
