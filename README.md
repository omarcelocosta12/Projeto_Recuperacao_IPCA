# 🛠️ Recuperador de Ficheiros (File Carving)

Projeto desenvolvido no âmbito da unidade curricular de **Segurança e Proteção de Dados para Sistemas de Informação** no Instituto Politécnico do Cávado e do Ave (IPCA).

Uma ferramenta de recuperação de dados em bruto (File Carving) desenhada para macOS. Todo o motor de extração, clonagem de segurança e interface gráfica de terminal estão **consolidados num único ficheiro Python**, tornando a ferramenta portátil e fácil de auditar.

## 🚀 Como Funciona

Em vez de depender do sistema operativo (que pode classificar uma pen como "ilegível"), este script lê a superfície física do disco à procura das assinaturas originais dos ficheiros (como JPG, PDF e MP4) e resgata-os de forma autónoma.

*   **Arquitetura *Standalone*:** Todo o código (clonagem, leitura de memória `mmap` e animações) vive no ficheiro `recuperador.py`.
*   **Cópia de Segurança Obrigatória:** Para garantir a integridade do dispositivo original, o script invoca o comando `dd` do macOS para criar um clone físico provisório antes de iniciar a extração.
*   **Feedback Visual:** Utiliza sinais de sistema (`SIGINFO`) integrados numa *Thread* paralela para animar o progresso no terminal em tempo real.

## ⚙️ Requisitos
*   **Sistema Operativo:** macOS
*   **Ambiente:** Python 3 (sem necessidade de bibliotecas externas)
*   **Permissões:** Privilégios de Administrador (para autorizar a leitura a baixo nível do dispositivo).

## 💻 Guia de Utilização Rápida

**1. Descobrir o identificador do seu disco**
Ligue a pen ou disco ao Mac. Abra o Terminal e escreva:
```bash
diskutil list


(Anote o identificador, por exemplo: /dev/rdisk4)

2. Executar a Ferramenta
Navegue até à pasta onde guardou o script único e execute:

Bash
python3 recuperador.py
3. Iniciar a Extração
O programa pedirá o identificador do disco.

Plaintext
👉 Escreva o identificador da pen: /dev/rdisk4
A partir daqui, introduza a password do Mac (quando solicitada) e o processo decorre de forma totalmente automática.

📁 Resultados da Recuperação
No final do processo, tudo fica organizado na mesma pasta onde está o seu script:

Pasta /dados_recuperados/: Contém todos os ficheiros resgatados (fotografias, documentos, vídeos).

Ficheiro copia_temporaria.img: O clone físico do seu disco. Pode (e deve) apagar este ficheiro grandalhão assim que confirmar que os seus dados foram recuperados com sucesso.

Nota sobre Vídeos (MP4): Devido à técnica de extração cega, os vídeos recuperados terão um tamanho fixo (ex: 50MB). Recomenda-se a visualização dos mesmos com o VLC Media Player.
