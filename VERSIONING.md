# Versioning Contract — Ideias Standard

O Standard usa SemVer quando sair de `draft`. Durante `0.x`, toda mudanca incompatível deve continuar explícita e acompanhada de migration quando houver projetos gerenciados afetados.

## PATCH

Pode corrigir bug, mensagem, teste, fixture ou regra sem alterar significado material de contrato existente.

## MINOR

Pode adicionar pack, capability, workflow, adapter, check, campo opcional ou comportamento backward-compatible.

## MAJOR

Obrigatório quando houver incompatibilidade material em:

- autoridade ou gate;
- significado de invariant existente;
- ownership;
- schema obrigatorio;
- formato de lock;
- comportamento destrutivo;
- semantica de PASS/FAIL;
- politica de upgrade/adopt.

## Regras

1. ID existente nao muda de significado silenciosamente.
2. Remocao ou renomeacao material exige migration ou major version.
3. `standard.lock` registra provenance suficiente para decidir upgrade.
4. Compatibilidade e declarada em `COMPATIBILITY.yaml`; nao e presumida.
5. Um projeto nunca e atualizado apenas porque existe versao nova.
6. Upgrade segue `check -> render target -> diff -> preview -> apply -> validate -> lock`.
