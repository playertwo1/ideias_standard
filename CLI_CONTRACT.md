# CLI Contract — Ideias Standard

Este documento define comportamento esperado da futura CLI antes de sua implementacao. Ele nao declara S1 concluida.

## Principios

- comandos de leitura sao seguros por padrao;
- operacoes de escrita suportam `--dry-run` antes de aplicar;
- saida JSON e deterministica e propria para automacao;
- ordem dos findings e estavel;
- nenhum comando converte WARN/NOT_RUN em PASS;
- nenhum comando destrutivo usa confirmacao implicita.

## Exit codes

- `0`: execucao concluida sem finding bloqueante (`PASS` ou `WARN` conforme o comando);
- `1`: conformance/validacao resultou em `FAIL`;
- `2`: erro operacional — arquivo ausente, parse impossivel, dependencia indisponivel ou uso invalido da CLI.

## Flags comuns planejadas

- `--json`: emitir somente documento estruturado;
- `--strict`: tratar WARN selecionados como falha de politica, sem alterar o significado canônico do check;
- `--offline`: proibir acesso de rede e falhar se recurso remoto for indispensavel;
- `--dry-run`: mostrar efeito esperado sem gravar;
- `--diff`: apresentar alteracoes propostas;
- `--no-color`: saida estavel para CI/logs.

## Comandos planejados

### `check`
Valida conformance estrutural e semantica. Nao escreve no projeto.

### `doctor`
Explica os mesmos findings do `check` em formato humano. Nao cria uma segunda regra de validacao.

### `init`
Compila manifesto em projeto novo. Escrita exige preview/dry-run quando houver destino nao vazio.

### `adopt`
Inventaria brownfield antes de qualquer escrita. Arquivos existentes sao USER_OWNED por padrao.

### `upgrade`
Renderiza alvo em staging, compara baseline/local/alvo e so atualiza lock apos validacao.

### `compile-context`
Produz contexto REQUIRED/CONDITIONAL/DISCOVERY com justificativas. Overflow de REQUIRED retorna `CONTEXT_OVERFLOW` em vez de truncar.

## Determinismo

Para a mesma versao do Standard, mesmo input e mesmo conjunto de artefatos locais, a saida estruturada deve ser semanticamente identica. Campos de tempo ou ambiente devem ser explicitamente marcados como nao deterministas quando inevitaveis.
