"""
Fase de construção do GRASP (Greedy Randomized Adaptive Search Procedure).
Responsabilidade única: construir solução inicial semi-gulosa.
"""

import random
from typing import List, Optional
from src.domain import Solucao, Posto, PontoDemanda
from src.services.alocacao import AlocadorDemanda


class ConstrutorGrasp:
    """
    Constrói solução usando critério guloso-aleatório (semi-guloso).
    Implementa a fase de construção do GRASP.
    """

    def __init__(self, alocador: AlocadorDemanda):
        """
        Args:
            alocador: Serviço para alocar demandas
        """
        self.alocador = alocador

    def construir(
        self,
        postos: List[Posto],
        demandas: List[PontoDemanda],
        alpha: float,
        custo_por_km: float,
        custo_nao_atend: float
    ) -> Solucao:
        """
        Constrói solução gulosa-aleatória com LRC (Lista Restrita de Candidatos).

        Processo:
        1. Avalia custo marginal de cada posto candidato
        2. Cria LRC com postos entre [melhor, melhor + α*(pior - melhor)]
        3. Escolhe aleatoriamente da LRC
        4. Repete até convergência (demanda atendida ou sem melhora)

        Args:
            postos: Lista de postos disponíveis
            demandas: Lista de pontos de demanda
            alpha: Grau de aleatoriedade (0=guloso, 1=aleatório)
            custo_por_km: Custo por unidade de distância
            custo_nao_atend: Custo por unidade não atendida

        Returns:
            Solução construída
        """
        postos_disponiveis = list(postos)
        postos_escolhidos = []

        # Construção iterativa
        while postos_disponiveis:
            # Avalia custo marginal de cada candidato
            custos_marginais = []
            for posto in postos_disponiveis:
                sol_teste = self.alocador.alocar(
                    postos_escolhidos + [posto.id],
                    postos, demandas, custo_por_km, custo_nao_atend
                )
                custos_marginais.append((posto, sol_teste.custo_total))

            custos_marginais.sort(key=lambda x: x[1])

            # Calcula limiar da LRC
            c_melhor = custos_marginais[0][1]    # melhor
            c_pior = custos_marginais[-1][1]     # pior
            limiar = c_melhor + alpha * (c_pior - c_melhor)

            # LRC: postos com custo dentro do limiar
            lrc = [
                posto for posto, custo in custos_marginais
                if custo <= limiar
            ]

            # Escolhe aleatoriamente da LRC
            escolhido = random.choice(lrc)
            postos_escolhidos.append(escolhido.id)
            postos_disponiveis.remove(escolhido)

            # Critério de parada
            sol_atual = self.alocador.alocar(
                postos_escolhidos, postos, demandas,
                custo_por_km, custo_nao_atend
            )

            # Se toda demanda atendida, para
            if not sol_atual.nao_atendidos:
                return sol_atual

            # Se adicionar mais postos não melhora, para
            if len(postos_disponiveis) > 0:
                melhor_prox = min(
                    self.alocador.alocar(
                        postos_escolhidos + [p.id], postos, demandas,
                        custo_por_km, custo_nao_atend
                    ).custo_total
                    for p in postos_disponiveis
                )
                if melhor_prox >= sol_atual.custo_total:
                    return sol_atual

        return self.alocador.alocar(
            postos_escolhidos, postos, demandas,
            custo_por_km, custo_nao_atend
        )
