---
name: gold-audit
description: Auditar uma alteração pelo pedido, aceite, diff e check, expandindo contexto somente quando necessário.
---

# Gold Audit

1. Leia o pedido e os critérios de aceite.
2. Inspecione `git diff` e os arquivos alterados.
3. Execute ou confira o `check` curto; expanda logs somente em falha.
4. Verifique escopo, regressões, segurança e complexidade.
5. Retorne `PASS` ou findings acionáveis com arquivo, impacto e correção.

Segurança: não execute comandos destrutivos nem exponha secrets. Provider-neutral.
Licença: texto original do projeto; sem conteúdo de terceiros incorporado.
Teste mínimo: aplicar a sequência a uma fixture válida e a uma fixture com defeito.
