# Estrutura de pastas

Resumo do que está presente no repositório:

```
manage.py
requirements.txt
db.sqlite3
core/
  __init__.py
  asgi.py
  settings.py
  urls.py
  wsgi.py
users/
  __init__.py  admin.py  apps.py  migrations/  models.py  tests.py  views.py
profiles/
  __init__.py  admin.py  apps.py  migrations/  models.py  tests.py  views.py
accounts/
  __init__.py  admin.py  apps.py  migrations/  models.py  tests.py  views.py
categories/
  __init__.py  admin.py  apps.py  migrations/  models.py  tests.py  views.py
transactions/
  __init__.py  admin.py  apps.py  migrations/  models.py  tests.py  views.py
PRD.md
AGENTS.md
```

Observações:
- Apps estão criados, porém modelos/visões ainda são mínimos.
- A organização segue separação por domínio para isolar responsabilidades.
