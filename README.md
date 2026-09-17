# Ideias Standard

O **Ideias Standard** é uma base Gold simples e reutilizável para criar, validar e melhorar projetos desenvolvidos por humanos e agentes de IA.

A proposta é direta:

> projeto fácil de entender + contexto mínimo + verificação objetiva + auditoria independente.

Sem transformar cada repositório em um sistema de governança complexo.

## Princípios

- **Small Core** — poucas regras universais;
- **Progressive Context** — contexto específico somente quando necessário;
- **Token Discipline** — maximizar sinal por token;
- **Executable Verification** — mudanças devem poder ser verificadas por comandos reais;
- **Independent Audit** — alterações relevantes podem ser revisadas por outro agente/processo;
- **Optional Packs & Skills** — capacidades específicas entram somente quando úteis;
- **No Overengineering** — nenhuma abstração existe sem problema concreto.

## O que é um projeto Gold

Um projeto Gold:

- explica claramente o que faz;
- possui `README.md` útil;
- possui `AGENTS.md` curto e operacional;
- tem estrutura compreensível;
- possui build/test/lint/typecheck aplicáveis;
- possui um mecanismo conhecido de `check`;
- executa verificações importantes no CI;
- carrega documentação específica somente sob necessidade;
- filtra ou resume outputs grandes antes de colocá-los no contexto;
- pode ser auditado pelo diff sem exigir leitura integral do repositório;
- usa segurança proporcional ao risco.

Gold padroniza qualidade e operação. Não obriga projetos diferentes a terem a mesma arquitetura.

## Contexto para agentes

O bootstrap padrão é mínimo:

```text
AGENTS.md + pedido atual
```

`PROJECT_STATE.md`, `STANDARD.md`, `ROADMAP.md`, documentação, packs, Skills e dependências são consultados somente quando relevantes.

```text
pedido
  ↓
localizar antes de ler
  ↓
menor trecho suficiente
  ↓
expandir somente quando necessário
```

`AGENTS.md` é a fonte canônica de instruções universais e deve permanecer pequeno. Evite duplicar as mesmas instruções em arquivos específicos de Codex, Claude, Gemini, Antigravity ou Copilot.

## Fluxo de trabalho

```text
pedido
  ↓
Builder
  ↓
check resumido
  ↓
diff
  ↓
Auditor independente
  ↓
PASS ou FINDINGS
```

O Auditor começa pelo pedido, critérios de aceite, diff e evidências de validação. Ele amplia contexto somente quando houver uma razão concreta.

A automação Builder ↔ Auditor pode ser feita pelo projeto externo [playertwo1/runner](https://github.com/playertwo1/runner), mas o Runner não é requisito para usar o Standard.

## Skills

Skills guardam procedimentos especializados fora do contexto permanente.

Prioridades iniciais do Gold:

- `gold-audit` — revisar alterações pelo diff;
- `goldify` — analisar projeto existente e gerar Golden Diff;
- `skill-author` — criar/revisar Skills pequenas e seguras.

Skills externas nunca são copiadas cegamente. O fluxo é:

```text
DISCOVER → REVIEW → TRIM → ADAPT → TEST → INSTALL
```

Adoção depende de utilidade real, revisão de segurança, licença e compatibilidade com o modelo de contexto progressivo.

## Roadmap

O desenvolvimento segue seis blocos simples:

1. **F0 — Golden Standard**: definir e provar a base Gold;
2. **F1 — Create**: criar projetos novos usando primeiro GitHub Template;
3. **F2 — Check + Audit**: verificação executável, saída curta e revisão independente;
4. **F3 — Packs + Skills**: capacidades específicas sob demanda;
5. **F4 — Adopt / Goldify**: elevar projetos existentes ao Gold sem reconstruí-los;
6. **F5 — Sync**: futuro, para distribuir melhorias do Standard.

Consulte `ROADMAP.md` para detalhes e `PROJECT_STATE.md` para o estado atual.

## Arquivos principais deste repositório

- `STANDARD.md` — regras canônicas do Gold Standard;
- `ROADMAP.md` — ordem de evolução;
- `PROJECT_STATE.md` — estado atual;
- `AGENTS.md` — instruções mínimas para agentes neste próprio repositório;
- `CLI_CONTRACT.md` — superfície mínima esperada de automação/CLI;
- `packs/`, `examples/`, `fixtures/`, `schemas/` e `scripts/` — ativos existentes que serão mantidos somente quando continuarem úteis ao modelo Gold.

## Estado atual

O projeto está em **F0 — Golden Standard**.

A arquitetura antiga baseada em profiles, bundles, gates e lifecycle amplo foi substituída pelo modelo Gold. O código e os artefatos existentes serão reaproveitados apenas quando simplificarem o novo Standard.

## Regra principal

> Se uma solução mais simples resolve corretamente o problema, use a solução mais simples.
