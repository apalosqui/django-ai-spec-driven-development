# Repository Guidelines

These guidelines summarize how to work in this repository based on the initial structure, PRD (PRD.md), and docs (docs/readme.md). Keep the code simple and avoid over‑engineering.

## Project Structure & Module Organization
- Core: `core/` (settings, URLs, WSGI/ASGI).
- Domain apps: `users/`, `profiles/`, `accounts/`, `categories/`, `transactions/`.
- Docs: `docs/` (index in `docs/readme.md`). Product doc in `PRD.md`.
- Templates: `templates/` (DTL) with shared layout `templates/base.html` and partials in `templates/_includes/` (add when needed).
- Static: `static/` (Tailwind via CDN initially). Optional custom CSS: `static/css/finanpy.css`.

## Build, Test, and Development Commands
- Setup DB: `python manage.py migrate`; superuser: `python manage.py createsuperuser`.
- Run locally: `python manage.py runserver`.
- Migrations: `python manage.py makemigrations <app>`.
- Collect static (if required): `python manage.py collectstatic`.

## Coding Style & Naming Conventions
- PEP 8, 4 spaces, use single quotes.
- Code in English; UI text in pt‑BR.
- Prefer Class‑Based Views and native Django features.
- Models must include `created_at` and `updated_at` (`auto_now_add`/`auto_now`).
- Signals live in `signals.py` within each app and are imported in `apps.py`.
- Authentication: use Django auth with e‑mail login; custom user in `users` (`AUTH_USER_MODEL = 'users.User'`).

## Testing Guidelines
- Tests are deferred. When added: place under each app (`tests.py` or `tests/`), name files `test_*.py`, run with `python manage.py test`.

## Commit & Pull Request Guidelines
- Commits: concise, imperative. Prefer Conventional Commits (e.g., `feat(accounts): add list view`).
- PRs: description of scope, screenshots for UI, linked issues; include migrations and keep UI consistent with the design system.

## Agent‑Specific Instructions
- Do not add dependencies or Docker; SQLite only.
- Implement only what is requested; align with `PRD.md` and `docs/`.
- Use Tailwind via CDN; reuse the shared layout and partials to keep the design consistent and dark with gradients.
