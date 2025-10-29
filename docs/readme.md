# Documenta��ǜo do Projeto (docs)

Bem-vindo �� documenta��ǜo do Finanpy. Este ��ndice aponta para os guias essenciais do reposit��rio. Documentamos apenas o que existe no projeto hoje e referǦncias diretas ao PRD.

- Visǜo geral: [overview.md](overview.md)
- Configura��ǜo e execu��ǜo: [setup.md](setup.md)
- Estrutura de pastas: [structure.md](structure.md)
- Conven����es e padr��es: [conventions.md](conventions.md)
- Design system (diretrizes): [design-system.md](design-system.md)
- Boas práticas de código (SOLID e Design Patterns): [best-practices.md](best-practices.md)
- PRD do produto: ../PRD.md

Extras opcionais
- Leitura de Excel (fórmulas via openpyxl): instale com `pip install -r requirements.txt -r requirements-excel.txt`.
 - Util para leitura: `core/utils/excel.py` → `from core.utils.excel import read_sheet_as_dicts`
   - Exemplo rápido: `rows = read_sheet_as_dicts('dados.xlsx', sheet='Transacoes')`
