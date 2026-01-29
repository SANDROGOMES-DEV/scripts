import os
import platform
import shutil
from datetime import datetime

def executar_manutencao():
    print("--- INICIANDO AUTOMACAO PYTHON ---")
    
    # 1. Informações do Sistema
    print(f"Sistema: {platform.system()} {platform.release()}")
    
    # 2. Automação de Arquivos: Organizar Downloads (Exemplo)
    # Move arquivos .txt e .pdf para uma pasta de 'Documentos_Organizados'
    path = os.path.expanduser("~/Downloads")
    target = os.path.join(path, "Documentos_Organizados")
    
    if not os.path.exists(target):
        os.makedirs(target)
        
    contagem = 0
    for arquivo in os.listdir(path):
        if arquivo.endswith((".pdf", ".txt", ".docx")):
            shutil.move(os.path.join(path, arquivo), os.path.join(target, arquivo))
            contagem += 1
            
    # 3. Gerar Log de Execução
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("log_automacao.txt", "a") as log:
        log.write(f"Executado em {data_atual} - Arquivos organizados: {contagem}\n")
    
    print(f"Sucesso! {contagem} arquivos foram organizados.")
    print(f"Log atualizado em: {os.getcwd()}/log_automacao.txt")

if __name__ == "__main__":
    executar_manutencao()