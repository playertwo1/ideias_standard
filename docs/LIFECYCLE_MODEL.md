# Lifecycle Model — Ideias Standard

## Objetivo

Definir um ciclo único para projetos novos e existentes sem transformar o Standard em um gerador destrutivo de boilerplate.

## Fluxos principais

### Novo projeto

`manifest → resolve profile/packs/bundle/workflow → dry-run → diff → materialize → validate → lock`

### Projeto existente

`inventory → recommend → map equivalents → classify ownership → preview → adopt → validate → lock`

### Upgrade

`check → render target in staging → baseline/local/target diff → conflicts → preview → apply → validate → new lock`

### Mudança de feature

`change unit → delta + invariants → implement → proportional verify → close change → update state`

## Regras de escrita

- `MANAGED`: Standard controla baseline; drift local bloqueia overwrite automático.
- `MERGEABLE`: three-way merge com revisão em conflito.
- `USER_OWNED`: nunca sobrescrito automaticamente.

## Dry-run first

Operações que escrevem múltiplos arquivos devem oferecer preview/diff antes da aplicação. A ausência de baseline ou conflito de provenance reduz automação; nunca aumenta permissão de overwrite.

## Provenance

O lock deve permitir responder:

- qual versão do Standard gerou o artefato;
- qual profile/pack/bundle o incluiu;
- qual template/origem foi usado;
- qual fingerprint representa o baseline;
- se existe override local conhecido.

## Conformance

`check` é a base do lifecycle. `doctor` explica findings para humanos. `init`, `adopt` e `upgrade` só podem avançar quando conseguem validar sua saída com os mesmos contratos.

## Idempotência

Reaplicar a mesma versão, mesma composição e mesmas entradas não deve produzir mudanças materiais inesperadas.

## Falhas e rollback

- lock só atualiza após validação;
- operações multi-arquivo devem ser preparadas em staging quando aplicável;
- conflito material interrompe aplicação;
- falha não deve deixar estado parcialmente promovido como sucesso.

## Anti-drift

Adapters, workflows e bundles são conveniências derivadas. Eles não competem com decisões do projeto nem com a autoridade humana.
