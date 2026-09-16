# O0 v2 M1 — ensaio parcial (BLOCKED)

Base: `7f2bb68d9e9475da9a52ef4e5622a6086bcb8925`. Ambiente: Windows, PowerShell, 2026-09-16. Nenhuma aprovação de gate foi inferida.

## CLIs

- `where.exe agy` → `C:\Users\fael\AppData\Local\Programs\Antigravity IDE\bin\agy.cmd`. O alias continua apontando para o IDE, não para a CLI headless. Na repetição, `C:\Users\fael\AppData\Local\agy\bin\agy.exe` passou a existir: versão `1.2.4`, com `-p`, `--output-format` e `--print-timeout`.
- `codex --version` → `codex-cli 0.154.0`; `codex login status` → `Logged in using ChatGPT`; `codex exec --help` confirma `-C`, `-s read-only`, `--json` e `--ephemeral`.

## Repositório descartável e prova parcial Codex

Comandos executados (os nomes dos diretórios são desta execução):

```powershell
git -C $probe init -b main
git -C $probe -c user.name='M1 Probe' -c user.email='m1@example.invalid' commit --allow-empty -m baseline
$sha = git -C $probe rev-parse HEAD
git clone --no-local $probe $audit
git -C $audit checkout --detach $sha
codex exec -C $audit -s read-only --json --ephemeral 'Audit only. Read git HEAD and git status in this checkout. Return a JSON object with audited_sha, clean, verdict. Do not modify files.'
```

- Builder/probe: `C:\Users\fael\AppData\Local\Temp\o0v2-m1-d9e00c727cc841cabe438bff5a1e2ba3`.
- Auditor: diretório acima com sufixo `-audit`; checkout separado e detached em `e1a435a2dc71cd1e621737070913b8a62a4ae3fb`.
- Codex: exit code `0`; eventos JSONL `item.completed` e `turn.completed`; resposta final estruturada `{"audited_sha":"e1a435a2dc71cd1e621737070913b8a62a4ae3fb","clean":false,"verdict":"Working tree is dirty: untracked .serena/ directory."}`.
- `git status --porcelain` após a execução → `?? .serena/`. Conforme esclarecimento do usuário, `.serena/` é dado auxiliar de MCP; não conta como modificação do código auditado. Nenhum arquivo rastreado foi alterado nessa prova parcial.
- O SHA acima é só do commit vazio de preparação, **não** um commit produzido por Antigravity. Não houve teste de arquivo alterado, teste executado e commit do Builder, nem auditoria desse resultado.

## Bloqueio e próximo passo

## Repetição com Antigravity CLI real

- Repositório descartável: `C:\Users\fael\Documents\Codex\2026-09-14\ideias-o0-v2-m1-probe`. Baseline `9f72e6fbd054de1aeee5c7addc7277f800ed639d`: `value.py` devolve `1`, `test_value.py` exige `2`; `python -B -m unittest test_value` falhou como esperado (`2 != 1`).
- `agy.exe -p 'Reply with exactly OK. Do not use tools.' --output-format json --print-timeout 30s` → código `0`, `status=SUCCESS`, `response=OK`. Autenticação headless comprovada.
- Builder: `agy.exe -p '<corrigir value.py, executar teste, criar commit e devolver SHA>' --output-format json --print-timeout 3m --dangerously-skip-permissions --sandbox` → código `0`, envelope `status=SUCCESS` e `response` vazia; stderr informou `print timeout after 3m0s with turn in progress`. `git rev-parse HEAD` permaneceu no baseline, `git status --porcelain` vazio.
- Segunda tentativa, só edição: `agy.exe -p '<trocar return 1 por return 2>' --output-format json --print-timeout 2m --dangerously-skip-permissions --disable-slash-commands` → mesmo resultado: código `0`, resposta vazia, timeout e diff vazio.

M1 **não aceito**. A [CLI headless](https://antigravity.google/docs/cli/headless/) está instalada e autenticada, mas não concluiu nem a edição mínima; código `0` e `status=SUCCESS` não bastam diante de `response` vazia e timeout. Investigar o bloqueio de execução antes de repetir Builder → commit → auditoria do SHA real e antes de M2. Gate S1 = NOT_RUN; S2 = NOT_STARTED.
