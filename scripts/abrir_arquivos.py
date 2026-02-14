import os
from pathlib import Path

def abrir_recursos_locais():
    # Detecta a pasta onde este script .py esta salvo
    base_path = Path(__file__).parent
    
    recursos = {
        "1": {"nome": "Busca de Prestador", "path": base_path / "busca_de_prestador" / "index.html"},
        "2": {"nome": "Bloco de Notas", "path": base_path / "notas.txt"},
        "3": {"nome": "Pasta Semeadores", "path": base_path / "semeadores"}
    }

    print("=== EXPLORADOR DE PROJETOS LOCAL ===")
    for k, v in recursos.items():
        print(f"[{k}] {v['nome']}")
    
    escolha = input("\nSelecione: ")

    if escolha in recursos:
        alvo = recursos[escolha]['path']
        if alvo.exists():
            os.startfile(alvo)
            print(f"[v] Abrindo {recursos[escolha]['nome']}...")
        else:
            print(f"[!] Erro: {alvo} nao encontrado nesta pasta.")
    else:
        print("[!] Opcao invalida.")

if __name__ == "__main__":
    abrir_recursos_locais()