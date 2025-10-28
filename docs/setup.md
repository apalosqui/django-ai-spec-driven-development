# Configuração e execução

Pré‑requisitos:
- Python 3.11+ (recomendado), virtualenv (opcional).

Instalação:
1. Criar e ativar ambiente virtual (opcional):
   - Windows PowerShell: `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
2. Instalar dependências: `pip install -r requirements.txt`
3. Aplicar migrações: `python manage.py migrate`
4. (Opcional) Criar superusuário: `python manage.py createsuperuser`
5. Executar servidor: `python manage.py runserver`

Banco de dados:
- Usa SQLite por padrão (`db.sqlite3`). Nenhuma configuração adicional é necessária em desenvolvimento.

Estrutura de diretórios úteis:
- Código do projeto: `core/`
- Apps de domínio: `users/`, `profiles/`, `accounts/`, `categories/`, `transactions/`
