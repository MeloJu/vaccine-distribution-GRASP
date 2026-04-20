#!/bin/bash
# Script para executar GRASP Vacinacao em Linux/Mac

# Detecta Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Python não encontrado no PATH"
        echo ""
        echo "Instale Python 3.9+ ou adicione ao PATH"
        exit 1
    fi
    PYTHON="python"
else
    PYTHON="python3"
fi

echo "Usando Python: $PYTHON"
$PYTHON run.py "$@"
