# AGENTS.md — Ideias Standard

## Objetivo

Construir e manter o Ideias Standard como uma base Gold simples, reutilizável e preparada para humanos e agentes de IA.

## Antes de alterar

Leia somente:

1. este `AGENTS.md`;
2. `PROJECT_STATE.md`;
3. o pedido atual.

Abra `STANDARD.md`, `ROADMAP.md` ou outros arquivos apenas quando forem relevantes para a tarefa.

## Regras

- faça a menor mudança correta;
- preserve comportamento e trabalho existentes;
- não trate suposição como fato;
- não crie abstrações para necessidades hipotéticas;
- não duplique contexto entre arquivos;
- não esconda erros nem altere testes apenas para obter PASS;
- valide antes de concluir;
- não leia o repositório inteiro sem necessidade objetiva.

## Verificação

Use os testes, lint, build e checks aplicáveis à mudança.

Para alterações relevantes, revise o diff e prefira auditoria independente começando pelo delta.

## Contexto

Mantenha contexto progressivo: comece pequeno e abra documentação, packs, Skills ou dependências somente quando necessário.

Atualize `PROJECT_STATE.md` apenas quando o estado real do projeto mudar.
