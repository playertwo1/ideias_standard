# ROADMAP V3 — IDEIAS STANDARD

## 1. PRINCÍPIO

Objetivo do Standard:

correção  
→ integridade  
→ autoridade  
→ evidência  
→ economia de contexto/tokens  
→ velocidade

Usar sempre o Minimum Sufficient Context.

Economizar tokens sem remover informação crítica.

---

## 2. REGRAS GLOBAIS

Estas regras valem para S0–S8.

- **R01** — Não ler o repositório inteiro sem necessidade.
- **R02** — Começar por estado atual + tarefa + regras aplicáveis + arquivos diretamente necessários.
- **R03** — Expandir contexto somente quando houver necessidade objetiva.
- **R04** — Preferir delta + findings pendentes + dependências diretas + invariantes aplicáveis em vez de reler contexto completo.
- **R05** — Evidência válida pode ser reutilizada somente quando ainda aplicável ao mesmo SHA/baseline.
- **R06** — PASS não migra entre SHAs.
- **R07** — NOT_RUN != PASS.
- **R08** — Preferir saída estruturada, curta e referenciável.
- **R09** — Não repetir documentação já confirmada.
- **R10** — Não explicar conceitos básicos sem necessidade.
- **R11** — Bug corrigido deve ganhar teste/fixture de regressão quando aplicável.
- **R12** — Builder != Auditor quando auditoria independente for obrigatória.
- **R13** — Auditor não corrige o alvo auditado.
- **R14** — Product Authority registra gates humanos.
- **R15** — Automação não amplia autoridade.
- **R16** — Decisão LOCKED não muda sem autoridade adequada.
- **R17** — Operação destrutiva não deve ocorrer automaticamente sem autorização quando exigida.
- **R18** — Processos longos devem ser retomáveis.
- **R19** — Estado crítico não pode depender apenas da memória de chat.
- **R20** — Codex, Claude, Gemini ou outro fornecedor nunca são fonte canônica.
- **R21** — Não iniciar fase seguinte para compensar pendência da atual.
- **R22** — Não antecipar funcionalidades futuras sem autorização explícita.
- **R23** — Validação executada prevalece sobre aparência documental.
- **R24** — Relatórios devem citar IDs/códigos em vez de repetir textos longos.
- **R25** — Quando resultado estruturado existir, não duplicá-lo em narrativa extensa.

---

## 3. ESTADO ATUAL

- S0 = PASS / CLOSED
- S1 = ACTIVE
- S2 = NOT_STARTED
- S3 = NOT_STARTED
- S4 = NOT_STARTED
- S5 = NOT_STARTED
- S6 = NOT_STARTED
- S7 = NOT_STARTED
- S8 = NOT_STARTED

S0 auditado no SHA:

`a327dc15d7a1a9c138903d6eb700977115166351`

---

## 4. DEPENDÊNCIAS

- S1 → S0 PASS
- S2 → Gate S1 PASS
- S3 → Gate S2 PASS
- S4 → Gate S3 PASS
- S5 → Gate S4 PASS
- S6 → Gate S5 PASS
- S7 → Gate S6 PASS
- S8 → Gate S7 PASS

O Runner é uma ferramenta externa opcional. Nenhuma fase do Standard depende da sua implementação.

---

## 5. REGRA PADRÃO DE FASE

Cada fase usa:

- Objective
- Checklist
- Validation
- Audit
- Gate

Não repetir regras globais dentro das fases.

Semântica dos checkboxes:

- `[x]` indica implementação registrada no estado canônico;
- auditoria e integração são estados separados, registrados em `PROJECT_STATE.md` por SHA;
- implementação não implica `AUDIT_PASS`, integração, gate humano ou PASS de produto.

---

## S0 — FOUNDATION

**Status:** PASS / CLOSED

### Objective

Definir e validar a fundação canônica do Standard.

### Checklist

- [x] S0-C01 Missão e fronteira definidas.
- [x] S0-C02 `STANDARD.md` definido.
- [x] S0-C03 `AGENTS.md` definido.
- [x] S0-C04 `PROJECT_STATE.md` definido.
- [x] S0-C05 Schemas iniciais válidos.
- [x] S0-C06 Profiles LIGHT/STANDARD/DEEP definidos.
- [x] S0-C07 Packs iniciais definidos.
- [x] S0-C08 Ownership definido.
- [x] S0-C09 Bundles/workflows/adapters iniciais definidos.
- [x] S0-C10 Change lifecycle inicial definido.
- [x] S0-C11 Invariantes estruturados definidos.
- [x] S0-C12 Compatibility/versioning definidos.
- [x] S0-C13 CLI contract definido.
- [x] S0-C14 Fixtures positivas/adversariais criadas.
- [x] S0-C15 Golden outputs criados.
- [x] S0-C16 Validador estrutural/semântico funcionando.
- [x] S0-C17 Self-check funcionando.
- [x] S0-C18 CI Python 3.11/3.12/3.13 verde.
- [x] S0-C19 Builder/Auditor separados por contrato.
- [x] S0-C20 Audit SHA imutável.
- [x] S0-C21 Loop Builder↔Auditor limitado.
- [x] S0-C22 Human gate preservado.
- [x] S0-C23 Orchestration state machine validada.
- [x] S0-C24 Auditoria independente PASS.

### Gate

Gate S0 = PASS

Registrado pela Product Authority.

---

## Runner externo

A automação Builder ↔ Auditor foi separada para [playertwo1/runner](https://github.com/playertwo1/runner). O histórico O0 permanece no Git deste repositório até `baf5c393e9e391dd0ddfc65551d37f4bfc7b2c58`; a execução e as evidências agora pertencem ao repositório Runner. O Standard mantém somente os contratos gerais de governança.

---
## S1 — CONFORMANCE FIRST

**Status:** ACTIVE — retomado em D-C02; S1-C01 (`check`), S1-C02 (validação de project manifest), S1-C03 (validação de standard lock) e S1-C04 (validação de context manifest) concluídos.

### Objective

Criar interface estável de conformance.

### Checklist

- [x] S1-C01 Implementar `check`.
- [x] S1-C02 Validar project manifest.
- [x] S1-C03 Validar standard lock.
- [x] S1-C04 Validar contexto aplicável.
- [x] S1-C05 Validar ownership.
- [x] S1-C06 Validar arquivos obrigatórios (aguardando auditoria independente).
- [x] S1-C07 Validar compatibility (aguardando auditoria independente).
- [x] S1-C08 Validar packs aplicáveis (aguardando auditoria independente).
- [x] S1-C09 Validar workflows aplicáveis (aguardando auditoria independente).
- [ ] S1-C10 Validar bundles aplicáveis.
- [ ] S1-C11 Validar adapters aplicáveis.
- [ ] S1-C12 Detectar status contraditórios.
- [ ] S1-C13 Detectar status duplicados.
- [ ] S1-C14 Detectar arquivos ausentes.
- [ ] S1-C15 Detectar referências inválidas.
- [ ] S1-C16 Detectar adapters divergentes.
- [ ] S1-C17 Findings possuem códigos determinísticos.
- [ ] S1-C18 Mesma violação produz mesmo código.
- [ ] S1-C19 Implementar `doctor`.
- [ ] S1-C20 `doctor` usa o mesmo rule engine do `check`.
- [ ] S1-C21 `doctor` não cria regras próprias.
- [ ] S1-C22 Output estruturado segue `conformance-report.schema.json`.
- [ ] S1-C23 Suportar PASS/FAIL/WARN/NOT_APPLICABLE.
- [ ] S1-C24 Preservar NOT_RUN != PASS.
- [ ] S1-C25 Implementar modo não interativo.
- [ ] S1-C26 Exit codes seguem `CLI_CONTRACT.md`.
- [ ] S1-C27 Exit code e relatório nunca se contradizem.
- [ ] S1-C28 Fixture válida → PASS.
- [ ] S1-C29 Fixtures inválidas → códigos esperados.
- [ ] S1-C30 Execuções repetidas → resultado determinístico.
- [ ] S1-C31 CI verde.
- [ ] S1-C32 Audit packet S1 produzido.
- [ ] S1-C33 Auditoria independente PASS.

### Gate

Todos os critérios obrigatórios PASS.

Depois:

AUDIT RESULT: PASS

Depois Product Authority registra:

Gate S1 = PASS

Somente então S2.

---

## S2 — INIT / COMPILER

**Status:** NOT_STARTED

### Objective

Gerar projeto mínimo e determinístico a partir de manifest válido.

### Checklist

- [ ] S2-C01 Compor BASE.
- [ ] S2-C02 Aplicar PROFILE.
- [ ] S2-C03 Aplicar PACKS.
- [ ] S2-C04 Aplicar PROJECT RULES.
- [ ] S2-C05 Materializar somente artefatos aplicáveis.
- [ ] S2-C06 Gerar `standard.lock`.
- [ ] S2-C07 Gerar fingerprints.
- [ ] S2-C08 Registrar provenance.
- [ ] S2-C09 Classificar MANAGED/MERGEABLE/USER_OWNED.
- [ ] S2-C10 Implementar dry-run.
- [ ] S2-C11 Mostrar diff antes de escrita quando aplicável.
- [ ] S2-C12 Detectar conflitos entre packs.
- [ ] S2-C13 Expandir bundles explicitamente.
- [ ] S2-C14 Materializar adapters sem criar fonte canônica concorrente.
- [ ] S2-C15 Geração LIGHT determinística.
- [ ] S2-C16 Geração STANDARD determinística.
- [ ] S2-C17 Geração DEEP determinística.
- [ ] S2-C18 Segunda execução sem mudança → sem diff indevido.
- [ ] S2-C19 Falha não avança lock.
- [ ] S2-C20 Auditoria independente PASS.

### Gate

Gate S2 = PASS após registro da Product Authority.

---

## S3 — ADOPT / BROWNFIELD

**Status:** NOT_STARTED

### Objective

Adotar projetos existentes sem destruir conteúdo legítimo.

### Checklist

- [ ] S3-C01 Inventário inicial read-only.
- [ ] S3-C02 Identificar arquivos-chave antes de ler conteúdo amplo.
- [ ] S3-C03 Recomendar profile.
- [ ] S3-C04 Recomendar packs.
- [ ] S3-C05 Produzir gap analysis.
- [ ] S3-C06 Mapear equivalências existentes.
- [ ] S3-C07 Produzir plano de adoção.
- [ ] S3-C08 Produzir preview antes de alterações.
- [ ] S3-C09 Arquivos existentes = USER_OWNED por padrão.
- [ ] S3-C10 Overwrite implícito proibido.
- [ ] S3-C11 Conflitos explicitados.
- [ ] S3-C12 Provenance preservada.
- [ ] S3-C13 Lock criado somente após validação.
- [ ] S3-C14 Fixture legacy preserva conteúdo válido.
- [ ] S3-C15 Auditoria independente PASS.

### Gate

Gate S3 = PASS.

---

## S4 — UPGRADE LIFECYCLE

**Status:** NOT_STARTED

### Objective

Atualizar projetos gerenciados preservando alterações legítimas.

### Checklist

- [ ] S4-C01 Suportar versionamento semântico.
- [ ] S4-C02 Usar provenance no lock.
- [ ] S4-C03 Implementar migrations versionadas.
- [ ] S4-C04 Renderizar target em staging.
- [ ] S4-C05 Comparar baseline anterior × local × target.
- [ ] S4-C06 Produzir diff antes de aplicar.
- [ ] S4-C07 MERGEABLE suporta merge controlado.
- [ ] S4-C08 Detectar conflitos locais.
- [ ] S4-C09 Fingerprints evitam análise desnecessária.
- [ ] S4-C10 Analisar prioritariamente artefatos alterados/dependentes.
- [ ] S4-C11 Implementar rollback quando seguro.
- [ ] S4-C12 Falha pós-upgrade não avança lock.
- [ ] S4-C13 Upgrade preserva ownership.
- [ ] S4-C14 Upgrade preserva provenance.
- [ ] S4-C15 Rollback preserva estado válido.
- [ ] S4-C16 Auditoria independente PASS.

### Gate

Gate S4 = PASS.

---

## S5 — CONTEXT LIFECYCLE

**Status:** NOT_STARTED

### Objective

Formalizar Minimum Sufficient Context.

### Checklist

- [ ] S5-C01 Implementar REQUIRED.
- [ ] S5-C02 Implementar CONDITIONAL.
- [ ] S5-C03 Implementar DISCOVERY.
- [ ] S5-C04 Registrar why-included.
- [ ] S5-C05 Registrar why-excluded.
- [ ] S5-C06 Fingerprints por bloco.
- [ ] S5-C07 Implementar delta-context.
- [ ] S5-C08 Implementar byte/token budgets.
- [ ] S5-C09 Implementar `CONTEXT_OVERFLOW`.
- [ ] S5-C10 REQUIRED nunca é truncado silenciosamente.
- [ ] S5-C11 Implementar context reuse.
- [ ] S5-C12 Medir critical recall.
- [ ] S5-C13 Medir irrelevant-context rate.
- [ ] S5-C14 Mudança pequena usa contexto menor que full-project baseline.
- [ ] S5-C15 Critical recall = 100% nas fixtures críticas.
- [ ] S5-C16 Overflow insuficiente gera erro explícito.
- [ ] S5-C17 Auditoria independente PASS.

### Gate

Gate S5 = PASS.

---

## S6 — MULTI-PROVIDER ECOSYSTEM

**Status:** NOT_STARTED

### Objective

Compor contratos de projeto para diferentes fornecedores sem acoplar o Standard a um executor.

### Checklist

- [ ] S6-C01 Definir contrato provider-neutral para adapters de projeto.
- [ ] S6-C02 Validar adapters genéricos e específicos nos catálogos.
- [ ] S6-C03 Garantir que adapters não mudem autoridade, gates ou ownership.
- [ ] S6-C04 Versionar bundles e workflows declarativos.
- [ ] S6-C05 Detectar conflitos entre packs, bundles e adapters.
- [ ] S6-C06 Testar equivalência dos contratos gerados para provedores distintos.
- [ ] S6-C07 Auditoria independente PASS.

### Gate

Gate S6 = PASS.

---

## S7 — IDEA INTEGRATION

**Status:** NOT_STARTED

### Objective

Permitir que Idea produza manifest consumível diretamente pelo Standard.

### Checklist

- [ ] S7-C01 Definir contrato Idea → Standard.
- [ ] S7-C02 Export versionado.
- [ ] S7-C03 Import versionado.
- [ ] S7-C04 Validation de handoff.
- [ ] S7-C05 Compatibility explícita.
- [ ] S7-C06 Preservar decisões relevantes.
- [ ] S7-C07 Preservar provenance.
- [ ] S7-C08 Não exigir replay da conversa original.
- [ ] S7-C09 Handoff usa estrutura em vez de transcript completo.
- [ ] S7-C10 Fixture E2E Idea → Standard PASS.
- [ ] S7-C11 Projeto gerado compila/valida sem reconstruir conversa.
- [ ] S7-C12 Auditoria independente PASS.

### Gate

Gate S7 = PASS.

---

## S8 — CHANGE LIFECYCLE

**Status:** NOT_STARTED

### Objective

Permitir evolução incremental do projeto por delta.

### Checklist

- [ ] S8-C01 Change possui ID.
- [ ] S8-C02 Change possui tipo.
- [ ] S8-C03 Change possui estado.
- [ ] S8-C04 Change possui rationale.
- [ ] S8-C05 Registrar decisions afetadas.
- [ ] S8-C06 Registrar requirements afetados.
- [ ] S8-C07 Registrar paths afetados.
- [ ] S8-C08 Registrar acceptance.
- [ ] S8-C09 Registrar evidências.
- [ ] S8-C10 Gerar impact delta.
- [ ] S8-C11 Gerar Minimum Sufficient Context da change.
- [ ] S8-C12 Builder recebe somente contexto necessário.
- [ ] S8-C13 Auditor recebe contexto independente necessário.
- [ ] S8-C14 Change pequena não exige full-project context.
- [ ] S8-C15 Change pode ser fechada formalmente.
- [ ] S8-C16 Histórico permanece auditável.
- [ ] S8-C17 Comparar full-context vs delta-context.
- [ ] S8-C18 Critical recall permanece preservado.
- [ ] S8-C19 Auditoria independente PASS.

### Gate

Gate S8 = PASS.

---

## 6. DOGFOODING

- [x] D-C01 Histórico: O0 v2 M1–M5 aceitos e usado no próprio `ideias_standard`; execução transferida ao repositório Runner.
- [x] D-C02 Histórico: S1 retomado após D-C01.
- [ ] D-C03 Testar o Runner em outro projeto no repositório próprio; não bloqueia S6.
- [ ] D-C04 S5 passa a gerar contexto do próprio Standard.
- [ ] D-C05 S8 passa a controlar novas mudanças do próprio Standard.

Regra:

provar internamente → depois generalizar

---

## 7. MÉTRICAS

Métricas são evidência auxiliar, não gates cosméticos.

### Correção

- false PASS
- regressions
- SHA mismatches
- validation failures

### Automação

- manual handoffs
- automatic cycles
- blocked correctly
- resume success

### Contexto

- tokens/bytes por tarefa
- repeated-context ratio
- delta/full ratio
- critical recall

### Eficiência

- arquivos lidos
- rodadas Builder/Auditor
- evidência reutilizada
- tempo até resolução

Meta:

menos contexto + menos retransmissão + menos intervenção manual, sem reduzir correção.

---

## 8. FORMATO DE PROGRESSO

Cada fase deve manter apenas:

- [ ] IMPLEMENTATION_COMPLETE
- [ ] VALIDATION_PASS
- [ ] AUDIT_READY
- [ ] AUDIT_PASS
- [ ] PRODUCT_AUTHORITY_GATE_PASS

Quando aplicável.

Para cada entrega auditável, distinguir:

- `IMPLEMENTED` — commit produzido;
- `AUDIT_PASS` — auditoria independente aprovou o SHA exato;
- `INTEGRATED` — SHA auditado foi incorporado à referência canônica;
- `GATE_PASS` — somente quando a Product Authority registra um gate aplicável.

---

## 9. AUDITORIA

Auditor recebe somente:

- target SHA
- acceptance/gate aplicável
- invariantes aplicáveis
- diff/paths relevantes
- evidência existente
- contexto adicional sob demanda

Não enviar automaticamente:

- conversa inteira;
- raciocínio completo do Builder;
- documentação irrelevante;
- histórico já substituído.

Objetivo:

Minimum Sufficient Audit Context

---

## 10. ESCALADA

Automação deve parar em:

- nova decisão de produto
- conflito LOCKED
- operação destrutiva não autorizada
- DISPUTED
- ESCALATE
- limite de auditorias
- evidência insuficiente
- risco de segurança
- falha de integridade
- ambiguidade material

Resultado:

BLOCKED → Product Authority

Não preencher lacuna material por suposição.

---

## 11. VISÃO FINAL

- S0 Foundation — ✅ CLOSED
- Runner — ferramenta externa: https://github.com/playertwo1/runner
- S1 Conformance First — 🟢 ACTIVE
- S2 Init / Compiler
- S3 Adopt / Brownfield
- S4 Upgrade Lifecycle
- S5 Context Lifecycle
- S6 Multi-provider Ecosystem
- S7 Idea Integration
- S8 Change Lifecycle

Resultado desejado:

- Idea → define o projeto
- Ideias Standard → define contrato e lifecycle
- Context System → entrega contexto mínimo
- Builder → implementa
- Auditor → verifica independentemente
- Adapters → descrevem integração sem prender o Standard a um executor
- Product Authority → mantém decisões materiais e gates

Regra final:

> Adapters não ampliam a autoridade do projeto.

Regra de contexto:

> Usar o mínimo de tokens possível preservando 100% das obrigações críticas.
