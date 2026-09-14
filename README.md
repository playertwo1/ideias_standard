# Ideias Standard

**Ideias Standard** é um padrão executável, versionado e atualizável para criar e manter projetos preparados para trabalhar com agentes de IA.

Ele não é apenas um template. O objetivo é definir um ciclo de vida comum para projetos novos e existentes:

`Idea → Project Manifest → Ideias Standard → projeto operacional → check/doctor/adopt/upgrade → contexto mínimo por tarefa`

## Princípios

- uma fonte canônica por tipo de informação;
- contexto mínimo suficiente, carregado progressivamente;
- evidência antes de PASS;
- autoridade humana separada de sugestão de IA;
- perfis proporcionais ao risco: LIGHT / STANDARD / DEEP;
- packs composáveis por capacidade, sem transformar todo projeto em DEEP;
- padrão versionado com lock e migrações;
- adoção de projetos legados sem reescrever o que já funciona;
- independência de Codex, Claude, Gemini ou outro agente específico;
- `NOT_RUN != PASS`.

## Modelo de composição

`STANDARD BASE + PROFILE + PACKS + PROJECT RULES = PROJECT AGENT CONTRACT`

Perfis definem profundidade de governança. Packs adicionam capacidades específicas, por exemplo Android, AI, dados sensíveis ou multiagente.

## v0.1 — fundação

A primeira versão formaliza:

- contrato do Standard;
- `project-manifest`;
- `standard-lock`;
- `context-manifest`;
- perfis LIGHT/STANDARD/DEEP;
- catálogo inicial de packs;
- política de contexto progressivo;
- roadmap de `init`, `check`, `doctor`, `adopt`, `upgrade`, `diff` e `compile-context`.

Ainda não existe CLI funcional nesta versão documental.

## Relação com o projeto Idea

O **Idea** decide o que um projeto precisa e pode gerar o `project-manifest`.

O **Ideias Standard** compila esse manifesto em estrutura, contratos, templates e validações reutilizáveis.

O **projeto gerado** contém apenas o necessário para seu perfil, packs e regras específicas. Ele não herda toda a documentação interna do Idea nem do Standard.

## Estado

Consulte `PROJECT_STATE.md` para o estado operacional atual e `ROADMAP.md` para a evolução planejada.
