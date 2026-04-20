# Padrões de Design e Exemplos de Uso

## 🎯 Padrões de Design Implementados

### 1. **Dependency Injection (DI)**

O projeto usa injeção de dependência para desacoplar componentes:

```python
# Em src/main.py - Container DI centralizado
class ContainerDI:
    @staticmethod
    def criar_grasp() -> GRASP:
        # Cria todos os serviços
        calculadora_distancia = DistanciaEuclidiana()
        calculadora_custo = CalculadoraCusto(calculadora_distancia)
        alocador = AlocadorDemanda(calculadora_distancia, calculadora_custo)
        
        # Passa dependências para algoritmos
        construtor = ConstrutorGrasp(alocador)
        buscador = BuscadorLocal(alocador)
        
        return GRASP(construtor, buscador)
```

**Benefício**: Fácil trocar implementações (ex: usar DistanciaManhattan)

### 2. **Strategy Pattern**

`CalculadoraDistancia` é uma interface que permite múltiplas estratégias:

```python
# Interface abstrata
class CalculadoraDistancia(ABC):
    @abstractmethod
    def calcular(self, x1, y1, x2, y2) -> float:
        pass

# Implementações
class DistanciaEuclidiana(CalculadoraDistancia):
    def calcular(self, x1, y1, x2, y2) -> float:
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

class DistanciaManhattan(CalculadoraDistancia):
    def calcular(self, x1, y1, x2, y2) -> float:
        return abs(x1-x2) + abs(y1-y2)
```

### 3. **Factory Pattern**

`CarregadorInstancia` atua como factory:

```python
postos, demandas, params = CarregadorInstancia.carregar("data/instancia.json")
# Retorna objetos construídos corretamente
```

### 4. **Single Responsibility Principle (SRP)**

Cada classe tem uma responsabilidade única:

| Classe | Responsabilidade |
|--------|------------------|
| `Posto` | Representar dados de um posto |
| `DistanciaEuclidiana` | Calcular distância |
| `CalculadoraCusto` | Calcular custos |
| `ConstrutorGrasp` | Construir solução inicial |
| `BuscadorLocal` | Melhorar solução |
| `CarregadorInstancia` | Ler JSON |
| `FormatterResultado` | Imprimir resultado |

## 📚 Exemplos de Uso

### Exemplo 1: Uso Básico (Linha de Comando)

```bash
# Executa com configuração padrão
python run.py

# Com parâmetros customizados
python run.py data/instancia.json 0.5 100 42
```

### Exemplo 2: Uso Programático

```python
from src.services import DistanciaEuclidiana, CalculadoraCusto, AlocadorDemanda
from src.algorithms import ConstrutorGrasp, BuscadorLocal, GRASP
from src.io import CarregadorInstancia
from src.domain import ParametrosInstancia

# Carrega dados
postos, demandas, params = CarregadorInstancia.carregar("data/instancia.json")

# Cria serviços
distancia = DistanciaEuclidiana()
custo = CalculadoraCusto(distancia)
alocador = AlocadorDemanda(distancia, custo)

# Cria algoritmos
construtor = ConstrutorGrasp(alocador)
buscador = BuscadorLocal(alocador)
grasp = GRASP(construtor, buscador)

# Executa
solucao, historico = grasp.executar(
    postos=postos,
    demandas=demandas,
    params=params,
    alpha=0.3,
    max_iteracoes=50,
    semente=42
)

print(f"Custo final: {solucao.custo_total}")
```

### Exemplo 3: Teste de Serviço

```python
# tests/test_services.py
from src.services import DistanciaEuclidiana

def test_distancia():
    calc = DistanciaEuclidiana()
    dist = calc.calcular(0, 0, 3, 4)  # Triângulo 3-4-5
    assert dist == 5.0
```

### Exemplo 4: Estratégia de Distância Customizada

```python
from src.services import CalculadoraDistancia

# Nova estratégia
class DistanciaChebyshev(CalculadoraDistancia):
    def calcular(self, x1, y1, x2, y2) -> float:
        return max(abs(x1-x2), abs(y1-y2))

# Usa em vez de Euclidiana
distancia = DistanciaChebyshev()
custo = CalculadoraCusto(distancia)
# ... resto do código
```

### Exemplo 5: Apenas Alocação (sem GRASP)

```python
from src.services import DistanciaEuclidiana, CalculadoraCusto, AlocadorDemanda
from src.io import CarregadorInstancia

postos, demandas, params = CarregadorInstancia.carregar("data/instancia.json")

distancia = DistanciaEuclidiana()
custo = CalculadoraCusto(distancia)
alocador = AlocadorDemanda(distancia, custo)

# Aloca com um conjunto específico de postos
solucao = alocador.alocar(
    postos_abertos_ids=[1, 3, 5],
    postos=postos,
    demandas=demandas,
    custo_por_km=params.custo_por_km,
    custo_nao_atend=params.custo_nao_atendimento
)

print(f"Custo da alocação: {solucao.custo_total}")
print(f"Cobertura: {sum(d.populacao for d in demandas) - sum(solucao.nao_atendidos.values())} / {sum(d.populacao for d in demandas)}")
```

## 🔄 Fluxo de Execução

```
main.py
  │
  ├─→ CarregadorInstancia.carregar()
  │   └─→ Lê data/instancia.json
  │
  ├─→ ContainerDI.criar_grasp()
  │   ├─→ DistanciaEuclidiana()
  │   ├─→ CalculadoraCusto()
  │   ├─→ AlocadorDemanda()
  │   ├─→ ConstrutorGrasp()
  │   ├─→ BuscadorLocal()
  │   └─→ GRASP()
  │
  ├─→ GRASP.executar()
  │   ├─→ Para cada iteração:
  │   │   ├─→ ConstrutorGrasp.construir()
  │   │   │   └─→ AlocadorDemanda.alocar() [múltiplas vezes]
  │   │   │       └─→ CalculadoraCusto.recalcular_solucao()
  │   │   │
  │   │   └─→ BuscadorLocal.buscar()
  │   │       └─→ AlocadorDemanda.alocar() [múltiplas vezes]
  │   │
  │   └─→ Atualiza melhor solução global
  │
  └─→ FormatterResultado.imprimir()
      └─→ Exibe resultado formatado
```

## 📊 Complexidade

| Operação | Complexidade |
|----------|--------------|
| `alocar_demanda()` | O(n_demandas × n_postos × log(n_postos)) |
| `construir_grasp()` | O(n_postos × alocar_demanda()) |
| `busca_local()` | O(n_postos² × alocar_demanda()) |
| `GRASP completo` | O(max_iter × construir × busca_local) |

## 🧩 Extensão: Adicionar Novo Algoritmo

1. Criar classe em `src/algorithms/novo_algoritmo.py`
2. Herdar da interface apropriada ou criar nova
3. Usar serviços existentes (alocador, etc)
4. Testar em `tests/test_algorithms.py`
5. Integrar em `main.py` via DI

Exemplo: Algoritmo Tabu Search

```python
# src/algorithms/tabu_search.py
from src.services import AlocadorDemanda

class BuscadorTabu:
    def __init__(self, alocador: AlocadorDemanda):
        self.alocador = alocador
        self.lista_tabu = set()
    
    def buscar(self, solucao, postos, demandas, ...):
        # Implementar Tabu Search
        pass
```

## 🎓 Conceitos Aplicados

- **Metaheurística**: GRASP (Greedy Randomized Adaptive Search Procedure)
- **Busca Local**: 3 movimentos (fechar, trocar, abrir postos)
- **Aleatoriedade Controlada**: Parâmetro α na LRC (Lista Restrita de Candidatos)
- **Reprodutibilidade**: Seed para resultados determinísticos
- **First-Improvement**: Aceita primeira melhora na busca local

## 📖 Referências

- **GRASP**: Feo & Resende (1995)
- **Local Search**: Neighborhood search strategies
- **Optimization**: Facility Location Problem (FLP)
