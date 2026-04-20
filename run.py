"""
Script de execução rápida do GRASP.
Executa a instância padrão da pasta data/.
"""

import sys
import os

# Adiciona o diretório raiz ao caminho
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import main

if __name__ == "__main__":
    main()
