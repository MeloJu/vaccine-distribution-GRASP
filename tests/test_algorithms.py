"""
Testes para camada de algoritmos.
"""

import unittest
import random
from src.domain import Posto, PontoDemanda, ParametrosInstancia
from src.services import (
    DistanciaEuclidiana,
    CalculadoraCusto,
    AlocadorDemanda
)
from src.algorithms import ConstrutorGrasp, BuscadorLocal, GRASP


class TestConstrutorGrasp(unittest.TestCase):
    """Testes para fase de construção."""

    def setUp(self):
        random.seed(42)

        # Serviços
        calculadora_dist = DistanciaEuclidiana()
        calculadora_custo = CalculadoraCusto(calculadora_dist)
        self.alocador = AlocadorDemanda(calculadora_dist, calculadora_custo)
        self.construtor = ConstrutorGrasp(self.alocador)

        # Dados
        self.postos = [
            Posto(1, "P1", 100, 1000.0, 0, 0),
            Posto(2, "P2", 100, 1500.0, 10, 0),
            Posto(3, "P3", 100, 2000.0, 20, 0)
        ]

        self.demandas = [
            PontoDemanda(1, "D1", 50, 0, 0),
            PontoDemanda(2, "D2", 40, 10, 0),
            PontoDemanda(3, "D3", 30, 20, 0)
        ]

    def test_construcao_completa(self):
        """Testa construção de solução."""
        solucao = self.construtor.construir(
            postos=self.postos,
            demandas=self.demandas,
            alpha=0.5,
            custo_por_km=1.0,
            custo_nao_atend=500.0
        )

        self.assertIsNotNone(solucao)
        self.assertGreater(len(solucao.postos_abertos), 0)
        self.assertGreater(solucao.custo_total, 0)

    def test_alpha_determinismo(self):
        """Testa que alpha=0 é guloso (determinístico)."""
        random.seed(42)
        sol1 = self.construtor.construir(
            self.postos, self.demandas, 0.0, 1.0, 500.0
        )

        random.seed(42)
        sol2 = self.construtor.construir(
            self.postos, self.demandas, 0.0, 1.0, 500.0
        )

        self.assertEqual(sol1.custo_total, sol2.custo_total)

    def test_alpha_aleatoriedade(self):
        """Testa que alpha=1 é aleatório."""
        random.seed(42)
        sol1 = self.construtor.construir(
            self.postos, self.demandas, 1.0, 1.0, 500.0
        )

        random.seed(43)
        sol2 = self.construtor.construir(
            self.postos, self.demandas, 1.0, 1.0, 500.0
        )

        # Com seeds diferentes, custos devem ser diferentes
        # (não há garantia, mas é muito provável)
        self.assertNotEqual(sol1.custo_total, sol2.custo_total)


class TestBuscadorLocal(unittest.TestCase):
    """Testes para busca local."""

    def setUp(self):
        # Serviços
        calculadora_dist = DistanciaEuclidiana()
        calculadora_custo = CalculadoraCusto(calculadora_dist)
        self.alocador = AlocadorDemanda(calculadora_dist, calculadora_custo)
        self.buscador = BuscadorLocal(self.alocador)

        # Dados
        self.postos = [
            Posto(1, "P1", 100, 1000.0, 0, 0),
            Posto(2, "P2", 100, 1500.0, 10, 0),
            Posto(3, "P3", 100, 2000.0, 20, 0)
        ]

        self.demandas = [
            PontoDemanda(1, "D1", 50, 0, 0),
            PontoDemanda(2, "D2", 40, 10, 0),
            PontoDemanda(3, "D3", 30, 20, 0)
        ]

    def test_busca_local_melhora(self):
        """Testa que busca local não piora solução."""
        # Cria solução inicial subótima
        solucao_inicial = self.alocador.alocar(
            postos_abertos_ids=[1, 2, 3],
            postos=self.postos,
            demandas=self.demandas,
            custo_por_km=1.0,
            custo_nao_atend=500.0
        )

        solucao_melhorada = self.buscador.buscar(
            solucao_inicial,
            self.postos,
            self.demandas,
            custo_por_km=1.0,
            custo_nao_atend=500.0
        )

        # Busca local não deve piorar
        self.assertLessEqual(
            solucao_melhorada.custo_total,
            solucao_inicial.custo_total + 1e-6  # Tolerância para erros numéricos
        )

    def test_busca_local_não_abre_sem_necessidade(self):
        """Testa que busca local não abre postos sem razão."""
        solucao_inicial = self.alocador.alocar(
            postos_abertos_ids=[1],
            postos=self.postos,
            demandas=[self.demandas[0]],  # Apenas uma demanda pequena
            custo_por_km=1.0,
            custo_nao_atend=500.0
        )

        postos_inicial = set(solucao_inicial.postos_abertos)

        solucao_melhorada = self.buscador.buscar(
            solucao_inicial,
            self.postos,
            [self.demandas[0]],
            custo_por_km=1.0,
            custo_nao_atend=500.0
        )

        postos_final = set(solucao_melhorada.postos_abertos)

        # Não deve adicionar muitos postos
        self.assertLessEqual(len(postos_final), len(postos_inicial) + 2)


class TestGRASP(unittest.TestCase):
    """Testes para algoritmo GRASP completo."""

    def setUp(self):
        random.seed(42)

        # Serviços
        calculadora_dist = DistanciaEuclidiana()
        calculadora_custo = CalculadoraCusto(calculadora_dist)
        alocador = AlocadorDemanda(calculadora_dist, calculadora_custo)

        # Algoritmos
        construtor = ConstrutorGrasp(alocador)
        buscador = BuscadorLocal(alocador)

        self.grasp = GRASP(construtor, buscador)

        # Dados
        self.postos = [
            Posto(1, "P1", 100, 1000.0, 0, 0),
            Posto(2, "P2", 100, 1500.0, 10, 0),
            Posto(3, "P3", 100, 2000.0, 20, 0)
        ]

        self.demandas = [
            PontoDemanda(1, "D1", 50, 0, 0),
            PontoDemanda(2, "D2", 40, 10, 0),
            PontoDemanda(3, "D3", 30, 20, 0)
        ]

        self.params = ParametrosInstancia(
            custo_por_km=1.0,
            custo_nao_atendimento=500.0
        )

    def test_grasp_executa(self):
        """Testa que GRASP executa sem erros."""
        solucao, historico = self.grasp.executar(
            postos=self.postos,
            demandas=self.demandas,
            params=self.params,
            alpha=0.5,
            max_iteracoes=5,
            semente=42,
            verbose=False
        )

        self.assertIsNotNone(solucao)
        self.assertEqual(len(historico), 5)
        self.assertGreater(solucao.custo_total, 0)

    def test_grasp_melhora_iterativamente(self):
        """Testa que GRASP não piora entre iterações."""
        solucao, historico = self.grasp.executar(
            postos=self.postos,
            demandas=self.demandas,
            params=self.params,
            alpha=0.5,
            max_iteracoes=10,
            semente=42,
            verbose=False
        )

        # Histórico deve ser não crescente
        for i in range(1, len(historico)):
            self.assertLessEqual(
                historico[i],
                historico[i - 1] + 1e-6  # Tolerância numérica
            )

    def test_grasp_reprodutibilidade(self):
        """Testa que mesma semente produz mesmo resultado."""
        sol1, hist1 = self.grasp.executar(
            self.postos, self.demandas, self.params,
            alpha=0.5, max_iteracoes=5, semente=999,
            verbose=False
        )

        sol2, hist2 = self.grasp.executar(
            self.postos, self.demandas, self.params,
            alpha=0.5, max_iteracoes=5, semente=999,
            verbose=False
        )

        self.assertEqual(sol1.custo_total, sol2.custo_total)
        self.assertEqual(hist1, hist2)


if __name__ == "__main__":
    unittest.main()
