import os
import sys
import mmap
import subprocess
import time
import threading

# ==============================================================================
# SISTEMA DE RECUPERAÇÃO DE FICHEIROS APAGADOS (FILE CARVING)
# Projeto: Segurança e Proteção de Dados para Sistemas de Informação (IPCA)
# ==============================================================================

TAMANHO_MAXIMO_BYTES = 50 * 1024 * 1024  

ASSINATURAS = {
    "jpg": { "inicio": b'\xff\xd8\xff', "fim": b'\xff\xd9', "tamanho_marcador_fim": 2 },
    "png": { "inicio": b'\x89PNG\r\n\x1a\n', "fim": b'IEND\xaeB`\x82', "tamanho_marcador_fim": 8 },
    "pdf": { "inicio": b'%PDF-', "fim": b'%%EOF', "tamanho_marcador_fim": 5 },
    "zip_office": { "inicio": b'PK\x03\x04', "fim": b'PK\x05\x06', "tamanho_marcador_fim": 22 },
    "mp4": { "inicio": b'ftyp', "fim": None, "tamanho_marcador_fim": 0 } 
}

def monitorizar_progresso(processo_dd, evento_conclusao):
    contador_ciclos = 0
    pos = 0
    direcao = 1
    largura = 15 
    
    while not evento_conclusao.is_set():
        trilho_antes = "=" * pos
        trilho_depois = "=" * (largura - pos)
        texto_animado = f"\r    [{trilho_antes}🚜{trilho_depois}] A copiar dados brutos da pen... "
        sys.stdout.write(texto_animado)
        sys.stdout.flush()
        
        pos += direcao
        if pos == largura or pos == 0: direcao *= -1
            
        if contador_ciclos % 50 == 0 and contador_ciclos > 0:
            if processo_dd.poll() is None:
                try: subprocess.run(["sudo", "kill", "-29", str(processo_dd.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except: pass
        
        contador_ciclos += 1
        time.sleep(0.1) 

def criar_imagem_disco(dispositivo, caminho_imagem):
    print(f"\n[*] PASSO 1: Preparar o disco (Criar Cópia Segura)")
    print(f"[-] A ler: {dispositivo}")
    
    comando = ["sudo", "dd", f"if={dispositivo}", f"of={caminho_imagem}", "bs=1m"]
    inicio_tempo = time.time()
    
    try:
        processo = subprocess.Popen(comando, stderr=subprocess.PIPE, text=True)
        evento_conclusao = threading.Event()
        threading.Thread(target=monitorizar_progresso, args=(processo, evento_conclusao), daemon=True).start()

        for linha in processo.stderr:
            if "bytes" in linha.lower():
                sys.stdout.write("\r" + " " * 70 + "\r")
                print(f"    🟢 Progresso: {linha.strip()}")

        processo.wait()
        evento_conclusao.set()
        sys.stdout.write("\r" + " " * 70 + "\r")
        sys.stdout.flush()

        if processo.returncode == 0:
            print(f"[+] Cópia concluída em {round(time.time() - inicio_tempo, 2)} segundos!")
            return True
        return False
    except KeyboardInterrupt:
        if 'evento_conclusao' in locals(): evento_conclusao.set()
        if 'processo' in locals(): processo.terminate()
        return False
    except Exception as e:
        print(f"\n[Erro na Cópia]: {e}")
        return False

def motor_recuperacao(caminho_imagem, pasta_saida):
    print(f"\n[*] PASSO 2: Motor de Recuperação e Relatório...")
    os.makedirs(pasta_saida, exist_ok=True)
    
    bytes_recuperados_total = 0
    estatisticas = {}
        
    try:
        with open(caminho_imagem, "rb") as disco:
            with mmap.mmap(disco.fileno(), length=0, access=mmap.ACCESS_READ) as disco_virtual:
                tamanho_total = len(disco_virtual)
                
                for extensao, marcadores in ASSINATURAS.items():
                    print(f"[-] A procurar .{extensao.upper()}...")
                    subpasta = os.path.join(pasta_saida, extensao.upper())
                    os.makedirs(subpasta, exist_ok=True)
                    
                    cursor = 0
                    recuperados = 0
                    
                    while True:
                        inicio_idx = disco_virtual.find(marcadores["inicio"], cursor)
                        if inicio_idx == -1: break 
                            
                        if marcadores["inicio"] == b'ftyp': inicio_idx = max(0, inicio_idx - 4)
                            
                        if marcadores["fim"] is None:
                            fim_idx = min(inicio_idx + TAMANHO_MAXIMO_BYTES, len(disco_virtual))
                        else:
                            fim_idx = disco_virtual.find(marcadores["fim"], inicio_idx)
                        
                        if fim_idx == -1:
                            cursor = inicio_idx + len(marcadores["inicio"]); continue
                            
                        if marcadores["fim"] is not None: fim_idx += marcadores["tamanho_marcador_fim"]
                            
                        tamanho_ficheiro = fim_idx - inicio_idx
                        if tamanho_ficheiro > TAMANHO_MAXIMO_BYTES:
                            cursor = inicio_idx + len(marcadores["inicio"]); continue
                            
                        nome_ficheiro = os.path.join(subpasta, f"recuperado_{recuperados}.{extensao}")
                        with open(nome_ficheiro, "wb") as f_saida:
                            f_saida.write(disco_virtual[inicio_idx:fim_idx])
                            
                        bytes_recuperados_total += tamanho_ficheiro
                        recuperados += 1
                        cursor = fim_idx 
                        
                    estatisticas[extensao] = recuperados
                    print(f"    -> {recuperados} guardados na pasta '{extensao.upper()}'.")
                
                # Gerar o Resumo de Dados Órfãos
                bytes_orfaos = max(0, tamanho_total - bytes_recuperados_total)
                mb_total = tamanho_total / (1024 * 1024)
                mb_recup = bytes_recuperados_total / (1024 * 1024)
                mb_orfaos = bytes_orfaos / (1024 * 1024)
                
                # Criar o ficheiro de relatório
                caminho_relatorio = os.path.join(pasta_saida, "Relatorio_Recuperacao.txt")
                with open(caminho_relatorio, "w", encoding="utf-8") as relatorio:
                    relatorio.write("=========================================\n")
                    relatorio.write("   RELATÓRIO DE RECUPERAÇÃO DE DADOS\n")
                    relatorio.write("=========================================\n\n")
                    relatorio.write(f"Tamanho total da imagem analisada: {mb_total:.2f} MB\n")
                    relatorio.write(f"Dados úteis reconhecidos e extraídos: {mb_recup:.2f} MB\n")
                    relatorio.write(f"DADOS ÓRFÃOS (Espaço vazio ou não reconhecido): {mb_orfaos:.2f} MB\n\n")
                    relatorio.write("Ficheiros recuperados por formato:\n")
                    for ext, qtd in estatisticas.items():
                        relatorio.write(f" - {ext.upper()}: {qtd} ficheiros\n")

                # Mostrar no terminal
                print(f"\n📊 RESUMO ESTATÍSTICO:")
                print(f"   🔹 Analisado: {mb_total:.2f} MB")
                print(f"   🔹 Recuperado: {mb_recup:.2f} MB")
                print(f"   🔸 Dados Órfãos: {mb_orfaos:.2f} MB")
                print(f"   📝 Foi criado um 'Relatorio_Recuperacao.txt' na pasta de resultados.")

    except Exception as e: print(f"[Erro Crítico]: {e}")

if __name__ == "__main__":
    print("=====================================================")
    print("      FERRAMENTA DE RECUPERAÇÃO DE DADOS APAGADOS    ")
    print("=====================================================")
    dispositivo_alvo = input("\n👉 Escreva o identificador da pen: ").strip()
    
    nome_imagem = "copia_temporaria.img"
    caminho_imagem_temp = os.path.join(os.path.dirname(os.path.abspath(__file__)), nome_imagem)
    destino_escolhido = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados_recuperados")
    
    if dispositivo_alvo:
        sucesso_clone = criar_imagem_disco(dispositivo_alvo, caminho_imagem_temp)
        if sucesso_clone: motor_recuperacao(caminho_imagem_temp, destino_escolhido)
    else: print("[!] Erro: Nenhum dispositivo introduzido.")
