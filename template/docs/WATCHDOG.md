# WATCHDOG — guardião de execução

> Origem: [playertwo1/guardrail](https://github.com/playertwo1/guardrail) (`WATCHDOG.md` + `AGENTS_GUARDRAILS.md`), adaptado ao kit: o que já é regra no `AGENTS.md` ou gate no `docs/RELEASE_CHECKLIST.md` virou link. Sem marcadores a preencher; ajuste só se o projeto pedir.

Leia antes de mudança média, grande ou arriscada (`AGENTS.md`, regra 4). Objetivo: dar autonomia ao agente sem deixá-lo sair do escopo, quebrar o que existe ou tomar decisão perigosa sem perceber.

**READ → UNDERSTAND → PLAN → CHANGE → TEST → AUDIT → FINISH.** Nunca: ASSUME → CHANGE EVERYTHING → HOPE IT WORKS.

## 1. Antes de alterar
1. Entenda o pedido atual e examine o estado real do projeto (`STATE.md`, `git status`, código relacionado).
2. Identifique os arquivos envolvidos e o que depende deles.
3. Faça só o necessário para o objetivo; valide antes de declarar concluído.

Suposição não é fato. Se documentação e código divergirem, investigue antes de alterar e registre em `STATE.md`.

## 2. Hierarquia de decisão
Em conflito, nesta ordem:
1. Pedido explícito do usuário.
2. `AGENTS.md`.
3. Este arquivo.
4. Documentação do projeto (`PROJECT`, `DESIGN`, `docs/DECISIONS.md`).
5. Arquitetura e padrões existentes.
6. Julgamento técnico do agente.

Silêncio nunca autoriza mudança destrutiva.

## 3. Escopo e anti-drift
Não aproveite a tarefa para: reescrever partes não relacionadas, trocar arquitetura ou biblioteca sem necessidade, reorganizar o projeto, adicionar ou remover funcionalidade não pedida, ou transformar uma correção pequena em reconstrução.

Melhoria percebida no caminho vira sugestão (linha em "Ideias" do `ROADMAP.md` ou nota no handoff), não código. Primeiro termine o que foi pedido.

Na dúvida entre (A) mudança ampla baseada em suposição e (B) preservar o estado atual, escolha B e investigue.

## 4. Proteção contra regressão
Antes de mexer em código existente, pergunte:
- O que depende disso? Pode quebrar outro fluxo?
- Estou removendo comportamento ou mudando API, banco, schema, configuração ou interface?
- Existe solução menos invasiva?

Prefira mudanças pequenas, incrementais e reversíveis.

## 5. Ações de alto risco
Apagar arquivos ou dados; resetar banco; alterar migration existente; remover dependência importante; trocar framework ou arquitetura principal; mexer em autenticação, permissões, segredos ou credenciais; comando destrutivo; force push ou reescrita de histórico; remoção de grandes blocos de código.

Antes delas: confirme que são necessárias, procure alternativa mais segura, garanta rollback e obtenha a aprovação humana do `AGENTS.md` (regra 7). Nada irreversível com base em suposição.

## 6. Não esconda problemas
Proibido fazer o sistema "parecer funcionar" com dados falsos, mocks apresentados como produção, hardcode escondido, erro engolido, validação removida, teste desativado ou alterado só para passar. Corrija a causa.

## 7. Loop de erro
Após cerca de 3 falhas parecidas, pare de tentar variações: releia o erro, reavalie a hipótese, procure a causa raiz e outra abordagem. Se continuar travado, registre o bloqueio em `STATE.md`.

## 8. Preserve o trabalho existente
Antes de mudança grande, examine `git status` e o diff já existente; separe alterações anteriores das da tarefa. Não reverta nem sobrescreva trabalho do usuário só porque não foi o agente que fez.

## 9. Dependências
Não adicione dependência quando o que já existe resolve razoavelmente. Se adicionar: necessidade, compatibilidade, manutenção e licença (gate G5).

## 10. Regra de parada
Se surgir decisão irreversível, destrutiva, arquiteturalmente crítica, incompatível com o pedido ou impossível de determinar com segurança: pare antes dela e explique o que encontrou, o risco, as opções e qual recomenda.

## Verificação e segurança
Ficam onde já estão, sem cópia aqui: gates G1–G8 em `docs/RELEASE_CHECKLIST.md`, segredos e dados pessoais na regra 8 do `AGENTS.md`, auditoria final em `docs/AUDIT.md`.

---
Autônomo na execução. Conservador nas mudanças. Cético com suposições. Rigoroso na validação. Transparente na incerteza.
