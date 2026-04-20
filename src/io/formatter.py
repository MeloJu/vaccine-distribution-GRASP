"""
Formatação e impressão de resultados.
Responsabilidade única: apresentar solução de forma legível.
"""

from typing import Dict
from src.domain import Solucao, Posto, PontoDemanda


class FormatterResultado:
    """Formata e imprime resultados."""

    @staticmethod
    def imprimir(
        solucao: Solucao,
        postos: Dict[int, Posto],
        demandas: Dict[int, PontoDemanda]
    ) -> None:
        """
        Imprime solução de forma formatada.

        Args:
            solucao: Solução a imprimir
            postos: Dicionário {id: Posto}
            demandas: Dicionário {id: PontoDemanda}
        """
        print(f"\n{'='*55}")
        print("  MELHOR SOLUÇÃO ENCONTRADA")
        print(f"{'='*55}")

        # Custos
        print(f"  Custo total          : {solucao.custo_total:,.2f}")
        print(f"  └ Abertura           : {solucao.custo_abertura:,.2f}")
        print(f"  └ Distância          : {solucao.custo_distancia:,.2f}")
        print(f"  └ Não atendimento    : {solucao.custo_nao_atendimento:,.2f}")

        # Postos abertos
        print(f"\n  Postos abertos ({len(solucao.postos_abertos)}):")
        for pid in sorted(solucao.postos_abertos):
            p = postos[pid]
            print(
                f"    • [{pid}] {p.nome}  "
                f"(cap={p.capacidade}, abertura={p.custo_abertura})"
            )

        # Alocações
        print(f"\n  Alocação de demanda:")
        for did, pid in sorted(solucao.alocacao.items()):
            dem = demandas[did]
            posto = postos[pid]
            nao_at = solucao.nao_atendidos.get(did, 0)
            status = f"  ⚠ {nao_at} não atendidos" if nao_at else ""
            print(
                f"    • {dem.nome} (pop={dem.populacao}) "
                f"→ {posto.nome}{status}"
            )

        # Estatísticas
        total_nao_at = sum(solucao.nao_atendidos.values())
        total_pop = sum(d.populacao for d in demandas.values())
        cobertura = 100 * (1 - total_nao_at / total_pop) if total_pop > 0 else 100

        print(f"\n  Cobertura            : {cobertura:.1f}%")
        print(f"  Não atendidos        : {total_nao_at} / {total_pop}")
        print(f"{'='*55}\n")
