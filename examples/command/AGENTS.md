# AGENTS.md — Command

Regras comuns: as 10 do [template](../../template/AGENTS.md), sem alteração. Comece por `STATE.md`.

## Comandos
- Verificar tudo: `./gradlew check && pytest agent/`
- Rodar o agente local: `python -m agent --dev`

## Regras deste projeto
- Nenhum endpoint de controle exposto à internet; só rede local autenticada.
- Comando que altera o PC (abrir/encerrar app) só da allowlist e com confirmação no celular.
- Token de pareamento nunca aparece em tela, log ou evidência.

## Git
- Branch curta + PR revisado por outro agente; push na main só após review `PASS`.
