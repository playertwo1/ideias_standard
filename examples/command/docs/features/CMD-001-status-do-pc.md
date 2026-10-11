# FEATURE CMD-001 — ver o estado do PC pelo celular

**Marco:** v0.1 (V01-02) · **Prioridade:** P0 · **Estado:** IN_PROGRESS · **Decisões:** D-001 (transporte local autenticado)

## Comportamento verificável
**Dado** um celular pareado e o agente local rodando, **quando** abro a tela de status, **então** vejo RAM, CPU, temperatura (se houver sensor) e online/offline em até 3 s.

## Contrato e casos-limite
- Pré-condição: token de pareamento válido no cofre do celular.
- Pós-condição: nenhum dado é gravado no celular além do último status e seu horário.
- Erro: PC offline mostra "indisponível" com o horário da última leitura; nunca número inventado.
- Não objetivos: controlar o PC nesta feature.
- Segurança: token nunca aparece em tela, log ou evidência.

## Critérios de aceite
- [ ] AC-01 PC online: dados exibidos com horário da última atualização.
- [ ] AC-02 PC offline: "indisponível", sem números.
- [ ] AC-03 Sem sensor de temperatura: "não informado".
- [ ] AC-04 Token ausente das telas e dos logs (conferido no logcat).
