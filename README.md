# Ideias Standard

Base para começar qualquer projeto trabalhado por pessoas e agentes de IA (Claude, Codex, Gemini, Hermes…). Você copia uma pasta e já tem visão, roadmap, estado retomável, regras de agente e critérios de "pronto", sem ferramenta para instalar.

> Menos contexto, mais sinal. Menos processo, mais verificação. Primeiro provar, depois padronizar.

## Por que existe

Sem uma base, cada projeto com IA perde o estado entre sessões, o roadmap vira uma lista infinita, "pronto" passa a significar "a IA disse que fez" e as regras se repetem em vários arquivos, inchando o contexto. O kit resolve com poucos arquivos, cada um respondendo a **uma** pergunta, e com a regra de que nada é `DONE` sem evidência. As escolhas vêm de pesquisa e documentação oficial resumidas em [docs/PESQUISA.md](docs/PESQUISA.md).

## O que vem no kit

```text
template/
├── README.md         como rodar e verificar
├── PROJECT.md        por que existe, para quem, MVP, fora de escopo
├── ROADMAP.md        marcos e fila: o que entra agora, depois e no futuro
├── STATE.md          onde paramos e a próxima ação — todo agente começa aqui
├── AGENTS.md         10 regras comuns a qualquer agente + comandos do projeto
├── CLAUDE.md         só @AGENTS.md (sem duplicar)
├── DESIGN.md         a cara do app: tokens, layout, componentes (apague se não houver UI)
├── CHANGELOG.md
├── .gitignore, .editorconfig
└── docs/
    ├── DECISIONS.md            o porquê das escolhas caras de desfazer
    ├── RELEASE_CHECKLIST.md    como provar que está pronto (gates e publicação)
    └── templates/              FEATURE, EXECUTION_PLAN, REVIEW (copiados quando precisar)
```

**Obrigatórios:** `README`, `PROJECT`, `ROADMAP`, `STATE` e `AGENTS`. O resto entra quando a complexidade justifica. Os nomes podem variar quando uma ferramenta exige outro: `PRODUCT.md` vale como `PROJECT.md`.

## Como usar

### Projeto novo
1. Copie a pasta:
   ```bash
   cp -r template/. ../meu-projeto/
   ```
   ```powershell
   New-Item -ItemType Directory -Force ..\meu-projeto | Out-Null
   Copy-Item -Recurse -Force template\* ..\meu-projeto\
   Copy-Item -Force template\.gitignore, template\.editorconfig ..\meu-projeto\
   ```
2. Preencha os marcadores entre chaves duplas, nesta ordem: `PROJECT.md` (problema e MVP) → `ROADMAP.md` (um marco ativo) → `STATE.md` (próxima ação) → comandos reais em `AGENTS.md` e `docs/RELEASE_CHECKLIST.md` → `DESIGN.md`, se houver interface. Apague o que não se aplica.
3. Confira: `python scripts/check.py ../meu-projeto`.

### Projeto existente
Não copie por cima. Mapeie o que já cumpre cada papel, proponha o diff, mova preservando histórico e corte as duplicatas, seguindo o [GUIA §7](docs/GUIA.md#7-adotar-em-projeto-existente). Depois rode o `check.py`.

## Ciclo de trabalho

```text
ideia → PROJECT → ROADMAP (marco ativo) → FEATURE com ACs → código + testes → REVIEW → checklist + aceite humano → STATE
```

A documentação acompanha o risco da tarefa: uma correção simples só precisa de commit e teste; uma feature pede uma spec curta; uma mudança grande pede também plano e revisão independente ([GUIA §1](docs/GUIA.md#1-quanto-documento-cada-tarefa-merece)). Estados, papéis entre agentes e prompts prontos estão no [GUIA](docs/GUIA.md).

**Regras que não mudam:**
- Roadmap (quando e o quê) ≠ spec (comportamento) ≠ plano (como) ≠ review (prova).
- `NOT_RUN` não é `PASS`; "feito" dito pela IA não é evidência; teste verde não é aprovação de produto.
- Exclusões, ações irreversíveis, produção, gastos, segredos e dados pessoais exigem aprovação humana.
- Cada regra vive em um só lugar e o resto aponta para ela. Marco fechado sai do roadmap.

## Verificar um projeto

```bash
python scripts/check.py <projeto>             # 0 ok · 1 falhou · 2 erro de uso
python scripts/check.py <projeto> --strict    # avisos também reprovam
```

Só leitura, sem dependências. O script confere os arquivos obrigatórios, marcadores não preenchidos (também no `DESIGN.md`, se existir), a próxima ação no `STATE.md`, o tamanho do `AGENTS.md`, o `CLAUDE.md` sem regras duplicadas e o `.env` no `.gitignore`. Ele não substitui os testes, o lint e o build do projeto.

## Este repositório

O próprio repositório segue o kit: [PROJECT.md](PROJECT.md), [ROADMAP.md](ROADMAP.md), [STATE.md](STATE.md) e [AGENTS.md](AGENTS.md) descrevem o kit em si.

| Caminho | Conteúdo |
|---|---|
| [`template/`](template/) | o kit a copiar |
| [`examples/command/`](examples/command/) | exemplo preenchido (didático), incluindo o `DESIGN.md` |
| [`docs/GUIA.md`](docs/GUIA.md) | passo a passo, estados, papéis, prompts, adoção, segurança |
| [`docs/PESQUISA.md`](docs/PESQUISA.md) | evidências, fontes R01–R28 e protocolo comparativo |
| [`scripts/check.py`](scripts/check.py), [`tests/`](tests/) | verificador e seus testes |

Para mudar o kit: a mudança precisa ter vindo de atrito real de uso ([ROADMAP](ROADMAP.md)). Quem altera o `template/` atualiza o exemplo no mesmo commit e roda:

```bash
python -m unittest discover -s tests -v
python scripts/check.py template --template --strict
```

A versão anterior (Gold V5: schemas, lock, packs, goldify, sync) está preservada na tag [`v0.1-gold-legacy`](https://github.com/playertwo1/ideias_standard/tree/v0.1-gold-legacy).
