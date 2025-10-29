# Boas práticas de código

Pragmáticas, alinhadas ao Django e sem over‑engineering. Introduza abstrações quando houver repetição, regras de negócio em crescimento ou acoplamento excessivo. Mantenha o foco em clareza, consistência e simplicidade.

## Princípios SOLID (no contexto Django)
- Single Responsibility (SRP)
  - Views orquestram fluxo; regras de negócio ficam em `models` (métodos de domínio), `forms` (validações) ou `services.py`.
  - Evite views com responsabilidades múltiplas e longas.
- Open/Closed (OCP)
  - Estenda CBVs com mixins e métodos (`get_queryset`, `get_context_data`, `form_valid`) ao invés de copiar código.
  - Validações extensíveis em `clean()` de `Model`/`Form` e validadores simples reutilizáveis.
- Liskov Substitution (LSP)
  - Subclasses/mixins devem preservar contratos: mesmos nomes/semântica de métodos e contextos esperados por templates/URLs.
- Interface Segregation (ISP)
  - Serviços e helpers com assinaturas pequenas e focadas. Evite “objetos canivete suíço”.
- Dependency Inversion (DIP)
  - Views dependem de serviços/seletores (abstrações simples), não de queries/implementações de baixo nível embutidas.

## Design Patterns recomendados (Django‑friendly)
- Template Method (CBV)
  - Especialize o fluxo sobrescrevendo métodos padrão da CBV sem duplicar lógica.
- Service Layer (`services.py`)
  - Operações de escrita/efeitos colaterais atômicos (ex.: registrar transação e atualizar saldo) com `transaction.atomic()` quando necessário.
- Selectors (`selectors.py`)
  - Consultas de leitura e agregações reutilizáveis (ex.: saldo por período/conta/categoria) mantendo views finas.
- Strategy
  - Alternar regras de cálculo/filtragem (ex.: critério de saldo) por injeção de estratégia no serviço.
- Repository (idiomático no Django)
  - Use `QuerySet`/`Manager` personalizados para encapsular consultas recorrentes; evite camadas artificiais quando o ORM já resolve.
- Observer (Signals)
  - Eventos de domínio em `signals.py` (ex.: criar `Profile` após novo `User`), importados em `apps.py`.
- Decorator
  - Preocupações transversais (auth, cache, auditoria) via decoradores (`login_required`, `permission_required`) ou pequenos wrappers.
- Facade
  - Uma interface simples para compor dados do dashboard (totais, recentes), escondendo chamadas múltiplas internas.

## Estrutura leve por app (opcional, incremental)
- `models.py`: lógica de domínio enxuta e coesa; timestamps padrões.
- `forms.py`: validações e UX de formulário.
- `views.py`: orquestração via CBVs; mínimo de regra de negócio.
- `services.py`: comandos de domínio que escrevem/alteram estado.
- `selectors.py`: consultas de leitura/relatórios.
- `managers.py`: `QuerySet`/`Manager` custom quando operações se repetem.
- `signals.py`: observers de eventos do domínio.

## Do’s & Don’ts
- Prefira “fat models, thin views” com services/selectors onde fizer sentido.
- Prefira CBVs/mixins a copiar e colar lógica.
- Evite abstrações prematuras; extraia quando houver repetição clara.
- Evite estado global para regras de negócio; passe dependências por parâmetro.
- Evite lógica de negócio em templates; templates servem apenas à apresentação.

## Transações e consistência
- Use `transaction.atomic()` em operações que tocam múltiplas tabelas.
- Valide entradas em `forms` e/ou `clean()` dos `models` para preservar invariantes do domínio.

## Testabilidade (quando testes forem introduzidos)
- Services/selectors devem ser pequenos e fáceis de testar em isolamento.
- Prefira funções puras quando possível e minimize efeitos colaterais.

