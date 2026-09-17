---
name: goldify
description: Produzir Golden Diff mínimo para elevar um projeto existente ao Gold sem reescrevê-lo.
---

# Goldify

1. Localize README, AGENTS, testes, CI, check e estrutura.
2. Separe `NECESSÁRIO` de `RECOMENDADO`.
3. Preserve arquitetura e arquivos válidos.
4. Proponha apenas o menor diff que melhora compreensão, verificação ou segurança.
5. Rode o check e registre limitações.

Segurança: leitura por padrão; não remova dados nem altere o projeto sem autorização. Provider-neutral.
Licença: texto original do projeto.
Teste mínimo: produzir um Golden Diff em `examples/gold-standard`.
