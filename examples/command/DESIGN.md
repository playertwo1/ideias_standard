---
name: "Command — design"
description: "Alvo aprovado em 2026-10-11 (exemplo didático)"
colors:
  background: "#0F1115"
  surface: "#171A21"
  border: "#262B36"
  foreground: "#E6E8EE"
  muted: "#8A93A6"
  primary: "#4F8CFF"
  primary-foreground: "#0F1115"
  danger: "#F05252"
  warning: "#F5A524"
  success: "#2BB673"
typography:
  heading:
    fontFamily: "Inter, Roboto, sans-serif"
    fontSize: "22px"
    fontWeight: 700
    lineHeight: "28px"
  body:
    fontFamily: "Inter, Roboto, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: "22px"
  label:
    fontFamily: "Inter, Roboto, sans-serif"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: "16px"
rounded:
  control: "10px"
  card: "16px"
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
    height: "48px"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.card}"
    padding: "16px"
---

# Command — design

## Overview
- **Personalidade:** sóbrio, legível de relance, seguro.
- **Para quem e onde:** dono do PC, celular na mão, muitas vezes de longe e com pressa.
- **Modo:** operação. **Plataforma:** Android, 360–412 px. **Tema:** escuro.
- **Referências:** painéis de status de roteadores (um número grande por cartão).
- **Anti-referências:** área de trabalho remota cheia de botões; gráficos decorativos sem dado.

## Colors
Azul só para ação principal; verde/âmbar/vermelho só para estado do PC (online, alto uso, offline), sempre com rótulo.

## Typography
Inter local com fallback Roboto. Valores de RAM/CPU em 32 px com numerais tabulares; nunca abaixo de 12 px.

## Layout
Uma coluna; cartão de status no topo (online/offline + horário da leitura), depois RAM, CPU e temperatura. Barra inferior: Status, Apps, Ajustes. Alvos ≥ 48 px.

## Elevation & Depth
Separação por tom e borda de 1 px; sem sombras.

## Shapes
Controles 10 px, cartões 16 px.

## Components
- Cartão de métrica: valor, unidade, rótulo; "não informado" quando o sensor não existe.
- Offline: cartão inteiro em estado neutro com "indisponível" e horário da última leitura; nunca número antigo como se fosse atual.
- Encerrar app: botão de perigo com confirmação que repete o nome do app.

## Do's and Don'ts
- Não mostrar token de pareamento em nenhuma tela.
- Não animar números; atualização silenciosa com horário visível.
