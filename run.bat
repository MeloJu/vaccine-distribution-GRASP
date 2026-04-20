@echo off
REM Script para executar GRASP Vacinacao no Windows

setlocal enabledelayedexpansion

REM Detecta Python
for /f "delims=" %%A in ('where python.exe 2^>nul') do set "PYTHON=%%A"

if "!PYTHON!"=="" (
    echo Python nao encontrado no PATH
    echo.
    echo Resolva uma dessas opcoes:
    echo 1. Instale Python de https://www.python.org/
    echo 2. Adicione Python ao PATH durante a instalacao
    echo 3. Configure manualmente o caminho no script
    exit /b 1
)

echo Usando Python em: !PYTHON!
!PYTHON! run.py %*
