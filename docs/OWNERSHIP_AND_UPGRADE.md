# Ownership e Upgrade

## Problema

Um Standard atualizável precisa distinguir arquivos que controla integralmente de arquivos que recebem trabalho humano. Sem isso, `upgrade` ou destrói customizações ou deixa de conseguir atualizar o projeto.

## Classes de ownership

### MANAGED

Gerado integralmente a partir do Standard/profile/pack. Alterações locais são tratadas como drift e nunca sobrescritas sem preview explícito.

Exemplos candidatos: arquivos de adapter gerados, metadados internos e manifests derivados.

### MERGEABLE

Possui baseline do Standard e customização local legítima. Upgrade usa diff/merge e pode produzir conflito para revisão.

Exemplos candidatos: `AGENTS.md`, políticas, arquivos de CI ou configuração compartilhada.

### USER_OWNED

Pertence ao projeto. O Standard pode validar, referenciar ou sugerir mudanças, mas não sobrescreve automaticamente.

Exemplos: código de domínio, requisitos específicos, decisões humanas e documentação autoral do produto.

## Fluxo de upgrade

1. Validar repositório e lock atual.
2. Renderizar a versão alvo em staging.
3. Comparar baseline anterior, estado local e alvo.
4. Classificar mudanças por ownership.
5. Mostrar preview/diff.
6. Bloquear em conflito material não resolvido.
7. Aplicar apenas mudanças autorizadas.
8. Executar validação/conformance.
9. Atualizar `standard.lock` somente após sucesso.

## Adopt

Projeto brownfield não possui baseline do Standard. `adopt` deve:

1. inventariar sem escrever;
2. recomendar profile/packs;
3. mapear equivalências existentes;
4. classificar arquivos atuais como USER_OWNED por padrão;
5. gerar baseline sintético apenas para artefatos que o usuário decidir incorporar;
6. mostrar conflitos antes de qualquer aplicação;
7. criar lock somente após adoção validada.

## Regra de segurança

Nunca inferir que um arquivo pode ser sobrescrito apenas porque seu nome coincide com um template do Standard.
