# IDEIAS STANDARD — PROJECT STATE

- **Versão:** 0.2.0-draft
- **Fase atual:** F0 — Golden Standard
- **Status:** ACTIVE
- **Roadmap:** V5 — Gold
- **Objetivo atual:** consolidar a menor base reutilizável que torne um projeto fácil de entender, verificar, auditar e manter.

## Mudança de direção

A arquitetura anterior baseada em S0–S8, profiles, bundles, gates e lifecycle amplo foi substituída pelo modelo Gold.

O trabalho antigo não é descartado automaticamente. Scripts, schemas, packs, fixtures e validadores existentes serão mantidos somente quando simplificarem ou protegerem comportamento útil no novo Standard.

Não continuar a antiga sequência S1-C10–C33.

## Foco de F0

- reduzir `AGENTS.md` ao contexto mínimo universal;
- consolidar `STANDARD.md` e `README.md` no modelo Gold;
- definir a estrutura mínima do projeto Gold;
- definir mecanismo simples de `check`;
- manter CI e testes essenciais;
- revisar ativos legados e remover complexidade sem função prática;
- criar um exemplo Gold completo;
- realizar uma auditoria independente final da fase.

## Princípios ativos

- Small Core;
- Progressive Context;
- Executable Verification;
- Independent Audit;
- Optional Packs;
- No Overengineering;
- Preserve Existing Work;
- Security Proportional to Risk.

## Builder ↔ Auditor

O Standard define o fluxo mínimo de Builder, `check`, diff e Auditor independente.

A automação desse ciclo continua separada no repositório:
https://github.com/playertwo1/runner

O Runner é opcional e não bloqueia o desenvolvimento do Standard.

## Próxima ação

Revisar a estrutura e os ativos existentes do repositório contra o Gold Standard e classificar cada item como:

- manter;
- simplificar;
- mover para pack/Skill;
- remover/arquivar.
