# Ideias Standard

O **Ideias Standard** é uma base Gold simples e reutilizável para criar, validar e melhorar projetos desenvolvidos por humanos e agentes de IA.

A proposta é direta:

> projeto fácil de entender + contexto mínimo + verificação objetiva + auditoria independente.

Sem transformar cada repositório em um sistema de governança complexo.

## Princípios

- **Small Core** — poucas regras universais;
- **Progressive Context** — contexto específico somente quando necessário;
- **Token Discipline** — maximizar sinal por token;
- **Executable Verification** — mudanças devem poder ser verificadas por comandos reais;
- **Independent Audit** — alterações relevantes podem ser revisadas por outro agente/processo;
- **Optional Packs & Skills** — capacidades específicas entram somente quando úteis;
- **No Overengineering** — nenhuma abstração existe sem problema concreto.

## O que é um projeto Gold

Um projeto Gold:

- explica claramente o que faz;
- possui `README.md` útil;
- possui `AGENTS.md` curto e operacional;
- tem estrutura compreensível;
- possui build/test/lint/typecheck aplicáveis;
- possui um mecanismo conhecido de `check`;
- executa verificações importantes no CI;
- carrega documentação específica somente sob necessidade;
- filtra ou resume outputs grandes antes de colocá-los no contexto;
- pode ser auditado pelo diff sem exigir leitura integral do repositório;
- usa segurança proporcional ao risco.

Gold padroniza qualidade e operação. Não obriga projetos diferentes a terem a mesma arquitetura.

## Contexto para agentes

O bootstrap padrão é mínimo:

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

O Auditor começa pelo pedido, critérios de aceite, diff e evidências de validação. Ele amplia contexto somente quando houver uma razão concreta.

A automação Builder ↔ Auditor pode ser feita pelo projeto externo [playertwo1/runner](https://github.com/playertwo1/runner), mas o Runner não é requisito para usar o Standard.

## Skills no Gold

Skills guardam procedimentos especializados fora do contexto permanente.

O Template Gold não instala um catálogo inteiro de Skills. Ele nasce preparado para adicionar somente as que o projeto realmente precisa.

Primeiras Skills Gold planejadas:

- **`gold-audit`** — revisar alteração usando pedido + critérios de aceite + diff + resultado do `check`;
- **`goldify`** — analisar projeto existente, descobrir o necessário e produzir um Golden Diff curto;
- **`skill-author`** — criar/revisar Skills pequenas, seguras e com progressive disclosure.

Candidata futura:

- **`skill-curator`** — recomendar o menor conjunto útil de Skills para um projeto sem instalar capacidades sobrepostas.

Skills externas nunca são copiadas cegamente:

```text
DISCOVER → REVIEW → TRIM → ADAPT → TEST → INSTALL
```

Adoção depende de utilidade real, revisão de segurança, licença, ausência de sobreposição e compatibilidade com o modelo de contexto progressivo.

## Pesquisa de Skills usada pelo projeto

O roadmap mantém uma trilha formal para estudar e reaproveitar padrões maduros em vez de construir tudo do zero.

Principais referências já estudadas:

- [Agent Skills](https://github.com/agentskills/agentskills) — especificação e progressive disclosure;
- [Anthropic Claude Code — skill-development](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev/skills/skill-development) — organização de Skills, scripts e referências;
- [OpenAI Codex — code-review](https://github.com/openai/codex/tree/main/.codex/skills/code-review) — revisão de mudanças focada em findings;
- [Trail of Bits — second-opinion](https://github.com/trailofbits/skills/tree/main/plugins/second-opinion/skills/second-opinion) — revisão independente de diff/commit por outro modelo;
- [Trail of Bits — audit-context-building](https://github.com/trailofbits/skills/tree/main/plugins/audit-context-building/skills/audit-context-building) — expansão de contexto somente conforme necessidade da auditoria;
- [GitHub Awesome Copilot — ai-ready](https://github.com/github/awesome-copilot/tree/main/skills/ai-ready) — preparar um repositório para trabalho com agentes;
- [GitHub Awesome Copilot — acquire-codebase-knowledge](https://github.com/github/awesome-copilot/tree/main/skills/acquire-codebase-knowledge) — descobrir stack, estrutura, CI e testes;
- [GitHub Awesome Copilot — agent-skill-stack](https://github.com/github/awesome-copilot/tree/main/skills/agent-skill-stack) — escolher o menor conjunto compatível de Skills;
- [GitHub Awesome Copilot — security-review](https://github.com/github/awesome-copilot/tree/main/skills/security-review) — referência para projetos que realmente exigem revisão de segurança;
- [GitHub Awesome Copilot — secret-scanning](https://github.com/github/awesome-copilot/tree/main/skills/secret-scanning) — referência para proteção de secrets;
- [GitHub Awesome Copilot — agentic-eval](https://github.com/github/awesome-copilot/tree/main/skills/agentic-eval) — referência futura para projetos de IA que precisem de evals.

Discussões práticas no Reddit foram usadas como sinal complementar. O aprendizado principal foi evitar stacks enormes de Skills/plugins, usar catálogos como fonte de pesquisa e testar Skills importantes contra pequenos fixtures para detectar regressões. Essas observações não substituem documentação oficial nem revisão do código da Skill.

## Como a pesquisa vira Template Gold

A pesquisa não termina em uma lista de links. Cada padrão aprovado deve melhorar o template de forma concreta:

```text
pesquisa
   ↓
padrão útil comprovado
   ↓
trim + adaptação provider-neutral
   ↓
teste em fixture/projeto exemplo
   ↓
capacidade opcional reutilizável
   ↓
próximos projetos Gold
```

O objetivo é que um projeto novo possa nascer com:

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
└─ .agents/skills/...    somente Skills realmente necessárias
```

Nenhuma pasta ou Skill opcional precisa existir se não houver uso concreto.

## Roadmap

O desenvolvimento segue seis blocos simples:

1. **F0 — Golden Standard**: definir e provar a base Gold, incluindo a pesquisa das primeiras Skills Gold;
2. **F1 — Create**: criar projetos novos usando primeiro GitHub Template;
3. **F2 — Check + Audit**: verificação executável, saída curta e revisão independente;
4. **F3 — Packs + Skills**: disponibilizar capacidades específicas já estudadas e testadas;
5. **F4 — Adopt / Goldify**: elevar projetos existentes ao Gold sem reconstruí-los;
6. **F5 — Sync**: futuro, para distribuir melhorias do Standard sem empurrar capacidades desnecessárias.

Consulte `ROADMAP.md` para a matriz de estudo das Skills e `PROJECT_STATE.md` para o estado atual.

## Arquivos principais deste repositório

- `STANDARD.md` — regras canônicas do Gold Standard;
- `ROADMAP.md` — ordem de evolução e trilha de pesquisa/adaptação de Skills;
- `PROJECT_STATE.md` — estado atual;
- `AGENTS.md` — instruções mínimas para agentes neste próprio repositório;
- `CLI_CONTRACT.md` — superfície mínima esperada de automação/CLI;
- `packs/`, `examples/`, `fixtures/`, `schemas/` e `scripts/` — ativos existentes que serão mantidos somente quando continuarem úteis ao modelo Gold.

## Estado atual

O projeto está em **F0 — Golden Standard**.

A arquitetura antiga baseada em profiles, bundles, gates e lifecycle amplo foi substituída pelo modelo Gold. O código e os artefatos existentes serão reaproveitados apenas quando simplificarem o novo Standard.

A próxima frente é estudar em profundidade as referências da trilha F0-SK e transformar o aprendizado nas primeiras Skills Gold reutilizáveis, começando por `gold-audit`.

## Regra principal

> Se uma solução mais simples resolve corretamente o problema, use a solução mais simples.
