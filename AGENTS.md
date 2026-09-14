# AGENTS.md — Ideias Standard

## Missão

Construir o Ideias Standard como padrão versionado e reutilizável para projetos preparados para agentes de IA.

## Bootstrap mínimo

Antes de agir, leia apenas:

1. `AGENTS.md`;
2. `PROJECT_STATE.md`;
3. o pedido atual.

Depois abra somente os contratos necessários à tarefa. `STANDARD.md` é canônico para o padrão; `ROADMAP.md` orienta evolução; `PROJECT_STATE.md` é o estado atual.

## Regras

- trabalhe somente na etapa atual;
- mudança pequena e verificável antes de expansão;
- não transformar o repositório em template estático sem lifecycle;
- não acoplar o Standard a Codex, Claude, Gemini ou stack específica;
- preservar compatibilidade e migração como requisitos de primeira classe;
- não confundir perfil com pack;
- não adicionar controles DEEP a projetos LIGHT sem risco que justifique;
- nenhum PASS sem evidência;
- nenhuma sugestão de IA vira decisão humana automaticamente;
- não criar implementação funcional fictícia: documentação não é CLI entregue.

## Arquitetura alvo

`Idea → project-manifest → Ideias Standard compiler → project contract`

O Standard combina:

`BASE + PROFILE + PACKS + PROJECT RULES`

## Contexto

Use leitura progressiva. Não escaneie o repositório inteiro por padrão. Toda informação incluída em contexto deve ter razão concreta.

## Conclusão de tarefa

Registre:

- arquivos alterados;
- decisão;
- validação;
- limitações;
- próxima ação.

Atualize `PROJECT_STATE.md` quando o estado operacional mudar.
