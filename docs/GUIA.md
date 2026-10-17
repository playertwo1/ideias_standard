# Guia — como usar o kit

Leia sob demanda; nada aqui precisa entrar no contexto permanente do agente.

## 1. Quanto documento cada tarefa merece

| Complexidade | Artefatos | Gate mínimo |
|---|---|---|
| Simples (correção, ajuste) | commit + `STATE.md` se mudou o estado | teste pertinente |
| Média (feature) | `FEATURE` + `STATE` + review curta | ACs e testes |
| Alta / arriscada | `FEATURE` + `EXECUTION_PLAN` + `REVIEW` (+ `DECISIONS` se a escolha for cara de desfazer) | revisão independente + aprovação humana |

O projeto funciona só com `PROJECT`, `ROADMAP`, `STATE` e `AGENTS`. O resto entra quando traz valor.

## 2. Da ideia à primeira versão

1. **Descoberta** — preencha `PROJECT.md`: quem sofre, por que a solução atual não basta, qual fluxo básico entrega valor. Pesquise alternativas e licenças antes de reimplementar.
2. **Decida o que NÃO fazer** — tire o que não ajuda a validar o primeiro fluxo e escreva em "Fora do MVP".
3. **Marcos com demonstração** — D0 visão → v0.1 fluxo real → v0.2 MVP → v0.3 estabilização → v1.0 entrega. Cada marco termina em algo observável, não em "API pronta".
3a. **Cara do app (se houver interface)** — preencha `DESIGN.md` antes da primeira tela: personalidade, referências e anti-referências, tokens de cor e tipografia, layout por tela e estados. Telas geradas por ferramenta (Stitch, Figma, v0) entram como referência em `docs/design/`; o `DESIGN.md` consolida o que vale. Referência adotada não é tela aprovada.
4. **Detalhe só o marco ativo** — IDs, dependências e prioridade no `ROADMAP.md`, em unidades que caibam numa sessão.
5. **Especifique** — `FEATURE` com Dado/Quando/Então, casos negativos, pré e pós-condições e AC-01, AC-02… O responsável pelo produto confirma o que é sucesso.
6. **Plano só se necessário** — `EXECUTION_PLAN` autocontido para integração ou refatoração grande.
7. **Fatia vertical** — um caminho ponta a ponta funcionando; registre o que rodou ou `NOT_RUN`.
8. **Revise com evidência** — `REVIEW` com commits, saída dos checks, prints, erros e regressões. Revisor diferente quando o risco for alto.
9. **Feche o marco** — `docs/RELEASE_CHECKLIST.md`, aprovação humana quando exigida, `ROADMAP` e `STATE` sincronizados. A próxima sessão, mesmo com outra IA, começa sem depender da conversa.

## 3. Estados

| Estado | Significa | Próxima ação |
|---|---|---|
| `READY` | critérios definidos e desbloqueado | pode implementar |
| `IN_PROGRESS` | em andamento | atualizar plano/`STATE` |
| `BLOCKED` | falta dependência, permissão ou decisão | não declarar concluído |
| `REVIEW` | pronto para avaliar ou AC pendente | rodar revisão e obter aprovação |
| `DONE` | aceite demonstrado e aprovação obtida | registrar evidência, seguir |
| `NOT_RUN` | teste não executado | é lacuna, não `PASS` |

## 4. Papéis entre agentes

Papéis, não capacidades exclusivas de um modelo. O ponto de integração são os documentos versionados, não mensagens privadas entre modelos.

- **Autoridade de produto** (pessoa): resolve trade-offs e autoriza fechar marco.
- **Planejador**: confirma objetivo e cria ID, spec e gate.
- **Builder**: escopo limitado, menor mudança correta, registra commits, comandos e alterações.
- **Auditor** (outro agente ou pessoa): começa por pedido, ACs, diff e resultado dos checks; expande contexto só para testar uma hipótese; devolve `PASS` ou findings com arquivo, impacto e correção. Verifica correção, regressão, escopo, complexidade desnecessária e falso sucesso. Roteiro e severidades (CRITICAL/HIGH/MEDIUM/LOW) em `docs/AUDIT.md` do template.

Não deixe dois agentes alterando os mesmos arquivos sem coordenação. O Builder segue `docs/WATCHDOG.md` (escopo, alto risco, regra de parada) em mudança média ou maior.

## 5. Prompts prontos

**Planejar, sem executar**
> Leia PROJECT.md, ROADMAP.md e STATE.md. Examine só o código relevante. Revise escopo do MVP, dependências e riscos. Proponha as próximas três entregas verificáveis com ACs e gates. Atualize apenas os documentos de planejamento; não implemente e não afirme o que não verificou.

**Executar uma feature**
> Implemente somente a FEATURE [ID], respeitando pré-condições e ACs. Se for complexa, escreva ou atualize o plano. Rode os testes pertinentes, registre resultados reais e bloqueios e atualize STATE.md. Não marque DONE sem evidência.

**Auditar**
> Siga docs/AUDIT.md. Revise a entrega [ID] a partir do pedido, dos ACs, do `git diff` e da saída dos checks. Reproduza os ACs que puder. Devolva `AUDIT RESULT: PASS` ou `FAIL` com findings (severidade, arquivo, impacto, correção). Marque NOT_RUN o que não executou.

## 6. Contexto e tokens

O objetivo é o máximo de sinal por token sem perder correção.

- `AGENTS.md` é mapa, não manual; o checker avisa acima de 120 linhas.
- Localize antes de ler; prefira o trecho ao arquivo; filtre saídas grandes de testes e builds.
- Tarefa nova e diferente: sessão nova em vez de histórico irrelevante. Trabalho longo: estado externo curto (`STATE`, plano).
- Não corte contexto crítico para economizar: retrabalho também custa.
- Arquivo exigido por fornecedor (`CLAUDE.md`, etc.) só aponta para `AGENTS.md`; nunca duplica regras.

## 7. Adotar em projeto existente

1. **Descubra sem alterar**: leia README, docs e estrutura; liste o que já cumpre o papel de cada arquivo do kit (um `PRODUCT.md` pode ser o `PROJECT.md` — o checker aceita os dois; um guia visual existente vira o `DESIGN.md`; uma tabela "Agora" no roadmap é o `STATE.md`; guardrails próprios, como os do repositório `guardrail`, viram `docs/WATCHDOG.md` e `docs/AUDIT.md`, com o bloco de agente incorporado ao `AGENTS.md` por link e não copiado).
2. **Proponha um diff** antes de mover: o que entra, o que muda de lugar, o que vira histórico. Arquivos do projeto (código, decisões humanas, docs autorais) não são sobrescritos; o kit só sugere.
3. **Corte redundância**: uma regra em um só lugar (gates no `RELEASE_CHECKLIST`, regras no `AGENTS`, estado no `STATE`); fases fechadas saem do roadmap para `docs/arquivo/`; repetidos viram link.
4. **Preserve**: mova com `git mv`, corrija links relativos, não reescreva histórico, não apague evidência de aceite.
5. **Verifique**: `python scripts/check.py <projeto>` limpo, links sem quebra, testes do projeto rodando.

## 8. Segurança e limites

- Nunca grave senhas, tokens ou conversas privadas em roadmap, logs ou evidências.
- Projeto que controla computadores ou contas: autenticação e menor privilégio desde o MVP.
- Separe desenvolvimento de ações em serviços reais; confirmação humana para o irreversível.
- Proibido "teste verde" obtido alterando o teste para mascarar bug.
- Integração com mensageria, dados de clientes ou finanças: escopo e política de uso antes de qualquer automação.

## 9. Checklist do responsável pelo projeto

- [ ] Consigo descrever o problema sem citar tecnologia?
- [ ] O MVP tem até três fluxos e o que fica de fora está escrito?
- [ ] Cada marco termina com algo demonstrável?
- [ ] A próxima tarefa tem ID, critérios e dependências?
- [ ] Um agente novo retoma sem ler a conversa antiga?
- [ ] Os testes foram realmente executados? Há evidência?
- [ ] A aprovação de produto está separada da revisão técnica?
- [ ] Estamos criando documentos só quando trazem valor?

## 10. Antes de complicar

Texto simples antes de schema; link antes de duplicação; script simples antes de framework; prática comprovada antes de padronizar. Uma regra só entra no kit depois de provar utilidade em projeto real (ver `ROADMAP.md` deste repositório).
