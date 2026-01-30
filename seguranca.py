import hashlib
import requests
import os
import getpass
import urllib3
from cryptography.fernet import Fernet
from datetime import datetime

# Desabilita avisos de certificados SSL para evitar erros de conexão em redes restritas
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def verificar_vazamento(senha):
    """Verifica se a senha consta em bancos de dados de vazamentos públicos (HIBP)."""
    sha1hash = hashlib.sha1(senha.encode('utf-8')).hexdigest().upper()
    prefixo, sufixo = sha1hash[:5], sha1hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefixo}"
    
    try:
        # verify=False ignora erros de certificado SSL detectados anteriormente
        resposta = requests.get(url, verify=False, timeout=10) 
        if resposta.status_code != 200:
            return "[!] Erro ao consultar a base de dados da API."
        
        hashes = (line.split(':') for line in resposta.text.splitlines())
        for h, count in hashes:
            if h == sufixo:
                return f"[ALERTA] Esta senha ja vazou {count} vezes na internet! Troque-a imediatamente."
        
        return "[v] Senha segura. Nao foram encontrados vazamentos publicos registrados."
    except Exception as e:
        return f"[!] Erro de conexao: {e}"

# --- FUNÇÕES DE CRIPTOGRAFIA ---

def gerar_chave():
    """Gera uma nova chave de criptografia Fernet."""
    chave = Fernet.generate_key()
    with open("filekey.key", "wb") as filekey:
        filekey.write(chave)
    print("\n[v] Chave 'filekey.key' gerada com sucesso na pasta do script.")
    print("[!] AVISO: Guarde este arquivo em local seguro. Sem ele, os dados sao irrecuperaveis.")

def carregar_chave():
    """Tenta carregar a chave salva no diretório atual."""
    if not os.path.exists("filekey.key"):
        print("\n[!] Erro: Arquivo 'filekey.key' nao encontrado. Gere uma chave (Opcao 2) primeiro.")
        return None
    return open("filekey.key", "rb").read()

def processar_arquivo(caminho, acao):
    """Criptografa ou descriptografa um arquivo baseado na acao ('enc' ou 'dec')."""
    chave = carregar_chave()
    if not chave: return

    try:
        f = Fernet(chave)
        with open(caminho, "rb") as file:
            dados = file.read()
        
        if acao == "enc":
            resultado = f.encrypt(dados)
            msg = "criptografado"
        else:
            resultado = f.decrypt(dados)
            msg = "descriptografado"
        
        with open(caminho, "wb") as file:
            file.write(resultado)
        print(f"\n[v] Arquivo '{caminho}' {msg} com sucesso!")
        
    except Exception as e:
        print(f"\n[!] Erro durante o processo: {e}")

# --- INTERFACE DO USUÁRIO ---

def auditoria_seguranca():
    while True:
        # Limpa a tela de forma compatível com Windows/Linux
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("====================================================")
        print("         MODULO DE SEGURANCA E AUDITORIA            ")
        print("====================================================")
        print(f" Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("----------------------------------------------------")
        print("[1] Verificar Vazamento de Senha (Oculto)")
        print("[2] Gerar Nova Chave de Criptografia (.key)")
        print("[3] Criptografar um Arquivo")
        print("[4] Descriptografar um Arquivo")
        print("[5] Voltar ao Menu Principal")
        print("====================================================")
        
        escolha = input("Selecione uma opcao: ")
        
        if escolha == "1":
            # getpass impede que a senha apareça na tela enquanto você digita
            senha = getpass.getpass("\nDigite a senha para teste (os caracteres nao aparecerao): ")
            if not senha:
                print("[!] Senha vazia ignorada.")
            else:
                print("Consultando base de dados segura...")
                print(f"Resultado: {verificar_vazamento(senha)}")
            input("\nPressione Enter para continuar...")
        
        elif escolha == "2":
            confirmar = input("\nIsso pode sobrescrever chaves antigas. Continuar? (s/n): ")
            if confirmar.lower() == 's':
                gerar_chave()
            input("\nPressione Enter para continuar...")
            
        elif escolha == "3":
            arq = input("\nDigite o nome ou caminho do arquivo para CRIPTOGRAFAR: ")
            if os.path.exists(arq):
                processar_arquivo(arq, "enc")
            else:
                print("[!] Arquivo nao encontrado.")
            input("\nPressione Enter para continuar...")
            
        elif escolha == "4":
            arq = input("\nDigite o nome ou caminho do arquivo para DESCRIPTOGRAFAR: ")
            if os.path.exists(arq):
                processar_arquivo(arq, "dec")
            else:
                print("[!] Arquivo nao encontrado.")
            input("\nPressione Enter para continuar...")
            
        elif escolha == "5":
            print("Retornando ao Central Master...")
            break
        
        else:
            print("[!] Opcao invalida.")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    auditoria_seguranca()