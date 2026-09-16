# O0 v2 M1 — ensaio parcial (BLOCKED)

Base: `7f2bb68d9e9475da9a52ef4e5622a6086bcb8925`. Ambiente: Windows, PowerShell, 2026-09-16. Nenhuma aprovação de gate foi inferida.

## CLIs

- `where.exe agy` → `C:\Users\fael\AppData\Local\Programs\Antigravity IDE\bin\agy.cmd`. O arquivo chama `antigravity-ide.cmd`; `agy --version` → `Antigravity IDE 1.107.0`; `agy --help` mostra opções do IDE, sem `-p`, `--output-format` ou `--cwd`. `C:\Users\fael\AppData\Local\agy\bin\agy.exe` não existe. Logo, não foi possível verificar autenticação nem executar o Builder Antigravity CLI. O executável do IDE não é substituto para a CLI headless.
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
- `git status --porcelain` após a execução → `?? .serena/`. O sandbox `read-only` protegeu os arquivos rastreados, mas um servidor MCP criou metadados não rastreados no checkout. Não considerar a proteção integral comprovada; isolar/desabilitar esse MCP antes do aceite.
- O SHA acima é só do commit vazio de preparação, **não** um commit produzido por Antigravity. Não houve teste de arquivo alterado, teste executado e commit do Builder, nem auditoria desse resultado.

## Bloqueio e próximo passo

M1 **não aceito**. É necessária a [Antigravity CLI headless](https://antigravity.google/docs/cli/headless/) real (distinta do IDE), instalada/autenticada, para `agy -p ... --output-format json`. A [instalação oficial no Windows](https://antigravity.google/docs/cli/install/) aponta para `AppData\Local\agy\bin`. Repetir M1 com repositório descartável e checkout de auditoria livre de writes auxiliares antes de M2. Gate S1 = NOT_RUN; S2 = NOT_STARTED.
