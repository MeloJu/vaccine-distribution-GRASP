"""
Ponto de entrada da aplicação.
Orquestra DI (injeção de dependência) e execução.
"""

import sys
from src.domain import Posto, PontoDemanda, ParametrosInstancia
from src.services import (
    DistanciaEuclidiana,
    CalculadoraCusto,
    AlocadorDemanda
)
from src.algorithms import ConstrutorGrasp, BuscadorLocal, BuscaTabu
from src.io import CarregadorInstancia, FormatterResultado


class ContainerDI:
    """
    Container de injeção de dependência.
    Centraliza criação de serviços e algoritmos.
    """

    @staticmethod
    def criar_tabu() -> BuscaTabu:
        """Factory para criar instância de Busca Tabu."""
        calculadora_distancia = DistanciaEuclidiana()
        calculadora_custo = CalculadoraCusto(calculadora_distancia)
        alocador = AlocadorDemanda(calculadora_distancia, calculadora_custo)
        construtor = ConstrutorGrasp(alocador)
        return BuscaTabu(construtor, alocador)


def main():
    """Função principal."""
    import os

    # Parse argumentos
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
    else:
        # Busca instância padrão em data/
        caminho = os.path.join(os.path.dirname(__file__), "..", "data", "instancia.json")

    tabu_tenure = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    max_iter = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    semente = int(sys.argv[4]) if len(sys.argv) > 4 else None

    # Se arquivo não existe, mostra uso
    if not os.path.exists(caminho):
        print("Uso: python -m src.main [instancia.json] [tabu_tenure] [iteracoes] [semente]")
        print("\nExemplos de uso:")
        print("  python -m src.main  (Roda padrao com Tabu Search)")
        print("  python -m src.main data/instancia.json 5 50")
        sys.exit(1)

    # Carrega instância
    print(f"Carregando instância: {caminho}...")
    postos, demandas, params = CarregadorInstancia.carregar(caminho)
    print(f"✓ {len(postos)} postos, {len(demandas)} pontos de demanda")

    print("\nExecutando BUSCA TABU...")
    algoritmo = ContainerDI.criar_tabu()
    melhor_solucao, historico = algoritmo.executar(
        postos=postos,
        demandas=demandas,
        params=params,
        max_iteracoes=max_iter,
        tabu_tenure=tabu_tenure,
        verbose=True
    )

    # Formata resultado
    postos_dict = {p.id: p for p in postos}
    demandas_dict = {d.id: d for d in demandas}
    FormatterResultado.imprimir(melhor_solucao, postos_dict, demandas_dict)


if __name__ == "__main__":
    main()
