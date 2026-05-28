"""
Modelos e entidades do domínio.
Sem dependências com lógica de negócio - apenas estruturas de dados puras.
"""

import copy
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Posto:
    """Representa um posto de vacinação."""
    id: int
    nome: str
    capacidade: int          # máximo de pessoas que pode atender
    custo_abertura: float    # custo fixo para abrir o posto
    x: float                 # coordenada x (para calcular distância)
    y: float                 # coordenada y
    tipo: str = "posto_saude" # tipo (escola, posto_saude, etc)
    prioridade: int = 1      # multiplicador de penalidade/prioridade (default 1)
    funcionarios: int = 0    # quantidade de profissionais da saúde alocados
    vacinas_disponiveis: int = 0 # estoque inicial de vacinas no local


@dataclass
class PontoDemanda:
    """Representa um ponto de demanda (população a vacinar)."""
    id: int
    nome: str
    populacao: int           # pessoas que precisam ser vacinadas
    x: float                 # coordenada x
    y: float                 # coordenada y


@dataclass
class Solucao:
    """
    Representa uma solução para o problema de alocação.
    Mantém todos os custos e a alocação de demandas.
    """
    postos_abertos: list[int]              # IDs dos postos abertos
    alocacao: Dict[int, int]               # demanda_id -> posto_id
    nao_atendidos: Dict[int, int]          # demanda_id -> qtd não atendida
    custo_total: float = 0.0
    custo_abertura: float = 0.0
    custo_distancia: float = 0.0
    custo_nao_atendimento: float = 0.0

    def copia(self) -> "Solucao":
        """Retorna uma cópia profunda da solução."""
        return copy.deepcopy(self)

    def __lt__(self, other: "Solucao") -> bool:
        """Comparação para ordenação por custo."""
        return self.custo_total < other.custo_total


@dataclass
class ParametrosInstancia:
    """Parâmetros de configuração da instância."""
    custo_por_km: float
    custo_nao_atendimento: float
