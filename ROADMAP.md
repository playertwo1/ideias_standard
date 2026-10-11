# ROADMAP — Ideias Standard

**Onde paramos:** [STATE.md](STATE.md) · **Evidência de base:** [docs/PESQUISA.md](docs/PESQUISA.md)

| Marco | Resultado verificável | Estado | Gate |
|---|---|---|---|
| v0.1 — Gold V5 | validadores, schemas, packs, goldify, sync | SUPERSEDED | tag `v0.1-gold-legacy` |
| v1.0 — Kit de documentos | template + exemplo + guia + checker, CI verde | DONE | testes e checker PASS |
| v1.1 — Piloto | kit usado em 1 projeto novo e 1 existente, atritos registrados | READY | ajustes só com evidência do uso |
| v1.2 — Comparativo | 6–12 tarefas medidas (protocolo em PESQUISA §4) | BACKLOG | resultados descritivos publicados |

## Marco ativo — v1.1
| ID | Tarefa | Estado | Evidência exigida |
|---|---|---|---|
| v1.1-01 | Projeto novo criado do `template/` | READY | `check.py` PASS + lista de atritos |
| v1.1-02 | Adoção em projeto existente (já feita uma vez à mão; registrar atritos) | READY | diff revisado + lista de atritos |

## Ideias (não autorizadas até o piloto pedir)
| Ideia | Quando reavaliar |
|---|---|
| Script `new` que copia o template e preenche o nome | se copiar à mão gerar erro repetido |
| Skill de auditoria em `.agents/skills/` | se o prompt do GUIA §5 não bastar |
| Pack por stack (Python, web, Android) | se dois projetos repetirem a mesma regra |

## Critério para mudar o kit
Entra: resolve problema visto em uso real, é a solução mais simples e cabe em um lugar. Sai: ninguém usou em dois projetos ou duplica outro arquivo.
