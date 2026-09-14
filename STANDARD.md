# Ideias Standard — Contrato Canônico

Versão inicial: `0.1.0-draft`.

## 1. Missão

Padronizar como projetos preparados para agentes de IA nascem, são validados, evoluem e trocam contexto, sem acoplar o projeto a um agente, stack ou provedor específico.

## 2. Autoridade

Ordem de precedência recomendada para projetos gerados:

`invariantes de segurança → pedido vigente da Product Authority → decisões LOCKED → contrato específico do projeto → Standard aplicável → estado operacional → julgamento técnico`

O Standard nunca transforma sugestão de IA em decisão humana.

## 3. Perfis

### LIGHT
Para utilitários, experimentos e mudanças pequenas. Exige governança e validação mínimas proporcionais ao risco.

### STANDARD
Perfil padrão para aplicativos e features normais. Inclui estado operacional, fases, auditoria proporcional, contexto progressivo e evidências.

### DEEP
Para sistemas sensíveis, amplos, multiagente ou com integrações críticas. Adiciona controles, auditoria e artefatos extras quando a capacidade realmente se aplica.

Selecionar DEEP não autoriza automaticamente todos os packs.

## 4. Packs

Packs são extensões composáveis. Exemplos iniciais:

- `android`
- `python`
- `backend`
- `ai`
- `sensitive-data`
- `multi-agent`

Um projeto pode usar `STANDARD + android + ai` sem receber controles DEEP irrelevantes.

## 5. Contratos estruturados

Todo projeto gerenciado pelo Standard deve poder declarar:

- identidade e tipo;
- versão do Standard;
- perfil;
- packs;
- capacidades ativas;
- papéis de autoridade;
- estratégia de contexto;
- overrides locais;
- estado de compatibilidade.

Os arquivos principais são:

- `project-manifest.json`
- `.idea-standard/standard.lock`
- `context-manifest.json`

## 6. Contexto

Regra central: **menor contexto suficiente para executar a tarefa corretamente**.

Classes:

- `REQUIRED`: necessário para a tarefa;
- `CONDITIONAL`: carregado quando um gatilho concreto se aplica;
- `DISCOVERY`: consultado apenas quando os níveis anteriores não resolvem.

Nenhuma regra crítica pode ser truncada silenciosamente por orçamento. Overflow obrigatório deve gerar estado explícito e pedir divisão/expansão.

## 7. Atualização

Projetos não devem precisar ser recriados para receber uma nova versão do Standard.

O ciclo desejado é:

`check → diff → plan migration → apply → validate → lock new version`

Mudanças locais precisam ser detectadas e preservadas ou apresentadas para revisão.

## 8. Adoção de legado

`adopt` deve analisar o projeto existente, recomendar perfil/packs, detectar lacunas e produzir plano antes de alterar arquivos.

Nunca substituir silenciosamente contratos ou documentação válida do projeto.

## 9. Independência de agente

O contrato canônico não é `AGENTS.md`, `CLAUDE.md` ou `GEMINI.md`.

Esses arquivos podem ser adapters/materializações derivados de um contrato comum. Divergência entre adapters deve ser detectável.

## 10. Verificação

Estados mínimos:

- `NOT_RUN`
- `PASS`
- `FAIL`
- `NOT_APPLICABLE` com rationale

`NOT_RUN != PASS`.

## 11. Regra final

O Standard deve reduzir ambiguidade, desperdício de contexto e drift sem criar burocracia maior que o risco do projeto.
