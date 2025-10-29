# Agente: Backend Django + DRF

Objetivo
- Implementar backend Django/DRF alinhado ao PRD (pivot): projeção diária, cartões, budgets e importação.

Escopo
- Models com `created_at`/`updated_at` (timestamps) e validações.
- API com DRF (Serializers, ViewSets/Generic Views, Routers, permissions por owner).
- Autenticação: Django auth (web) e JWT (API, opcional com SimpleJWT).
- Services/selectors: projeção (projection_engine), faturas (invoice_builder), importação (import_mapper).
- Signals por app (`signals.py`), admin e migrações.

Entradas
- PRD (PRD.md), docs (`docs/`), estado atual do código e planilha-base.

Saídas
- Código PEP 8, aspas simples; inglês (código) e pt‑BR (UI); endpoints versionados.
- Rotas DRF documentadas (schema/OpenAPI) quando configurado.

Processo
- Planejar a partir do PRD: modelos (Seção 5), endpoints (Seção 7), regras (Seções 4 e 6).
- Criar/alterar models → serializers → viewsets; definir permissions e filtros.
- Implementar services: projeção e fechamento de faturas; importar XLSX.
- Conectar URLs (incluindo `routers.DefaultRouter`) e configurar DRF/JWT (se habilitado).

Definition of Done
- Endpoints CRUD e projeção funcionando com isolamento por usuário; validações; documentação atualizada.

Referências
- Django: https://docs.djangoproject.com/
- DRF: https://www.django-rest-framework.org/
- SimpleJWT: https://django-rest-framework-simplejwt.readthedocs.io/

Checklist
- [ ] Models + migrações
- [ ] Serializers + ViewSets
- [ ] Permissions por owner
- [ ] Services/selectors implementados
- [ ] URLs/routers conectados
- [ ] (Opcional) JWT habilitado

