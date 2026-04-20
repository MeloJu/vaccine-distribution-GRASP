"""
Testes para camada de I/O.
"""

import unittest
import json
import tempfile
import os
from src.io import CarregadorInstancia, FormatterResultado
from src.domain import Posto, PontoDemanda, Solucao


class TestCarregadorInstancia(unittest.TestCase):
    """Testes para carregamento de instâncias."""

    def setUp(self):
        """Cria arquivo JSON temporário para testes."""
        self.temp_dir = tempfile.mkdtemp()
        self.arquivo_valido = os.path.join(self.temp_dir, "instancia_valida.json")
        self.arquivo_invalido = os.path.join(self.temp_dir, "instancia_invalida.json")

        # Instância válida
        dados_validos = {
            "postos": [
                {"id": 1, "nome": "P1", "capacidade": 100, "custo_abertura": 1000.0, "x": 0.0, "y": 0.0},
                {"id": 2, "nome": "P2", "capacidade": 150, "custo_abertura": 1500.0, "x": 10.0, "y": 0.0}
            ],
            "demandas": [
                {"id": 1, "nome": "D1", "populacao": 50, "x": 0.0, "y": 0.0},
                {"id": 2, "nome": "D2", "populacao": 40, "x": 10.0, "y": 0.0}
            ],
            "parametros": {
                "custo_por_km": 10.0,
                "custo_nao_atendimento": 500.0
            }
        }

        with open(self.arquivo_valido, "w") as f:
            json.dump(dados_validos, f)

        # JSON inválido
        with open(self.arquivo_invalido, "w") as f:
            f.write("{ json inválido")

    def tearDown(self):
        """Limpa arquivos temporários."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_carrega_instancia_valida(self):
        """Testa carregamento de instância válida."""
        postos, demandas, params = CarregadorInstancia.carregar(self.arquivo_valido)

        self.assertEqual(len(postos), 2)
        self.assertEqual(len(demandas), 2)
        self.assertEqual(params.custo_por_km, 10.0)
        self.assertEqual(params.custo_nao_atendimento, 500.0)

    def test_carrega_postos_corretamente(self):
        """Testa que postos são carregados com atributos corretos."""
        postos, _, _ = CarregadorInstancia.carregar(self.arquivo_valido)

        self.assertEqual(postos[0].id, 1)
        self.assertEqual(postos[0].nome, "P1")
        self.assertEqual(postos[0].capacidade, 100)

    def test_carrega_demandas_corretamente(self):
        """Testa que demandas são carregadas com atributos corretos."""
        _, demandas, _ = CarregadorInstancia.carregar(self.arquivo_valido)

        self.assertEqual(demandas[0].id, 1)
        self.assertEqual(demandas[0].populacao, 50)

    def test_arquivo_nao_encontrado(self):
        """Testa erro ao carregar arquivo inexistente."""
        with self.assertRaises(FileNotFoundError):
            CarregadorInstancia.carregar("/caminho/inexistente.json")

    def test_json_invalido(self):
        """Testa erro ao carregar JSON inválido."""
        with self.assertRaises(ValueError):
            CarregadorInstancia.carregar(self.arquivo_invalido)

    def test_json_estrutura_invalida(self):
        """Testa erro com estrutura JSON incompleta."""
        arquivo_incompleto = os.path.join(self.temp_dir, "incompleto.json")
        with open(arquivo_incompleto, "w") as f:
            json.dump({"postos": []}, f)  # Falta demandas e parametros

        with self.assertRaises(ValueError):
            CarregadorInstancia.carregar(arquivo_incompleto)


class TestFormatterResultado(unittest.TestCase):
    """Testes para formatação de resultados."""

    def setUp(self):
        """Cria dados para testes."""
        self.postos = {
            1: Posto(1, "P1", 100, 1000.0, 0, 0),
            2: Posto(2, "P2", 100, 1500.0, 10, 0)
        }

        self.demandas = {
            1: PontoDemanda(1, "D1", 50, 0, 0),
            2: PontoDemanda(2, "D2", 40, 10, 0)
        }

        self.solucao = Solucao(
            postos_abertos=[1, 2],
            alocacao={1: 1, 2: 2},
            nao_atendidos={},
            custo_total=5000.0,
            custo_abertura=2500.0,
            custo_distancia=2000.0,
            custo_nao_atendimento=500.0
        )

    def test_imprime_sem_erro(self):
        """Testa que formatação não lança erro."""
        try:
            FormatterResultado.imprimir(
                self.solucao,
                self.postos,
                self.demandas
            )
        except Exception as e:
            self.fail(f"FormatterResultado.imprimir lançou {e}")

    def test_calcula_cobertura_completa(self):
        """Testa cálculo de cobertura com 100%."""
        # Este teste apenas verifica que não há erro
        # A cobertura é impressa na saída padrão
        solucao_100_pct = Solucao(
            postos_abertos=[1, 2],
            alocacao={1: 1, 2: 2},
            nao_atendidos={},
            custo_total=5000.0
        )

        try:
            FormatterResultado.imprimir(
                solucao_100_pct,
                self.postos,
                self.demandas
            )
        except Exception as e:
            self.fail(f"Erro ao imprimir 100% cobertura: {e}")


if __name__ == "__main__":
    unittest.main()
