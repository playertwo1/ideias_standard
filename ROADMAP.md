# Roadmap — Ideias Standard Gold

Mapa operacional do Standard. O contrato normativo está em `STANDARD.md`; o
estado mutável está em `PROJECT_STATE.md`. Este arquivo responde apenas:
**por que existe cada fase, o que entrega e como sabemos que está pronta**.

## 1. Direção

O Ideias Standard ajuda projetos humanos e assistidos por IA a manterem:

1. contexto mínimo suficiente;
2. regras e ownership explícitos;
3. verificações executáveis;
4. mudanças pequenas e reversíveis;
5. auditoria independente quando o risco justificar.

O Standard não impõe stack, arquitetura, fornecedor de IA ou governança máxima.

## 2. Regras operacionais

- Começar por `AGENTS.md`, estado e pedido atual.
- Localizar antes de ler; expandir contexto somente por necessidade concreta.
- `NOT_RUN` não é `PASS`.
- PASS só vale para o SHA e os comandos que o produziram.
- Builder e Auditor são papéis distintos quando revisão independente for exigida.
- Auditor não corrige seu próprio alvo.
- Automação não registra gate humano nem inicia fase seguinte sozinha.
- Sugestões de IA não viram decisões LOCKED sem autoridade adequada.
- Arquivos e decisões existentes são preservados por padrão.
- Nova capacidade reutilizável precisa ser provada antes de entrar no Gold.

## 3. Estado e dependências

Estado atual: `F5 — SYNC`, consolidado, aguardando auditoria final do conjunto.

```text
F0 Golden Standard
 ├─ F1 Create
 ├─ F2 Check + Audit
 ├─ F3 Packs + Skills
 ├─ F4 Adopt / Goldify
 └─ F5 Sync
```

As fases organizam a construção; não são uma autorização genérica para executar
qualquer item descoberto. A próxima ação sempre vem de `PROJECT_STATE.md`.

## 4. F0 — Golden Standard

**Objetivo:** provar a menor base reutilizável que torna um projeto Gold.

**Entregas:**

- `AGENTS.md` mínimo e contexto progressivo;
- `STANDARD.md`, schemas, fixtures e validadores coerentes;
- `check` com resumo curto e detalhes sob demanda;
- segurança básica, CI e testes essenciais;
- `gold-audit`, `goldify` e `skill-author` revisadas e provadas;
- dogfooding do próprio Standard e exemplo Gold completo.

**Critério:** cada prática promovida ao Gold foi exercitada no Standard, fixture,
exemplo ou projeto adequado; documentação isolada não basta.

**Estado:** implementada; auditoria individual registrada, consolidação final
pendente.

## 5. F1 — Create

**Objetivo:** criar projetos Gold sem um gerador maior que a necessidade.

**Entrega inicial:** Template Repository com `README.md`, `AGENTS.md`,
`.editorconfig`, `.gitignore`, CI, `src/` e `tests/` conforme o projeto.

**Regras:** packs e Skills entram somente quando aplicáveis; pastas opcionais
não são criadas vazias; o projeto criado deve passar pelo `check`.

**Critério:** um projeto novo nasce compreensível, verificável e sem herdar
documentação interna desnecessária do Standard.

**Estado:** implementada; auditoria individual registrada.

## 6. F2 — Check + Audit

**Objetivo:** responder com evidência se uma alteração quebrou o projeto.

**Entrega:** `scripts/check.py` executa somente verificações aplicáveis e oferece
saída curta, `--details` e `--json`; CI reutiliza as verificações relevantes.

**Critério:** falhas são acionáveis, regressões relevantes têm teste quando
necessário e o Auditor consegue começar pelo diff sem ler o repositório inteiro.

**Estado:** implementada; auditoria individual registrada.

## 7. F3 — Packs + Skills

**Objetivo:** adicionar capacidades sem inflar o Core.

**Entrega:** mecanismo e catálogo mínimo para Packs/Skills opcionais, com revisão
de conteúdo, segurança, licença, sobreposição e custo de contexto.

**Critério:** nenhuma capacidade vira recomendação reutilizável sem problema real,
teste adequado e benefício verificável.

**Estado:** implementada; auditoria individual registrada.

## 8. F4 — Adopt / Goldify

**Objetivo:** elevar projeto existente ao Gold sem reescrever o produto.

```text
inventário leve → Golden Diff → plano curto → mudanças necessárias → check → audit
```

`goldify` é somente leitura e classifica o resultado em:

- `NECESSÁRIO` — impede o contrato Gold;
- `RECOMENDADO` — melhora útil, mas não bloqueia.

Arquivos existentes são USER_OWNED por padrão. O fluxo preserva arquitetura,
mudanças locais, conflitos e possibilidade de retorno.

**Estado:** implementada; auditoria individual registrada.

## 9. F5 — Sync

**Objetivo:** atualizar projetos Gold com melhorias comprovadas sem sobrescrever
customizações.

**Entrega:** `scripts/sync.py` gera o plano antes de escrever, ignora áreas fora
do escopo, preserva conflitos USER_OWNED e exige confirmação explícita para
ações destrutivas.

**Critério:** uma atualização mostra origem, destino, conflito e ação prevista;
nenhum arquivo é alterado silenciosamente.

**Estado:** implementada; auditoria individual registrada, consolidação final
pendente.

## 10. Contratos e limites

| Necessidade | Fonte |
|---|---|
| instruções universais | `AGENTS.md` |
| regras normativas | `STANDARD.md` |
| estado e próxima ação | `PROJECT_STATE.md` |
| uso/retomada conceitual | `PROJECT_GUIDE.md` |
| validação | `scripts/validate_standard.py` e `scripts/check.py` |
| adoção | `scripts/goldify.py` |
| sincronização | `scripts/sync.py` |

O Runner Builder↔Auditor é externo e opcional. O Standard continua independente
de Codex, Claude, Gemini ou qualquer fornecedor.

## 11. Critérios de mudança

Antes de adicionar regra, arquivo, Pack, Skill ou abstração:

1. identifique um problema real;
2. tente a solução local mais simples;
3. prove-a em uso adequado;
4. verifique segurança, compatibilidade e custo de contexto;
5. promova ao Gold somente se o benefício for reutilizável.

Antes de concluir uma mudança: executar checks aplicáveis, revisar diff, registrar
limitações e atualizar `PROJECT_STATE.md` somente se o estado real mudou.

## 12. Próxima ação

Executar a auditoria independente final da consolidação Gold. Até essa auditoria,
não declarar a consolidação como novo PASS nem iniciar uma trilha posterior por
inferência.
