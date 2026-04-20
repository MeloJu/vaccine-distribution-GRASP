"""
Algoritmo GRASP completo.
Responsabilidade única: orquestrar construção e busca local.
"""

import random
from typing import List, Optional, Tuple
from src.domain import Solucao, Posto, PontoDemanda, ParametrosInstancia
from src.algorithms.construcao import ConstrutorGrasp
from src.algorithms.busca_local import BuscadorLocal


class GRASP:
    """
    Implementa GRASP (Greedy Randomized Adaptive Search Procedure).
    Orquestra construção e busca local.
    """

    def __init__(
        self,
        construtor: ConstrutorGrasp,
        buscador: BuscadorLocal
    ):
        """
        Args:
            construtor: Fase de construção
            buscador: Fase de busca local
        """
        self.construtor = construtor
        self.buscador = buscador

    def executar(
        self,
        postos: List[Posto],
        demandas: List[PontoDemanda],
        params: ParametrosInstancia,
        alpha: float = 0.3,
        max_iteracoes: int = 50,
        semente: Optional[int] = None,
        verbose: bool = True
    ) -> Tuple[Solucao, List[float]]:
        """
        Executa GRASP completo.

        Args:
            postos: Lista de postos
            demandas: Lista de pontos de demanda
            params: Parâmetros da instância
            alpha: Grau de aleatoriedade (0=guloso, 1=aleatório)
            max_iteracoes: Número de iterações
            semente: Semente para reprodutibilidade
            verbose: Se imprime progresso

        Returns:
            Tupla (melhor_solucao, historico_custos)
        """
        if semente is not None:
            random.seed(semente)

        melhor_global: Optional[Solucao] = None
        historico = []

        if verbose:
            print(f"\n{'='*55}")
            print(f"  GRASP – Vacinação em Massa")
            print(f"  α={alpha}  |  iterações={max_iteracoes}")
            print(f"{'='*55}")

        for it in range(1, max_iteracoes + 1):
            # Fase 1: Construção
            sol_construida = self.construtor.construir(
                postos, demandas, alpha,
                params.custo_por_km,
                params.custo_nao_atendimento
            )

            # Fase 2: Busca Local
            sol_melhorada = self.buscador.buscar(
                sol_construida, postos, demandas,
                params.custo_por_km,
                params.custo_nao_atendimento
            )

            # Fase 3: Atualiza melhor global
            if (melhor_global is None or
                sol_melhorada.custo_total < melhor_global.custo_total):
                melhor_global = sol_melhorada.copia()
                flag = " ◀ novo melhor"
            else:
                flag = ""

            historico.append(melhor_global.custo_total)

            if verbose:
                print(
                    f"  iter {it:3d} | construção: {sol_construida.custo_total:10.2f}"
                    f" | após BL: {sol_melhorada.custo_total:10.2f}"
                    f" | melhor: {melhor_global.custo_total:10.2f}{flag}"
                )

        if verbose:
            print(f"{'='*55}\n")

        return melhor_global, historico
