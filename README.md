Esta ferramenta recupera ficheiros apagados de pens e discos,
criando primeiro uma copia fisica segura.

REQUISITOS:

Computador: Mac (macOS)

Password de administrador do Mac

PASSO A PASSO (Apenas 3 comandos)

LIGUE A PEN E DESCUBRA O SEU NOME
Abra o Terminal do Mac e escreva o comando abaixo, seguido de Enter:

diskutil list

(Vai aparecer uma lista. Procure a sua pen pelo tamanho e anote o
identificador na coluna da direita. Exemplo: /dev/rdisk4)

INICIE O PROGRAMA
No terminal, va para a pasta onde guardou o script 'recuperador.py'
e escreva o comando abaixo, seguido de Enter:

python3 recuperador.py

AUTORIZE A RECUPERACAO
O programa vai pedir o nome da pen. Escreva o identificador que anotou no Passo 1:

Exemplo: /dev/rdisk4

O terminal vai pedir a password do seu Mac. Escreva a password
(nao vao aparecer letras no ecra, e normal) e prima Enter.

O QUE ACONTECE DEPOIS?
O programa vai trabalhar sozinho. Quando terminar, va a pasta onde
guardou o script. Vai encontrar la:

Uma pasta chamada 'dados_recuperados' (com as suas fotos e documentos).

Um ficheiro chamado 'copia_temporaria.img' (o clone da pen. Pode
apagar este ficheiro quando ja tiver confirmado que recuperou tudo).





GUIA DE UTILIZACAO - RECUPERADOR DE FICHEIROS (WINDOWS)
=======================================================

Esta ferramenta recupera ficheiros apagados de pens e discos, 
criando primeiro uma copia fisica segura.

REQUISITOS:
- Computador: Windows 10 ou 11
- O terminal tem de ser aberto como Administrador.

---

PASSO A PASSO (Apenas 3 comandos)

1. LIGUE A PEN E DESCUBRA O SEU NOME
No menu Iniciar do Windows, procure por "cmd".
Clique com o botao direito em "Linha de Comandos" e escolha 
"Executar como Administrador".

Na janela preta que abrir, escreva o seguinte comando e prima Enter:

wmic diskdrive list brief

(Vai aparecer uma tabela com os seus discos. Procure a sua pen pelo
tamanho e anote o nome exato na coluna 'DeviceID'. 
Exemplo: \\.\PHYSICALDRIVE1)


2. INICIE O PROGRAMA
No mesmo terminal, navegue ate a pasta onde guardou o script 
'recuperador_win.py' (usando o comando 'cd', ex: cd Desktop\Projeto) 
e escreva:

python recuperador_win.py


3. AUTORIZE A RECUPERACAO
O programa vai pedir o nome da pen. Escreva o identificador exato 
que anotou no Passo 1 (com as barras todas):

Exemplo: \\.\PHYSICALDRIVE1

Prima Enter e deixe o programa trabalhar.

---

O QUE ACONTECE DEPOIS?
Quando o programa terminar, va a pasta onde guardou o script. 
Vai encontrar la:

- Uma pasta chamada 'dados_recuperados' (com as suas fotos e documentos).
- Um ficheiro chamado 'copia_temporaria.img' (o clone da pen. Pode 
  apagar este ficheiro quando ja tiver confirmado que recuperou tudo).
