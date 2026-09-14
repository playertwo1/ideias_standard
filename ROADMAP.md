# Roadmap — Ideias Standard

## S0 — Fundação do padrão

Objetivo: definir o contrato antes da implementação.

- [x] Missão e fronteira
- [x] STANDARD.md
- [x] AGENTS.md
- [x] PROJECT_STATE.md
- [x] Schemas estruturados iniciais
- [x] Perfis LIGHT/STANDARD/DEEP
- [x] Packs iniciais
- [x] Política de ownership/upgrade
- [x] Exemplos positivos de manifest
- [ ] Fixtures negativas/adversariais
- [ ] Validador determinístico

**Gate S0:** schemas válidos, fixtures reproduzíveis e zero ambiguidade material entre profile, pack, capability, authority e ownership.

## S1 — Conformance first

Objetivo: provar que o Standard consegue verificar um projeto antes de gerar projetos.

- `check`: valida manifest, lock, contexto, ownership, arquivos obrigatórios e compatibilidade;
- `doctor`: diagnóstico legível por humanos;
- detecção de status duplicado, adapters divergentes e arquivos ausentes;
- códigos determinísticos para falhas;
- relatório PASS/FAIL/WARN sem percentual cosmético como fonte de verdade;
- modo não interativo para automação.

**Gate S1:** fixture correta passa; fixtures quebradas falham com códigos previsíveis.

## S2 — Init / compiler

Objetivo: gerar projeto mínimo a partir de manifesto.

- compor BASE + PROFILE + PACKS + PROJECT RULES;
- materializar arquivos apenas quando aplicáveis;
- gerar lock/fingerprint/provenance;
- classificar artefatos como MANAGED/MERGEABLE/USER_OWNED;
- dry-run e diff antes de escrever;
- detectar conflitos entre packs;
- adapters iniciais para agentes sem criar fontes de verdade concorrentes.

**Gate S2:** geração determinística e idempotente para fixtures LIGHT/STANDARD/DEEP.

## S3 — Adopt / Brownfield

Objetivo: trazer projetos existentes para o padrão como caso de primeira classe.

- inventário read-only;
- recomendação de profile/packs;
- gap analysis;
- mapear equivalências existentes;
- baseline sintético controlado;
- plano de adoção;
- preview antes de alterações;
- arquivos existentes são USER_OWNED por padrão;
- proteção a arquivos existentes e overrides locais.

**Gate S3:** adoção de fixture legacy sem perda de conteúdo válido e sem overwrite implícito.

## S4 — Upgrade lifecycle

Objetivo: evoluir projetos já gerenciados.

- versionamento semântico do Standard;
- `standard.lock` com provenance por artefato;
- migrations versionadas;
- renderização da versão alvo em staging;
- comparação baseline anterior × local × alvo;
- `diff` antes de aplicar;
- merge para artefatos MERGEABLE;
- detecção de conflitos locais;
- rollback/recuperação quando seguro;
- atualizar lock somente após validação.

**Gate S4:** upgrade e rollback de fixtures preservam regras e customizações específicas do projeto.

## S5 — Context lifecycle

Objetivo: compilar contexto mínimo verificável por tarefa.

- REQUIRED / CONDITIONAL / DISCOVERY;
- why-included / why-excluded;
- fingerprints por bloco;
- delta-context;
- byte-cap de saídas potencialmente grandes;
- validação proporcional ao risco;
- budgets e `CONTEXT_OVERFLOW`;
- benchmark de critical recall e irrelevant context.

**Gate S5:** 100% das obrigações críticas da fixture presentes com redução mensurável de contexto.

## S6 — Ecosystem adapters, workflows e bundles

Objetivo: interoperar sem acoplamento e permitir composição reutilizável.

- Codex;
- Claude;
- Gemini;
- generic;
- workflow schemas declarativos;
- bundles versionados de profile + packs + adapters;
- conflict checks e provenance por bundle;
- formatos externos úteis somente via adapters.

**Gate S6:** adapters materializam instruções equivalentes sem divergência canônica e bundles não ampliam autoridade silenciosamente.

## S7 — Integração com Idea

Objetivo: Idea gerar manifestos consumíveis pelo Standard.

- contrato de handoff Idea → Standard;
- export versionado;
- import/validation;
- fixtures ponta a ponta;
- separação entre produto Idea e lifecycle Standard.

**Gate S7:** projeto criado pelo Idea pode ser compilado e validado pelo Standard sem reconstruir a conversa original.

## S8 — Change lifecycle

Objetivo: tratar evolução de features sem regenerar contexto global.

- change unit por feature/correção;
- delta de requirements/decisions;
- impacto explícito sobre artefatos derivados;
- arquivo/fechamento de change concluída;
- contexto de implementação baseado no delta + invariantes vigentes.

**Gate S8:** mudança pequena pode ser planejada, implementada e auditada sem carregar ou reescrever o projeto inteiro.

## Princípio de avanço

Não implementar a fase seguinte para compensar contrato incompleto da anterior. Estado real em `PROJECT_STATE.md`.
