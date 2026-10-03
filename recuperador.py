import os
import mmap

# ==============================================================================
# MOTOR FORENSE DE FILE CARVING (Recuperação de Dados em Modo Read-Only)
# Projeto: Segurança e Proteção de Dados para Sistemas de Informação (IPCA)
# ==============================================================================

# Limite de segurança: 50 MB por ficheiro. 
# Previne o esgotamento de disco em caso de ficheiros corrompidos ou falsos positivos.
TAMANHO_MAXIMO_BYTES = 50 * 1024 * 1024  

# Dicionário de Magic Numbers (Assinaturas Hexadecimais)
ASSINATURAS = {
    "jpg": { 
        "inicio": b'\xff\xd8\xff', 
        "fim": b'\xff\xd9',
        "tamanho_marcador_fim": 2
    },
    "png": { 
        "inicio": b'\x89PNG\r\n\x1a\n', 
        "fim": b'IEND\xaeB`\x82',
        "tamanho_marcador_fim": 8
    },
    "pdf": { 
        "inicio": b'%PDF-', 
        "fim": b'%%EOF',
        "tamanho_marcador_fim": 5
    },
    # Documentos Word (.docx), Excel (.xlsx) e PowerPoint (.pptx) usam a estrutura ZIP
    "zip_office": { 
        "inicio": b'PK\x03\x04', 
        "fim": b'PK\x05\x06',
        "tamanho_marcador_fim": 22 # O marcador End of Central Directory tem 22 bytes no total
    }
}

def motor_file_carving(caminho_imagem, pasta_saida):
    """
    Analisa uma imagem de disco bit a bit e extrai ficheiros com base nas suas assinaturas.
    """
    print(f"\n[*] A iniciar o motor forense de File Carving...")
    print(f"[*] Alvo: {caminho_imagem}\n")
    
    os.makedirs(pasta_saida, exist_ok=True)
        
    try:
        # Abertura em modo binário estrito
        with open(caminho_imagem, "rb") as disco:
            
            # Mapeamento de memória (mmap) para não sobrecarregar a RAM (Access Read = Read Only)
            with mmap.mmap(disco.fileno(), length=0, access=mmap.ACCESS_READ) as disco_virtual:
                
                for extensao, marcadores in ASSINATURAS.items():
                    print(f"[-] A procurar ficheiros do tipo .{extensao.upper()}...")
                    
                    cursor = 0
                    recuperados = 0
                    
                    while True:
                        # 1. Procurar o byte de início
                        inicio_idx = disco_virtual.find(marcadores["inicio"], cursor)
                        if inicio_idx == -1:
                            break # Fim da procura para este formato
                            
                        # 2. Procurar o byte de fim
                        fim_idx = disco_virtual.find(marcadores["fim"], inicio_idx)
                        
                        # Validações Forenses de Segurança
                        if fim_idx == -1:
                            # Ficheiro incompleto, avançar o cursor para evitar loops
                            cursor = inicio_idx + len(marcadores["inicio"])
                            continue
                            
                        # Ajustar o fim para incluir os próprios bytes do marcador de encerramento
                        fim_idx += marcadores["tamanho_marcador_fim"]
                        tamanho_ficheiro = fim_idx - inicio_idx
                        
                        if tamanho_ficheiro > TAMANHO_MAXIMO_BYTES:
                            # Ignorar extrações gigantes (provável lixo binário)
                            cursor = inicio_idx + len(marcadores["inicio"])
                            continue
                            
                        # 3. Extração e gravação segura do ficheiro
                        nome_ficheiro = os.path.join(pasta_saida, f"recuperado_{recuperados}.{extensao}")
                        with open(nome_ficheiro, "wb") as f_saida:
                            f_saida.write(disco_virtual[inicio_idx:fim_idx])
                            
                        recuperados += 1
                        cursor = fim_idx # Mover o cursor para a frente para a próxima procura
                        
                    print(f"    -> {recuperados} ficheiro(s) recuperado(s).")

    except FileNotFoundError:
        print(f"[Erro] O ficheiro/disco '{caminho_imagem}' não foi encontrado.")
    except PermissionError:
        print("[Erro] Permissões insuficientes. Se estiver a ler um disco físico, use 'sudo'.")
    except Exception as e:
        print(f"[Erro Crítico] Ocorreu uma falha inesperada: {e}")

# ==============================================================================
# PONTO DE ENTRADA DO PROGRAMA (MODO INTERATIVO)
# ==============================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("    SISTEMA DE RECUPERAÇÃO DE DADOS (FILE CARVING)   ")
    print("=====================================================")
    
    # O programa agora pergunta qual é o alvo e onde guardar!
    alvo_escolhido = input("\n👉 Arraste o ficheiro de imagem (.img) para aqui ou escreva o caminho: ").strip()
    
    # Remove aspas caso o utilizador arraste o ficheiro no Mac
    alvo_escolhido = alvo_escolhido.replace("'", "").replace('"', "")
    
    destino_escolhido = "./dados_recuperados"
    
    if alvo_escolhido:
        motor_file_carving(alvo_escolhido, destino_escolhido)
        print("\n[*] Processo concluído.")
    else:
        print("[!] Erro: Não introduziu nenhum caminho.")