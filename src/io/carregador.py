"""
Carregamento de instâncias.
Responsabilidade única: ler/carregar instâncias do problema.
"""

import json
from typing import Dict, Tuple
from src.domain import Posto, PontoDemanda, ParametrosInstancia


class CarregadorInstancia:
    """Carrega instâncias de arquivo JSON."""

    @staticmethod
    def carregar(caminho: str) -> Tuple[
        list[Posto],
        list[PontoDemanda],
        ParametrosInstancia
    ]:
        """
        Carrega instância de um arquivo JSON.

        Formato esperado:
        {
            "postos": [...],
            "demandas": [...],
            "parametros": {
                "custo_por_km": float,
                "custo_nao_atendimento": float
            }
        }

        Args:
            caminho: Caminho do arquivo JSON

        Returns:
            Tupla (postos, demandas, parametros)

        Raises:
            FileNotFoundError: Se arquivo não existir
            ValueError: Se formato inválido
        """
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao decodificar JSON: {e}")

        # Valida estrutura
        if not all(key in dados for key in ["postos", "demandas", "parametros"]):
            raise ValueError(
                "JSON deve conter: postos, demandas, parametros"
            )

        # Cria entidades
        postos = [Posto(**p) for p in dados["postos"]]
        demandas = [PontoDemanda(**d) for d in dados["demandas"]]
        params = ParametrosInstancia(**dados["parametros"])

        return postos, demandas, params
