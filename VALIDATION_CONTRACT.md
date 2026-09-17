# Validation Contract — Ideias Standard Gold

Este contrato define o comportamento mínimo do `check` no modelo Gold.

O objetivo é responder de forma simples:

> O projeto está saudável para continuar o trabalho?

## Resultado

O resultado principal deve ser:

- `PASS` — verificações aplicáveis concluídas sem falha relevante;
- `FAIL` — existe falha que precisa ser corrigida antes de considerar o projeto saudável.

`WARN` pode ser usado quando houver informação útil que não bloqueie o trabalho, mas não é obrigatório.

## O que pode ser verificado

Somente o que for aplicável ao projeto, por exemplo:

- arquivos essenciais;
- configuração da stack;
- lint/format;
- typecheck;
- testes;
- build;
- CI;
- packs ativos;
- problemas básicos de segurança ou configuração.

Nem todo projeto precisa de todas as verificações.

## Saída humana

Preferir saída curta e acionável.

Exemplo:

```text
PASS
✓ lint
✓ tests
✓ build
```

Falha:

```text
FAIL
- tests: 2 testes falharam
- build: não executado após falha dos testes
```

## Saída estruturada

JSON só deve ser mantido ou ampliado quando houver consumidor real de automação.

Se usado, deve representar o mesmo resultado da saída humana e nunca contradizê-la.

## Códigos

O Gold Standard não exige um catálogo grande de códigos determinísticos para cada detalhe interno.

Quando um código estável trouxer valor para automação ou diagnóstico, ele pode existir. Não criar códigos apenas para satisfazer documentação.

## Exit codes

Quando usados pela CLI/script:

- `0`: PASS;
- `1`: FAIL de validação;
- `2`: erro operacional ou uso inválido.

## Testes

Testar comportamentos importantes:

- projeto saudável → PASS;
- falha importante → FAIL com mensagem útil;
- mesma entrada não produz resultado contraditório;
- bug relevante corrigido recebe regressão quando fizer sentido.

Não existe meta de quantidade de testes ou cobertura como gate do produto.

## Auditoria

`check` não substitui auditoria independente.

Para alterações relevantes, o Auditor recebe inicialmente pedido/aceite, diff e resultado do `check`, e amplia contexto somente quando necessário.

## Transição do modelo antigo

Scripts e schemas existentes podem continuar emitindo códigos do modelo de conformance anterior durante F0.

Esses códigos são ativos legados em revisão e não definem mais o roadmap. Devem ser mantidos, simplificados ou removidos conforme seu valor prático no Gold Standard.
