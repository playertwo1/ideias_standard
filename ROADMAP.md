# Roadmap — Ideias Standard

## S0 — Fundação do padrão

Objetivo: definir o contrato antes da implementação.

- [x] Missão e fronteira
- [x] STANDARD.md
- [x] AGENTS.md
- [x] PROJECT_STATE.md
- [ ] Schemas estruturados
- [ ] Perfis LIGHT/STANDARD/DEEP
- [ ] Packs iniciais
- [ ] Fixtures válidas e inválidas
- [ ] Validador determinístico

**Gate S0:** schemas válidos, fixtures reproduzíveis e zero ambiguidade material entre perfil, pack, capability e autoridade.

## S1 — Conformance first

Objetivo: provar que o Standard consegue verificar um projeto antes de gerar projetos.

- `check`: valida manifest, lock, contexto, arquivos obrigatórios e compatibilidade;
- `doctor`: diagnóstico legível por humanos;
- detecção de status duplicado, adapters divergentes e arquivos ausentes;
- relatório PASS/FAIL/WARN sem percentual cosmético como fonte de verdade.

**Gate S1:** fixture correta passa; fixtures quebradas falham com códigos previsíveis.

## S2 — Init / compiler

Objetivo: gerar projeto mínimo a partir de manifesto.

- compor BASE + PROFILE + PACKS + PROJECT RULES;
- materializar arquivos apenas quando aplicáveis;
- gerar lock/fingerprint;
- dry-run e diff antes de escrever;
- adapters iniciais para agentes sem criar fontes de verdade concorrentes.

**Gate S2:** geração determinística e idempotente para fixtures LIGHT/STANDARD/DEEP.

## S3 — Adopt

Objetivo: trazer projetos existentes para o padrão.

- inventário read-only;
- recomendação de perfil/packs;
- gap analysis;
- plano de adoção;
- preview antes de alterações;
- proteção a arquivos existentes e overrides locais.

**Gate S3:** adoção de fixture legacy sem perda de conteúdo válido.

## S4 — Upgrade lifecycle

Objetivo: evoluir projetos já gerenciados.

- versionamento semântico do Standard;
- `standard.lock`;
- migrations versionadas;
- `diff` entre versão instalada e alvo;
- detecção de conflitos locais;
- rollback/recuperação quando seguro.

**Gate S4:** upgrade e rollback de fixtures preservam regras específicas do projeto.

## S5 — Context lifecycle

Objetivo: compilar contexto mínimo verificável por tarefa.

- REQUIRED / CONDITIONAL / DISCOVERY;
- why-included / why-excluded;
- fingerprints por bloco;
- delta-context;
- budgets e `CONTEXT_OVERFLOW`;
- benchmark de critical recall e irrelevant context.

**Gate S5:** 100% das obrigações críticas da fixture presentes com redução mensurável de contexto.

## S6 — Ecosystem adapters

Objetivo: interoperar sem acoplamento.

- Codex;
- Claude;
- Gemini;
- generic;
- formatos externos úteis somente via adapters.

**Gate S6:** adapters materializam instruções equivalentes sem divergência canônica.

## S7 — Integração com Idea

Objetivo: Idea gerar manifestos consumíveis pelo Standard.

- contrato de handoff Idea → Standard;
- export versionado;
- import/validation;
- fixtures ponta a ponta;
- separação entre produto Idea e lifecycle Standard.

**Gate S7:** projeto criado pelo Idea pode ser compilado e validado pelo Standard sem reconstruir a conversa original.

## Princípio de avanço

Não implementar a fase seguinte para compensar contrato incompleto da anterior. Estado real em `PROJECT_STATE.md`.
