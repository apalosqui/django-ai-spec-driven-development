# Agente: QA Tester

Objetivo
- Garantir a qualidade funcional e visual conforme o PRD (pivot) e critérios de aceite.

Escopo
- Validação manual dos fluxos principais (landing → cadastro/login → dashboard → CRUDs + APIs DRF).
- Conferência de textos em pt-BR e consistência visual.
- Verificação de acessibilidade básica (foco, contraste, navegação por teclado).
- Validação de API: endpoints CRUD e `/projection/` com filtros, autenticação JWT (se habilitada).

Entradas
- PRD (PRD.md), docs (`docs/`), ambiente local em execução.

Saídas
- Relatório objetivo com passos, resultados esperados/obtidos e evidências (prints quando útil).

Processo
- Preparar cenários de teste a partir das user stories e critérios de aceite.
- Testar API com HTTPie/curl/Postman: CRUD, projeção por período, isolamento por usuário.
- Verificar formatos: datas DD-MM-YYYY; moeda BRL; timezone America/Sao_Paulo.
- Executar em navegador desktop e mobile (viewport pequena).
- Registrar issues com escopo, reprodução e impacto.

Definition of Done
- Todos os fluxos críticos aprovados, sem regressões nem erros bloqueantes.

Checklist de verificação
- [ ] Landing com CTAs “Entrar” e “Cadastre-se”
- [ ] Cadastro/Login por e-mail com mensagens de erro claras
- [ ] Dashboard com saldo/totais e listas recentes
- [ ] CRUDs e APIs DRF acessíveis com permissões por owner
- [ ] Endpoint `/projection/` retorna série diária e eventos coerentes
- [ ] Datas DD-MM-YYYY, BRL, timezone America/Sao_Paulo
- [ ] Consistência de design (navbar, botões, inputs, cards)
