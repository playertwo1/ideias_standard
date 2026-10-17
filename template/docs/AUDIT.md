# AUDIT — auditoria final

> Origem: [playertwo1/guardrail](https://github.com/playertwo1/guardrail) (`AUDIT.md`), adaptado ao kit: validação e git apontam para os gates de `docs/RELEASE_CHECKLIST.md`; o resultado vai para a review (`docs/templates/REVIEW.md`).

Aplique antes de declarar `DONE` uma mudança relevante, e sempre na revisão independente de mudança grande ou arriscada (`AGENTS.md`, regra 4). Quem audita age como revisor independente: o objetivo não é confirmar que o agente acertou, é descobrir onde ele pode ter errado. Comece pelo pedido, pelos ACs, pelo `git diff` e pela saída dos checks; expanda o contexto só para testar uma hipótese.

## 1. Escopo
- O pedido original foi atendido de fato?
- Há mudança fora do escopo, funcionalidade não pedida ou funcionalidade existente removida?
- A solução ficou mais complexa que o necessário?

## 2. Diff
Pergunta central: **cada alteração tem uma razão clara ligada à tarefa?** Se não, investigue.

Procure: arquivos alterados sem necessidade, código removido por acidente, mudança gigante para problema pequeno, duplicação, código morto, TODO esquecido, log de debug, hardcode, mock, comentário temporário, alteração suspeita.

## 3. Regressão
Impacto em: funcionalidades existentes, APIs, banco e migrations, configuração, autenticação e permissões, UI, integrações, persistência, jobs em segundo plano, compatibilidade.

## 4. Qualidade
Legibilidade, simplicidade, consistência com o projeto, tratamento de erros, casos-limite, concorrência, nulos, estados inesperados, lógica duplicada. Prefira a solução mais simples que resolve corretamente.

## 5. Segurança
Segredos, tokens, credenciais, permissões excessivas, dado sensível em log, validação removida, input não tratado, operação perigosa.

## 6. Validação e git
Rode e registre os gates G1–G4 de `docs/RELEASE_CHECKLIST.md` (testes, lint, tipos/build, diff e `git status` sem arquivo inesperado, grande, gerado ou segredo). Falha não se esconde; não executado é `NOT_RUN`. Não confunda alterações anteriores do usuário com as da tarefa.

## 7. Caça a atalhos
Soluções que só fazem o problema sumir da vista: exceção ignorada, `catch` vazio, validação desativada, teste removido ou afrouxado, valor hardcoded, feature desligada, sucesso falso, mock em produção.

## 8. Classificação
- **CRITICAL** — perda de dados, vulnerabilidade, quebra grave ou comportamento destrutivo.
- **HIGH** — grande chance de regressão ou funcionamento incorreto.
- **MEDIUM** — problema real que deveria ser corrigido.
- **LOW** — melhoria recomendada que não impede o funcionamento.

## 9. Resultado
Registre na review (`docs/reviews/<ID>.md`):

```text
AUDIT RESULT: PASS
```
ou `AUDIT RESULT: FAIL`, com cada finding: severidade, arquivo/local, problema, impacto e correção recomendada.

Qualquer CRITICAL ou HIGH aberto é `FAIL`. `PASS` técnico não é aceite de produto (`APPROVED` continua com a pessoa responsável). Teste verde é evidência, não prova: não aprove só porque build e testes passaram.

---
Não pergunte "como provo que funciona?". Pergunte "como isso pode quebrar?" e tente falsificar a solução. Aprove só quando não encontrar problema relevante após essa tentativa.
