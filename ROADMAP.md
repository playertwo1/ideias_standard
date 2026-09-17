# ROADMAP V4 — IDEIAS STANDARD

## 1. OBJETIVO

O **Ideias Standard** é um template opinativo e reutilizável para iniciar projetos com uma base profissional, simples e preparada para desenvolvimento humano e assistido por IA.

A prioridade é entregar **boas práticas úteis por padrão**, sem transformar cada projeto em um sistema de governança complexo.

Princípio:

> Bom por padrão. Simples por padrão. Extensível quando necessário.

Regra contra overengineering:

> Toda nova abstração, regra, arquivo, teste ou camada precisa justificar qual problema concreto resolve e por que uma solução mais simples não é suficiente.

---

## 2. ESCOPO

O Standard deve ajudar um projeto a começar com:

- estrutura clara;
- `README.md` útil;
- `AGENTS.md` com instruções para agentes de IA;
- configuração básica de Git e editor;
- CI simples;
- testes essenciais;
- documentação mínima;
- boas práticas de segurança proporcionais ao projeto;
- packs opcionais para tecnologias ou necessidades específicas.

O Standard **não precisa**, por padrão, controlar todo o ciclo de vida do projeto, todas as decisões humanas ou cada mudança realizada por um agente.

O Runner Builder ↔ Auditor continua sendo uma ferramenta externa e opcional:

https://github.com/playertwo1/runner

---

## 3. REGRAS DE SIMPLICIDADE

1. Começar sempre pela solução mais simples que atende o problema.
2. Não criar arquivo, schema, estado ou camada sem uso concreto.
3. Não duplicar informação em múltiplos lugares.
4. Não criar gates humanos para tarefas técnicas comuns.
5. Não exigir auditoria em cada pequeno critério.
6. Não testar detalhes internos sem valor prático.
7. Bugs relevantes corrigidos devem receber teste de regressão quando fizer sentido.
8. Recursos opcionais devem permanecer opcionais.
9. O template deve continuar compreensível para uma pessoa nova no projeto.
10. Segurança deve ser proporcional ao risco real do projeto.

---

## 4. COMO UMA FASE É CONCLUÍDA

Cada fase possui apenas três passos:

1. **Implementar** o objetivo da fase.
2. **Validar** com os testes essenciais.
3. **Auditar** o resultado final para confirmar que está correto, simples e sem regressões importantes.

Não existem gates adicionais por padrão.

A auditoria deve responder somente:

- funciona como planejado?
- existe erro ou regressão importante?
- algo ficou desnecessariamente complexo?
- a documentação necessária está coerente?

Se a resposta estiver satisfatória, a fase é considerada concluída.

---

# F0 — GOLDEN TEMPLATE

**Status:** ACTIVE

## Objetivo

Definir a melhor base reutilizável possível para novos projetos.

## Entregas

- [ ] definir a estrutura mínima do template;
- [ ] consolidar `README.md`;
- [ ] consolidar `AGENTS.md`;
- [ ] manter `PROJECT_STATE.md` simples e opcional para projetos que precisem dele;
- [ ] fornecer `.gitignore` adequado;
- [ ] fornecer `.editorconfig`;
- [ ] fornecer CI básico;
- [ ] definir padrão mínimo de testes;
- [ ] definir documentação mínima recomendada;
- [ ] revisar o conteúdo existente e remover estruturas que não tenham utilidade no novo modelo;
- [ ] criar pelo menos um projeto de exemplo usando o template completo.

## Reaproveitar do trabalho atual

Sempre que continuar útil, reaproveitar:

- `AGENTS.md`;
- `README.md`;
- validadores já existentes;
- schemas simples que ainda tenham função prática;
- packs existentes que representem necessidades reais;
- fixtures que protejam comportamentos importantes;
- CI já funcional.

Nada deve ser mantido apenas porque já foi implementado.

## Validação mínima

- o exemplo criado a partir do template é compreensível;
- os arquivos essenciais existem;
- CI executa corretamente;
- testes essenciais passam;
- um agente de IA consegue identificar como trabalhar no projeto lendo as instruções principais.

## Auditoria

Uma única auditoria da fase confirma se o Golden Template está correto e simples.

---

# F1 — GENERATOR

**Status:** NOT_STARTED

## Objetivo

Permitir criar um novo projeto a partir do Standard sem copiar arquivos manualmente.

Exemplo de uso desejado:

```powershell
ideias-standard init meu-app
```

Ou, quando houver packs:

```powershell
ideias-standard init meu-app --android --ai
```

## Entregas

- [ ] implementar comando `init`;
- [ ] receber nome e opções principais do projeto;
- [ ] copiar/renderizar o template base;
- [ ] aplicar somente os packs escolhidos;
- [ ] evitar sobrescrever destino existente sem confirmação explícita;
- [ ] gerar projeto pronto para abrir e desenvolver;
- [ ] emitir mensagem simples de sucesso ou erro.

## Validação mínima

Testar apenas os cenários essenciais:

- projeto básico é criado corretamente;
- projeto com pack é criado corretamente;
- entrada inválida falha de forma compreensível;
- destino que já contém arquivos não é sobrescrito silenciosamente;
- projeto gerado passa no CI básico.

## Auditoria

Uma única auditoria confirma que o gerador produz corretamente o template esperado.

---

# F2 — QUALITY CHECK

**Status:** NOT_STARTED

## Objetivo

Fornecer uma verificação simples para saber se um projeto continua compatível com o Standard.

Uso desejado:

```powershell
ideias-standard check
```

## O `check` deve verificar

- [ ] arquivos essenciais presentes;
- [ ] configuração principal válida;
- [ ] `AGENTS.md` presente quando aplicável;
- [ ] packs declarados existem e são compatíveis;
- [ ] CI básico configurado quando esperado;
- [ ] inconsistências óbvias que realmente impeçam o uso do template.

## Resultado esperado

Saída humana curta:

```text
✓ configuração válida
✓ arquivos essenciais presentes
✓ AGENTS.md encontrado
✓ packs válidos
✓ CI configurado

PASS
```

Quando houver problema:

```text
FAIL
- arquivo obrigatório ausente: AGENTS.md
```

Pode existir saída JSON se ela for útil para automação, mas ela não deve tornar a implementação mais complexa que o necessário.

## Reaproveitar do S1 antigo

O trabalho já feito em `check`, manifests, ownership, packs e workflows pode ser reaproveitado **somente onde simplificar esta fase**.

Não continuar automaticamente a antiga lista S1-C10–C33.

## Validação mínima

- projeto válido → PASS;
- projeto claramente inválido → FAIL com mensagem útil;
- execuções repetidas no mesmo projeto não produzem resultados contraditórios.

## Auditoria

Uma única auditoria confirma que o `check` detecta os problemas importantes sem criar burocracia.

---

# F3 — PACKS E ECOSSISTEMA

**Status:** NOT_STARTED

## Objetivo

Adicionar extensões reutilizáveis somente quando houver necessidade real.

## Packs iniciais candidatos

- `android`;
- `python`;
- `web`;
- `ai`;
- `multi-agent`;
- `sensitive-data`.

A lista não é uma obrigação. Um pack deve existir somente quando houver projeto real que justifique sua criação.

## Cada pack deve conter somente o necessário

Exemplos:

### Android

- estrutura/recomendações Android;
- `.gitignore` adequado;
- CI adequado;
- instruções relevantes para agentes.

### Python

- estrutura Python;
- dependências e ambiente;
- lint/test básico;
- CI adequado.

### AI

- instruções para uso de modelos;
- tratamento de secrets;
- configuração de avaliação somente quando o projeto realmente precisar.

### Multi-agent

- regras básicas de papéis;
- integração opcional com o Runner;
- sem obrigar todos os projetos a usar Builder/Auditor.

## Validação mínima

Para cada pack mantido:

- pode ser aplicado a um projeto novo;
- não quebra o template base;
- possui pelo menos um exemplo ou teste que prove seu funcionamento principal.

## Auditoria

Auditar cada pack quando ele estiver pronto para uso real, sem criar uma fase independente de governança para cada detalhe interno.

---

# 5. BACKLOG — SOMENTE SE HOUVER NECESSIDADE REAL

Os itens abaixo **não fazem parte do roadmap obrigatório**. Só devem ser promovidos para uma fase quando um problema real justificar a complexidade.

- adoção automática de projetos antigos (`adopt`);
- atualização automática de templates já aplicados (`upgrade`);
- migrations complexas;
- fingerprints de arquivos;
- provenance detalhada;
- three-way merge;
- gerenciamento avançado de ownership;
- bundles;
- múltiplos profiles de governança;
- lifecycle formal de mudanças;
- sistema avançado de contexto/token budget;
- métricas de critical recall;
- integração automática Idea → Standard;
- adapters específicos por fornecedor;
- validações extensivas multi-provider.

Regra:

> Primeiro provar que precisamos. Depois construir.

---

# 6. TESTES

Testar comportamento importante, não o roadmap.

Base mínima:

1. template válido funciona;
2. gerador cria projeto válido;
3. `check` aprova projeto válido;
4. `check` rejeita erro importante;
5. packs principais não quebram o template;
6. bug relevante corrigido recebe regressão quando aplicável.

Não existe meta de quantidade de testes.

Cobertura é ferramenta de diagnóstico, não objetivo do produto.

---

# 7. SEGURANÇA

Segurança deve seguir boas práticas proporcionais ao risco.

Baseline:

- secrets nunca entram no repositório;
- dependências devem poder ser atualizadas;
- CI não deve expor credenciais;
- entradas externas devem ser validadas quando aplicável;
- operações destrutivas importantes não devem ocorrer silenciosamente.

Projetos sensíveis podem adicionar controles extras por meio de um pack específico.

O projeto base não deve carregar controles de sistemas críticos que não precisa.

---

# 8. RELAÇÃO COM AGENTES DE IA

O Standard deve facilitar o trabalho de Codex, Claude, Gemini, Antigravity e outros agentes sem depender de um fornecedor específico.

O principal mecanismo é documentação clara e instruções persistentes no projeto.

Fluxo esperado:

```text
Golden Template
      ↓
Novo Projeto
      ↓
AGENTS.md + README + estrutura clara
      ↓
Builder / agente de desenvolvimento
      ↓
Testes + CI
      ↓
Auditoria quando necessária
```

Para projetos que desejarem automação Builder ↔ Auditor:

```text
Ideias Standard
      ↓
projeto preparado
      ↓
Runner opcional
      ↓
Builder ↔ Auditor
```

O Runner não é requisito para usar o Standard.

---

# 9. IDEIA FUTURA

O projeto `Idea` poderá futuramente gerar a configuração inicial usada pelo Ideias Standard.

Fluxo desejado:

```text
Idea
  ↓
Definição do projeto
  ↓
Ideias Standard
  ↓
Template + packs
  ↓
Projeto pronto para desenvolvimento
```

Essa integração só deve ser construída depois que o próprio Standard estiver simples e estável.

---

# 10. DEFINIÇÃO DE SUCESSO

O Ideias Standard estará cumprindo sua função quando for possível criar um projeto novo e, em poucos minutos, obter:

- estrutura profissional;
- instruções claras para agentes;
- documentação mínima útil;
- CI funcionando;
- testes essenciais;
- packs adequados à tecnologia escolhida;
- baixa quantidade de configuração manual;
- pouca burocracia.

A pergunta principal não será:

> Quantos controles o Standard possui?

Será:

> Ele me ajuda a começar um projeto melhor e mais rápido?

---

# 11. ORDEM DE EXECUÇÃO

```text
F0 Golden Template
        ↓
F1 Generator
        ↓
F2 Quality Check
        ↓
F3 Packs e Ecossistema
```

Qualquer capacidade além disso entra primeiro no backlog.

**Não construir antecipadamente.**
