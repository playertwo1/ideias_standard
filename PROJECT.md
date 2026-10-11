# PROJECT — Ideias Standard

## Problema
Todo projeto novo com agentes de IA recomeça a organização do zero: estado perdido entre sessões, roadmap que vira lista infinita, "pronto" sem prova e regras duplicadas que incham o contexto.

## Para quem
Quem cria projetos trabalhando com vários agentes (Claude, Codex, Gemini, Hermes) e precisa que qualquer um deles retome o trabalho sem a conversa anterior.

## MVP
1. Copiar `template/` e ter, em minutos, visão, roadmap, estado e regras de agente.
2. Conferir o projeto com `scripts/check.py`.
3. Adotar o kit num projeto existente seguindo o `docs/GUIA.md`.

## Fora do MVP
- Script de criação (copiar a pasta basta), lockfile, sincronização automática de versões, packs por stack (ver ideias no `ROADMAP.md`).

## Restrições
- Repositório público; independente de fornecedor de IA; só biblioteca padrão do Python.

## Como saberemos que funcionou
Projetos criados a partir do kit passam no checker e um agente novo retoma a próxima ação só com `STATE.md` + `ROADMAP.md`.

## Autoridade de produto
O dono do repositório aprova mudanças no kit.
