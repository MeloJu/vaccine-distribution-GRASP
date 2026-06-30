# Busca Tabu — Distribuição de Recursos em Campanhas de Vacinação

Implementação em Python da metaheurística **Busca Tabu** aplicada ao problema de alocação de postos de vacinação municipais, baseado no modelo de cobertura capacitada proposto por Santos (2018).

## Problema

Dado um conjunto de postos candidatos e bairros com demanda populacional, o objetivo é decidir **quais postos abrir** e **como alocar cada bairro a um posto**, minimizando o custo total:

```
Custo total = custo de abertura dos postos
            + custo de deslocamento da população
            + penalidade por pessoas não atendidas
```

## Algoritmo

A **Busca Tabu** parte de uma solução inicial gulosa e melhora iterativamente explorando três movimentos de vizinhança:

- **Add** — abre um posto fechado
- **Drop** — fecha um posto aberto
- **Swap** — troca um posto aberto por um fechado

Uma lista tabu bloqueia movimentos reversos por `tabu_tenure` iterações para evitar ciclagem. O **critério de aspiração** permite aceitar um movimento tabu se ele produzir um novo melhor global.

## Como Executar

**Execução padrão** (instância com 10 postos e 10 bairros):

```bash
py run.py
```

**Com parâmetros:**

```bash
py -m src.main data/instancia.json [tabu_tenure] [iteracoes]
```

| Parâmetro | Descrição | Padrão |
|---|---|---|
| `tabu_tenure` | Iterações que um movimento fica bloqueado | `5` |
| `iteracoes` | Número máximo de iterações | `50` |

**Exemplo:**

```bash
py -m src.main data/instancia.json 5 50
```

## Estrutura do Projeto

```
metaheurisitcas/
├── src/
│   ├── domain/
│   │   └── models.py           # Entidades: Posto, PontoDemanda, Solucao
│   ├── services/
│   │   ├── distancia.py        # Distância Euclidiana
│   │   ├── custo.py            # Cálculo dos componentes de custo
│   │   └── alocacao.py        # Alocação gulosa de demanda aos postos
│   ├── algorithms/
│   │   ├── construcao.py       # Construção da solução inicial (gulosa)
│   │   ├── busca_local.py      # Busca local (first-improvement)
│   │   └── tabu_search.py      # Busca Tabu (Add/Drop/Swap + lista tabu)
│   ├── io/
│   │   ├── carregador.py       # Leitura de instâncias JSON
│   │   └── formatter.py        # Impressão dos resultados
│   └── main.py                 # Ponto de entrada e injeção de dependência
├── data/
│   ├── instancia.json          # Instância padrão (10 postos, 10 bairros)
│   └── instancia_pequena.json  # Instância pequena (5 postos, 5 bairros)
├── tests/                      # Testes unitários
└── run.py                      # Script de execução rápida
```

## Testes

```bash
py -m unittest discover tests -v
```

## Formato da Instância

Arquivo JSON com postos candidatos, pontos de demanda e parâmetros de custo:

```json
{
  "parametros": {
    "custo_por_km": 2.5,
    "custo_nao_atendimento": 500
  },
  "postos": [
    {"id": 1, "nome": "Posto Centro", "capacidade": 800, "custo_abertura": 3000, "x": 5.0, "y": 5.0}
  ],
  "demandas": [
    {"id": 1, "nome": "Bairro Centro", "populacao": 700, "x": 5.0, "y": 5.5}
  ]
}
```

## Referência

SANTOS, Letícia Caldas dos. *Proposição de um modelo de programação matemática para distribuição de imunobiológicos no município de Rio das Ostras*. Projeto Final de Curso — Engenharia de Produção, UFF/PURO, Rio das Ostras, 2018.
