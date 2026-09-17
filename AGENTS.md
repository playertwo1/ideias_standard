# AGENTS.md — Ideias Standard

## Objetivo

Construir e manter o Ideias Standard como uma base Gold simples, reutilizável e preparada para humanos e agentes de IA.

## Antes de alterar

Leia somente:

1. este `AGENTS.md`;
2. o pedido atual.

Abra `PROJECT_STATE.md`, `STANDARD.md`, `ROADMAP.md` ou outros arquivos apenas quando forem relevantes para a tarefa.

## Regras

- faça a menor mudança correta;
- preserve comportamento e trabalho existentes;
- não trate suposição como fato;
- não crie abstrações para necessidades hipotéticas;
- não duplique contexto entre arquivos;
- localize antes de ler e carregue o menor trecho suficiente;
- limite ou filtre outputs potencialmente grandes;
- não esconda erros nem altere testes apenas para obter PASS;
- aplique ao próprio Standard as práticas Gold que forem relevantes;
- não promova nova capacidade ao Gold antes de provar sua utilidade;
- valide antes de concluir.

## Verificação

Use os testes, lint, build e checks aplicáveis à mudança.

Para alterações relevantes, revise o diff e prefira auditoria independente começando pelo delta.

## Contexto

Use contexto progressivo. Abra documentação, packs, Skills, estado ou dependências somente quando necessário.

Atualize `PROJECT_STATE.md` apenas quando o estado real do projeto mudar.
