# Agentes de IA do Projeto (Pivot)

Índice dos agentes especializados que suportam o ciclo de desenvolvimento. Use conforme o PRD (PRD.md) e a documentação (docs/readme.md).

- Backend Django + DRF: backend-django.md
  - Models, serializers, ViewSets/CBVs, URLs, signals e integrações (JWT opcional).
- Frontend DTL + TailwindCSS: frontend-dtl-tailwind.md
  - Templates DTL, design system, responsividade e acessibilidade.
- QA Tester: qa-tester.md
  - Planejamento e validações manuais, critérios de aceite e checklist.
- Projection Engine: projection-engine.md
  - Algoritmo de projeção diária (24 meses+), faturas e cache incremental.
- Import Mapper: import-mapper.md
  - Importação XLSX/CSV com openpyxl e mapeamento de colunas.

Princípios gerais
- Simplicidade; seguir PRD/docs; evitar over‑engineering.
- Código em inglês; UI pt‑BR; PEP 8; aspas simples; CBVs/DRF; SQLite em dev.
- Design: tema escuro com gradientes; componentes consistentes (docs/design-system.md).
- Contexto BR: BRL, timezone America/Sao_Paulo, datas DD‑MM‑YYYY.

