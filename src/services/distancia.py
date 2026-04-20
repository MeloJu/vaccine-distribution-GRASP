"""
Serviço de cálculo de geometria (distâncias).
Responsabilidade única: operações de distância Euclidiana.
"""

import math
from abc import ABC, abstractmethod


class CalculadoraDistancia(ABC):
    """Interface para calcular distância entre dois pontos."""

    @abstractmethod
    def calcular(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Calcula distância entre dois pontos (x1,y1) e (x2,y2)."""
        pass


class DistanciaEuclidiana(CalculadoraDistancia):
    """Implementação usando distância Euclidiana."""

    def calcular(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Calcula distância Euclidiana."""
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
