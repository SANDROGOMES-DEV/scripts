@echo off
pushd "%~dp0"
echo [v] Carregando Central Master Premium (Python GUI)...
:: Instala as bibliotecas necessarias para o grafico e interface
python -m pip install customtkinter psutil requests cryptography >nul 2>&1
:: Inicia sem mostrar o console preto (modo janela)
start /b pythonw CentralMaster.py
exit