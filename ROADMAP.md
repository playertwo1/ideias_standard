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
- [ ] revisar Skills maduras que possam ser reaproveitadas;
- [ ] remover ou arquivar estruturas legadas que não agregam ao modelo Gold;
- [ ] criar pelo menos um exemplo Gold completo;
- [ ] executar auditoria independente da fase.

## Validação

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
- [ ] garantir que o projeto criado passa no `check`;
- [ ] documentar fluxo de criação em poucas linhas.

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

## Skills Gold iniciais

Pesquisar e adaptar soluções maduras antes de criar do zero.

Prioridade inicial:

- `gold-audit` — auditoria independente baseada em pedido + diff + `check`;
- `goldify` — descobrir stack, comparar com Gold e gerar Golden Diff;
- `skill-author` — criar e revisar Skills pequenas, seguras e com progressive disclosure.

Outras Skills entram somente quando houver uso concreto repetido.

## Política para Skills externas

```text
DISCOVER → REVIEW → TRIM → ADAPT → TEST → INSTALL
```

Antes de incorporar:

- revisar instruções e scripts;
- verificar segurança e permissões;
- verificar licença;
- remover conteúdo irrelevante;
- evitar dependência de fornecedor quando não necessária;
- confirmar que progressive disclosure é preservado;
- testar em projeto de exemplo.

Uma Skill deve ter uma responsabilidade clara. Scripts existentes devem ser executados como ferramentas quando possível, sem carregar sua implementação inteira no contexto.

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
10. Remova complexidade que deixou de justificar sua existência.

---

## 8. ORDEM DE EXECUÇÃO

```text
F0 Golden Standard
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
8. criar projetos novos no mesmo padrão;
9. elevar projetos antigos ao Gold sem reconstruí-los.
