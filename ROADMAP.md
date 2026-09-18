# ROADMAP V5 — IDEIAS STANDARD GOLD

## 1. VISÃO

O **Ideias Standard** define uma base Gold simples e reutilizável para projetos desenvolvidos por humanos e agentes de IA.

A missão possui dois caminhos:

```text
NOVO PROJETO → CREATE → TEMPLATE GOLD → PROJETO GOLD
PROJETO EXISTENTE → GOLDIFY → GOLDEN DIFF → CHECK + AUDIT → PROJETO GOLD
```

O objetivo não é criar um framework de governança. É tornar projetos fáceis de entender, alterar, validar, auditar e manter.

Princípios:

> Pequeno por padrão. Contexto sob demanda. Verificação executável. Auditoria independente. Extensão somente quando necessária.

> Toda nova regra, arquivo, abstração, teste ou camada deve justificar o problema concreto que resolve.

### Duas regras de execução

**Dogfooding obrigatório**

> O próprio `ideias_standard` deve seguir o Gold que define. Antes de recomendar uma prática aos próximos projetos, devemos conseguir usá-la de forma simples neste repositório ou em um exemplo Gold representativo.

**Provar antes de expandir**

> Nova Skill, pack, regra, arquivo, abstração ou capacidade não entra no Core apenas porque parece útil. Primeiro deve resolver um problema real, ser testada e demonstrar valor. Se a necessidade for local, permanece local.

Fluxo:

```text
ideia nova
   ↓
resolve problema real?
   ├─ não → ignorar/backlog
   └─ sim
        ↓
solução mais simples?
        ↓
testar no próprio Standard ou projeto real
        ↓
funcionou e tende a se repetir?
   ├─ não → manter local
   └─ sim → considerar no Gold
```

---

## 2. O QUE É UM PROJETO GOLD

Um projeto Gold, quando aplicável:

- explica claramente o que faz;
- possui `README.md` útil;
- possui `AGENTS.md` pequeno e operacional;
- tem estrutura compreensível;
- possui uma forma conhecida de verificar alterações;
- executa build/test/lint/typecheck aplicáveis;
- executa verificações importantes no CI;
- carrega contexto específico somente quando necessário;
- filtra ou resume outputs grandes antes de colocá-los no contexto;
- pode ser auditado pelo diff sem exigir leitura integral do repositório;
- usa segurança proporcional ao risco;
- não carrega burocracia sem utilidade prática.

Gold padroniza **qualidade e operação**, não arquitetura interna obrigatória.

---

## 3. CONTEXTO PROGRESSIVO E TOKEN DISCIPLINE

`AGENTS.md` é o contexto universal mínimo.

Bootstrap padrão:

```text
AGENTS.md + pedido atual
```

`PROJECT_STATE.md`, `STANDARD.md`, `ROADMAP.md`, documentação, packs, Skills e dependências são carregados somente quando a tarefa justificar.

Fluxo:

```text
pedido
  ↓
localizar antes de ler
  ↓
menor trecho suficiente
  ↓
expandir somente se necessário
```

Regras de Token Discipline:

1. maximizar sinal por token, não apenas minimizar tokens;
2. localizar antes de carregar;
3. preferir trechos a arquivos completos;
4. limitar ou filtrar logs e outputs grandes;
5. usar `check` como resumo executável das validações;
6. carregar docs, packs e Skills somente sob demanda;
7. ativar somente ferramentas/MCPs úteis quando isso for controlável;
8. Auditor começa pelo delta;
9. tarefa materialmente nova prefere contexto novo a histórico irrelevante;
10. contexto crítico nunca é cortado apenas para economizar tokens.

Regra do `AGENTS.md`:

> Se uma instrução não é útil para a maioria das tarefas, ela não pertence ao `AGENTS.md`.

---

## 4. FLUXO DE TRABALHO GOLD

Tarefa pequena:

```text
entender → alterar → check → auditoria → concluir
```

Tarefa complexa:

```text
entender → plano curto → alterar → check → auditoria → concluir
```

Planejamento deve ser proporcional à tarefa.

### Builder

- entende o pedido antes de editar;
- faz a menor mudança correta;
- preserva comportamento e trabalho existentes;
- não trata suposição como fato;
- não cria abstrações para necessidades hipotéticas;
- valida antes de concluir.

### Auditor

Começa por:

- pedido e critérios de aceite;
- diff;
- arquivos alterados;
- resultado resumido do `check`;
- erros/warnings relevantes.

Amplia contexto somente quando existir razão concreta.

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

**Status:** IMPLEMENTED — auditoria independente registrada; consolidação final pendente

## Objetivo

Definir e provar a menor base que torna um projeto Gold.

## Entregas

- [x] consolidar o Standard Gold (aguardando auditoria independente);
- [x] manter `AGENTS.md` como contexto mínimo universal;
- [x] consolidar `README.md` do template;
- [x] definir estrutura mínima recomendada;
- [x] formalizar Token Discipline;
- [x] definir `check` com saída curta e detalhes sob demanda;
- [x] manter CI simples e testes essenciais;
- [x] definir segurança básica;
- [x] executar a trilha F0-SK de Skills Gold;
- [x] revisar ativos legados e remover complexidade sem função prática;
- [x] aplicar o Gold ao próprio `ideias_standard` como dogfood;
- [x] criar pelo menos um exemplo Gold completo;
- [x] executar auditoria independente final da fase (registro individual; consolidação final pendente).

### Critério adicional de F0

Uma prática não deve ser promovida para os templates futuros apenas por ter sido documentada. Ela precisa ser exercitada no próprio Standard, em fixture, exemplo Gold ou projeto real adequado.

---

## F0-SK — PESQUISA DE SKILLS GOLD

A pesquisa de Skills faz parte da construção do Template Gold. O objetivo não é montar uma coleção grande, mas reaproveitar padrões maduros com **progressive disclosure, baixo custo de contexto e responsabilidade única**.

### Fontes prioritárias estudadas

1. Agent Skills specification — https://github.com/agentskills/agentskills
2. Anthropic / Claude Code `skill-development` — https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev/skills/skill-development
3. OpenAI Codex `code-review` — https://github.com/openai/codex/tree/main/.codex/skills/code-review
4. Trail of Bits `second-opinion` — https://github.com/trailofbits/skills/tree/main/plugins/second-opinion/skills/second-opinion
5. Trail of Bits `audit-context-building` — https://github.com/trailofbits/skills/tree/main/plugins/audit-context-building/skills/audit-context-building
6. GitHub Awesome Copilot `ai-ready` — https://github.com/github/awesome-copilot/tree/main/skills/ai-ready
7. GitHub Awesome Copilot `acquire-codebase-knowledge` — https://github.com/github/awesome-copilot/tree/main/skills/acquire-codebase-knowledge
8. GitHub Awesome Copilot `agent-skill-stack` — https://github.com/github/awesome-copilot/tree/main/skills/agent-skill-stack
9. GitHub Awesome Copilot `security-review` — referência para futuro pack de segurança
10. GitHub Awesome Copilot `secret-scanning` — referência para proteção de secrets
11. GitHub Awesome Copilot `agentic-eval` — referência para projetos de IA que realmente precisem de evals

Discussões em Reddit são sinal complementar, não fonte canônica. O aprendizado principal é evitar stacks enormes de Skills/plugins, usar catálogos para descoberta e testar Skills importantes contra pequenos fixtures.

### Método obrigatório para Skill externa

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
TEST ON FIXTURE / REAL USE
   ↓
KEEP or REJECT
```

Antes de incorporar, responder:

- qual problema repetitivo resolve?
- por que não pertence ao `AGENTS.md`?
- por que um script simples não resolve melhor?
- que contexto evita ou que erro previne?
- existe sobreposição com Skill já adotada?
- a licença permite o reaproveitamento?
- scripts/instruções foram revisados por segurança?
- foi testada em fixture, exemplo ou projeto real?

### Skills Gold prioritárias

#### 1. `gold-audit` — PRIORIDADE 1

Combinar somente os padrões úteis de:

- Codex `code-review`;
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
- ampliar contexto somente por hipótese concreta;
- limitar diffs/logs grandes;
- saída curta e acionável;
- provider-neutral;
- fixture correta e fixture com bug proposital;
- provar a Skill primeiro no próprio `ideias_standard` ou exemplo Gold antes de promovê-la aos templates.

#### 2. `goldify` — PRIORIDADE 2

Estudar principalmente `ai-ready` e `acquire-codebase-knowledge`.

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

Resultado padrão:

```text
NECESSÁRIO
...

RECOMENDADO
...
```

Requisitos:

- preservar arquitetura e trabalho existentes;
- localizar antes de ler;
- evitar relatórios excessivos;
- alimentar F4 diretamente;
- provar em projeto existente real antes de tratar a abordagem como padrão universal.

#### 3. `skill-author` — PRIORIDADE 3

Estudar Agent Skills specification e Anthropic/Claude Code `skill-development`.

Antes de criar Skill:

1. a tarefa é repetitiva?
2. precisa de procedimento especializado?
3. cabe melhor em Skill do que em `AGENTS.md`?
4. script simples resolveria?
5. existe Skill madura adaptável?
6. há teste mínimo de utilidade?

Resultado:

```text
CREATE SKILL
```

ou:

```text
DO NOT CREATE SKILL
```

#### 4. `skill-curator` — FUTURA

Estudar `agent-skill-stack` para recomendar o menor conjunto útil de Skills.

Não implementar antes das três Skills prioritárias estarem comprovadas.

### Skills opcionais por domínio

Avaliar somente diante de necessidade real:

- `security-review` → security/sensitive-data;
- `secret-scanning` → segurança de repositório;
- `agentic-eval` → projetos de IA;
- Skills Android → pack Android;
- migration/release → quando houver fluxo repetitivo real.

### Saída esperada de F0-SK

- [x] matriz de decisão das Skills prioritárias;
- [x] `gold-audit` desenhada, testada e dogfooded;
- [x] `goldify` desenhada e testada em fixture de projeto existente (sem alegar projeto real);
- [x] `skill-author` desenhada para controlar futuras Skills;
- [x] critérios claros de rejeição;
- [ ] nenhum aumento relevante do contexto permanente do `AGENTS.md`.

---

# F1 — CREATE

**Status:** IMPLEMENTED — aguardando auditoria independente

## Objetivo

Criar novos projetos Gold da forma mais simples possível.

## Estratégia

Começar por **GitHub Template Repository**.

Adicionar gerador próprio somente se uma necessidade real provar que o template simples é insuficiente.

## Entregas

- [x] template Gold utilizável;
- [x] criação de projeto base em poucos passos;
- [x] packs escolhidos somente quando aplicáveis;
- [x] Skills fora do Core por padrão;
- [x] Skills aprovadas adicionadas somente quando pertinentes;
- [x] projeto criado passa no `check`;
- [x] fluxo de criação documentado em poucas linhas.

## Template alvo

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

Nenhuma pasta opcional precisa existir vazia.

O template deve ser primeiro exercitado pelo próprio `ideias_standard` e por pelo menos um exemplo/projeto real antes de ser considerado estável.

---

# F2 — CHECK + AUDIT

**Status:** IMPLEMENTED — aguardando auditoria independente

## Objetivo

Responder objetivamente:

> Como eu provo que esta alteração não quebrou o projeto?

`check` executa somente verificações aplicáveis:

```text
check
 ├─ format/lint
 ├─ typecheck
 ├─ tests
 └─ build
```

Saída padrão curta:

```text
PASS
✓ lint
✓ tests
✓ build
```

Falhas mostram informação acionável; logs completos ficam sob demanda.

## Entregas

- [x] `check` simples e reproduzível;
- [x] saída curta;
- [x] detalhes expandíveis;
- [x] CI reutiliza as verificações importantes;
- [x] regressão relevante recebe teste quando fizer sentido;
- [x] Auditor começa pelo diff;
- [x] `gold-audit` utilizada quando comprovada;
- [ ] Auditor amplia contexto somente quando necessário.

---

# F3 — PACKS + SKILLS

**Status:** IMPLEMENTED — aguardando auditoria independente

## Objetivo

Adicionar capacidade sem inflar o Core.

Packs candidatos:

- `android`;
- `python`;
- `web`;
- `ai`;
- `multi-agent`;
- `sensitive-data`;
- `agent-guardrails`.

Regra:

> Pack ou Skill só entra no ecossistema reutilizável depois que uma necessidade real e uso comprovado justificarem sua existência.

As três primeiras Skills planejadas são `gold-audit`, `goldify` e `skill-author`; permanecem opcionais e não são instaladas no template.

O projeto `playertwo1/guardrail` continua como fonte de padrões úteis; controles ampliados pertencem ao pack `agent-guardrails`, não ao Core.

---

# F4 — ADOPT / GOLDIFY

**Status:** IMPLEMENTED — aguardando auditoria independente

## Objetivo

Elevar projetos existentes ao Gold sem reescrever o produto nem destruir trabalho válido.

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
aplicar somente o necessário
      ↓
check
      ↓
auditoria independente
      ↓
GOLD
```

Golden Diff:

```text
NECESSÁRIO
- itens que impedem o Gold

RECOMENDADO
- melhorias úteis, não obrigatórias
```

A Skill `goldify` é candidata principal para essa descoberta.

Implementação mínima: `scripts/goldify.py` faz descoberta somente leitura e produz
Golden Diff em `NECESSÁRIO` e `RECOMENDADO`; arquivos existentes são USER_OWNED por padrão.

Proteções:

- preservar mudanças locais e trabalho válido;
- não reorganizar arquitetura sem necessidade;
- preferir infraestrutura Gold ao redor do código existente;
- mostrar mudanças relevantes quando aplicável.

F4 foi validada em fixture representativa; automação ampla permanece fora do escopo.

---

# F5 — SYNC

**Status:** IMPLEMENTED — auditoria independente registrada; consolidação final pendente

## Objetivo

Permitir que projetos Gold existentes recebam melhorias futuras sem reescrever o projeto.

Só implementar depois de Create, Check e Adopt estarem comprovados em uso real.

Nada novo é empurrado automaticamente para projetos que não precisam da capacidade.

Implementação mínima: `scripts/sync.py` gera plano antes de escrever, preserva conflitos
USER_OWNED e exige confirmação explícita para ações destrutivas.

---

## 6. SEGURANÇA

Baseline:

- não versionar secrets;
- `.gitignore` adequado;
- dependências atualizáveis;
- CI sem exposição de credenciais;
- validar entradas externas quando aplicável;
- nenhuma operação destrutiva silenciosa.

Projetos de maior risco recebem packs específicos.

Skills externas fazem parte da superfície de confiança: instruções, scripts, permissões e licença devem ser revisados antes da adoção.

---

## 7. ANTI-OVERENGINEERING

1. Faça a menor mudança coerente que resolva o pedido.
2. Não crie abstrações para necessidades hipotéticas.
3. Não duplique contexto.
4. Não transforme documentação em burocracia.
5. Não crie schema quando texto simples resolve.
6. Não crie ferramenta própria quando solução madura e simples já atende.
7. Não leia o repositório inteiro sem necessidade objetiva.
8. Não adicione testes sem comportamento útil a proteger.
9. Não imponha pack ou Skill opcional ao Core.
10. Não instale catálogo de Skills quando uma ou duas resolvem.
11. Não promova algo ao Gold antes de provar em uso adequado.
12. Remova complexidade que deixou de justificar sua existência.

---

## 8. ORDEM DE EXECUÇÃO

```text
F0 Golden Standard
   ├─ dogfooding do próprio Standard
   └─ F0-SK pesquisa/prova das Skills Gold
        ↓
F1 Create
        ↓
F2 Check + Audit
        ↓
F3 Packs + Skills
        ↓
F4 Adopt / Goldify
        ↓
F5 Sync
```

As fases organizam construção; não são gates burocráticos.

---

## 9. DEFINIÇÃO FINAL

O Ideias Standard cumpre sua função quando consegue:

1. aplicar suas próprias regras de forma simples;
2. entender rapidamente um projeto;
3. carregar somente o contexto necessário;
4. fazer mudança pequena e correta;
5. provar que funciona com saída enxuta;
6. submeter alteração a revisão independente;
7. usar Skills somente quando necessárias;
8. criar projetos novos no Gold;
9. elevar projetos existentes ao Gold sem reconstruí-los;
10. promover ao padrão reutilizável apenas práticas comprovadas em uso real.
