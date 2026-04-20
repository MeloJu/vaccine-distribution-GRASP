"""
Testes para camada de domínio.
"""

import unittest
from src.domain import Posto, PontoDemanda, Solucao, ParametrosInstancia


class TestPosto(unittest.TestCase):
    """Testes para classe Posto."""

    def test_criar_posto(self):
        """Testa criação de um posto."""
        posto = Posto(
            id=1,
            nome="Posto Central",
            capacidade=100,
            custo_abertura=1000.0,
            x=0.0,
            y=0.0
        )
        self.assertEqual(posto.id, 1)
        self.assertEqual(posto.nome, "Posto Central")
        self.assertEqual(posto.capacidade, 100)


class TestPontoDemanda(unittest.TestCase):
    """Testes para classe PontoDemanda."""

    def test_criar_demanda(self):
        """Testa criação de um ponto de demanda."""
        dem = PontoDemanda(
            id=1,
            nome="Bairro A",
            populacao=500,
            x=10.0,
            y=20.0
        )
        self.assertEqual(dem.id, 1)
        self.assertEqual(dem.populacao, 500)


class TestSolucao(unittest.TestCase):
    """Testes para classe Solucao."""

    def test_criar_solucao(self):
        """Testa criação de uma solução."""
        sol = Solucao(
            postos_abertos=[1, 2],
            alocacao={1: 1, 2: 2},
            nao_atendidos={},
            custo_total=5000.0
        )
        self.assertEqual(len(sol.postos_abertos), 2)
        self.assertEqual(sol.custo_total, 5000.0)

    def test_copia_solucao(self):
        """Testa cópia profunda de solução."""
        sol = Solucao(
            postos_abertos=[1, 2],
            alocacao={1: 1},
            nao_atendidos={2: 100},
            custo_total=5000.0
        )
        copia = sol.copia()

        # Modifica cópia
        copia.postos_abertos.append(3)
        copia.nao_atendidos[2] = 200

        # Original não deve mudar
        self.assertEqual(len(sol.postos_abertos), 2)
        self.assertEqual(sol.nao_atendidos[2], 100)

    def test_comparacao_solucoes(self):
        """Testa comparação entre soluções."""
        sol1 = Solucao(
            postos_abertos=[1],
            alocacao={},
            nao_atendidos={},
            custo_total=1000.0
        )
        sol2 = Solucao(
            postos_abertos=[2],
            alocacao={},
            nao_atendidos={},
            custo_total=2000.0
        )
        self.assertTrue(sol1 < sol2)


class TestParametrosInstancia(unittest.TestCase):
    """Testes para classe ParametrosInstancia."""

    def test_criar_parametros(self):
        """Testa criação de parâmetros."""
        params = ParametrosInstancia(
            custo_por_km=10.0,
            custo_nao_atendimento=500.0
        )
        self.assertEqual(params.custo_por_km, 10.0)
        self.assertEqual(params.custo_nao_atendimento, 500.0)


if __name__ == "__main__":
    unittest.main()
