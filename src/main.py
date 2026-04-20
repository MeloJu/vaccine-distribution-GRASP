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
from src.algorithms import ConstrutorGrasp, BuscadorLocal, GRASP
from src.io import CarregadorInstancia, FormatterResultado


class ContainerDI:
    """
    Container de injeção de dependência.
    Centraliza criação de serviços e algoritmos.
    """

    @staticmethod
    def criar_grasp() -> GRASP:
        """Factory para criar instância de GRASP com todas as dependências."""
        # Serviços
        calculadora_distancia = DistanciaEuclidiana()
        calculadora_custo = CalculadoraCusto(calculadora_distancia)
        alocador = AlocadorDemanda(calculadora_distancia, calculadora_custo)

        # Algoritmos
        construtor = ConstrutorGrasp(alocador)
        buscador = BuscadorLocal(alocador)

        # GRASP
        return GRASP(construtor, buscador)


def main():
    """Função principal."""
    import os

    # Parse argumentos
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
    else:
        # Busca instância padrão em data/
        caminho = os.path.join(os.path.dirname(__file__), "..", "data", "instancia.json")

    alpha = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
    max_iter = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    semente = int(sys.argv[4]) if len(sys.argv) > 4 else None

    # Se arquivo não existe, mostra uso
    if not os.path.exists(caminho):
        print("Uso: python -m src.main [instancia.json] [alpha] [iteracoes] [semente]")
        print(f"\nInstância padrão não encontrada: {caminho}")
        print("Crie um arquivo JSON em data/instancia.json ou especifique o caminho.")
        print("\nExemplos de uso:")
        print("  python -m src.main")
        print("  python -m src.main data/instancia.json 0.3 50 42")
        print("  python -m src.main ./minha_instancia.json 0.5 100")
        sys.exit(1)

    # Carrega instância
    print(f"Carregando instância: {caminho}...")
    postos, demandas, params = CarregadorInstancia.carregar(caminho)
    print(f"✓ {len(postos)} postos, {len(demandas)} pontos de demanda")

    # Cria e executa GRASP
    print("\nExecutando GRASP...")
    grasp = ContainerDI.criar_grasp()
    melhor_solucao, historico = grasp.executar(
        postos=postos,
        demandas=demandas,
        params=params,
        alpha=alpha,
        max_iteracoes=max_iter,
        semente=semente,
        verbose=True
    )

    # Formata resultado
    postos_dict = {p.id: p for p in postos}
    demandas_dict = {d.id: d for d in demandas}
    FormatterResultado.imprimir(melhor_solucao, postos_dict, demandas_dict)


if __name__ == "__main__":
    main()
