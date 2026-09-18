# Ideias Standard

O **Ideias Standard** é uma base Gold simples e reutilizável para criar, validar e melhorar projetos desenvolvidos por humanos e agentes de IA.

A proposta é direta:

> projeto fácil de entender + contexto mínimo + verificação objetiva + auditoria independente.

Sem transformar cada repositório em um sistema de governança complexo.

## Missão

O projeto atende dois caminhos:

```text
NOVO PROJETO → CREATE → TEMPLATE GOLD → PROJETO GOLD
PROJETO EXISTENTE → GOLDIFY → GOLDEN DIFF → CHECK + AUDIT → PROJETO GOLD
```

Gold padroniza qualidade e operação. Não obriga projetos diferentes a terem a mesma arquitetura.

## Princípios

- **Small Core** — poucas regras universais;
- **Progressive Context** — contexto específico somente quando necessário;
- **Token Discipline** — maximizar sinal por token;
- **Executable Verification** — mudanças devem poder ser verificadas por comandos reais;
- **Independent Audit** — alterações relevantes podem ser revisadas por outro agente/processo;
- **Optional Packs & Skills** — capacidades específicas entram somente quando úteis;
- **No Overengineering** — nenhuma abstração existe sem problema concreto;
- **Dogfooding** — o próprio Standard deve usar o que recomenda;
- **Prove Before Expand** — primeiro provar em uso adequado, depois promover ao Gold.

## Duas regras de execução

### Dogfooding obrigatório

O próprio `ideias_standard` deve seguir o Gold que define sempre que a prática for aplicável. Se uma regra gera burocracia ou contexto excessivo aqui, ela deve ser revisada antes de ser recomendada aos próximos projetos.

### Provar antes de expandir

Nova Skill, pack, regra, arquivo ou abstração não entra no Core apenas porque parece útil.

```text
problema real
   ↓
solução mais simples
   ↓
teste no próprio Standard, fixture, exemplo ou projeto real
   ↓
benefício comprovado
   ↓
reutilizável no Gold
```

Se a necessidade for local, a solução permanece local.

## O que é um projeto Gold

Um projeto Gold:

- explica claramente o que faz;
- possui `README.md` útil;
- possui `AGENTS.md` curto e operacional;
- tem estrutura compreensível;
- possui build/test/lint/typecheck aplicáveis;
- possui mecanismo conhecido de `check`;
- executa verificações importantes no CI;
- carrega documentação específica somente sob necessidade;
- filtra ou resume outputs grandes antes de colocá-los no contexto;
- pode ser auditado pelo diff sem exigir leitura integral do repositório;
- usa segurança proporcional ao risco.

## Contexto para agentes

Bootstrap padrão:

```text
AGENTS.md + pedido atual
```

`PROJECT_STATE.md`, `STANDARD.md`, `ROADMAP.md`, documentação, packs, Skills e dependências são consultados somente quando relevantes.

```text
pedido
  ↓
localizar antes de ler
  ↓
menor trecho suficiente
  ↓
expandir somente quando necessário
```

`AGENTS.md` é a fonte canônica de instruções universais e deve permanecer pequeno. Evite duplicar as mesmas instruções em arquivos específicos de Codex, Claude, Gemini, Antigravity ou Copilot.

## Fluxo de trabalho

```text
pedido
  ↓
Builder
  ↓
check resumido
  ↓
diff
  ↓
Auditor independente
  ↓
PASS ou FINDINGS
```

O Auditor começa pelo pedido, critérios de aceite, diff e evidências de validação. Ele amplia contexto somente quando houver razão concreta.

A automação Builder ↔ Auditor pode ser feita pelo projeto externo [playertwo1/runner](https://github.com/playertwo1/runner), mas o Runner não é requisito para usar o Standard.

`python scripts/check.py <projeto>` produz resumo curto; use `--details` para expandir checks ou
`--json` para automação. Exit codes: `0` sucesso, `1` falha de validação, `2` erro operacional.

## Skills no Gold

Skills guardam procedimentos especializados fora do contexto permanente.

O Template Gold não instala um catálogo inteiro de Skills. Ele nasce preparado para adicionar somente as que o projeto realmente precisa.

Primeiras Skills Gold planejadas:

- **`gold-audit`** — revisar alteração usando pedido + critérios de aceite + diff + resultado do `check`;
- **`goldify`** — analisar projeto existente e produzir um Golden Diff curto;
- **`skill-author`** — criar/revisar Skills pequenas, seguras e com progressive disclosure.

Candidata futura:

- **`skill-curator`** — recomendar o menor conjunto útil de Skills para um projeto.

Skills externas seguem:

```text
DISCOVER → REVIEW → TRIM → ADAPT → TEST → INSTALL
```

Adoção depende de utilidade real, revisão de segurança, licença, ausência de sobreposição, teste e compatibilidade com contexto progressivo.

## Pesquisa de Skills usada pelo projeto

Principais referências já estudadas:

- [Agent Skills](https://github.com/agentskills/agentskills) — especificação e progressive disclosure;
- [Anthropic Claude Code — skill-development](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev/skills/skill-development) — Skills, scripts e referências;
- [OpenAI Codex — code-review](https://github.com/openai/codex/tree/main/.codex/skills/code-review) — revisão focada em findings;
- [Trail of Bits — second-opinion](https://github.com/trailofbits/skills/tree/main/plugins/second-opinion/skills/second-opinion) — revisão independente de diff/commit;
- [Trail of Bits — audit-context-building](https://github.com/trailofbits/skills/tree/main/plugins/audit-context-building/skills/audit-context-building) — expansão progressiva de contexto;
- [GitHub Awesome Copilot — ai-ready](https://github.com/github/awesome-copilot/tree/main/skills/ai-ready) — preparar repositórios para agentes;
- [GitHub Awesome Copilot — acquire-codebase-knowledge](https://github.com/github/awesome-copilot/tree/main/skills/acquire-codebase-knowledge) — descobrir stack, estrutura, CI e testes;
- [GitHub Awesome Copilot — agent-skill-stack](https://github.com/github/awesome-copilot/tree/main/skills/agent-skill-stack) — escolher o menor conjunto de Skills;
- [GitHub Awesome Copilot — security-review](https://github.com/github/awesome-copilot/tree/main/skills/security-review) — referência para projetos de maior risco;
- [GitHub Awesome Copilot — secret-scanning](https://github.com/github/awesome-copilot/tree/main/skills/secret-scanning) — proteção de secrets;
- [GitHub Awesome Copilot — agentic-eval](https://github.com/github/awesome-copilot/tree/main/skills/agentic-eval) — referência futura para projetos de IA.

Discussões práticas no Reddit são usadas como sinal complementar. O aprendizado principal é evitar stacks enormes de Skills/plugins, usar catálogos como fonte de pesquisa e testar Skills importantes contra pequenos fixtures.

## Como a pesquisa vira Template Gold

```text
pesquisa
   ↓
padrão útil
   ↓
trim + adaptação provider-neutral
   ↓
teste / dogfooding
   ↓
benefício comprovado
   ↓
capacidade opcional reutilizável
   ↓
próximos projetos Gold
```

Estrutura conceitual de projeto novo:

```text
novo-projeto/
├─ README.md
├─ AGENTS.md
├─ .gitignore
├─ .editorconfig
├─ .github/workflows/ci.yml
├─ src/...
├─ tests/...
├─ docs/...              somente quando útil
└─ .agents/skills/...    somente Skills necessárias
```

Nenhuma pasta ou Skill opcional precisa existir se não houver uso concreto.

## Roadmap

1. **F0 — Golden Standard**: definir, dogfood e provar a base Gold;
2. **F1 — Create**: criar projetos novos usando primeiro GitHub Template;
3. **F2 — Check + Audit**: verificação executável e revisão independente;
4. **F3 — Packs + Skills**: capacidades específicas já estudadas e comprovadas;
5. **F4 — Adopt / Goldify**: elevar projetos existentes ao Gold sem reconstruí-los;
6. **F5 — Sync**: futuro, para distribuir melhorias comprovadas.

Consulte `ROADMAP.md` para os critérios detalhados e `PROJECT_STATE.md` para o estado atual.

## Arquivos principais

- `STANDARD.md` — regras canônicas do Gold Standard;
- `ROADMAP.md` — evolução, dogfooding e trilha de Skills;
- `PROJECT_STATE.md` — estado atual;
- `AGENTS.md` — instruções mínimas para agentes;
- `CLI_CONTRACT.md` — superfície mínima esperada de automação/CLI;
- `packs/`, `examples/`, `fixtures/`, `schemas/` e `scripts/` — ativos mantidos somente quando continuam úteis ao Gold.

## Estado atual

O projeto está em **F1 — CREATE**.

A arquitetura antiga baseada em profiles, bundles, gates e lifecycle amplo foi substituída pelo modelo Gold. O código e os artefatos existentes serão reaproveitados apenas quando simplificarem o novo Standard.

F0/F0-SK, F1, F2, F3, F4 e F5 estão implementados e aguardam auditoria independente. Sync
gera diff antes de aplicar, preserva USER_OWNED e não sobrescreve conflitos silenciosamente.

## Regra principal

> Se uma solução mais simples resolve corretamente o problema, use a solução mais simples. Se ainda não foi provada, não a transforme em padrão.
