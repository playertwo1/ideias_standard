# Ideias Standard

Base Gold simples para criar, validar, adotar e atualizar projetos preparados
para humanos e agentes de IA.

> **Small Core · contexto progressivo · verificação executável · auditoria independente**

## O problema que resolve

Projetos assistidos por IA precisam de estado operacional claro, contexto curto,
regras estáveis e evidência reproduzível. O Standard fornece essa base sem impor
arquitetura, fornecedor de IA ou burocracia igual para todo projeto.

## Dois caminhos

```text
NOVO PROJETO      → CREATE  → TEMPLATE GOLD → PROJETO GOLD
PROJETO EXISTENTE → GOLDIFY → GOLDEN DIFF   → CHECK + AUDIT → PROJETO GOLD
```

Gold padroniza qualidade e operação; não padroniza a implementação interna.

## O contrato mínimo

Um projeto Gold, quando aplicável, tem:

- `README.md` útil e `AGENTS.md` curto;
- estado atual e próxima ação identificáveis;
- comandos reais de verificação;
- contexto carregado progressivamente;
- ownership, origem e mudanças locais preservados;
- segurança proporcional ao risco;
- diff revisável e auditoria independente para mudanças relevantes.

Regras essenciais:

- `NOT_RUN` não significa `PASS`;
- sugestão de IA não vira decisão humana automaticamente;
- automação não amplia autoridade;
- contexto obrigatório não é truncado silenciosamente;
- uma nova regra só entra no Gold após prova em uso adequado;
- arquivos existentes são preservados por padrão.

## Contexto para agentes

Bootstrap padrão:

```text
AGENTS.md + pedido atual
```

Depois, localizar antes de ler e abrir somente o trecho necessário de
`PROJECT_STATE.md`, `STANDARD.md`, `ROADMAP.md`, documentação e Skills.

## Verificação

Para validar o próprio Standard:

```bash
python scripts/validate_standard.py --self-check
python -m unittest discover -s tests -p 'test_*.py' -v
```

Para verificar um projeto:

```bash
python scripts/check.py <projeto>
python scripts/check.py <projeto> --details
python scripts/check.py <projeto> --json
```

Exit codes de `check.py`: `0` sucesso, `1` falha de validação, `2` erro
operacional. O resumo não substitui testes, lint, typecheck ou build do projeto.

## Fluxo de mudança

```text
pedido → Builder → check resumido → diff → Auditor independente → PASS ou findings
```

O Auditor começa pelo pedido, aceite, diff e evidências. O Runner externo
[`playertwo1/runner`](https://github.com/playertwo1/runner) é opcional e não é
fonte canônica nem requisito do Standard.

## Skills e Packs

Skills e Packs são opcionais. Só entram quando resolvem uma necessidade real e
foram revisados, testados e considerados menores que uma regra ou script local.

Skills Gold prioritárias:

- `gold-audit` — revisão curta orientada por pedido, aceite, diff e check;
- `goldify` — descoberta somente leitura e Golden Diff;
- `skill-author` — criação segura de Skills pequenas.

O Template Gold não instala um catálogo inteiro por padrão.

## Roadmap resumido

| Fase | Resultado | Estado |
|---|---|---|
| F0 — Golden Standard | Core, check, Skills provadas e dogfooding | implementada |
| F1 — Create | Template Gold utilizável | implementada |
| F2 — Check + Audit | verificação e revisão reproduzíveis | implementada |
| F3 — Packs + Skills | capacidades opcionais comprovadas | implementada |
| F4 — Adopt / Goldify | adoção sem sobrescrever o projeto | implementada |
| F5 — Sync | atualização conservadora e revisável | implementada |

O mapa operacional está em [`ROADMAP.md`](ROADMAP.md). O estado atual está em
[`PROJECT_STATE.md`](PROJECT_STATE.md).

## Arquivos principais

- [`AGENTS.md`](AGENTS.md) — instruções universais mínimas;
- [`STANDARD.md`](STANDARD.md) — contrato normativo Gold;
- [`ROADMAP.md`](ROADMAP.md) — objetivos, entregas e critérios por fase;
- [`PROJECT_STATE.md`](PROJECT_STATE.md) — estado operacional atual;
- [`PROJECT_GUIDE.md`](PROJECT_GUIDE.md) — orientação conceitual e retomada;
- `scripts/` — validação, check, Goldify e sync;
- `schemas/`, `fixtures/`, `examples/`, `templates/` — contratos e provas.

## Estado atual

O repositório está consolidado em **F5 — SYNC**. As auditorias individuais de
F0/F0-SK a F5 estão registradas; a auditoria final da consolidação Gold ainda é
a próxima ação. Isso não registra novo gate humano nem autoriza uma fase futura.

## Licença e evolução

Mudanças devem ser pequenas, verificáveis e compatíveis. Preserve trabalho
local, atualize evidência somente após executar os checks e prefira remover
complexidade sem função prática.
