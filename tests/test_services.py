"""
Testes para camada de serviços.
"""

import unittest
from src.domain import Posto, PontoDemanda, Solucao, ParametrosInstancia
from src.services import (
    DistanciaEuclidiana,
    CalculadoraCusto,
    AlocadorDemanda
)


class TestDistanciaEuclidiana(unittest.TestCase):
    """Testes para cálculo de distância."""

    def setUp(self):
        self.calculadora = DistanciaEuclidiana()

    def test_distancia_mesmo_ponto(self):
        """Testa distância entre o mesmo ponto."""
        dist = self.calculadora.calcular(0, 0, 0, 0)
        self.assertEqual(dist, 0.0)

    def test_distancia_euclidiana(self):
        """Testa cálculo de distância Euclidiana."""
        # Triângulo 3-4-5
        dist = self.calculadora.calcular(0, 0, 3, 4)
        self.assertEqual(dist, 5.0)

    def test_distancia_simetria(self):
        """Testa simetria da distância."""
        dist1 = self.calculadora.calcular(0, 0, 10, 10)
        dist2 = self.calculadora.calcular(10, 10, 0, 0)
        self.assertEqual(dist1, dist2)


class TestCalculadoraCusto(unittest.TestCase):
    """Testes para cálculo de custos."""

    def setUp(self):
        self.calculadora_dist = DistanciaEuclidiana()
        self.calculadora_custo = CalculadoraCusto(self.calculadora_dist)

        # Cria dados de teste
        self.postos_dict = {
            1: Posto(1, "P1", 100, 1000.0, 0, 0),
            2: Posto(2, "P2", 100, 2000.0, 10, 0)
        }

        self.demandas_dict = {
            1: PontoDemanda(1, "D1", 50, 0, 0),
            2: PontoDemanda(2, "D2", 30, 10, 0)
        }

    def test_custo_abertura(self):
        """Testa cálculo de custo de abertura."""
        custo = self.calculadora_custo.calcular_custo_abertura(
            [1, 2],
            self.postos_dict
        )
        self.assertEqual(custo, 3000.0)

    def test_custo_distancia(self):
        """Testa cálculo de custo de distância."""
        alocacao = {1: 1, 2: 2}
        custo = self.calculadora_custo.calcular_custo_distancia(
            alocacao,
            self.demandas_dict,
            self.postos_dict,
            custo_por_km=1.0
        )
        # D1: 0 distância, 50 pessoas = 0
        # D2: 10 distância, 30 pessoas = 300
        self.assertEqual(custo, 300.0)

    def test_custo_nao_atendimento(self):
        """Testa cálculo de custo de não atendimento."""
        nao_atendidos = {1: 10, 2: 5}
        custo = self.calculadora_custo.calcular_custo_nao_atendimento(
            nao_atendidos,
            custo_nao_atend=500.0
        )
        self.assertEqual(custo, 7500.0)

    def test_recalcular_solucao(self):
        """Testa recálculo completo de custos."""
        solucao = Solucao(
            postos_abertos=[1, 2],
            alocacao={1: 1, 2: 2},
            nao_atendidos={}
        )

        postos = list(self.postos_dict.values())
        demandas = list(self.demandas_dict.values())

        resultado = self.calculadora_custo.recalcular_solucao(
            solucao,
            postos,
            demandas,
            custo_por_km=1.0,
            custo_nao_atend=500.0
        )

        self.assertEqual(resultado.custo_abertura, 3000.0)
        self.assertEqual(resultado.custo_nao_atendimento, 0.0)
        self.assertGreater(resultado.custo_total, 0)


class TestAlocadorDemanda(unittest.TestCase):
    """Testes para alocação de demandas."""

    def setUp(self):
        self.calculadora_dist = DistanciaEuclidiana()
        self.calculadora_custo = CalculadoraCusto(self.calculadora_dist)
        self.alocador = AlocadorDemanda(
            self.calculadora_dist,
            self.calculadora_custo
        )

        # Dados de teste
        self.postos = [
            Posto(1, "P1", 100, 1000.0, 0, 0),
            Posto(2, "P2", 100, 2000.0, 10, 0)
        ]

        self.demandas = [
            PontoDemanda(1, "D1", 50, 0, 0),
            PontoDemanda(2, "D2", 30, 10, 0)
        ]

    def test_alocar_demanda_simples(self):
        """Testa alocação simples."""
        solucao = self.alocador.alocar(
            postos_abertos_ids=[1, 2],
            postos=self.postos,
            demandas=self.demandas,
            custo_por_km=1.0,
            custo_nao_atend=500.0
        )

        self.assertEqual(len(solucao.postos_abertos), 2)
        self.assertIn(1, solucao.alocacao.values())
        self.assertGreater(solucao.custo_total, 0)

    def test_alocar_sem_capacidade(self):
        """Testa alocação com falta de capacidade."""
        # Criar postos com capacidade insuficiente
        postos_pequenos = [
            Posto(1, "P1", 10, 1000.0, 0, 0),  # Capacidade baixa
        ]
        demandas_grandes = [
            PontoDemanda(1, "D1", 100, 0, 0),  # Demanda grande
        ]

        solucao = self.alocador.alocar(
            postos_abertos_ids=[1],
            postos=postos_pequenos,
            demandas=demandas_grandes,
            custo_por_km=1.0,
            custo_nao_atend=500.0
        )

        # Deve ter não atendidos
        self.assertGreater(
            solucao.nao_atendidos.get(1, 0),
            0
        )


if __name__ == "__main__":
    unittest.main()
