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
echo ========================================================
set /p escolha=Selecione uma opcao: 

if "%escolha%"=="1" goto classe_links
if "%escolha%"=="2" goto classe_otimizar
if "%escolha%"=="3" goto classe_rede
if "%escolha%"=="4" goto classe_sistema
if "%escolha%"=="5" goto classe_hibrida
if "%escolha%"=="6" goto classe_android
if "%escolha%"=="7" exit
goto menu
:: --- CLASSE 1: LINKS ---
:classe_links
cls
echo Abrindo ferramentas de trabalho e estudo...
start chrome "https://github.com" "https://www.w3schools.com/python/" "https://youtube.com"
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
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python nao encontrado. Executando automacao em Batch nativo...
    goto classe_otimizar
) else (
    echo [v] Python detectado! Iniciando script inteligente...
    :: Se você tiver um arquivo .py, ele chamaria aqui:
    :: python seu_script.py
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
if "%op_android%"=="4" goto menu
goto classe_android

:: ... (mantenha aqui as outras classes de links, otimização, etc.)
