# Recuperador de Ficheiros (File Carving)

Este é um projeto prático desenvolvido para a unidade curricular de Segurança e Proteção de Dados para Sistemas de Informação (IPCA).

É um script simples em Python que serve para recuperar ficheiros apagados ou perdidos de pens e discos. Em vez de depender do que o sistema operativo vê, o programa faz a leitura física do dispositivo à procura de assinaturas de ficheiros (magic numbers) e extrai os dados em bruto.

O código foi pensado para não alterar a prova: ele cria sempre um clone (imagem) da pen original primeiro, e só depois é que vasculha esse clone. Assim não há risco de corromper o disco original.

## Como testar

Vão precisar de ter o Python 3 instalado e de correr isto com permissões de administrador para conseguir ler o hardware a baixo nível.

### 🍎 Se usarem macOS
1. Abram o Terminal e corram `diskutil list` para ver qual é o identificador da pen (ex: `/dev/rdisk4`).
2. Corram o script: `python3 recuperador.py`
3. Quando pedir o alvo, escrevam o identificador e metam a password do Mac para autorizar a clonagem.

### 🪟 Se usarem Windows
1. Abram a Linha de Comandos (cmd) **como Administrador**.
2. Corram `wmic diskdrive list brief` para ver o nome da pen (ex: `\\.\PHYSICALDRIVE1`).
3. Corram o script: `python recuperador_win.py` e insiram o identificador quando pedir.

## Onde vão parar os ficheiros?
Quando o processo terminar, vão aparecer duas coisas na pasta do script:
- Uma pasta `dados_recuperados` com as imagens, documentos e vídeos arrumados por subpastas.
- Um ficheiro `copia_temporaria.img`. Este é o clone gigante da pen. Quando confirmarem que os ficheiros estão recuperados, podem mandar o `.img` para o lixo para libertar espaço.

**Nota:** Como a extração de vídeos (MP4) é feita às cegas, os ficheiros podem ficar com algum lixo binário colado no fim. Se o leitor normal não conseguir abrir, o VLC safa isso sem problemas.
