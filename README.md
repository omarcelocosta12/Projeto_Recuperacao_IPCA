Markdown
# 🛠️ Guia de Utilização - Recuperador de Ficheiros

Esta ferramenta recupera ficheiros apagados de pens e discos, criando primeiro uma cópia física segura. Abaixo encontra as instruções detalhadas para sistemas macOS e Windows.

---

## 🍎 Utilização no macOS

### 📋 Requisitos
* **Sistema Operativo:** macOS
* **Permissões:** Password de administrador do Mac

### 🚀 Passo a Passo (Apenas 3 comandos)

**1. Ligue a pen e descubra o seu nome**  
Abra o **Terminal** do Mac e escreva o comando abaixo, seguido de `Enter`:
```bash
diskutil list
(Vai aparecer uma lista. Procure a sua pen pelo tamanho e anote o identificador na coluna da direita. Exemplo: /dev/rdisk4)

2. Inicie o programa

No terminal, vá para a pasta onde guardou o script recuperador.py e escreva o comando abaixo, seguido de Enter:

Bash
python3 recuperador.py
3. Autorize a recuperação

O programa vai pedir o nome da pen. Escreva o identificador que anotou no Passo 1:

Plaintext
👉 Escreva o identificador da pen: /dev/rdisk4
O terminal vai pedir a password do seu Mac. Escreva a password (não vão aparecer letras no ecrã, é uma medida de segurança normal) e prima Enter.

🪟 Utilização no Windows
📋 Requisitos
Sistema Operativo: Windows 10 ou 11

Permissões: A Linha de Comandos (CMD) tem de ser aberta como Administrador

🚀 Passo a Passo (Apenas 3 comandos)
1. Ligue a pen e descubra o seu nome

No menu Iniciar do Windows, procure por cmd. Clique com o botão direito em "Linha de Comandos" e escolha Executar como Administrador. Na janela que abrir, escreva o seguinte comando e prima Enter:

DOS
wmic diskdrive list brief
(Vai aparecer uma tabela com os seus discos. Procure a sua pen pelo tamanho e anote o nome exato na coluna 'DeviceID'. Exemplo: \\.\PHYSICALDRIVE1)

2. Inicie o programa

No mesmo terminal, navegue até à pasta onde guardou o script recuperador_win.py (usando o comando cd, ex: cd Desktop\Projeto) e escreva:

DOS
python recuperador_win.py
3. Autorize a recuperação

O programa vai pedir o nome da pen. Escreva o identificador exato que anotou no Passo 1 (incluindo todas as barras):

Plaintext
👉 Escreva o identificador da pen: \\.\PHYSICALDRIVE1
Prima Enter e deixe o programa trabalhar.

📁 O que acontece depois?
O programa vai trabalhar sozinho e apresentar o progresso no ecrã. Quando terminar, vá à pasta onde guardou o script. Vai encontrar lá:

📂 Uma pasta chamada dados_recuperados: Contém as suas fotos e documentos.

💿 Um ficheiro chamado copia_temporaria.img: Este é o clone físico da pen gerado para a extração segura. Pode (e deve) apagar este ficheiro quando já tiver confirmado que recuperou tudo o que precisava.
