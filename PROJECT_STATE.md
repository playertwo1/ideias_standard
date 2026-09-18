# IDEIAS STANDARD — PROJECT STATE

- **Versão do repositório:** 0.1.0-draft
- **Modelo atual:** Gold V5
- **Fase atual:** F4 — ADOPT / GOLDIFY
- **Status:** ACTIVE
- **Objetivo atual:** F4 — Goldify somente leitura e Golden Diff mínimo; aguarda auditoria independente.
- **Evidência F0-SK:** `F0_SK_EVIDENCE.json` referencia fixtures e Skills por SHA-256; `scripts.test_gold_skills` reproduz as provas locais.

## Direção atual

A arquitetura anterior baseada em S0–S8, profiles, bundles, gates e lifecycle amplo foi substituída pelo modelo Gold.

O trabalho antigo não é descartado automaticamente. Scripts, schemas, packs, fixtures e validadores existentes serão mantidos somente quando simplificarem ou protegerem comportamento útil no novo Standard.

Não continuar a antiga sequência S1-C10–C33.

## Regras de execução ativas

### Dogfooding obrigatório

O próprio `ideias_standard` deve seguir o Gold que recomenda. Práticas aplicáveis devem ser exercitadas aqui, em fixture, exemplo Gold ou projeto real antes de serem promovidas aos templates futuros.

### Prove Before Expand

Nova Skill, pack, regra, arquivo ou abstração só entra no Gold reutilizável depois de resolver problema real, ser testada e demonstrar benefício claro.

Se a necessidade for local, a solução permanece local.

## Foco de F0

- manter `AGENTS.md` como contexto mínimo universal;
- usar `AGENTS.md + pedido atual` como bootstrap padrão;
- manter `STANDARD.md`, `ROADMAP.md` e `README.md` coerentes com o Gold;
- aplicar Token Discipline: localizar antes de ler, menor trecho suficiente e outputs resumidos;
- definir estrutura mínima do projeto Gold;
- definir `check` simples, com saída curta e detalhes sob demanda;
- manter CI e testes essenciais;
- executar F0-SK de pesquisa e adaptação de Skills maduras;
- priorizar `gold-audit`, `goldify` e `skill-author`;
- revisar ativos legados e remover complexidade sem função prática;
- dogfood as práticas Gold no próprio repositório;
- criar um exemplo Gold completo;
- realizar auditoria independente final de F0.

## Princípios ativos

- Small Core;
- Progressive Context;
- Token Discipline;
- Executable Verification;
- Independent Audit;
- Optional Packs & Skills;
- No Overengineering;
- Preserve Existing Work;
- Security Proportional to Risk;
- Dogfooding;
- Prove Before Expand.

## Trilha F0-SK — Skills Gold

Fontes prioritárias já identificadas:

- Agent Skills specification;
- Anthropic Claude Code `skill-development`;
- OpenAI Codex `code-review`;
- Trail of Bits `second-opinion`;
- Trail of Bits `audit-context-building`;
- GitHub Awesome Copilot `ai-ready`;
- GitHub Awesome Copilot `acquire-codebase-knowledge`;
- GitHub Awesome Copilot `agent-skill-stack`;
- referências opcionais de `security-review`, `secret-scanning` e `agentic-eval`.

Ordem planejada:

1. `gold-audit`;
2. `goldify`;
3. `skill-author`;
4. `skill-curator` somente se houver necessidade comprovada.

Skills externas seguem:

`DISCOVER → REVIEW → TRIM → ADAPT → TEST → INSTALL`

Nenhuma Skill entra apenas por popularidade. Utilidade, segurança, licença, sobreposição, custo de contexto e teste mínimo precisam justificar sua adoção.

## Builder ↔ Auditor

O Standard define o fluxo mínimo de Builder, `check`, diff e Auditor independente.

A automação continua separada em:
https://github.com/playertwo1/runner

O Runner é opcional e não bloqueia o desenvolvimento do Standard.

## Transição técnica

`VERSION`, `COMPATIBILITY.yaml`, scripts, schemas e fixtures ainda podem refletir partes do modelo 0.1 anterior durante F0.

Não alterar esses ativos apenas para fazê-los parecer alinhados documentalmente. Cada um deve ser revisado contra o Gold antes de ser mantido, simplificado ou removido.

## Próxima ação

1. executar auditoria independente de F4 no SHA final;
2. manter F5 não iniciada.
