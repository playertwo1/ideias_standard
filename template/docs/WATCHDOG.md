# WATCHDOG — guardião de execução

Leia antes de mudança média, grande ou arriscada (`AGENTS.md`, regra 4). Complementa as regras do `AGENTS.md` sem repeti-las. Sem marcadores a preencher; ajuste só se o projeto pedir.

**READ → UNDERSTAND → PLAN → CHANGE → TEST → AUDIT → FINISH.** Nunca: ASSUME → CHANGE EVERYTHING → HOPE IT WORKS.

## 1. Hierarquia de decisão
Em conflito, nesta ordem: pedido explícito do usuário → `AGENTS.md` → este arquivo → documentação do projeto (`PROJECT`, `DESIGN`, `docs/DECISIONS.md`) → arquitetura e padrões existentes → julgamento do agente. Silêncio nunca autoriza mudança destrutiva.

## 2. Escopo
Não aproveite a tarefa para reescrever partes não relacionadas, trocar arquitetura ou biblioteca, reorganizar o projeto ou transformar correção pequena em reconstrução. Melhoria percebida no caminho vira linha em "Ideias" do `ROADMAP.md` ou nota no handoff.

## 3. Regressão e trabalho existente
Antes de mexer em código existente:
- Examine `git status` e o diff já existente; não reverta nem sobrescreva trabalho que não é da tarefa.
- O que depende disso? Estou removendo comportamento ou mudando API, banco, schema, configuração ou interface?
- Existe solução menos invasiva? Prefira mudanças pequenas, incrementais e reversíveis.

## 4. Alto risco e regra de parada
Apagar arquivos ou dados; resetar banco; alterar migration existente; remover dependência importante; trocar framework ou arquitetura principal; mexer em autenticação, permissões, segredos ou credenciais; comando destrutivo; force push ou reescrita de histórico; remoção de grandes blocos de código.

Antes delas: confirme que são necessárias, procure alternativa mais segura, garanta rollback e obtenha a aprovação humana (`AGENTS.md`, regra 7). O mesmo vale para decisão arquiteturalmente crítica, incompatível com o pedido ou impossível de determinar com segurança: pare e explique o que encontrou, o risco, as opções e a recomendação.

## 5. Não esconda problemas
Proibido fazer o sistema "parecer funcionar": dado falso, mock apresentado como produção, hardcode escondido, erro engolido, validação removida, teste desativado. Corrija a causa. Não enfraqueça a segurança para facilitar o desenvolvimento nem envie informação privada a serviço externo sem necessidade.

## 6. Loop de erro
Após cerca de 3 falhas parecidas, pare de tentar variações: releia o erro, reavalie a hipótese, procure a causa raiz e outra abordagem. Se continuar travado, registre o bloqueio em `STATE.md`.

## 7. Dependências
Não adicione dependência quando o que já existe resolve razoavelmente. Se adicionar: necessidade, compatibilidade, manutenção e licença (gate G5 de `docs/RELEASE_CHECKLIST.md`).
