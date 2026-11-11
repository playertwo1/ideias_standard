<p align="center">
  <img src="assets/banner.svg" alt="Ideias Standard" width="100%">
</p>

# Ideias Standard

Esqueleto de documentos para projetos feitos por pessoas e agentes de IA (Claude, Codex, Gemini, Hermes…): visão, roadmap, ponto de retomada e regras curtas, mais um verificador sem dependências.

Princípios: menos contexto, mais sinal · menos processo, mais verificação · primeiro provar, depois padronizar · `NOT_RUN` não é `PASS`.

## Início rápido

```bash
# Linux / macOS
curl -sSL https://raw.githubusercontent.com/playertwo1/ideias_standard/main/scripts/init.py | python3 - meu-projeto
```
```powershell
# Windows (PowerShell)
irm https://raw.githubusercontent.com/playertwo1/ideias_standard/main/scripts/init.py | python - meu-projeto
```

Com o repositório clonado: `python scripts/init.py ../meu-projeto [--name "Nome"] [--no-design] [--force]`. `--force` aceita pasta não vazia e só adiciona o que falta; nunca sobrescreve arquivo existente. Também funciona como [template do GitHub](https://github.com/playertwo1/ideias_standard/generate).

## O que o projeto recebe (`template/`)

| Arquivo | Papel | Quando o agente lê |
|---|---|---|
| `AGENTS.md` (+ `CLAUDE.md` que só o importa) | mapa, comandos e 10 regras | sempre |
| `STATE.md` | onde paramos e a próxima ação | início de toda sessão |
| `ROADMAP.md` | marcos; só o ativo detalhado | ao planejar |
| `PROJECT.md` | problema, MVP e fora de escopo | ao planejar |
| `DESIGN.md` | cara do app (opcional) | antes de mexer em tela |
| `docs/WATCHDOG.md`, `docs/AUDIT.md` | limites na execução e auditoria final | mudança média ou maior |
| `docs/RELEASE_CHECKLIST.md`, `docs/DECISIONS.md` | gates de fechamento e decisões caras | ao fechar / ao decidir |
| `docs/templates/` | `FEATURE`, `EXECUTION_PLAN`, `REVIEW` | sob demanda |

O projeto funciona só com `AGENTS`, `STATE`, `ROADMAP` e `PROJECT`; o resto entra quando traz valor.

## Ciclo

<p align="center">
  <img src="assets/workflow.svg" alt="Início → alinhamento → definição → execução → verificação → retomada" width="100%">
</p>

Passo a passo, papéis, prompts prontos e adoção em projeto existente: [docs/GUIA.md](docs/GUIA.md).

## Verificar

```bash
python scripts/check.py <projeto> [--strict]
```

Confere arquivos obrigatórios, marcadores de chaves duplas não preenchidos, "Próxima ação" no `STATE.md`, tamanho do `AGENTS.md`, `CLAUDE.md` importando `@AGENTS.md` e `.env` no `.gitignore`. `--strict` reprova também nos avisos.

## Mais

- [docs/GUIA.md](docs/GUIA.md) — como usar. [docs/PESQUISA.md](docs/PESQUISA.md) — evidências e fontes.
- [examples/command/](examples/command/) — exemplo preenchido.
- Contribuir: uma regra só entra depois de provada em projeto real ([ROADMAP.md](ROADMAP.md)). Testar: `python -m unittest discover -s tests -v` e `python scripts/check.py template --template --strict`.
