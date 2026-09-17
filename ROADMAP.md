# ROADMAP V5 — IDEIAS STANDARD GOLD

## 1. VISÃO

O **Ideias Standard** define uma base Gold simples e reutilizável para projetos desenvolvidos por humanos e agentes de IA.

O objetivo não é criar um framework de governança. O objetivo é tornar qualquer projeto fácil de entender, alterar, validar, auditar e manter.

Princípios:

> Pequeno por padrão. Contexto sob demanda. Verificação executável. Auditoria independente. Extensão somente quando necessária.

> Toda nova regra, arquivo, abstração, teste ou camada deve justificar o problema concreto que resolve.

---

## 2. O QUE É UM PROJETO GOLD

Um projeto está no padrão Gold quando:

- é fácil entender o que ele faz;
- possui `README.md` útil;
- possui `AGENTS.md` pequeno e operacional;
- a estrutura principal é clara;
- existe uma forma objetiva de validar alterações;
- build, testes e lint/typecheck aplicáveis funcionam;
- CI executa as verificações importantes;
- contexto específico é carregado somente quando necessário;
- outputs grandes são filtrados ou resumidos antes de entrar no contexto;
- alterações relevantes podem ser auditadas de forma independente;
- segurança básica é proporcional ao risco;
- não existe burocracia sem utilidade prática.

Gold padroniza **qualidade e operação**, não obriga todos os projetos a terem a mesma arquitetura.

---

## 3. CONTEXTO PROGRESSIVO E TOKEN DISCIPLINE

`AGENTS.md` é o contexto universal mínimo.

Ele deve permanecer curto e conter apenas:

- objetivo do projeto;
- regras essenciais;
- comandos principais;
- mapa mínimo da estrutura;
- referências para contexto adicional.

O bootstrap padrão é:

```text
AGENTS.md + pedido atual
```

`PROJECT_STATE.md`, `STANDARD.md`, `ROADMAP.md`, documentação, packs, Skills e dependências são carregados somente quando a tarefa justificar.

Fluxo recomendado:

```text
pedido
  ↓
localizar antes de ler
  ↓
menor trecho suficiente
  ↓
expandir somente se necessário
```

Informação específica deve ficar fora do `AGENTS.md`:

```text
AGENTS.md
   ↓
contexto mínimo
   ├─ docs/...                 quando necessário
   ├─ packs/...                quando necessário
   ├─ skills/...               quando necessário
   └─ dependências diretas     quando necessário
```

Regras de Token Discipline:

1. maximizar sinal por token, não apenas minimizar tokens;
2. localizar antes de carregar;
3. preferir trechos a arquivos completos;
4. limitar ou filtrar logs e outputs potencialmente grandes;
5. usar `check` como resumo executável das validações;
6. carregar docs, packs e Skills somente sob demanda;
7. ativar somente ferramentas/MCPs úteis à tarefa quando isso for controlável;
8. Auditor começa pelo delta;
9. tarefa materialmente nova prefere contexto novo a histórico irrelevante;
10. contexto crítico nunca é cortado apenas para economizar tokens.

Regra:

> Se uma instrução não é útil para a maioria das tarefas, ela não pertence ao `AGENTS.md`.

Evitar duplicar as mesmas instruções em `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` ou arquivos equivalentes. Quando um fornecedor exigir arquivo próprio, usar um adaptador mínimo para a fonte canônica sempre que possível.

---

## 4. FLUXO DE TRABALHO GOLD

### Tarefa pequena

```text
entender → alterar → check → auditoria → concluir
```

### Tarefa complexa

```text
entender → plano curto → alterar → check → auditoria → concluir
```

Planejamento deve ser proporcional à tarefa.

---

## 5. BUILDER E AUDITOR

O Builder implementa e valida o próprio trabalho.

O Auditor verifica de forma independente alterações relevantes.

O Auditor começa pelo delta, não pelo repositório inteiro.

Contexto inicial recomendado:

- pedido original;
- critério de aceite;
- diff;
- arquivos alterados;
- resultado resumido do `check`;
- erros ou warnings relevantes.

O Auditor expande contexto somente quando existir uma razão concreta.

Perguntas principais:

- o pedido foi atendido?
- a alteração funciona?
- existe regressão provável?
- há mudança fora do escopo?
- existe atalho, hardcode ou erro escondido?
- a solução ficou mais complexa do que precisava?
- os testes/verificações são suficientes para o comportamento alterado?

Resultado mínimo:

```text
AUDIT: PASS
```

ou:

```text
AUDIT: FAIL
- arquivo/local
- problema
- impacto
- correção esperada
```

O Runner pode automatizar Builder ↔ Auditor, mas continua externo e opcional:
https://github.com/playertwo1/runner

---

# F0 — GOLDEN STANDARD

**Status:** ACTIVE

## Objetivo

Definir e provar a menor base que torna um projeto Gold.

## Entregas

- [ ] consolidar este Standard Gold;
- [ ] manter `AGENTS.md` como contexto mínimo universal;
- [ ] consolidar `README.md` do template;
- [ ] definir estrutura mínima recomendada;
- [ ] formalizar Token Discipline;
- [ ] definir comando/mecanismo único de `check` com saída curta;
- [ ] manter CI simples;
- [ ] definir padrão mínimo de testes;
- [ ] definir segurança básica;
- [ ] executar a trilha de pesquisa de Skills Gold descrita abaixo;
- [ ] selecionar e adaptar somente Skills que reduzam contexto ou aumentem confiabilidade de forma clara;
- [ ] remover ou arquivar estruturas legadas que não agregam ao modelo Gold;
- [ ] criar pelo menos um exemplo Gold completo;
- [ ] executar auditoria independente da fase.

## F0-SK — TRILHA DE PESQUISA DE SKILLS GOLD

A pesquisa de Skills faz parte da construção do próprio Template Gold. O objetivo não é montar uma coleção grande: é descobrir padrões maduros que possam ser reaproveitados com **progressive disclosure, baixo custo de contexto e responsabilidade única**.

### Fontes prioritárias estudadas

1. **Agent Skills specification** — formato aberto e progressive disclosure:
   - https://github.com/agentskills/agentskills
2. **Anthropic / Claude Code skill-development** — estrutura, scripts e referências sob demanda:
   - https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev/skills/skill-development
3. **OpenAI Codex `code-review`** — revisão de mudanças com foco em findings:
   - https://github.com/openai/codex/tree/main/.codex/skills/code-review
4. **Trail of Bits `second-opinion`** — revisão de diff/commit por outro modelo e controle de diffs grandes:
   - https://github.com/trailofbits/skills/tree/main/plugins/second-opinion/skills/second-opinion
5. **Trail of Bits `audit-context-building`** — ampliar contexto de auditoria somente conforme hipóteses concretas:
   - https://github.com/trailofbits/skills/tree/main/plugins/audit-context-building/skills/audit-context-building
6. **GitHub Awesome Copilot `ai-ready`** — preparar repositórios para trabalho assistido por IA:
   - https://github.com/github/awesome-copilot/tree/main/skills/ai-ready
7. **GitHub Awesome Copilot `acquire-codebase-knowledge`** — identificar stack, estrutura, CI e testes:
   - https://github.com/github/awesome-copilot/tree/main/skills/acquire-codebase-knowledge
8. **GitHub Awesome Copilot `agent-skill-stack`** — selecionar o menor conjunto compatível de Skills:
   - https://github.com/github/awesome-copilot/tree/main/skills/agent-skill-stack
9. **GitHub Awesome Copilot `security-review`** — referência para futuro pack de segurança:
   - https://github.com/github/awesome-copilot/tree/main/skills/security-review
10. **GitHub Awesome Copilot `secret-scanning`** — referência para proteção de secrets:
    - https://github.com/github/awesome-copilot/tree/main/skills/secret-scanning
11. **GitHub Awesome Copilot `agentic-eval`** — referência para projetos de IA que realmente precisem de evals:
    - https://github.com/github/awesome-copilot/tree/main/skills/agentic-eval

### Sinais da comunidade estudados

Discussões no Reddit foram usadas como sinal prático, não como contrato canônico. Os padrões recorrentes foram:

- coleções muito grandes de Skills/plugins aumentam descoberta, contexto e manutenção;
- instalar uma Skill só porque parece útil tende a gerar sobreposição e drift;
- Skills importantes precisam de pequenos casos de teste/fixtures para detectar regressões após mudanças de ferramentas/modelos;
- catálogos grandes são melhores como fontes de pesquisa do que como conjuntos instalados por padrão.

Referências comunitárias avaliadas incluem discussões em `r/ClaudeCode`, `r/claudeskills`, `r/codex` e `r/vibecoding` sobre stacks de Skills, excesso de plugins, revisão independente e testes de Skills.

### Método obrigatório de avaliação

Para cada Skill candidata:

```text
DISCOVER
   ↓
READ MINIMUM
   ↓
REVIEW SECURITY + LICENSE
   ↓
EXTRACT USEFUL PATTERN
   ↓
TRIM
   ↓
ADAPT PROVIDER-NEUTRAL
   ↓
TEST ON FIXTURE
   ↓
KEEP or REJECT
```

A Skill só entra no Gold quando houver resposta clara para:

- qual problema repetitivo ela resolve;
- por que isso não deve ficar no `AGENTS.md`;
- por que um script simples sozinho não resolve melhor;
- quais tokens/contexto ela evita ou quais erros ela previne;
- se existe sobreposição com Skill já adotada;
- se a licença permite o reaproveitamento pretendido;
- se os scripts e instruções foram revisados por segurança;
- se funciona em pelo menos um fixture ou projeto de exemplo.

### Skills Gold prioritárias para construir

#### 1. `gold-audit` — PRIORIDADE 1

Estudar e combinar somente os padrões úteis de:

- OpenAI Codex `code-review`;
- Trail of Bits `second-opinion`;
- Trail of Bits `audit-context-building`.

Objetivo:

```text
pedido + aceite + diff + check
              ↓
        Auditor independente
              ↓
      PASS ou FINDINGS
```

Requisitos:

- começar pelo delta;
- não exigir leitura global do repositório;
- ampliar contexto somente por hipótese concreta;
- limitar diffs/logs muito grandes antes de carregá-los;
- saída curta e acionável;
- funcionar sem depender de um provedor específico;
- ter fixture com alteração correta e fixture com bug proposital.

O `gold-audit` servirá tanto ao próprio Ideias Standard quanto aos projetos futuros gerados pelo Template Gold.

#### 2. `goldify` — PRIORIDADE 2

Estudar principalmente:

- GitHub `ai-ready`;
- GitHub `acquire-codebase-knowledge`.

Objetivo:

```text
projeto existente
      ↓
descoberta leve
      ↓
stack + CI + tests + docs + AGENTS + check
      ↓
Golden Diff
```

Não copiar o comportamento de gerar documentação extensa por padrão. O resultado Gold deve ser curto:

```text
NECESSÁRIO
...

RECOMENDADO
...
```

Requisitos:

- preservar arquitetura e trabalho existente;
- localizar antes de ler;
- não produzir sete relatórios quando um Golden Diff resolve;
- alimentar diretamente F4 — Adopt / Goldify;
- ser reutilizável para os próximos repositórios existentes que forem levados ao Gold.

#### 3. `skill-author` — PRIORIDADE 3

Estudar:

- Agent Skills specification;
- Anthropic/Claude Code `skill-development`;
- boas práticas de scripts/references com progressive disclosure.

Objetivo: impedir que o ecossistema Gold vire uma coleção desorganizada de Skills.

Antes de criar uma nova Skill, verificar:

1. a tarefa é repetitiva?
2. precisa de conhecimento/procedimento especializado?
3. cabe melhor em Skill do que em `AGENTS.md`?
4. um script simples seria suficiente?
5. já existe uma Skill madura que podemos adaptar?
6. existe teste mínimo que prove sua utilidade?

Resultado possível:

```text
CREATE SKILL
```

ou:

```text
DO NOT CREATE SKILL
```

#### 4. `skill-curator` — CANDIDATA FUTURA

Estudar o padrão de `agent-skill-stack`.

Objetivo futuro: dado um projeto, recomendar o **menor conjunto necessário de Skills**, considerando utilidade, sobreposição, risco e custo de contexto.

Não implementar antes das três Skills prioritárias estarem comprovadas.

### Skills opcionais por domínio

Não fazem parte do Core e só serão avaliadas quando um projeto real exigir:

- `security-review` → pack `sensitive-data`/security;
- `secret-scanning` → segurança de repositório;
- `agentic-eval` → projetos de IA com avaliação de agentes;
- Skills Android → pack Android;
- Skills de migration/release → somente quando houver fluxo repetitivo real.

### Resultado esperado da pesquisa

Ao finalizar F0-SK, o projeto deve ter:

- [ ] matriz de decisão das Skills prioritárias;
- [ ] `gold-audit` desenhada e testada;
- [ ] `goldify` desenhada para alimentar F4;
- [ ] `skill-author` desenhada para controlar futuras Skills;
- [ ] critérios claros para rejeitar Skills desnecessárias;
- [ ] nenhum aumento relevante do contexto permanente do `AGENTS.md`;
- [ ] aprendizado incorporado ao Template Gold para novos projetos.

## Validação de F0

O exemplo Gold deve ser compreensível, verificável e utilizável sem documentação excessiva ou carregamento desnecessário de contexto.

---

# F1 — CREATE

**Status:** NOT_STARTED

## Objetivo

Criar novos projetos Gold da forma mais simples possível.

## Estratégia

Começar por **GitHub Template Repository**.

Adicionar gerador próprio somente se houver necessidade real que o template não resolva.

Se parametrização mais rica for necessária, avaliar ferramenta existente antes de criar engine própria.

## Entregas

- [ ] disponibilizar template Gold utilizável;
- [ ] permitir criação de projeto base em poucos passos;
- [ ] permitir escolha simples de packs quando aplicável;
- [ ] manter Skills fora do Core por padrão;
- [ ] permitir que Skills aprovadas sejam adicionadas somente quando pertinentes ao projeto;
- [ ] garantir que o projeto criado passa no `check`;
- [ ] documentar fluxo de criação em poucas linhas.

## Template Gold alvo

Estrutura conceitual mínima:

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

Nenhuma pasta opcional precisa existir vazia.

---

# F2 — CHECK + AUDIT

**Status:** NOT_STARTED

## Objetivo

Dar ao projeto uma resposta objetiva para:

> Como eu provo que esta alteração não quebrou o projeto?

## `check`

O projeto deve possuir um comando ou mecanismo conhecido que execute apenas as verificações aplicáveis, por exemplo:

```text
check
 ├─ format/lint
 ├─ typecheck
 ├─ tests
 └─ build
```

Nem toda stack exige todas as etapas.

A saída padrão deve ser resumida:

```text
PASS
✓ lint
✓ tests
✓ build
```

Falhas devem mostrar somente informação acionável por padrão. Logs completos ficam disponíveis por modo detalhado quando necessário.

## Entregas

- [ ] `check` simples e reproduzível;
- [ ] saída curta e clara de sucesso ou falha;
- [ ] detalhes expandíveis quando houver investigação;
- [ ] CI utiliza as mesmas verificações importantes;
- [ ] bug relevante recebe teste de regressão quando fizer sentido;
- [ ] auditoria independente começa pelo diff;
- [ ] `gold-audit` pode ser usada quando disponível;
- [ ] auditor amplia contexto somente sob necessidade.

## Regra

Testar comportamento importante, não detalhes internos apenas para aumentar cobertura.

---

# F3 — PACKS + SKILLS

**Status:** NOT_STARTED

## Objetivo

Adicionar capacidade sem inflar o Core.

## Packs candidatos

- `android`;
- `python`;
- `web`;
- `ai`;
- `multi-agent`;
- `sensitive-data`;
- `agent-guardrails`.

Um pack existe somente quando um projeto real justifica sua existência.

Packs não devem despejar grandes blocos no `AGENTS.md`. Devem manter contexto específico próximo do domínio e adicionar apenas referências mínimas quando necessário.

## Política de Skills

As três primeiras Skills do ecossistema Gold são:

1. `gold-audit`;
2. `goldify`;
3. `skill-author`.

Elas são estudadas durante F0 e só se tornam parte reutilizável do ecossistema depois de testadas.

Skills externas nunca são copiadas cegamente:

```text
DISCOVER → REVIEW → TRIM → ADAPT → TEST → INSTALL
```

Uma Skill deve ter responsabilidade única, progressive disclosure e justificativa concreta.

## Guardrails

As melhores ideias do projeto `playertwo1/guardrail` entram em duas camadas:

- Core: poucas regras essenciais no `AGENTS.md`;
- Pack `agent-guardrails`: controles ampliados apenas quando o risco justificar.

---

# F4 — ADOPT / GOLDIFY

**Status:** NOT_STARTED

## Objetivo

Elevar projetos existentes ao padrão Gold sem reescrever o produto nem destruir trabalho válido.

Fluxo:

```text
projeto existente
      ↓
inventário leve
      ↓
comparação com Gold
      ↓
Golden Diff
      ↓
plano curto
      ↓
preview das mudanças
      ↓
aplicar somente o necessário
      ↓
check
      ↓
auditoria independente
      ↓
GOLD
```

A Skill `goldify` será a principal candidata para implementar a descoberta e o Golden Diff sem carregar o repositório inteiro.

## Golden Diff

O relatório deve separar:

```text
NECESSÁRIO
- itens que impedem o padrão Gold

RECOMENDADO
- melhorias úteis, não obrigatórias
```

Sem nota arbitrária ou sistema complexo de pontuação.

## Proteção do projeto existente

Antes de alterar:

- examinar estado atual;
- preservar mudanças locais e trabalho válido;
- não reorganizar arquitetura sem necessidade;
- preferir adicionar infraestrutura Gold ao redor do código existente;
- mostrar diff antes de mudanças relevantes quando aplicável.

---

# F5 — SYNC

**Status:** FUTURE

## Objetivo

Permitir que projetos Gold existentes recebam melhorias futuras do Standard sem reescrever o projeto.

Só implementar após Create, Check e Adopt estarem comprovados em uso real.

Skills adicionadas ao ecossistema também devem respeitar compatibilidade e não ser empurradas automaticamente para projetos que não precisam delas.

---

## 6. SEGURANÇA

Baseline Gold:

- não versionar secrets;
- `.gitignore` adequado;
- dependências atualizáveis;
- CI sem exposição de credenciais;
- validação de entradas externas quando aplicável;
- nenhuma operação destrutiva silenciosa.

Projetos de maior risco recebem packs específicos. O Core não carrega controles de sistemas críticos que a maioria dos projetos não precisa.

Skills externas são parte da superfície de confiança: instruções, scripts, permissões e licença devem ser revisados antes da adoção.

---

## 7. ANTI-OVERENGINEERING

Regras permanentes:

1. Faça a menor mudança coerente que resolva o pedido.
2. Não crie abstrações para necessidades hipotéticas.
3. Não duplique contexto.
4. Não transforme documentação em burocracia.
5. Não crie schema quando texto simples resolve.
6. Não crie ferramenta própria quando uma solução madura e simples já atende.
7. Não leia o repositório inteiro sem necessidade objetiva.
8. Não adicione testes sem comportamento útil a proteger.
9. Não imponha pack ou Skill opcional ao Core.
10. Não instale catálogo de Skills inteiro quando uma ou duas Skills resolvem a necessidade.
11. Remova complexidade que deixou de justificar sua existência.

---

## 8. ORDEM DE EXECUÇÃO

```text
F0 Golden Standard
   └─ F0-SK pesquisa e desenho das Skills Gold
        ↓
F1 Create
        ↓
F2 Check + Audit
        ↓
F3 Packs + Skills
        ↓
F4 Adopt / Goldify
        ↓
F5 Sync (futuro)
```

As fases organizam construção; não são gates burocráticos.

---

## 9. DEFINIÇÃO FINAL

O Ideias Standard terá cumprido sua função quando um humano ou agente puder:

1. entender rapidamente um projeto;
2. carregar somente o contexto necessário;
3. localizar informação antes de carregar grandes volumes;
4. fazer uma mudança pequena e correta;
5. provar que ela funciona com saída enxuta;
6. submetê-la a uma revisão independente;
7. usar Skills especializadas somente quando necessárias;
8. criar projetos novos já preparados para progressive disclosure e auditoria;
9. elevar projetos antigos ao Gold sem reconstruí-los;
10. reutilizar o aprendizado de Skills maduras sem importar sua complexidade desnecessária.
