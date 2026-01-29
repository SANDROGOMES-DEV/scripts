@echo off
:menu
cls
title Central de Links - Chrome
color 0B

echo ==========================================
echo           ESCOLHA UMA CATEGORIA
echo ==========================================
echo.
echo [1] Trabalho (Google, Trello, Email)
echo [2] Lazer (YouTube, Netflix, Twitch)
echo [3] Estudo (Wikipedia, StackOverflow)
echo [4] Abrir TUDO
echo [5] Sair
echo.
echo ==========================================
set /p opcao=Digite o numero da opcao desejada: 

if "%opcao%"=="1" goto trabalho
if "%opcao%"=="2" goto lazer
if "%opcao%"=="3" goto estudo
if "%opcao%"=="4" goto tudo
if "%opcao%"=="5" exit

:trabalho
start chrome "https://mail.google.com" "https://trello.com" "https://docs.google.com"
goto fim

:lazer
start chrome "https://www.youtube.com" "https://www.netflix.com" "https://www.twitch.tv"
goto fim

:estudo
start chrome "https://www.wikipedia.org" "https://stackoverflow.com" "https://chatgpt.com"
goto fim

:tudo
start chrome "https://google.com" "https://youtube.com" "https://github.com"
goto fim

:fim
echo.
echo Links abertos com sucesso! Voltando ao menu em 3 segundos...
timeout /t 3 >nul
goto menu