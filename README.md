# Ideias Standard

**Ideias Standard** é um padrão executável, versionado e atualizável para criar e manter projetos preparados para agentes de IA.

Ele não é apenas um template. O objetivo é definir um ciclo de vida comum para projetos novos e existentes:

`Idea → Project Manifest → Ideias Standard → projeto operacional → check/doctor/adopt/upgrade → contexto mínimo por tarefa`

## Princípios

- uma fonte canônica por tipo de informação;
- contexto mínimo suficiente, carregado progressivamente;
- evidência antes de PASS;
- autoridade humana separada de sugestão de IA;
- perfis proporcionais ao risco: LIGHT / STANDARD / DEEP;
- packs composáveis por capacidade;
- bundles e workflows versionados sem ampliar autoridade;
- ownership por artefato: MANAGED / MERGEABLE / USER_OWNED;
- padrão versionado com lock, provenance e migrations;
- adoção de projetos legados sem reescrever o que já funciona;
- independência de Codex, Claude, Gemini ou outro agente específico;
- `NOT_RUN != PASS`.

## Modelo de composição

`BASE + PROFILE + PACKS + PROJECT RULES = PROJECT CONTRACT`

Perfis definem profundidade de governança. Packs adicionam capacidades. Bundles são composições reutilizáveis de profile + packs + workflow + adapters, mas continuam derivados do contrato canônico.

## Fundação v0.1

Já estão materializados:

- `STANDARD.md`;
- schemas de project manifest, standard lock, context manifest, artifact policy, bundle, workflow, change e conformance report;
- perfis LIGHT/STANDARD/DEEP;
- packs Android, Python, backend, AI, sensitive-data e multi-agent;
- bundles iniciais;
- workflows `default` e `migration-first`;
- catálogo de adapters com status ACTIVE/PLANNED;
- ownership e lifecycle de upgrade/adopt;
- fixtures positivas e adversariais;
- validador estrutural + semântico com códigos determinísticos;
- matriz de referências e roadmap de evolução.

Ainda não existe CLI completa de `init/check/doctor/adopt/upgrade`; o validador atual é a fundação do futuro `check`.

## Validação local

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_standard.py examples/standard-android-ai/project-manifest.json
python -m unittest scripts.test_validate_standard -v
```

O contrato dos códigos está em `VALIDATION_CONTRACT.md`.

## Lifecycle seguro

- novo projeto: manifest → dry-run → diff → materialize → validate → lock;
- brownfield: inventory → recommend → preview → adopt → validate → lock;
- upgrade: check → render target → three-way diff → conflicts → preview → apply → validate → new lock;
- feature/correção: change unit → delta + invariantes → implementação → validação proporcional → fechamento.

Veja `docs/LIFECYCLE_MODEL.md` e `docs/OWNERSHIP_AND_UPGRADE.md`.

## Relação com o projeto Idea

O **Idea** decide o que um projeto precisa e pode gerar o `project-manifest`.

O **Ideias Standard** compila esse manifesto em estrutura, contratos, templates e validações reutilizáveis.

O **projeto gerado** contém apenas o necessário para seu perfil, packs e regras específicas. Ele não herda toda a documentação interna do Idea nem do Standard.

## Estado

Consulte `PROJECT_STATE.md` para o estado operacional atual e `ROADMAP.md` para a evolução planejada.
