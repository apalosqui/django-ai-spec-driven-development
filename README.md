# Finanpy — Pivot DRF + Projeção

Aplicativo Django com Django REST Framework para controle e projeção financeira pessoal. Segue o PRD (pivot) em `PRD.md`. UI simples (DTL + Tailwind via CDN) e SQLite por padrão.

## Sobre
- Apps de domínio: `users`, `profiles`, `accounts`, `categories`, `transactions`.
- Autenticação por e‑mail com usuário customizado (`AUTH_USER_MODEL = 'users.User'`); API com JWT (opcional).
- Templates DTL com layout compartilhado em `templates/base.html`.
- Estilos com Tailwind via CDN (sem build local).
- Contexto BR: moeda BRL, timezone America/Sao_Paulo, datas DD‑MM‑YYYY.

## Requisitos
- Python 3.12+
- Sem Docker. Banco: SQLite (arquivo `db.sqlite3`).

## Como Rodar Localmente
1) Crie e ative o ambiente virtual
- Linux/macOS: `python3 -m venv .venv && source .venv/bin/activate`
- Windows (PowerShell): `python -m venv .venv; .venv\Scripts\Activate.ps1`

2) Instale dependências
- Base: `pip install -r requirements.txt`
- API (DRF/JWT, opcional): `pip install -r requirements-api.txt`
- Excel (openpyxl, opcional): `pip install -r requirements-excel.txt`

3) Migrações
- `python manage.py migrate`

4) Usuário admin (opcional)
- `python manage.py createsuperuser`

5) Executar servidor
- `python manage.py runserver`
- Acesse: `http://127.0.0.1:8000/`

## Rotas Principais (web)
- Home: `/`
- Login: `/login/` | Logout: `/logout/` | Cadastro: `/signup/`
- Dashboard: `/dashboard/` | Admin: `/admin/`
- Domínio: Contas `/accounts/`, Categorias `/categories/`, Transações `/transactions/`, Perfil `/perfil/`

## API (esqueleto)
- POST `/auth/register`, `/auth/login`
- CRUD: `/api/accounts/`, `/api/salary-rules/`, `/api/fixed-expenses/`, `/api/variable-budgets/`, `/api/credit-cards/`, `/api/card-transactions/`
- Invoices: GET `/api/card-invoices/?yyyy_mm=&card_id=`; POST `/api/card-invoices/rebuild`
- Transfers: GET/POST `/api/transfers/`
- Projection: GET `/api/projection/?start=YYYY-MM-DD&months=24`
- Import/Export: POST `/api/import` (XLSX/CSV), GET `/api/export.csv`

## Estrutura
- Core do projeto: `core/` (settings, urls, WSGI/ASGI, DRF config).
- Apps de domínio: `users/`, `profiles/`, `accounts/`, `categories/`, `transactions/`.
- Templates: `templates/`
- Estáticos: `static/` (opcional `static/css/finanpy.css`).
- Docs: `docs/` e `PRD.md`; agentes em `agents/`.

## Documentação
- Índice de docs: `docs/readme.md`
- PRD do produto (pivot): `PRD.md`
- Agentes: `agents/` (backend DRF, projection-engine, import-mapper, QA)

## Comandos úteis
- Migrações: `python manage.py makemigrations <app>` | `python manage.py migrate`
- Rodar servidor: `python manage.py runserver`
- Coletar estáticos (se necessário): `python manage.py collectstatic`

## Convenções
- Código em inglês; textos da UI em pt‑BR.
- PEP 8, 4 espaços, aspas simples.
- Preferir CBVs/DRF e recursos nativos do Django.
- Models com `created_at`/`updated_at` (auto timestamps).

## Contribuição
- Commits no formato Conventional Commits (ex.: `feat(api): add projection endpoint`).
- Abrir PR com escopo, screenshots (UI) e migrações quando aplicável.

