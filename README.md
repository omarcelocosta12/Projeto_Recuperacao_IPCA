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
