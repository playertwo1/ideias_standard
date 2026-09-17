# Ideias Standard

Padrão versionado para criar, validar e evoluir projetos preparados para agentes
de IA. Seu contrato combina **base + perfil + packs + regras do projeto**. O
objetivo é dar a cada projeto governança proporcional ao risco e apenas o
contexto necessário para a tarefa.

## O que está neste repositório

- `STANDARD.md`: regras canônicas do padrão.
- `PROJECT_STATE.md` e `ROADMAP.md`: estado atual e evolução planejada.
- `schemas/`: contratos de project manifest, standard lock, contexto,
  ownership, bundles, workflows e relatório de conformance.
- `packs/`, `profiles/`, `bundles/`, `workflows/`, `adapters/`: catálogos e
  definições que compõem o contrato de projeto.
- `examples/` e `fixtures/`: projetos e entradas de validação.
- `scripts/check.py` e `scripts/validate_standard.py`: validação local de
  conformance e dos contratos do Standard.

O Standard preserva a autoridade humana sobre decisões e gates. Um resultado
de agente ou uma validação técnica não equivale a aprovação de produto.

## Validar localmente

Instale as dependências de `requirements-dev.txt` e execute:

```powershell
python scripts/validate_standard.py --self-check
python -m unittest scripts.test_check scripts.test_validate_standard
python scripts/check.py examples/standard-android-ai --json
```

Consulte `CLI_CONTRACT.md` para modos de execução, resultados e códigos de
saída. O validador trabalha com os schemas e catálogos deste repositório.

## Estado atual

S0 está fechado. S1 — Conformance First — está ativo; S1-C06–C09 foram
implementados e a correção mais recente aguarda reauditoria independente.
Gate S1 permanece `NOT_RUN`; S2 permanece `NOT_STARTED`. O estado detalhado
está em `PROJECT_STATE.md`.

## Runner separado

A automação do ciclo Builder ↔ Auditor, seus adapters, testes, contratos
específicos e evidências O0 estão em
[playertwo1/runner](https://github.com/playertwo1/runner). Este repositório
mantém os contratos gerais do Standard; o Runner é uma ferramenta externa.
O histórico O0 anterior à separação continua recuperável no Git.
