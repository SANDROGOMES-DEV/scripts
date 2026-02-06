@echo off
setlocal enabledelayedexpansion
:menu
cls
title Central Master V2.0 - Windows e Android
color 0E

echo ========================================================
echo             SISTEMA DE AUTOMACAO MULTIPLATAFORMA
echo ========================================================
echo [1] LINKS      [2] OTIMIZAR PC    [3] REDE
echo [4] SISTEMA    [5] PYTHON HIBRIDO [6] ANDROID (ADB)
echo [7] SAIR
echo [8] SEGURANCA  - Auditoria de Senhas
echo [9] PROGRAMAS  - Acesso Rapido a Ferramentas
echo [10] RECURSOS  - Acesso a Arquivos e Pastas

echo ========================================================
set /p escolha=Selecione uma opcao: 

if "%escolha%"=="1" goto classe_links
if "%escolha%"=="2" goto classe_otimizar
if "%escolha%"=="3" goto classe_rede
if "%escolha%"=="4" goto classe_sistema
if "%escolha%"=="5" goto classe_hibrida
if "%escolha%"=="6" goto classe_android
if "%escolha%"=="7" exit
if "%escolha%"=="8" goto classe_seguranca
if "%escolha%"=="9" goto classe_programas
if "%escolha%"=="10" goto classe_recursos
goto menu
:: --- CLASSE 1: LINKS ---
:classe_links
cls
echo Abrindo ferramentas de trabalho e estudo...
start chrome "https://portalwfm.hapvida.com.br/sisqualIdentityServer/core/login?signin=ef11be1cd5fb328f715cf7a9bc18f826" "https://hapvidandi.beedoo.io/feed" "https://th3exe.github.io/bat-system/busca.html" "https://teams.microsoft.com/v2/" "https://docs.google.com/document/d/1z3eFgQkzXhO8INNo6mkiN2CO8_LAu9h1CYLuQoV0USc/edit?tab=t.0" "https://github.com" "https://www.w3schools.com/python/" 
echo.
echo Abas abertas com sucesso!
timeout /t 3 >nul
goto menu

:: --- CLASSE 2: OTIMIZAR ---
:classe_otimizar
cls
echo [OTIMIZACAO] Iniciando limpeza de arquivos temporarios...
del /q /f /s "%temp%\*.*" >nul 2>&1
del /q /f /s "C:\Windows\Temp\*.*" >nul 2>&1
echo [OTIMIZACAO] Limpando cache do Chrome...
del /q /f /s "%LocalAppData%\Google\Chrome\User Data\Default\Cache\*.*" >nul 2>&1
echo Concluido! O sistema esta mais leve.
pause
goto menu

:: --- CLASSE 3: REDE ---
:classe_rede
cls
echo [REDE] Resetando configuracoes de internet...
ipconfig /flushdns >nul
ipconfig /release >nul
ipconfig /renew >nul
netsh winsock reset >nul
echo Concluido! Sua conexao foi renovada.
pause
goto menu

:: --- CLASSE 4: SISTEMA ---
:classe_sistema
cls
echo [SISTEMA] Iniciando Verificador de Arquivos (SFC)...
echo Nota: Isso pode exigir privilegios de Administrador.
sfc /scannow
pause
goto menu

:: --- CLASSE 5: HIBRIDA (Abaixo explicada em detalhes) ---
:classe_hibrida
cls
echo [HIBRIDO] Verificando ambiente...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Erro: Python nao instalado ou nao adicionado ao PATH.
    echo Tentando abrir via navegador para instalacao...
    start chrome "https://www.python.org/downloads/"
    pause
    goto menu
) else (
    echo [v] Python detectado! 
    echo [v] Executando 'automacao.py'...
    echo ----------------------------------------------------
    python automacao.py
    echo ----------------------------------------------------
    pause
    goto menu
)
:: --- CLASSE 6: ANDROID (NOVO) ---
:classe_android
cls
echo [ANDROID] Verificando conexão via ADB...
adb devices
echo.
echo 1. Limpar Cache de Apps (Trim Caches)
echo 2. Desativar Bloatware (Apps Desnecessários)
echo 3. Reiniciar Celular
echo 4. Voltar ao Menu
echo.
set /p op_android=Escolha uma acao: 

if "%op_android%"=="1" (
    echo [v] Solicitando limpeza de cache...
    adb shell pm trim-caches 999G
    pause
    goto classe_android
)
if "%op_android%"=="2" (
    echo [!] Digite o nome do pacote do app (ex: com.facebook.katana):
    set /p pacote=Pacote: 
    adb shell pm disable-user --user 0 !pacote!
    pause
    goto classe_android
)
if "%op_android%"=="3" (
    echo [!] Reiniciando...
    adb reboot
    pause
    goto menu
)


:: No final do arquivo, adicione a Classe:
:classe_seguranca
cls
:: Define o caminho absoluto baseado na localização do arquivo .bat
pushd "%~dp0"
echo [SEGURANCA] Local: %cd%
echo [SEGURANCA] Verificando ambiente Python...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Instale o Python para usar este modulo.
    popd
    pause
    goto menu
) else (
    echo [v] Preparando bibliotecas...
    python -m pip install requests cryptography >nul 2>&1
    python seguranca.py
    popd
    pause
    goto menu
)

if "%op_android%"=="4" goto menu
goto classe_android

:: ... (mantenha aqui as outras classes de links, otimização, etc.)

:: --- CLASSE 09: PROGRAMAS E PROJETOS ---
:classe_programas
cls
echo ==========================================
echo       ABERTURA RAPIDA DE AMBIENTE
echo ==========================================
echo [1] Abrir VS Code (Projetos Python)
echo [2] Abrir Pasta de Scripts (Area de Trabalho)
echo [3] Abrir Painel de Controle / Teclado Virtual
echo [4] Abrir Calculadora
echo [5] Voltar
echo ==========================================
set /p prog=Escolha: 

if "%prog%"=="1" (
    :: Inicia o VS Code se estiver no PATH
    start code .
    goto classe_programas
)
if "%prog%"=="2" (
    :: Abre a pasta específica onde seus scripts residem
    start explorer "%~dp0"
    goto classe_programas
)
if "%prog%"=="3" (
    :: Útil para automação: Teclado virtual e Painel
    start osk
    start control
    goto classe_programas
)
if "%prog%"=="4" start calc & goto classe_programas
if "%prog%"=="5" goto menu
goto classe_programas

:: --- CLASSE 10: RECURSOS UNIVERSAIS ---
:classe_recursos
cls
:: Garante que o script entre na pasta correta antes de chamar o Python
pushd "%~dp0"
echo ===================================================
echo           RECURSOS EM QUALQUER MAQUINA
echo ===================================================
echo [1] Abrir Busca de Prestador (Navegador)
echo [2] Abrir Bloco de Notas (Notas.txt)
echo [3] Abrir Pasta do Projeto Semeadores
echo [4] Executar via Python (Caminhos Inteligentes)
echo [5] Voltar
echo ===================================================
set /p r=Escolha: 

if "%r%"=="1" (
    start "" "C:\Users\alexssandro.gomes\Documents\SANDRO\BASE_DE_DADOS\BUSCA_DE_PRESTADORES-main\inicio.html"
    goto classe_recursos
)
if "%r%"=="2" (
    :: Tenta abrir o notas.txt na mesma pasta do script
    start ""  "C:\Users\alexssandro.gomes\Documents\SANDRO\BASE_DE_DADOS\procedimentos.txt"
    )
    goto classe_recursos

if "%r%"=="3" (
    if exist "semeadores" (
        start explorer "semeadores"
    ) else (
        echo [!] Pasta 'semeadores' nao encontrada.
        pause
    )
    goto classe_recursos
)
if "%r%"=="4" (
    python abrir_arquivos.py
    popd
    pause
    goto classe_recursos
)
if "%r%"=="5" (
    popd
    goto menu
)
if "%r%"=="6" (
    if exist "seu_arquivo.pdf" (
        start "" "seu_arquivo.pdf"
    ) else (
        echo [!] Arquivo nao encontrado.
        pause
    )
    goto classe_recursos
)