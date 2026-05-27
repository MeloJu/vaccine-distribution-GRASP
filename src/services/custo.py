"""
Serviço de cálculo de custo.
Responsabilidade única: calcular componentes de custo da solução.
"""

from typing import Dict, List
from src.domain import Solucao, Posto, PontoDemanda
from src.services.distancia import CalculadoraDistancia


class CalculadoraCusto:
    """
    Calcula componentes de custo de uma solução.
    Desacoplado da lógica de construção/otimização.
    """

    def __init__(self, calculadora_distancia: CalculadoraDistancia):
        """
        Args:
            calculadora_distancia: Serviço para calcular distâncias
        """
        self.calculadora_distancia = calculadora_distancia

    def calcular_custo_abertura(
        self,
        postos_abertos_ids: List[int],
        postos: Dict[int, Posto]
    ) -> float:
        """Calcula custo total de abertura dos postos."""
        return sum(
            postos[pid].custo_abertura * postos[pid].prioridade
            for pid in postos_abertos_ids
            if pid in postos
        )

    def calcular_custo_distancia(
        self,
        alocacao: Dict[int, int],
        demandas: Dict[int, PontoDemanda],
        postos: Dict[int, Posto],
        custo_por_km: float
    ) -> float:
        """Calcula custo total de distância."""
        custo_total = 0.0
        for dem_id, posto_id in alocacao.items():
            if dem_id not in demandas or posto_id not in postos:
                continue
            dem = demandas[dem_id]
            posto = postos[posto_id]
            dist = self.calculadora_distancia.calcular(
                dem.x, dem.y, posto.x, posto.y
            )
            custo_total += dist * custo_por_km * dem.populacao
        return custo_total

    def calcular_custo_nao_atendimento(
        self,
        nao_atendidos: Dict[int, int],
        custo_nao_atend: float
    ) -> float:
        """Calcula custo de demanda não atendida."""
        return sum(
            qtd * custo_nao_atend
            for qtd in nao_atendidos.values()
        )

    def recalcular_solucao(
        self,
        solucao: Solucao,
        postos: List[Posto],
        demandas: List[PontoDemanda],
        custo_por_km: float,
        custo_nao_atend: float
    ) -> Solucao:
        """
        Recalcula todos os custos de uma solução.
        Modifica a solução in-place e a retorna.
        """
        postos_dict = {p.id: p for p in postos}
        demandas_dict = {d.id: d for d in demandas}

        solucao.custo_abertura = self.calcular_custo_abertura(
            solucao.postos_abertos, postos_dict
        )
        solucao.custo_distancia = self.calcular_custo_distancia(
            solucao.alocacao, demandas_dict, postos_dict, custo_por_km
        )
        solucao.custo_nao_atendimento = self.calcular_custo_nao_atendimento(
            solucao.nao_atendidos, custo_nao_atend
        )
        solucao.custo_total = (
            solucao.custo_abertura
            + solucao.custo_distancia
            + solucao.custo_nao_atendimento
        )
        return solucao
