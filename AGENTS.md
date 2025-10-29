# Repository Guidelines (Pivot)

These guidelines reflect the new scope (DRF + projeção financeira) and working practices. Keep code simple and cohesive.

## Project Structure & Module Organization
- Core: `core/` (settings, URLs, WSGI/ASGI, DRF config).
- Domain apps: `users/`, `profiles/`, `accounts/`, `categories/`, `transactions/`.
- Services/selectors close to each app (`services.py`, `selectors.py`).
- Docs: `docs/` (index in `docs/readme.md`) and `PRD.md`.
- Templates: `templates/` (DTL) with shared layout in `templates/base.html`.
- Static: `static/` (Tailwind via CDN). Optional CSS: `static/css/finanpy.css`.

## Build, Test, and Development Commands
- Setup DB: `python manage.py migrate`; superuser: `python manage.py createsuperuser`.
- Run locally: `python manage.py runserver`.
- Migrations: `python manage.py makemigrations <app>`.
- Collect static (if required): `python manage.py collectstatic`.
- API docs (quando configurado): `/api/schema/` e `/api/docs/`.

## Coding Style & Naming Conventions
- PEP 8, 4 spaces, single quotes.
- Code in English; UI text em pt-BR.
- Prefer Class-Based Views; para API, usar DRF (ViewSets/Generic Views, Serializers).
- Models must include `created_at` and `updated_at`.
- Signals permanecem em `signals.py` e são importadas no `apps.py`.
- Auth: Django auth com e-mail; API com JWT (SimpleJWT) quando habilitado.
- Timezone: `America/Sao_Paulo`; moeda: `BRL`; datas em UI: `DD-MM-YYYY`.

## Testing Guidelines
- Tests are deferred. When added: coloque sob cada app (`tests.py` ou `tests/`), nome `test_*.py`.
- Priorize testar selectors/services (projeção, faturas) em isolamento.

## Commit & Pull Request Guidelines
- Commits concisos, no imperativo (ex.: `feat(api): add projection endpoint`).
- PRs com escopo claro, migrações incluídas e evidências de UI quando houver.

## Agent-Specific Instructions
- Dependências permitidas para o pivot: `djangorestframework`, `djangorestframework-simplejwt` (opcional), `openpyxl` (importador XLSX). SQLite em dev; Postgres recomendado em prod. Não introduzir Docker neste repo por enquanto.
- Implementar apenas o solicitado; alinhar com `PRD.md` e `docs/`.
- Usar Tailwind via CDN; manter layout escuro com gradientes.
- SOLID e padrões: selectors/services, CBVs/DRF ViewSets, transações atômicas em serviços críticos.
