import os
import mmap
import subprocess
import time

# ==============================================================================
# MOTOR FORENSE DE FILE CARVING (Recuperação de Dados em Modo Read-Only)
# Projeto: Segurança e Proteção de Dados para Sistemas de Informação (IPCA)
# ==============================================================================

TAMANHO_MAXIMO_BYTES = 50 * 1024 * 1024  

ASSINATURAS = {
    "jpg": { "inicio": b'\xff\xd8\xff', "fim": b'\xff\xd9', "tamanho_marcador_fim": 2 },
    "png": { "inicio": b'\x89PNG\r\n\x1a\n', "fim": b'IEND\xaeB`\x82', "tamanho_marcador_fim": 8 },
    "pdf": { "inicio": b'%PDF-', "fim": b'%%EOF', "tamanho_marcador_fim": 5 },
    "zip_office": { "inicio": b'PK\x03\x04', "fim": b'PK\x05\x06', "tamanho_marcador_fim": 22 },
    "mp4": { "inicio": b'ftyp', "fim": None, "tamanho_marcador_fim": 0 } # Suporte a Blind Carving
}

def criar_imagem_forense(dispositivo, caminho_imagem):
    """
    Usa o comando 'dd' do macOS para clonar o disco antes da análise.
    """
    print(f"\n[*] FASE 1: Aquisição de Prova (Criar Clone)")
    print(f"[-] A ler o dispositivo: {dispositivo}")
    print(f"[-] A criar imagem forense em: {caminho_imagem}")
    print(f"    (Isto pode demorar alguns minutos. Por favor, aguarde...)")
    
    # O Python chama o terminal para executar o comando 'dd'
    comando = f"sudo dd if={dispositivo} of={caminho_imagem} bs=1m"
    
    inicio_tempo = time.time()
    
    try:
        # Pede a password do sistema (sudo) se necessário
        processo = subprocess.run(comando, shell=True, check=True, text=True, stderr=subprocess.PIPE)
        
        tempo_total = round(time.time() - inicio_tempo, 2)
        print(f"\n[+] Aquisição concluída com sucesso em {tempo_total} segundos!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n[Erro] Falha ao criar a imagem do disco.")
        print(f"Detalhes do sistema: {e.stderr}")
        return False

def motor_file_carving(caminho_imagem, pasta_saida):
    """
    Analisa uma imagem de disco bit a bit e extrai ficheiros com base nas suas assinaturas.
    """
    print(f"\n[*] FASE 2: Motor Forense de File Carving...")
    print(f"[*] Alvo: {caminho_imagem}\n")
    
    os.makedirs(pasta_saida, exist_ok=True)
        
    try:
        with open(caminho_imagem, "rb") as disco:
            with mmap.mmap(disco.fileno(), length=0, access=mmap.ACCESS_READ) as disco_virtual:
                
                for extensao, marcadores in ASSINATURAS.items():
                    print(f"[-] A procurar ficheiros do tipo .{extensao.upper()}...")
                    
                    cursor = 0
                    recuperados = 0
                    
                    while True:
                        inicio_idx = disco_virtual.find(marcadores["inicio"], cursor)
                        if inicio_idx == -1:
                            break 
                            
                        if marcadores["inicio"] == b'ftyp':
                            inicio_idx = max(0, inicio_idx - 4)
                            
                        if marcadores["fim"] is None:
                            fim_idx = min(inicio_idx + TAMANHO_MAXIMO_BYTES, len(disco_virtual))
                        else:
                            fim_idx = disco_virtual.find(marcadores["fim"], inicio_idx)
                        
                        if fim_idx == -1:
                            cursor = inicio_idx + len(marcadores["inicio"])
                            continue
                            
                        if marcadores["fim"] is not None:
                            fim_idx += marcadores["tamanho_marcador_fim"]
                            
                        tamanho_ficheiro = fim_idx - inicio_idx
                        if tamanho_ficheiro > TAMANHO_MAXIMO_BYTES:
                            cursor = inicio_idx + len(marcadores["inicio"])
                            continue
                            
                        nome_ficheiro = os.path.join(pasta_saida, f"recuperado_{recuperados}.{extensao}")
                        with open(nome_ficheiro, "wb") as f_saida:
                            f_saida.write(disco_virtual[inicio_idx:fim_idx])
                            
                        recuperados += 1
                        
                        if marcadores["fim"] is None:
                            cursor = fim_idx
                        else:
                            cursor = fim_idx 
                        
                    print(f"    -> {recuperados} ficheiro(s) recuperado(s).")

    except FileNotFoundError:
        print(f"[Erro] A imagem '{caminho_imagem}' não foi encontrada.")
    except Exception as e:
        print(f"[Erro Crítico] Ocorreu uma falha inesperada: {e}")

# ==============================================================================
# PONTO DE ENTRADA DO PROGRAMA (MODO INTERATIVO)
# ==============================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("    SISTEMA DE RECUPERAÇÃO DE DADOS (FILE CARVING)   ")
    print("=====================================================")
    
    print("\n[ DICA ] Para saber o identificador da pen, abra outro terminal e digite 'diskutil list'.")
    print("         Exemplo de dispositivo no Mac: /dev/rdisk4")
    
    dispositivo_alvo = input("\n👉 Escreva o identificador do disco/pen que quer clonar e recuperar: ").strip()
    
    # O programa cria o clone (.img) na mesma pasta onde o código está
    nome_imagem = "prova_forense_temp.img"
    caminho_imagem_temp = os.path.join(os.path.dirname(os.path.abspath(__file__)), nome_imagem)
    destino_escolhido = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados_recuperados")
    
    if dispositivo_alvo:
        print("\n[Aviso] Vai ser pedida a password do seu Mac para permitir a leitura física da pen.")
        
        # 1. Tentar criar o clone primeiro
        sucesso_clone = criar_imagem_forense(dispositivo_alvo, caminho_imagem_temp)
        
        # 2. Se o clone for criado com sucesso, inicia a extração
        if sucesso_clone:
            motor_file_carving(caminho_imagem_temp, destino_escolhido)
            print("\n[*] Processo completo concluído.")
        else:
            print("\n[!] A análise não prosseguiu porque falhou a criação da imagem do disco.")
    else:
        print("[!] Erro: Não introduziu nenhum identificador válido.")
