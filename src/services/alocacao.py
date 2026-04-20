"""
Serviço de alocação de demanda.
Responsabilidade única: alocar demandas aos postos abertos.
"""

from typing import Dict, List
from src.domain import Solucao, Posto, PontoDemanda
from src.services.distancia import CalculadoraDistancia
from src.services.custo import CalculadoraCusto


class AlocadorDemanda:
    """
    Aloca demandas aos postos abertos.
    Estratégia: greedy por distância com capacidade disponível.
    """

    def __init__(
        self,
        calculadora_distancia: CalculadoraDistancia,
        calculadora_custo: CalculadoraCusto
    ):
        """
        Args:
            calculadora_distancia: Para calcular distâncias
            calculadora_custo: Para recalcular custos da solução
        """
        self.calculadora_distancia = calculadora_distancia
        self.calculadora_custo = calculadora_custo

    def alocar(
        self,
        postos_abertos_ids: List[int],
        postos: List[Posto],
        demandas: List[PontoDemanda],
        custo_por_km: float,
        custo_nao_atend: float
    ) -> Solucao:
        """
        Para um conjunto de postos abertos, aloca cada demanda
        ao posto mais próximo com capacidade disponível.

        Args:
            postos_abertos_ids: IDs dos postos abertos
            postos: Lista de todos os postos
            demandas: Lista de pontos de demanda
            custo_por_km: Custo por unidade de distância
            custo_nao_atend: Custo por unidade não atendida

        Returns:
            Solução com alocação e custos calculados
        """
        postos_abertos = [p for p in postos if p.id in postos_abertos_ids]
        capacidade_restante = {p.id: p.capacidade for p in postos_abertos}

        alocacao = {}
        nao_atendidos = {}

        # Para cada demanda, aloca ao posto mais próximo com capacidade
        for dem in demandas:
            # Ordena postos por distância à demanda
            candidatos = sorted(
                postos_abertos,
                key=lambda p: self.calculadora_distancia.calcular(
                    dem.x, dem.y, p.x, p.y
                )
            )

            populacao_restante = dem.populacao
            for posto in candidatos:
                if populacao_restante <= 0:
                    break
                if capacidade_restante[posto.id] > 0:
                    atendido = min(
                        populacao_restante,
                        capacidade_restante[posto.id]
                    )
                    populacao_restante -= atendido
                    capacidade_restante[posto.id] -= atendido
                    # Registra primeiro posto que atendeu
                    if dem.id not in alocacao:
                        alocacao[dem.id] = posto.id

            # Registra não atendidos
            if populacao_restante > 0:
                nao_atendidos[dem.id] = populacao_restante
                if dem.id not in alocacao and postos_abertos:
                    # Aloca ao mais próximo para referência
                    alocacao[dem.id] = candidatos[0].id

        # Cria solução
        solucao = Solucao(
            postos_abertos=list(postos_abertos_ids),
            alocacao=alocacao,
            nao_atendidos=nao_atendidos,
        )

        # Recalcula custos
        return self.calculadora_custo.recalcular_solucao(
            solucao, postos, demandas, custo_por_km, custo_nao_atend
        )
