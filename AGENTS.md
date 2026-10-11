# AGENTS.md — Ideias Standard

Repositório do kit de projeto. Comece por `STATE.md`; abra `docs/` só se a tarefa pedir.

## Comandos
- Verificar: `python -m unittest discover -s tests -v` e `python scripts/check.py examples/command`

## Regras
1. Dogfooding: este repositório segue o próprio kit. Regra difícil de usar aqui não vai para o template.
2. Mudou o `template/`: atualize `examples/command/` e o `README.md` no mesmo commit; os testes têm de passar.
3. Uma regra em um só lugar: template → regra; `docs/GUIA.md` → explicação; `docs/PESQUISA.md` → evidência. Não duplicar.
4. Nova capacidade só entra depois de provada em projeto real e se for menor que a alternativa (ver `ROADMAP.md`).
5. Repositório **público**: nada de dado real de projeto (nomes, telefones, clientes), segredo ou caminho pessoal.
6. Não declarar teste não executado; `NOT_RUN` não é `PASS`. Atualize `STATE.md` quando o estado mudar.
7. Commits na `main`; não reescrever histórico nem apagar tags.
