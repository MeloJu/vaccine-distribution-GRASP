"""
Busca local para GRASP.
Responsabilidade única: melhorar solução através de movimentos locais.
"""

from typing import List
from src.domain import Solucao, Posto, PontoDemanda
from src.services.alocacao import AlocadorDemanda


class BuscadorLocal:
    """
    Implementa busca local com movimentos de troca/abertura/fechamento de postos.
    Estratégia: first-improvement (aceita qualquer melhora).
    """

    def __init__(self, alocador: AlocadorDemanda):
        """
        Args:
            alocador: Serviço para alocar demandas
        """
        self.alocador = alocador

    def buscar(
        self,
        solucao: Solucao,
        postos: List[Posto],
        demandas: List[PontoDemanda],
        custo_por_km: float,
        custo_nao_atend: float
    ) -> Solucao:
        """
        Busca local por troca: tenta substituir postos ou fechar.
        Aceita primeira melhora encontrada (first-improvement).

        Movimentos:
        1. Fechar um posto aberto
        2. Trocar posto aberto por um fechado
        3. Abrir um posto fechado

        Args:
            solucao: Solução inicial
            postos: Lista de todos os postos
            demandas: Lista de pontos de demanda
            custo_por_km: Custo por unidade de distância
            custo_nao_atend: Custo por unidade não atendida

        Returns:
            Melhor solução encontrada na vizinhança
        """
        todos_ids = {p.id for p in postos}
        melhor = solucao.copia()
        melhorou = True

        while melhorou:
            melhorou = False
            abertos = set(melhor.postos_abertos)
            fechados = todos_ids - abertos

            # Movimento 1: Fechar um posto
            for pid in list(abertos):
                if len(abertos) <= 1:
                    continue

                novos_abertos = [p for p in melhor.postos_abertos if p != pid]
                nova_sol = self.alocador.alocar(
                    novos_abertos, postos, demandas,
                    custo_por_km, custo_nao_atend
                )

                if nova_sol.custo_total < melhor.custo_total:
                    melhor = nova_sol
                    melhorou = True
                    break

            if melhorou:
                continue

            # Movimento 2: Trocar aberto por fechado
            for pid_aberto in list(melhor.postos_abertos):
                if melhorou:
                    break

                for pid_fechado in list(fechados):
                    novos_abertos = (
                        [p for p in melhor.postos_abertos if p != pid_aberto]
                        + [pid_fechado]
                    )
                    nova_sol = self.alocador.alocar(
                        novos_abertos, postos, demandas,
                        custo_por_km, custo_nao_atend
                    )

                    if nova_sol.custo_total < melhor.custo_total:
                        melhor = nova_sol
                        melhorou = True
                        break

            if melhorou:
                continue

            # Movimento 3: Abrir um fechado
            for pid_fechado in list(fechados):
                novos_abertos = melhor.postos_abertos + [pid_fechado]
                nova_sol = self.alocador.alocar(
                    novos_abertos, postos, demandas,
                    custo_por_km, custo_nao_atend
                )

                if nova_sol.custo_total < melhor.custo_total:
                    melhor = nova_sol
                    melhorou = True
                    break

        return melhor
