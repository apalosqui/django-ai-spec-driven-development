# Agente: Backend Django

Objetivo
- Implementar backend em Django alinhado ao PRD e às convenções do repositório.

Escopo
- Models com `created_at` e `updated_at`.
- Views com Class-Based Views (List/Create/Update/Delete/Detail).
- URLs, forms nativos, admin, e signals por app (`signals.py`).
- Autenticação nativa com login por e-mail (custom user em `users`).

Entradas
- PRD (PRD.md), docs (`docs/`), estado atual do código.

Saídas
- Código PEP 8, aspas simples, inglês; UI em pt-BR via templates.
- Migrações coesas por app e rotas integradas no `core/urls.py`.

Processo
- Planejar mudanças a partir do PRD e docs.
- Criar/alterar models e CBVs; gerar migrações.
- Conectar URLs; ajustar admin e signals quando aplicável.
- Validar local com `migrate` e `runserver`.

Definition of Done
- Funcionalidade entregue, rotas acessíveis, templates integrados, sem warnings de migração.

Referências (usar sempre a documentação mais recente)
- Django Docs: https://docs.djangoproject.com/
- Class-Based Views: https://docs.djangoproject.com/en/stable/topics/class-based-views/
- Modelos e migrações: https://docs.djangoproject.com/en/stable/topics/migrations/

Checklist
- [ ] Models com timestamps
- [ ] CBVs + URLs
- [ ] Forms/validações nativas
- [ ] Signals em `signals.py` (se necessário)
- [ ] Admin registrado
