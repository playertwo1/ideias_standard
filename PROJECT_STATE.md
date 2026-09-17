# IDEIAS STANDARD — PROJECT STATE

- **Versão do repositório:** 0.1.0-draft
- **Modelo atual:** Gold V5
- **Fase atual:** F0 — Golden Standard
- **Status:** ACTIVE
- **Objetivo atual:** consolidar a menor base reutilizável que torne um projeto fácil de entender, verificar, auditar e manter com alto sinal e baixo desperdício de contexto.

## Mudança de direção

A arquitetura anterior baseada em S0–S8, profiles, bundles, gates e lifecycle amplo foi substituída pelo modelo Gold.

O trabalho antigo não é descartado automaticamente. Scripts, schemas, packs, fixtures e validadores existentes serão mantidos somente quando simplificarem ou protegerem comportamento útil no novo Standard.

Não continuar a antiga sequência S1-C10–C33.

## Foco de F0

- manter `AGENTS.md` como contexto mínimo universal;
- usar `AGENTS.md + pedido atual` como bootstrap padrão;
- consolidar `STANDARD.md` e `README.md` no modelo Gold;
- formalizar Token Discipline: localizar antes de ler, menor trecho suficiente e outputs resumidos;
- definir estrutura mínima do projeto Gold;
- definir mecanismo simples de `check` com saída curta e detalhes sob demanda;
- manter CI e testes essenciais;
- executar a trilha F0-SK de pesquisa e adaptação de Skills maduras;
- priorizar `gold-audit`, `goldify` e `skill-author`;
- revisar ativos legados e remover complexidade sem função prática;
- criar um exemplo Gold completo;
- realizar uma auditoria independente final da fase.

## Princípios ativos

- Small Core;
- Progressive Context;
- Token Discipline;
- Executable Verification;
- Independent Audit;
- Optional Packs & Skills;
- No Overengineering;
- Preserve Existing Work;
- Security Proportional to Risk.

## Trilha F0-SK — Skills Gold

Fontes prioritárias já identificadas para estudo:

- Agent Skills specification;
- Anthropic Claude Code `skill-development`;
- OpenAI Codex `code-review`;
- Trail of Bits `second-opinion`;
- Trail of Bits `audit-context-building`;
- GitHub Awesome Copilot `ai-ready`;
- GitHub Awesome Copilot `acquire-codebase-knowledge`;
- GitHub Awesome Copilot `agent-skill-stack`;
- referências opcionais de `security-review`, `secret-scanning` e `agentic-eval`.

Ordem de construção planejada:

1. `gold-audit`;
2. `goldify`;
3. `skill-author`;
4. `skill-curator` somente se houver necessidade comprovada.

Skills externas seguem:

`DISCOVER → REVIEW → TRIM → ADAPT → TEST → INSTALL`

Nenhuma Skill é incorporada apenas por popularidade. Utilidade, segurança, licença, sobreposição, custo de contexto e teste mínimo precisam justificar sua adoção.

## Builder ↔ Auditor

O Standard define o fluxo mínimo de Builder, `check`, diff e Auditor independente.

A automação desse ciclo continua separada no repositório:
https://github.com/playertwo1/runner

O Runner é opcional e não bloqueia o desenvolvimento do Standard.

## Transição técnica

`VERSION`, `COMPATIBILITY.yaml`, scripts, schemas e fixtures ainda podem refletir partes do modelo 0.1 anterior durante F0.

Não alterar esses ativos apenas para fazê-los parecer alinhados documentalmente. Cada um deve ser revisado contra o Gold Standard antes de ser mantido, simplificado ou removido.

## Próxima ação

1. estudar em profundidade as fontes de `gold-audit`;
2. extrair apenas os padrões úteis de revisão independente, second opinion e expansão progressiva de contexto;
3. desenhar a primeira versão provider-neutral de `gold-audit`;
4. criar fixtures mínimos com um diff correto e um diff com bug proposital;
5. testar antes de promover a Skill para uso no Template Gold.
