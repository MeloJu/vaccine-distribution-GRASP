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

### Com Docker (recomendado)

**Pré-requisito:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução.

```bash
# Primeira execução — constrói a imagem e roda
docker compose up

# Execuções seguintes
docker compose up

# Com parâmetros customizados
docker compose run --rm tabu python -m src.main data/instancia.json <tabu_tenure> <iteracoes>
```

Exemplo com tenure 10 e 100 iterações:

```bash
docker compose run --rm tabu python -m src.main data/instancia.json 10 100
```

O diretório `data/` é montado como volume — instâncias adicionadas localmente ficam disponíveis no container sem rebuildar a imagem.

### Sem Docker

**Pré-requisito:** Python 3.9+, sem dependências externas.

```bash
# Execução padrão
python run.py

# Com parâmetros
python -m src.main data/instancia.json <tabu_tenure> <iteracoes>
```

> **Windows:** se `python` não for reconhecido, use `py run.py`.

## Parâmetros

| Parâmetro | Descrição | Padrão |
|---|---|---|
| `tabu_tenure` | Iterações que um movimento fica bloqueado na lista tabu | `5` |
| `iteracoes` | Número máximo de iterações da Busca Tabu | `50` |

## Testes

```bash
python -m unittest discover tests -v
```

## Estrutura do Projeto

```
metaheurisitcas/
├── src/
│   ├── domain/         # Entidades: Posto, PontoDemanda, Solucao
│   ├── services/       # Distância, custo, alocação de demanda
│   ├── algorithms/     # Construção gulosa, busca local, Busca Tabu
│   ├── io/             # Leitura de JSON e formatação de resultados
│   └── main.py         # Ponto de entrada e injeção de dependência
├── data/
│   ├── instancia.json          # Instância padrão (10 postos, 10 bairros)
│   └── instancia_pequena.json  # Instância reduzida (5 postos, 5 bairros)
├── tests/
├── Dockerfile
├── docker-compose.yml
└── run.py
```

## Formato da Instância

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
