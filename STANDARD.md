# Ideias Standard — Gold Standard

Versão: `0.2.0-draft`.

## 1. Missão

Definir uma base simples e reutilizável para projetos que precisam ser fáceis de entender, alterar, validar, auditar e manter por humanos e agentes de IA.

O Ideias Standard não é um framework de governança. É um **Golden Standard operacional**.

## 2. Princípios canônicos

1. **Small Core** — poucas regras universais.
2. **Progressive Context** — carregar somente o contexto necessário para a tarefa atual.
3. **Executable Verification** — preferir build, testes, lint, typecheck e scripts reais a instruções vagas.
4. **Independent Audit** — alterações relevantes podem ser revisadas por outro agente/processo.
5. **Optional Packs** — capacidades específicas permanecem fora do Core até serem necessárias.
6. **No Overengineering** — nenhuma abstração, arquivo ou camada existe sem problema concreto.
7. **Preserve Existing Work** — padronizar não significa reescrever o projeto.
8. **Security Proportional to Risk** — segurança cresce conforme o risco real.

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
AGENTS.md
   ↓
contexto mínimo
   ├─ documentação específica
   ├─ pack da tecnologia
   ├─ Skill do procedimento
   └─ dependências diretas necessárias
```

Não escanear o repositório inteiro por padrão.

Não criar um engine complexo de contexto enquanto referências simples e organização por domínio forem suficientes.

## 6. Builder

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

## 7. Verificação executável

Todo projeto Gold deve possuir uma forma conhecida de verificar alterações.

Conceitualmente:

```text
check
 ├─ lint/format quando aplicável
 ├─ typecheck quando aplicável
 ├─ tests quando aplicável
 └─ build quando aplicável
```

O mecanismo físico pode variar por stack.

CI deve preferencialmente executar as mesmas verificações importantes usadas localmente.

Testes protegem comportamento útil. Não existe meta de quantidade de testes nem obrigação de testar detalhes internos sem valor prático.

Bug relevante deve ganhar teste de regressão quando isso for útil e viável.

## 8. Auditoria independente

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

## 9. Packs

Packs adicionam boas práticas específicas sem inflar o Core.

Exemplos possíveis:

- `android`;
- `python`;
- `web`;
- `ai`;
- `multi-agent`;
- `sensitive-data`;
- `agent-guardrails`.

Um pack deve existir somente quando uma necessidade real justificar sua criação.

Packs não devem despejar grandes blocos de texto no `AGENTS.md`. Contexto específico deve permanecer próximo do domínio ao qual pertence.

## 10. Skills

Procedimentos especializados e reutilizáveis podem ser representados como Skills carregadas sob demanda.

Exemplos:

- code review;
- release;
- migration;
- build especializado.

Cada Skill deve fazer uma coisa bem e permanecer pequena.

Skills não substituem comandos executáveis quando um script simples resolve melhor o problema.

## 11. Create

A primeira forma de criar projetos Gold deve ser a solução mais simples disponível.

Preferência inicial: GitHub Template Repository.

Criar um gerador próprio somente se houver necessidade real não atendida por uma solução madura existente.

Projeto criado deve passar no `check` aplicável.

## 12. Adopt / Goldify

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

## 13. Segurança

Baseline:

- não versionar secrets;
- usar `.gitignore` adequado;
- não expor credenciais em CI/logs;
- manter dependências atualizáveis;
- validar entradas externas quando necessário;
- não executar operações destrutivas silenciosamente.

Projetos com maior risco recebem controles adicionais por packs específicos.

## 14. Anti-overengineering

Nunca adicionar complexidade apenas para antecipar possibilidades futuras.

Prefira:

- texto simples antes de schema;
- referência antes de duplicação;
- script simples antes de framework;
- ferramenta madura antes de engine própria;
- contexto local antes de leitura global;
- teste de comportamento antes de cobertura cosmética;
- mudança pequena antes de refatoração ampla.

Complexidade que deixou de justificar sua existência deve poder ser removida.

## 15. Regra final

> Menos contexto, mais sinal. Menos processo, mais verificação. Menos abstração, mais utilidade.
