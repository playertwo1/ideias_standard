# Roadmap — Ideias Standard

## S0 — Fundação do padrão

Objetivo: definir e provar o contrato antes da implementação da CLI.

- [x] Missão e fronteira
- [x] STANDARD.md / AGENTS.md / PROJECT_STATE.md
- [x] Schemas estruturados iniciais
- [x] Perfis LIGHT/STANDARD/DEEP e packs iniciais
- [x] Política de ownership/upgrade
- [x] Bundles, workflows, adapters e change lifecycle iniciais
- [x] Conformance report e validation contract
- [x] Registry estruturado de invariantes críticos
- [x] Matriz de compatibilidade + contrato de versionamento
- [x] Contrato da futura CLI e exit codes
- [x] Fixtures positivas e adversariais
- [x] Manifesto central de fixtures com resultados esperados
- [x] Golden outputs para invariantes críticos
- [x] Validador estrutural + semântico
- [x] Self-check de schemas, catálogos, invariantes, bundles e workflows
- [x] Testes automatizados data-driven
- [x] GitHub Actions em Python 3.11/3.12/3.13 com artefatos de evidência
- [x] Suíte completa executada com matriz verde e evidência registrada
- [x] Finding inicial de CI corrigido e revalidado
- [x] Contratos de handoff Builder/Auditor e policy/state de orquestração multiagente
- [x] Workflow `builder-auditor-loop` com SHA de auditoria imutável, loop limitado e gate humano
- [x] Máquina de estados provider-neutral para handoffs e registro explícito de gate
- [x] Fixtures e testes adversariais de orquestração integrados à conformance
- [x] Revalidar S0 após extensão de orquestração autorizada pela Product Authority
- [ ] Auditoria independente S0

**Gate S0:** schemas válidos; self-check PASS; fixtures reproduzíveis; golden outputs estáveis; CI verde nas versões Python suportadas; invariantes críticos protegidos; orquestração multiagente não amplia autoridade e mantém Builder/Auditor separados, SHA auditado imutável, loop limitado e gate humano; zero ambiguidade material entre profile, pack, capability, authority, ownership, bundle, workflow e compatibilidade; auditoria independente sem finding bloqueante.

## S1 — Conformance first

Objetivo: transformar o núcleo validado em interface estável de conformance.

- `check`: valida manifest, lock, contexto, ownership, arquivos obrigatórios e compatibilidade;
- `doctor`: explica os mesmos findings do `check` em linguagem humana;
- detecção de status duplicado, adapters divergentes e arquivos ausentes;
- códigos determinísticos para falhas;
- relatório PASS/FAIL/WARN sem percentual cosmético como fonte de verdade;
- modo não interativo para automação;
- saída estruturada compatível com `conformance-report.schema.json`;
- comportamento e exit codes conforme `CLI_CONTRACT.md`.

**Gate S1:** fixture correta passa; fixtures quebradas falham com códigos previsíveis; `doctor` explica os mesmos findings sem criar uma segunda regra.

## S2 — Init / compiler

Objetivo: gerar projeto mínimo a partir de manifesto.

- compor BASE + PROFILE + PACKS + PROJECT RULES;
- materializar arquivos apenas quando aplicáveis;
- gerar lock/fingerprint/provenance;
- classificar artefatos como MANAGED/MERGEABLE/USER_OWNED;
- dry-run e diff antes de escrever;
- detectar conflitos entre packs;
- expandir bundle para composição explícita;
- adapters iniciais sem criar fontes de verdade concorrentes.

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
- runners específicos que consumam o contrato provider-neutral de orquestração sem ampliar autoridade;
- workflow schemas declarativos;
- bundles versionados de profile + packs + adapters;
- conflict checks e provenance por bundle;
- formatos externos úteis somente via adapters.

**Gate S6:** adapters materializam instruções equivalentes sem divergência canônica, runners preservam os mesmos handoffs/invariantes e bundles não ampliam autoridade silenciosamente.

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
