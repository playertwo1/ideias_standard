---
name: "{{nome do projeto}} — design"
description: "{{alvo visual: proposto | aprovado em AAAA-MM-DD | aplicado ao frontend}}"
colors:
  background: "{{#hex}}"
  surface: "{{#hex}}"
  border: "{{#hex}}"
  foreground: "{{#hex}}"
  muted: "{{#hex}}"
  primary: "{{#hex}}"
  primary-foreground: "{{#hex}}"
  danger: "{{#hex}}"
  warning: "{{#hex}}"
  success: "{{#hex}}"
typography:
  heading:
    fontFamily: "{{fonte, fallback}}"
    fontSize: "{{px}}"
    fontWeight: 700
    lineHeight: "{{px}}"
  body:
    fontFamily: "{{fonte, fallback}}"
    fontSize: "{{px}}"
    fontWeight: 400
    lineHeight: "{{px}}"
  label:
    fontFamily: "{{fonte, fallback}}"
    fontSize: "{{px}}"
    fontWeight: 600
    lineHeight: "{{px}}"
rounded:
  control: "{{px}}"
  card: "{{px}}"
  pill: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-foreground}"
    rounded: "{rounded.control}"
    height: "{{px}}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.card}"
    padding: "{{px}}"
---

# {{nome do projeto}} — design

A cara do app: a fonte que qualquer agente consulta antes de construir ou mudar uma tela. Os tokens acima viram variáveis CSS/tema; o texto abaixo explica o porquê e os limites. Projeto sem interface: apague este arquivo.

## Overview
- **Personalidade:** {{três adjetivos, ex.: calmo, denso, confiável}}
- **Para quem e onde:** {{usuário, dispositivo principal, ambiente de uso}}
- **Modo:** {{trabalho diário/operação | marketing/vitrine | jogo/experiência}}
- **Plataformas e larguras-alvo:** {{ex.: desktop 1440/1280, mobile 390}} · **Tema:** {{escuro | claro | ambos}}
- **Referências que inspiram:** {{links ou caminhos em docs/design/; o que pegar de cada uma}}
- **Anti-referências:** {{o que este app não deve parecer}}
- **Estado:** este arquivo descreve {{o alvo aprovado | o que já está no frontend}}. Referência adotada não é aceite de implementação.

## Colors
{{papel de cada cor; quando usar a primária; cores de estado}}. Estado sempre acompanha texto ou ícone, nunca só cor. Contraste mínimo 4,5:1 em texto comum e 3:1 em texto grande e elementos essenciais.

## Typography
{{fonte e fallback; licença e se é servida localmente}}. Escala: título, seção, corpo, rótulo (tokens acima). Dados operacionais não descem abaixo de {{px}}; números em colunas usam numerais tabulares. Ícones: {{biblioteca única}}.

## Layout
{{navegação global (lateral/topo/abas inferiores), grade, larguras máximas}}. Espaçamento base 4 px. Por tela principal: {{composição em uma linha, ex.: Início = 4 indicadores + 6 painéis}}. Responsivo: {{o que vira gaveta, coluna empilhada ou folha inferior em cada quebra}}; alvos de toque ≥ 44 px; sem rolagem horizontal da página.

## Elevation & Depth
{{separação por tom e borda ou por sombra}}. Modal e gaveta prendem o foco e devolvem ao acionador. Animações curtas, respeitando movimento reduzido; dado crítico não depende de animação.

## Shapes
Controles {{px}}, cartões {{px}}, selos em cápsula. {{avatar: iniciais | foto}}.

## Components
- Botão: primário, secundário, perigo; estados carregando, desabilitado e erro. O rótulo diz o que acontece de fato.
- Campo e formulário: rótulo visível, ajuda, erro junto ao campo.
- Tabela/lista: a linha inteira abre a entidade; ações independentes; vazio e sem resultado distintos.
- Estados de tela: carregando, vazio, erro recuperável, offline/integração desconectada, sessão expirada. Nunca mostrar dado de exemplo como se fosse real.
- {{componente específico do produto}}

## Do's and Don'ts
- Seguir a composição de cada tela de referência; diferenças só registradas aqui com motivo.
- Reusar os componentes e a stack já existentes ({{ex.: React + Tailwind + shadcn}}); não copiar CDN, script ou dado ilustrativo da referência para produção.
- Não inventar funcionalidade que a referência mostra mas o produto não tem (ex.: botões de ligação, métricas sem fonte).
- Validar com capturas reais nas larguras-alvo, nomes longos, estados e teclado (`docs/RELEASE_CHECKLIST.md` §3).
