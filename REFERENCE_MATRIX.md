# Reference Matrix — Ideias Standard

Pesquisa inicial em GitHub/Reddit para orientar o Standard sem copiar cegamente outros projetos.

Legenda: `ADOPT` = adotar princípio; `ADAPT` = adaptar; `INSPIRE` = inspiração; `AVOID` = evitar como regra universal.

| Referência | Padrão útil | Decisão para Ideias Standard |
|---|---|---|
| Copier | lifecycle de projetos gerados, answers versionadas, atualização por diff e conflitos explícitos | ADOPT lifecycle/versionamento; ADAPT update para nosso `standard.lock` e ownership por arquivo |
| Cruft | lock com commit/template/variáveis; `check`; update revisável; skip de arquivos; link de projeto existente | ADOPT `check`, provenance e revisão; ADAPT `link` para nosso `adopt` |
| projen | configuração declarativa como fonte de verdade e síntese repetível em muitos repositórios | ADOPT fonte declarativa; AVOID proibir edição humana de todo arquivo gerado |
| Backstage Software Templates | catálogo de templates/componentes e metadados estruturados | INSPIRE catálogo de packs/perfis; evitar dependência de portal/infra Backstage |
| GitHub Spec Kit | constitution/spec/plan/tasks; CLI; integrações multiagente; extensions/presets/bundles versionados | ADOPT adapters e bundles com provenance; ADAPT fluxo para nossa governança proporcional |
| OpenSpec | brownfield-first; changes isoladas; deltas; schemas customizáveis por workflow; specs como comportamento | ADOPT deltas/brownfield e workflow schemas; ADAPT sem abandonar gates quando risco exigir |
| Reddit r/codex | byte-cap de saída; targeted context → smallest correct patch → proportional validation | ADOPT na política de contexto |
| Reddit r/codex / r/ClaudeCode | specs menores por unidade de trabalho; contexto específico; sessões frescas; evitar SDD pesado para mudanças pequenas | ADOPT proporcionalidade LIGHT/STANDARD/DEEP e context routing |

## Ideias incorporadas ao desenho

### 1. File ownership

Cada artefato gerenciado deve declarar uma política:

- `MANAGED`: derivado integralmente do Standard; não editar manualmente ou alterações serão substituídas mediante preview.
- `MERGEABLE`: Standard fornece baseline, mas preserva customização local através de diff/merge.
- `USER_OWNED`: Standard pode validar/recomendar, mas nunca sobrescreve automaticamente.

### 2. Provenance por artefato

O lock futuro deve poder registrar para cada artefato gerado:

- template/source id;
- versão;
- fingerprint;
- ownership;
- profile/pack que o incluiu;
- overrides locais conhecidos.

### 3. Update seguro

Fluxo alvo:

`check → render target → diff → classify conflicts → preview → apply → validate → update lock`

Nunca esconder conflito ou assumir overwrite.

### 4. Brownfield/adopt

Projetos existentes são caso de primeira classe. Sem baseline anterior, `adopt` deve construir um baseline sintético/inventário, classificar conflitos e exigir preview antes de escrever.

### 5. Workflow schemas

Além de profile/packs, versões futuras podem permitir workflows declarativos especializados (por exemplo research-first ou migration-first), sem transformar cada fluxo em código rígido.

### 6. Agent adapters e bundles

Adapters materializam instruções para ferramentas específicas; bundles podem compor profile + packs + adapters com versões, conflitos e provenance. O contrato canônico permanece independente de agente.

### 7. Anti-burocracia

Mudança trivial não deve exigir o mesmo ritual de projeto sensível. A profundidade do processo cresce com risco, impacto e ambiguidade.
