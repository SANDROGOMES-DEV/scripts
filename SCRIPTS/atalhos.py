import os
import subprocess

def abrir_ambiente_trabalho():
    # Caminhos baseados nas pastas que vi no seu computador
    caminho_base = os.path.join(os.environ['USERPROFILE'], "Desktop", "scripts")
    
    projetos = {
        "1": {"nome": "Semeadores", "path": "semeadores"},
        "2": {"nome": "Sistema AGD", "path": "sistema_AGD"},
        "3": {"nome": "Hospitalar (Java)", "path": "busca_de_prestador"}
    }

    print("--- GERENCIADOR DE PROJETOS ---")
    for k, v in projetos.items():
        print(f"[{k}] {v['nome']}")
    
    escolha = input("\nQual projeto deseja abrir? ")

    if escolha in projetos:
        pasta = os.path.join(caminho_base, projetos[escolha]['path'])
        if os.path.exists(pasta):
            os.startfile(pasta) # Abre a pasta no Explorer
            print(f"Projeto {projetos[escolha]['nome']} aberto.")
        else:
            print("[!] Pasta nao encontrada.")
    else:
        print("[!] Opcao invalida.")

if __name__ == "__main__":
    abrir_ambiente_trabalho()