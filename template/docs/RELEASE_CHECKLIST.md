# Checklist de fechamento — tarefa, marco e release

Fonte única dos gates. Copie os itens aplicáveis para a review do marco: `[x]` com comando e resultado de agora, `[-]` com o motivo quando não se aplica, `NOT_RUN` quando não executou (nunca conta como aprovado).

O resultado técnico (`PASS` / `FAIL` / `NOT_RUN`) é separado do aceite de produto (`APPROVED` / `CHANGES_REQUIRED` / `PENDING_HUMAN`). Teste verde não fecha marco sozinho.

## 1. Gate técnico
- [ ] G1 Testes passam: `{{comando}}`.
- [ ] G2 Lint/format passam: `{{comando}}`.
- [ ] G3 Tipos/build passam: `{{comando}}`.
- [ ] G4 Diff revisado: sem segredo, dado pessoal real, banco, backup ou artefato gerado; sem mudança fora do pedido.
- [ ] G5 Dependência nova justificada e com licença compatível (registrar avisos exigidos).
- [ ] G6 Migração de dados: backup antes, verificação de integridade depois, rollback descrito.
- [ ] G7 Bug corrigido ganhou teste de regressão quando viável.
- [ ] G8 `STATE.md` e `ROADMAP.md` atualizados e coerentes com o código.

## 2. Regras do projeto (invariantes)
- [ ] {{ex.: identidade canônica preservada; inferência não vira fato; ação de IA marcada}}

## 3. Entrega visual (se houver UI)
- [ ] V1 Capturas reais nas larguras-alvo ({{ex.: 1440 e 390 px}}), sem overflow nem texto sobreposto.
- [ ] V2 Estados vazios, carregando, erro e dados longos conferidos.
- [ ] V3 Teclado, foco visível, rótulos e contraste; estado indicado por texto/ícone além da cor.
- [ ] V4 Comparado à referência de design aprovada; diferenças registradas com motivo.
- [ ] V5 Aceite visual humano do que foi mostrado (data + link).

## 4. Fechamento e publicação
1. Gates acima registrados na review (`docs/reviews/<ID>.md`, modelo em `templates/REVIEW.md`).
2. Revisão independente quando o risco for alto (outro agente ou pessoa, começando por pedido, critérios, diff e checks).
3. Aceite humano exigido registrado com data.
4. Marco sai do `ROADMAP.md` (linha em "Entregues" + texto em `docs/arquivo/`); `STATE.md` aponta a próxima ação.
5. Commit só com arquivos do marco; push conforme `AGENTS.md`; depois conferir que o commit está no remoto.
6. Falhou algum passo: registrar o bloqueio em `STATE.md` e não declarar concluído.
