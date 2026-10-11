# Ideias Standard

Kit mínimo para começar qualquer projeto trabalhado por pessoas e agentes de IA (Claude, Codex, Gemini, Hermes…): visão clara, estado retomável, critérios verificáveis e evidência antes de "pronto".

> Menos contexto, mais sinal. Menos processo, mais verificação. Primeiro provar, depois padronizar.

## Começar um projeto novo

```bash
cp -r template/. ../meu-projeto/
```

```powershell
Copy-Item -Recurse -Force template\* ..\meu-projeto\
Copy-Item -Force template\.gitignore, template\.editorconfig ..\meu-projeto\
```

Depois:
1. Preencha os marcadores entre chaves duplas de `PROJECT.md`, `AGENTS.md`, `README.md`, `ROADMAP.md` e `STATE.md` (apague o que não se aplica).
2. Escolha **um** marco ativo no `ROADMAP.md`; os demais ficam só com objetivo e gate.
3. Escreva em `STATE.md` a próxima ação verificável.
4. Confira: `python scripts/check.py ../meu-projeto`.

Projeto existente: siga o [GUIA §7](docs/GUIA.md#7-adotar-em-projeto-existente).

## O que vem no template

| Arquivo | Pergunta que responde | Quando atualizar |
|---|---|---|
| `PROJECT.md` | Por que existe? Para quem? O que fica fora do MVP? | ao criar e quando a visão muda |
| `ROADMAP.md` | O que entra agora, depois e no futuro? | ao priorizar ou mudar escopo |
| `STATE.md` | Onde paramos e qual a próxima ação? | ao fim de cada sessão relevante |
| `AGENTS.md` | Como qualquer agente deve trabalhar aqui? | só quando a política muda |
| `CLAUDE.md` | só `@AGENTS.md`, sem duplicar | raramente |
| `DESIGN.md` | Qual é a cara do app? Cores, tipografia, layout, componentes (tokens + porquê) | antes da primeira tela; apague se não houver interface |
| `docs/DECISIONS.md` | Por que escolhemos isso? | em escolhas caras de desfazer |
| `docs/RELEASE_CHECKLIST.md` | Como provamos que está pronto? | ao definir os comandos do projeto |
| `docs/templates/FEATURE.md` | Qual comportamento, com quais critérios? | antes de feature média ou maior |
| `docs/templates/EXECUTION_PLAN.md` | Como executar mudança grande sem depender da conversa? | só mudança complexa |
| `docs/templates/REVIEW.md` | O que foi provado? | ao concluir feature ou marco |

O projeto funciona só com `PROJECT`, `ROADMAP`, `STATE` e `AGENTS`. Nomes podem variar quando uma ferramenta exige outro (ex.: `PRODUCT.md` no lugar de `PROJECT.md`; o checker aceita os dois). O resto é progressivo e entra quando a complexidade justifica ([GUIA §1](docs/GUIA.md#1-quanto-documento-cada-tarefa-merece)).

## Regras centrais
- Roadmap (quando/o quê) ≠ spec (comportamento) ≠ plano (como) ≠ review (prova).
- `NOT_RUN` não é `PASS`; "feito" dito pela IA não é evidência; teste verde não é aprovação de produto.
- Exclusões, ações irreversíveis, produção, gastos, segredos e dados pessoais exigem aprovação humana.
- Uma regra em um só lugar; o resto aponta para ela. Marco fechado sai do roadmap.
- Contexto progressivo: `AGENTS.md` curto, docs lidos sob demanda.

## Neste repositório

| Caminho | Conteúdo |
|---|---|
| [`template/`](template/) | o kit a copiar |
| [`examples/command/`](examples/command/) | exemplo preenchido (didático) |
| [`docs/GUIA.md`](docs/GUIA.md) | passo a passo, estados, papéis, prompts, adoção, segurança |
| [`docs/PESQUISA.md`](docs/PESQUISA.md) | evidências, fontes R01–R28 e protocolo comparativo |
| [`scripts/check.py`](scripts/check.py) | confere um projeto (só leitura, sem dependências) |
| [`STATE.md`](STATE.md), [`ROADMAP.md`](ROADMAP.md) | estado e evolução do próprio kit |

```bash
python scripts/check.py <projeto>              # 0 ok · 1 falhou · 2 erro de uso
python scripts/check.py template --template    # aceita marcadores não preenchidos
python -m unittest discover -s tests -v
```

A versão anterior (Gold V5: schemas, lock, packs, profiles, goldify, sync) está preservada na tag [`v0.1-gold-legacy`](https://github.com/playertwo1/ideias_standard/tree/v0.1-gold-legacy).
