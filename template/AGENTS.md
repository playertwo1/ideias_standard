# AGENTS.md — {{nome do projeto}}

Contrato curto para qualquer agente (Claude, Codex, Gemini, Hermes…). Se uma instrução não serve à maioria das tarefas, ela não fica aqui: vai para `docs/` e é lida só quando precisar.

## Fontes de verdade
- `STATE.md` — onde paramos e a próxima ação. **Comece por aqui.**
- `ROADMAP.md` — marcos e fila. `PROJECT.md` — problema, MVP e fora de escopo.
- `DESIGN.md` — a cara do app; leia antes de criar ou mudar tela.
- `docs/DECISIONS.md` — o porquê das escolhas caras. `docs/RELEASE_CHECKLIST.md` — como provar que está pronto.

## Comandos
- Instalar: `{{comando}}`
- Verificar tudo (lint, tipos, testes, build): `{{comando}}`
- Rodar: `{{comando}}`

## Regras
1. Leia só o necessário: localize antes de abrir, prefira o trecho ao arquivo inteiro e filtre saídas grandes.
2. Separe fato verificado, hipótese e sugestão. Confira o código antes de afirmar que algo existe.
3. Faça a menor mudança correta. Sem abstração para necessidade hipotética; preserve o comportamento e o trabalho existentes.
4. Correção simples: implemente e teste. Feature média: spec curta (`docs/templates/FEATURE.md`). Mudança grande ou arriscada: também plano (`docs/templates/EXECUTION_PLAN.md`) e revisão independente.
5. Registre os testes que rodou e o resultado. Não executado é `NOT_RUN`, nunca `PASS`. Não altere teste para esconder bug.
6. `DONE` só com critérios de aceite cumpridos e evidência de agora. Resposta "feito" da IA não é evidência.
7. Exigem aprovação humana: exclusões, ações irreversíveis, deploy/produção, gastos, segredos, dados pessoais, permissões e decisões de produto.
8. Nunca versione senha, token, chave ou dado pessoal real; não os escreva em logs nem em evidências.
9. Se plano e código divergirem, registre a diferença em `STATE.md`; não esconda a falha.
10. Ao encerrar sessão relevante, atualize `STATE.md`: o que mudou, testes, bloqueios e **uma** próxima ação. Handoff = ID da tarefa, arquivos, testes, riscos, decisão pendente.

## Regras deste projeto
- {{regra permanente específica, ex.: identidade canônica, política de dados, fronteira com outro sistema}}

## Git
- {{fluxo: ex. commits direto na main / branch + PR; quando pode fazer push}}
