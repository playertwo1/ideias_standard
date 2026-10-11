# PROJECT — Command

## Problema
Para saber se o PC de casa está ligado, sobrecarregado ou travado, hoje é preciso ir até ele ou abrir acesso remoto completo, que é pesado e arriscado.

## Para quem
Uma pessoa com um PC Windows e um celular Android na mesma rede (depois, via VPN própria).

## MVP — até três fluxos
1. Parear o celular com o PC de forma autenticada.
2. Ver RAM, CPU, temperatura e online/offline em poucos segundos.
3. Abrir ou encerrar um app da allowlist, com confirmação.

## Fora do MVP
- Orquestração de agentes de IA, multi-PC, transferência de arquivos, monitoramento contínuo pesado.

## Restrições
- Plataforma: Windows 11 + Android 12+.
- Dados sensíveis: token de pareamento fica no cofre do sistema; nenhuma telemetria sai da rede local.
- Sem custo recorrente; bibliotecas com licença permissiva.

## Como saberemos que funcionou
Do celular, ver o status real do PC em menos de 3 s e encerrar um app travado sem levantar da cadeira.

## Autoridade de produto
O dono do projeto aprova escopo e fecha marcos.

## Alternativas consideradas
Acesso remoto completo (pesado e expõe a máquina); apps de monitoramento na nuvem (enviam dados para terceiros).
