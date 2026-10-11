# Pesquisa — por que o kit é assim

Síntese do manual "Roadmaps para projetos com agentes de IA" (corte em 10/10/2026). Separa documentação oficial, pesquisa revisada, preprint e relato informal. **Nenhum estudo isolado prova que este kit, Spec Kit, OpenSpec, GSD ou BMAD seja superior.** A escolha final depende de piloto local (seção 4).

## 1. O que a pesquisa ensina

| Lição | Consequência no kit | Fonte |
|---|---|---|
| Separar visão de longo prazo, definição de recursos e execução diária | `PROJECT` / `ROADMAP` / `FEATURE`+`PLAN` | R15 (revisado) |
| Arquivos de contexto grandes frequentemente reduziram o sucesso e aumentaram o custo em mais de 20% | `AGENTS.md` curto, resto sob demanda; checker avisa | R22 (preprint) |
| Documentar pré/pós-condições antes de gerar testes: +9,8 p.p. de bugs detectados | ACs e contrato na `FEATURE` | R16 (workshop) |
| Cerca de metade dos PRs de IA que passavam no benchmark não seria aceita sem mudanças | revisão humana de qualidade e escopo; teste verde não fecha | R21 (nota) |
| Bons resultados multiagente dependem de testes humanos e verificação explícita por subtarefa | handoff com ID, evidência, riscos e próxima ação | R17, R18, R23 |
| Desenvolvedores experientes foram 19% mais lentos com IA no estudo de 2025; estimativas de 2026 têm viés | medir tempo até o aceite, incluindo retrabalho | R19, R20 |
| IA amplifica as práticas que a organização já tem | o kit reforça práticas, não substitui revisão | R26 |
| Prevalência de specs em repositórios não mostra causalidade | não padronizar por moda | R24, R25 |

## 2. O que cada ferramenta ensina

| Ferramenta | Ideia adotada | Cuidado |
|---|---|---|
| GitHub Spec Kit | spec → plano → tarefas → implementar → convergir; quebrar features grandes | não abrir hierarquia gigante em tarefa pequena |
| OpenAI Codex | `AGENTS.md` objetivo; ExecPlan autocontido para mudança grande | plano narrado não é teste feito |
| Claude Code | explorar antes de alterar, planejar quando há incerteza, verificar | `CLAUDE.md` não replica os docs |
| Hermes Agent | `/plan`, `/init`, skills sob demanda | não transferir autoridade do usuário ao agente |
| OpenSpec | spec por mudança incremental | evitar specs obsoletas proliferando |
| GSD Core | marcos menores e continuidade por fase | processo completo não é obrigatório |
| BMAD | papéis e decisões estruturadas | overhead em MVP pequeno |
| Superpowers | planejamento, testes e revisão como skills | escolher só as úteis |

## 3. Fontes

- **R01 — GitHub Spec Kit — repositório oficial** | Documentação oficial  
  [Abrir fonte](https://github.com/github/spec-kit) — Fluxo especificar → planejar → tarefas → implementar → convergir.
- **R02 — Spec Kit — Spec of Specs** | Documentação oficial  
  [Abrir fonte](https://github.com/github/spec-kit/blob/main/docs/concepts/spec-of-specs.md) — Quebrar marcos grandes em features independentes; usar somente se necessário.
- **R03 — Spec Kit — Quickstart** | Documentação oficial  
  [Abrir fonte](https://github.com/github/spec-kit/blob/main/docs/quickstart.md) — Validação de requisitos, consistência e convergência.
- **R04 — OpenAI — ExecPlans / PLANS.md** | Documentação oficial  
  [Abrir fonte](https://developers.openai.com/cookbook/articles/codex_exec_plans) — Plano autocontido com progresso, surpresas, decisões e verificação.
- **R05 — OpenAI — Code Modernization com Codex** | Documentação oficial  
  [Abrir fonte](https://developers.openai.com/cookbook/examples/codex/code_modernization) — AGENTS.md conciso + PLANS.md para trabalho complexo.
- **R06 — OpenAI — Repensando skills e prompts (set/2026)** | Documentação oficial  
  [Abrir fonte](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — Evitar instruções e contexto desnecessários.
- **R07 — Anthropic — Claude Code Best Practices** | Documentação oficial  
  [Abrir fonte](https://code.claude.com/docs/en/best-practices) — Explorar, planejar conforme complexidade, verificar e manter CLAUDE.md legível.
- **R08 — Hermes Agent — repositório** | Documentação oficial  
  [Abrir fonte](https://github.com/NousResearch/hermes-agent) — Agente que aproveita documentação de projeto e skills.
- **R09 — Hermes — slash commands: /plan e /init** | Documentação oficial  
  [Abrir fonte](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/slash-commands.md) — /plan cria planos; /init cria/atualiza AGENTS.md.
- **R10 — Hermes — sistema de skills** | Documentação oficial  
  [Abrir fonte](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md) — Skills progressivas sob demanda e diretórios externos.
- **R11 — OpenSpec — repositório** | Repositório  
  [Abrir fonte](https://github.com/Fission-AI/OpenSpec) — Especificações de mudanças incrementais.
- **R12 — BMAD Method — repositório** | Repositório  
  [Abrir fonte](https://github.com/bmad-code-org/BMAD-METHOD) — Papéis e planejamento mais elaborado.
- **R13 — GSD Core — repositório** | Repositório  
  [Abrir fonte](https://github.com/open-gsd/gsd-core) — Fases e execução incremental.
- **R14 — Superpowers — repositório** | Repositório  
  [Abrir fonte](https://github.com/obra/superpowers) — Skills para planejamento, testes e revisão.
- **R15 — Heikkilä et al. — Ericsson, Empirical Software Engineering (2017)** | Artigo revisado por pares  
  [Abrir fonte](https://link.springer.com/article/10.1007/s10664-016-9491-z) — Estudo de caso qualitativo com 43 entrevistas, estratégia→feature→execução.
- **R16 — Tufano et al. — Grounding AI Agents in Contracts (ACM SpecOps 2026)** | Artigo de conferência/workshop  
  [Abrir fonte](https://research.google/pubs/grounding-ai-agents-in-contracts-an-empirical-evaluation-of-spec-driven-test-generation/) — +9,8 p.p. em detecção de bugs e +2,5 p.p. em cobertura de ramos no cenário avaliado.
- **R17 — Han et al. — TDFlow (EACL 2026)** | Artigo revisado por pares  
  [Abrir fonte](https://aclanthology.org/2026.eacl-long.70/) — Agentes especializados em correção guiados por testes humanos.
- **R18 — Xu et al. — VeriMAP (EACL 2026)** | Artigo revisado por pares  
  [Abrir fonte](https://aclanthology.org/2026.eacl-long.353/) — Dependências e funções explícitas de verificação em tarefas multiagente.
- **R19 — METR — efeito da IA em desenvolvedores experientes (2025)** | Experimento randomizado  
  [Abrir fonte](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — Desenvolvedores 19% mais lentos no contexto experimental de 2025.
- **R20 — METR — atualização do experimento (fev/2026)** | Atualização metodológica  
  [Abrir fonte](https://metr.org/blog/2026-02-24-uplift-update/) — Viés de participação impede estimar confiavelmente aceleração atual.
- **R21 — METR — revisão de PRs SWE-bench (mar/2026)** | Nota de pesquisa  
  [Abrir fonte](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/) — Aprovação em teste automático não garante aceitação por mantenedores.
- **R22 — Gloaguen et al. — Evaluating AGENTS.md (arXiv 2026)** | Preprint  
  [Abrir fonte](https://arxiv.org/abs/2602.11988) — Contexto excessivo pode reduzir sucesso e aumentar custo; não generalizar.
- **R23 — Zhang et al. — AsynCodeBench (arXiv set/2026)** | Preprint  
  [Abrir fonte](https://arxiv.org/abs/2609.32662) — 19 tarefas, 52 dependências; colaboração difere de capacidade individual.
- **R24 — Agarwal et al. — SpecMine (arXiv 2026)** | Preprint/corpus  
  [Abrir fonte](https://arxiv.org/abs/2608.25202) — 470.795 specs em 73.030 repositórios; não mede causalidade.
- **R25 — Panda — Citation Discipline SDD (arXiv jun/2026)** | Preprint/comparação exploratória  
  [Abrir fonte](https://arxiv.org/abs/2606.30689) — Comparação em determinismo e detecção de alucinação, não em qualidade geral do produto.
- **R26 — Google DORA 2025 — relatório** | Relatório de pesquisa  
  [Abrir fonte](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/) — Pesquisa com quase 5.000 profissionais; IA amplifica práticas organizacionais.
- **R27 — Reddit r/ClaudeCode — SpecKit x OpenSpec x BMAD** | Discussão comunitária  
  [Abrir fonte](https://www.reddit.com/r/ClaudeCode/comments/1pba1ud/spec_driven_development_sdd_speckit_openspec_bmad/) — Relatos de trade-offs e excesso de processo; evidência anedótica.
- **R28 — Reddit r/ClaudeCode — 18 meses de agentic coding** | Discussão comunitária  
  [Abrir fonte](https://www.reddit.com/r/ClaudeCode/comments/1r3rb6y/18_months_of_agentic_coding_in_765_words_because/) — Relatos sobre continuidade e organização de trabalho.

## 4. Protocolo comparativo (antes de padronizar mudanças no kit)

Hipótese humilde: uma versão nova pode aumentar a taxa de aceite e facilitar handoffs, mas custar mais em tarefas pequenas. Compare mantendo modelo, escopo, critérios e ferramentas o mais constantes possível.

| Métrica | Como medir | Armadilha |
|---|---|---|
| Aceite funcional | ACs aprovados / aplicáveis | contar `NOT_RUN` como sucesso |
| Tempo total | do início ao aceite humano, com retrabalho | contar só geração de código |
| Custo total | tokens + tempo humano + infraestrutura | ignorar a revisão |
| Retrabalho | ciclos extras e regressões | não contar bug reaberto |
| Handoff | agente novo retoma sem o chat original | agente já conhece a resposta |
| Qualidade | revisão cega com rubrica | revisor sabe qual versão foi usada |

Piloto exploratório: 6–12 tarefas estratificadas por complexidade. Com amostra pequena, reporte resultados descritivos e problemas do procedimento; não declare significância nem superioridade universal.
