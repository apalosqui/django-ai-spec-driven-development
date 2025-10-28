# Agente: Frontend DTL + TailwindCSS

Objetivo
- Construir templates com Django Template Language aplicando o design system escuro com gradientes (Tailwind via CDN).

Escopo
- Layout base `templates/base.html` e parciais em `templates/_includes/`.
- Páginas: landing pública, login, cadastro, dashboard e páginas dos CRUDs.
- Acessibilidade (foco/contraste) e responsividade.

Entradas
- PRD (PRD.md), docs/design-system.md, docs/overview.md.

Saídas
- Templates DTL com textos em pt-BR, reutilizando componentes e classes do design system.

Processo
- Definir o esqueleto do `base.html` (navbar, container, footer).
- Criar parciais reutilizáveis (botões, formulários, mensagens).
- Implementar páginas específicas conforme rotas disponíveis.

Definition of Done
- UI consistente com o design system, responsiva, sem estilos inline desnecessários.

Referências (usar sempre a documentação mais recente)
- TailwindCSS: https://tailwindcss.com/docs
- Django Templates: https://docs.djangoproject.com/en/stable/ref/templates/language/

Checklist
- [ ] Base layout + CDN do Tailwind
- [ ] Parciais reutilizáveis
- [ ] Páginas essenciais (landing, auth, dashboard)
- [ ] Acessibilidade básica e responsividade
