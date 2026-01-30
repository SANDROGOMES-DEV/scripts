import os
import shutil
from pathlib import Path
from datetime import datetime

def executar_manutencao():
    print("--- INICIANDO AUTOMACAO HIBRIDA ---")
    
    # Define o caminho da pasta Downloads de forma absoluta
    path = Path.home() / "Downloads"
    
    if not path.exists():
        print(f"[!] Erro: A unidade ou caminho {path} nao existe.")
        return

    # Mapeamento de pastas
    organizacao = {
        "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
        "Imagens": [".jpg", ".png", ".gif", ".webp"],
        "Videos": [".mp4", ".mkv"],
        "Instaladores": [".exe", ".msi"]
    }

    contagem = 0

    # Itera sobre os arquivos usando Path (mais seguro que os.listdir)
    for item in path.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            
            for pasta, extensoes in organizacao.items():
                if ext in extensoes:
                    pasta_alvo = path / pasta
                    pasta_alvo.mkdir(exist_ok=True)
                    
                    try:
                        shutil.move(str(item), str(pasta_alvo / item.name))
                        print(f"[v] {item.name} -> {pasta}")
                        contagem += 1
                    except Exception as e:
                        print(f"[!] Erro ao mover {item.name}: {e}")

    print(f"\nSucesso: {contagem} arquivos organizados.")

if __name__ == "__main__":
    executar_manutencao()
