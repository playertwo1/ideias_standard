# CLI Contract — Ideias Standard Gold

Este documento define a superfície mínima esperada de automação do Standard. A CLI não deve crescer além do necessário.

## Princípios

- leitura é segura por padrão;
- escrita nunca sobrescreve trabalho existente silenciosamente;
- saída humana deve ser curta e acionável;
- JSON só existe quando houver necessidade real de automação;
- comandos devem reutilizar a mesma lógica de validação sempre que possível;
- nenhuma abstração de CLI deve existir apenas para antecipar uso futuro.

## Exit codes

Quando aplicável:

- `0`: execução concluída com sucesso;
- `1`: validação/check falhou;
- `2`: erro operacional ou uso inválido.

## Comandos

### `check`

Comando principal.

Verifica o que for aplicável ao projeto, por exemplo:

- estrutura essencial;
- configuração básica;
- lint/format;
- typecheck;
- testes;
- build;
- packs ativos.

A saída deve explicar claramente o que falhou.

### `adopt`

Futuro comando de Goldify para projetos existentes.

Primeiro analisa sem escrever. Depois produz um **Golden Diff** separando:

- `NECESSÁRIO`;
- `RECOMENDADO`.

Mudanças relevantes devem ter preview antes de aplicação quando houver risco de sobrescrever ou reorganizar trabalho existente.

### `sync`

Futuro. Só implementar depois que Create, Check e Adopt estiverem comprovados em uso real.

Serve para aplicar melhorias do Standard a projetos Gold existentes sem reconstruí-los.

## Create

A criação de projetos não exige obrigatoriamente uma CLI.

A primeira implementação deve preferir GitHub Template Repository. Um comando próprio de criação só deve existir se resolver uma necessidade real não atendida de forma mais simples.

## Auditoria

Auditoria independente não precisa ser um comando da CLI.

O contrato mínimo é:

1. receber pedido/aceite, diff e resultado do `check`;
2. começar pelo delta;
3. ampliar contexto somente quando necessário;
4. retornar `PASS` ou `FAIL` com findings acionáveis.

O Runner pode automatizar esse ciclo externamente.

## Regra final

> A CLI existe para reduzir trabalho manual, não para transformar o Standard em uma plataforma complexa.
