# STATE — ponto de retomada

**Atualizado:** 2026-10-11 · **Marco ativo:** v0.1 · **Estado:** IN_PROGRESS

## O que funciona hoje (confirmado no código)
- Agente local responde `/status` com RAM/CPU e recusa pedido sem token (401).

## Última atividade
- ID: V01-01 · commit `abc1234`
- Testes executados: `pytest agent/` → PASS (12); teste no aparelho real → NOT_RUN
- Evidência: `docs/reviews/V01-01.md`

## Próxima ação
- V01-02 — tela de status no app mostrando "indisponível" quando o PC está offline; começar por `app/src/.../StatusScreen.kt`; depende do token de pareamento já salvo.

## Bloqueios e aprovações humanas
- Nenhum.

## Divergências entre roadmap e implementação
- Temperatura não é exposta pelo sensor desta placa; AC-03 cobre o caso ("não informado").
