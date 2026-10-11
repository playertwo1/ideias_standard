# ROADMAP — {{nome do projeto}}

**Visão:** [PROJECT.md](PROJECT.md) · **Onde paramos:** [STATE.md](STATE.md) · **Como fechar:** [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md)

Roadmap diz **quando e o quê**; spec diz o comportamento; plano diz como; review prova. Detalhe só o marco ativo; os demais ficam com objetivo e gate. Marco fechado sai daqui: uma linha em "Entregues" e o texto completo em `docs/arquivo/`.

## Estados e prioridade
`BACKLOG` · `READY` · `IN_PROGRESS` · `BLOCKED` · `REVIEW` · `DONE` (só com evidência; aprovação humana é registrada à parte).
P0 bloqueia o fluxo principal · P1 sustenta o MVP · P2 melhoria · P3 futuro.

## Marcos
| Marco | Resultado verificável | Estado | Gate |
|---|---|---|---|
| D0 — Descoberta | MVP, riscos e decisão GO/NO-GO | BACKLOG | Produto define escopo |
| v0.1 — Fatia vertical | Um fluxo ponta a ponta no ambiente real | BACKLOG | Demonstração com evidência |
| v0.2 — MVP | Fluxos do `PROJECT.md` integrados | BACKLOG | Critérios do `PROJECT.md` |
| v0.3 — Estabilização | Sem bug crítico, segurança básica | BACKLOG | Verificação independente |
| v1.0 — Entrega | Instalação e uso repetíveis | BACKLOG | Checklist de release + aprovação |

## Marco ativo — {{ID}}
**Objetivo de produto:** {{...}} · **Quem valida:** {{papel}}

| ID | Tarefa | Prioridade | Depende de | Estado | Evidência exigida |
|---|---|---|---|---|---|
| {{V01-01}} | {{fluxo visível}} | P0 | — | READY | {{teste + demonstração}} |

**Gate de saída:** {{critério observável}} · **Riscos:** {{...}}

## Ideias futuras (não autorizadas)
| Ideia | Impacto esperado | Quando reavaliar |
|---|---|---|
| {{...}} | {{...}} | {{...}} |

## Entregues
| Marco | Data | Commit/evidência |
|---|---|---|

## Mudanças de escopo
- {{data}} {{mudança}} — {{decisão em docs/DECISIONS.md}}
