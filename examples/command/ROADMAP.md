# ROADMAP — Command

**Visão:** [PROJECT.md](PROJECT.md) · **Onde paramos:** [STATE.md](STATE.md)

| Marco | Resultado verificável | Estado | Gate |
|---|---|---|---|
| D0 — Descoberta | Transporte seguro e limites do MVP escolhidos | DONE | Decisão D-001 aprovada |
| v0.1 — Fatia vertical | Celular mostra o status real do PC de ponta a ponta | IN_PROGRESS | ACs de CMD-001 no aparelho real |
| v0.2 — MVP | Abrir/encerrar app da allowlist com confirmação | BACKLOG | 3 cenários + erro testados |
| v0.3 — Estabilização | Reconexão, falhas de rede, revisão de segurança | BACKLOG | Revisão independente |
| v1.0 — Entrega | Instalar e retomar o serviço com segurança | BACKLOG | Checklist de release + aprovação |

## Marco ativo — v0.1
**Objetivo:** ver o estado do PC pelo celular. **Quem valida:** dono do projeto, no aparelho real.

| ID | Tarefa | Prioridade | Depende de | Estado | Evidência exigida |
|---|---|---|---|---|---|
| V01-01 | Agente local expõe `/status` autenticado | P0 | — | DONE | teste de API + 401 sem token |
| V01-02 | App mostra status e offline (CMD-001) | P0 | V01-01 | IN_PROGRESS | ACs no aparelho real |

**Gate de saída:** AC-01 a AC-04 de CMD-001 `PASS` no aparelho. **Riscos:** temperatura indisponível em alguns hardwares.

## Ideias futuras (não autorizadas)
| Ideia | Impacto esperado | Quando reavaliar |
|---|---|---|
| Assistente de IA opcional | Comandos por voz | Depois da v1.0, só se os comandos diretos seguirem funcionando sem ele |
