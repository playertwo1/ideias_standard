# Ideias Standard — Gold Standard

Versão do repositório: `0.1.0-draft`.
Modelo canônico: **Gold V5**.

## 1. Missão

Definir uma base simples e reutilizável para projetos que precisam ser fáceis de entender, alterar, validar, auditar e manter por humanos e agentes de IA.

O Ideias Standard não é um framework de governança. É um **Golden Standard operacional** para dois cenários:

- criar projetos novos já bem estruturados;
- elevar projetos existentes ao Gold sem reconstruí-los.

## 2. Princípios canônicos

1. **Small Core** — poucas regras universais.
2. **Progressive Context** — carregar somente o contexto necessário para a tarefa atual.
3. **Token Discipline** — maximizar sinal por token e evitar contexto sem função prática.
4. **Executable Verification** — preferir build, testes, lint, typecheck e scripts reais a instruções vagas.
5. **Independent Audit** — alterações relevantes podem ser revisadas por outro agente/processo.
6. **Optional Packs & Skills** — capacidades específicas permanecem fora do Core até serem necessárias.
7. **No Overengineering** — nenhuma abstração, arquivo ou camada existe sem problema concreto.
8. **Preserve Existing Work** — padronizar não significa reescrever o projeto.
9. **Security Proportional to Risk** — segurança cresce conforme o risco real.
10. **Dogfooding** — o Standard deve conseguir aplicar a si mesmo o padrão que recomenda.
11. **Prove Before Expand** — nada vira regra reutilizável do Gold antes de demonstrar valor em uso adequado.

## 3. Definição de Gold

Um projeto Gold deve, quando aplicável:

- ter objetivo e uso claros;
- possuir `README.md` útil;
- possuir `AGENTS.md` pequeno e operacional;
- ter estrutura compreensível;
- possuir verificações executáveis;
- executar verificações importantes no CI;
- manter contexto específico fora do Core;
- permitir auditoria independente pelo delta;
- evitar secrets e configurações inseguras básicas;
- permanecer simples o suficiente para ser mantido.

O Standard padroniza qualidade e operação, não arquitetura interna obrigatória.

## 4. `AGENTS.md`

`AGENTS.md` é a fonte canônica de instruções universais para agentes.

Ele deve conter apenas informação de alto valor para a maioria das tarefas:

- objetivo do projeto;
- poucas regras permanentes;
- comandos principais;
- mapa mínimo da estrutura;
- referências para contexto adicional.

Regra:

> Se uma instrução não é útil para a maioria das tarefas, ela não pertence ao `AGENTS.md`.

Evitar copiar o mesmo conteúdo para arquivos específicos de fornecedores. Se um fornecedor exigir arquivo próprio, preferir um adaptador mínimo que aponte para a fonte canônica sempre que possível.

## 5. Contexto progressivo

A leitura começa pequena e cresce apenas sob necessidade.

```text
AGENTS.md + pedido
   ↓
contexto mínimo
   ├─ busca/localização
   ├─ trecho ou arquivo necessário
   ├─ documentação específica
   ├─ pack da tecnologia
   ├─ Skill do procedimento
   └─ dependências diretas necessárias
```

Regras:

- localizar antes de carregar;
- preferir trechos relevantes a arquivos inteiros;
- não escanear o repositório inteiro por padrão;
- não carregar estado, roadmap ou documentação sem relação concreta com a tarefa;
- expandir contexto somente quando uma hipótese ou dependência justificar.

Não criar um engine complexo de contexto enquanto referências simples e organização por domínio forem suficientes.

## 6. Token Discipline

O objetivo não é minimizar tokens a qualquer custo. É **maximizar sinal por token sem perder correção**.

Práticas Gold:

1. `AGENTS.md` funciona como mapa, não manual.
2. Localizar antes de ler e ler o menor trecho suficiente.
3. Limitar ou filtrar outputs potencialmente grandes de terminal, testes, builds e ferramentas.
4. `check` deve resumir validações; logs detalhados ficam disponíveis somente quando necessários.
5. Carregar docs, packs e Skills somente sob demanda.
6. Ativar somente ferramentas/MCPs necessários à tarefa atual quando isso for controlável.
7. Auditor começa por pedido, aceite, diff e resultado do `check`.
8. Nova tarefa materialmente diferente prefere novo contexto/sessão a histórico irrelevante.
9. Trabalho longo pode manter estado externo curto em vez de depender de histórico extenso.
10. Não reduzir contexto crítico apenas para economizar tokens; retrabalho também é desperdício.

Outputs de ferramentas devem preferir resumo acionável. Detalhes completos permanecem acessíveis para investigação.

## 7. Builder

O Builder deve:

- entender o pedido antes de editar;
- examinar o estado relacionado à tarefa;
- fazer a menor mudança correta;
- preservar comportamento e trabalho existentes;
- não tratar suposição como fato;
- não adicionar abstrações para necessidades hipotéticas;
- não esconder erro nem alterar testes apenas para obter PASS;
- executar as verificações aplicáveis antes de concluir.

Planejamento é proporcional à complexidade da tarefa.

## 8. Verificação executável

Todo projeto Gold deve possuir uma forma conhecida de verificar alterações.

```text
check
 ├─ lint/format quando aplicável
 ├─ typecheck quando aplicável
 ├─ tests quando aplicável
 └─ build quando aplicável
```

O mecanismo físico pode variar por stack.

A saída padrão deve ser curta e útil. Detalhes ou logs completos devem ser expandidos somente quando houver falha ou investigação explícita.

CI deve preferencialmente executar as mesmas verificações importantes usadas localmente.

Testes protegem comportamento útil. Não existe meta de quantidade de testes nem obrigação de testar detalhes internos sem valor prático.

Bug relevante deve ganhar teste de regressão quando isso for útil e viável.

## 9. Auditoria independente

O Auditor não precisa ler o projeto inteiro.

Contexto inicial recomendado:

- pedido original;
- critérios de aceite;
- diff;
- arquivos alterados;
- resultado das verificações;
- erros/warnings relevantes.

Depois, expandir contexto somente para validar uma hipótese concreta.

A auditoria verifica principalmente:

- correção;
- regressão;
- escopo;
- complexidade desnecessária;
- atalhos ou falso sucesso;
- suficiência da validação.

Resultado mínimo: `PASS` ou `FAIL` com findings acionáveis.

A automação Builder ↔ Auditor pertence ao projeto externo Runner quando desejada. O Standard define o comportamento esperado, não exige um executor específico.

## 10. Packs

Packs adicionam boas práticas específicas sem inflar o Core.

Exemplos possíveis:

- `android`;
- `python`;
- `web`;
- `ai`;
- `multi-agent`;
- `sensitive-data`;
- `agent-guardrails`.

Um pack só deve existir quando uma necessidade real justificar sua criação e, antes de virar reutilizável, deve ser exercitado em cenário adequado.

Packs não devem despejar grandes blocos de texto no `AGENTS.md`. Contexto específico deve permanecer próximo do domínio ao qual pertence.

## 11. Skills

Skills representam procedimentos especializados e reutilizáveis carregados sob demanda.

Princípios:

- uma Skill deve ter uma responsabilidade clara;
- metadata deve permitir descoberta sem carregar todo o conteúdo;
- referências e scripts devem ser carregados/executados somente quando necessários;
- não criar Skill quando comando/script simples resolve melhor;
- não duplicar instruções já presentes no Core;
- Skills de terceiros entram somente após revisão de conteúdo, segurança, licença e adequação ao Gold;
- nenhuma Skill vira parte recomendada do Template Gold antes de ser testada em fixture, exemplo ou projeto real apropriado.

Fluxo para reaproveitar Skill externa:

```text
DISCOVER → REVIEW → TRIM → ADAPT → TEST → INSTALL
```

Prioridade inicial:

- `gold-audit`;
- `goldify`;
- `skill-author`.

Novas Skills só entram quando uma tarefa repetitiva concreta justificar sua existência.

## 12. Create

A primeira forma de criar projetos Gold deve ser a solução mais simples disponível.

Preferência inicial: GitHub Template Repository.

Criar gerador próprio somente se uma necessidade real provar que uma solução madura e simples é insuficiente.

Projeto criado deve passar no `check` aplicável.

Antes de considerar o Template Gold estável, o próprio `ideias_standard` e pelo menos um exemplo/projeto adequado devem exercitar suas práticas essenciais.

## 13. Adopt / Goldify

Projetos existentes são casos de primeira classe.

Goldify deve:

1. examinar o estado atual sem assumir que está errado;
2. identificar o que já atende ao Gold;
3. produzir um **Golden Diff** curto;
4. separar `NECESSÁRIO` de `RECOMENDADO`;
5. preservar código, arquitetura e trabalho legítimos sempre que possível;
6. mostrar mudanças relevantes antes de aplicar quando necessário;
7. executar `check`;
8. submeter alterações relevantes a auditoria independente.

Não usar nota arbitrária ou sistema complexo de pontuação.

A abordagem de Goldify deve ser comprovada em projetos existentes reais antes de automação ampla.

## 14. Segurança

Baseline:

- não versionar secrets;
- usar `.gitignore` adequado;
- não expor credenciais em CI/logs;
- manter dependências atualizáveis;
- validar entradas externas quando necessário;
- não executar operações destrutivas silenciosamente.

Projetos com maior risco recebem controles adicionais por packs específicos.

## 15. Dogfooding e prova antes da expansão

### Dogfooding

O `ideias_standard` deve ser o primeiro consumidor do próprio Gold sempre que a prática for aplicável.

Se uma regra é difícil de usar, gera contexto excessivo ou cria burocracia neste próprio repositório, ela deve ser revisada antes de ser recomendada aos próximos projetos.

### Prove Before Expand

Uma capacidade só deve ser promovida de local/experimental para reutilizável quando:

- resolve problema real;
- a solução mais simples foi considerada;
- foi testada em contexto adequado;
- mostrou benefício claro;
- tende a se repetir em mais de um cenário ou possui valor evidente para um pack específico;
- não aumenta desnecessariamente o Core ou contexto permanente.

Se não atender, permanece local, experimental ou fora do Standard.

## 16. Anti-overengineering

Nunca adicionar complexidade apenas para antecipar possibilidades futuras.

Prefira:

- texto simples antes de schema;
- referência antes de duplicação;
- script simples antes de framework;
- ferramenta madura antes de engine própria;
- contexto local antes de leitura global;
- teste de comportamento antes de cobertura cosmética;
- mudança pequena antes de refatoração ampla;
- prática comprovada antes de padronização.

Complexidade que deixou de justificar sua existência deve poder ser removida.

## 17. Regra final

> Menos contexto, mais sinal. Menos processo, mais verificação. Menos abstração, mais utilidade. Primeiro provar, depois padronizar.
