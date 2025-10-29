# PR: Pivot → DRF + Projeção financeira (planilha -> app)

## Resumo
- Atualiza PRD para o novo escopo: proje��o di�ria 24+ meses, cart�es/faturas, budgets vari�veis e economias.
- Alinha AGENTS.md e agentes (backend DRF, projection-engine, import-mapper, frontend, QA).
- Atualiza README com esqueleto da API e instru��es de instala��o de extras (DRF/JWT e openpyxl).
- Adiciona requirements-api.txt.

## Por qu�
- Substituir a planilha e projetar impacto futuro conforme regras do PRD (pivot) e estrutura da planilha-base.

## Escopo
- docs: PRD.md, AGENTS.md, agents/*, README.md
- scripts: util para inspecionar XLSX sem depend�ncias (j� em branch anterior)
- requirements: extras opcionais (api, excel)

## Como validar
- Ler PRD.md e confirmar RF/RN/Modelos/API/Algoritmo.
- Conferir AGENTS.md e agentes especializados.
- Instalar extras (opcionais): -r requirements-api.txt e -r requirements-excel.txt.

## Pr�ximos passos
- Implementar modelos e serializers do pivot.
- Endpoints DRF + proje��o /api/projection/.
- Importador XLSX (openpyxl) e builder de faturas.