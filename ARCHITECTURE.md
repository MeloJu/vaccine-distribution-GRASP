# Visão Geral da Arquitetura

## 🏗️ Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────────┐
│                   PONTO DE ENTRADA                          │
│                    src/main.py                              │
│  (CLI - Command Line Interface + Container DI)             │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
┌──────────────────────┐            ┌──────────────────────┐
│   CARREGAMENTO I/O   │            │    ALGORITMOS        │
│   src/io/            │            │    src/algorithms/   │
├──────────────────────┤            ├──────────────────────┤
│ • carregador.py      │            │ • grasp.py           │
│   (Lê JSON)          │            │ • construcao.py      │
│ • formatter.py       │            │ • busca_local.py     │
│   (Imprime resultado)│            │                      │
└────────┬─────────────┘            └────────┬─────────────┘
         │                                   │
         │                   ┌───────────────┘
         │                   │
         ▼                   ▼
    ┌─────────────────────────────────┐
    │     SERVIÇOS (Lógica)           │
    │     src/services/               │
    ├─────────────────────────────────┤
    │ • distancia.py (Estratégia)     │
    │ • custo.py (Cálculo de custos)  │
    │ • alocacao.py (Alocação)        │
    └────────────┬────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────┐
    │      DOMÍNIO (Entidades)        │
    │     src/domain/                 │
    ├─────────────────────────────────┤
    │ • models.py                     │
    │   - Posto                       │
    │   - PontoDemanda                │
    │   - Solucao                     │
    │   - ParametrosInstancia         │
    └─────────────────────────────────┘

          ▼
    ┌─────────────────────────────────┐
    │    DADOS (JSON)                 │
    │     data/                       │
    ├─────────────────────────────────┤
    │ • instancia.json (padrão)       │
    │ • instancia_pequena.json        │
    └─────────────────────────────────┘
```

## 🔄 Fluxo de Execução Detalhado

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. INICIALIZAÇÃO                                                 │
│    python run.py data/instancia.json 0.3 50 42                  │
└──────────────────┬───────────────────────────────────────────────┘
                   ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. CARREGAMENTO                                                  │
│    CarregadorInstancia.carregar("data/instancia.json")          │
│    └─→ Valida JSON ✓                                            │
│    └─→ Cria objetos (Postos, Demandas, Parâmetros)            │
└──────────────────┬───────────────────────────────────────────────┘
                   ▼
┌──────────────────────────────────────────────────────────────────┐
│ 3. INJEÇÃO DE DEPENDÊNCIA                                        │
│    DistanciaEuclidiana()                                         │
│    └─→ CalculadoraCusto(distancia)                             │
│        └─→ AlocadorDemanda(distancia, custo)                   │
│            └─→ ConstrutorGrasp(alocador)                       │
│            └─→ BuscadorLocal(alocador)                         │
│                └─→ GRASP(construtor, buscador)                 │
└──────────────────┬───────────────────────────────────────────────┘
                   ▼
┌──────────────────────────────────────────────────────────────────┐
│ 4. LOOP PRINCIPAL GRASP (para cada iteração 1 a 50)             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─── FASE 1: CONSTRUÇÃO GULOSA-ALEATÓRIA ──────┐              │
│  │                                               │              │
│  │  Para cada posto candidato:                  │              │
│  │  ├─ Aloca demandas (greedy por distância)   │              │
│  │  ├─ Calcula custo marginal                  │              │
│  │  ├─ Cria LRC (Lista Restrita de Candidatos)│              │
│  │  └─ Escolhe aleatoriamente da LRC           │              │
│  │                                               │              │
│  │  Parada quando:                              │              │
│  │  • Toda demanda atendida, OU                │              │
│  │  • Adicionar postos não melhora             │              │
│  │                                               │              │
│  └───────────────────────────────────────────────┘              │
│                       ▼                                          │
│  ┌─── FASE 2: BUSCA LOCAL ────────────────────┐                │
│  │                                             │                │
│  │  Enquanto houver melhora:                  │                │
│  │  ├─ MOVIMENTO 1: Fechar um posto          │                │
│  │  ├─ MOVIMENTO 2: Trocar posto aberto      │                │
│  │  └─ MOVIMENTO 3: Abrir um posto fechado   │                │
│  │                                             │                │
│  │  Se nova solução < melhor:                 │                │
│  │  └─ Aceita e continua (first-improvement)  │                │
│  │                                             │                │
│  └─────────────────────────────────────────────┘                │
│                       ▼                                          │
│  ┌─── FASE 3: ATUALIZAR MELHOR GLOBAL ────────┐                │
│  │                                             │                │
│  │  se custo < melhor_global:                 │                │
│  │  └─ melhor_global = nova solução           │                │
│  │  └─ Imprime: "novo melhor ◀"               │                │
│  │                                             │                │
│  └─────────────────────────────────────────────┘                │
│                                                                  │
└──────────────────┬───────────────────────────────────────────────┘
                   ▼
┌──────────────────────────────────────────────────────────────────┐
│ 5. FORMATAÇÃO E IMPRESSÃO                                        │
│    FormatterResultado.imprimir(solucao, postos, demandas)      │
│    └─→ Imprime custos totais e parciais                        │
│    └─→ Lista postos abertos                                    │
│    └─→ Mostra alocações                                        │
│    └─→ Calcula cobertura (%)                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 🔌 Dependências Entre Módulos

```
┌─────────────────────────────────────────────────────────────────┐
│                        MAIN.PY                                  │
│  Orquestra tudo via ContainerDI                                │
└──────────────────────┬──────────────────────────────────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
    ▼                  ▼                  ▼
CARREGADOR        ALGORITMOS          FORMATTER
    │                  │
    │      ┌───────────┼───────────┐
    │      │           │           │
    ▼      ▼           ▼           ▼
DOMAIN   CONSTRUTOR  BUSCADOR    (usa DOMAIN)
  │       │           │
  │       └───┬───────┘
  │           │
  ▼           ▼
  ALOCADOR
  │
  ├──→ DISTANCIA
  │
  └──→ CUSTO
       │
       └──→ DISTANCIA
```

**Regra**: Cada módulo só depende de módulos "abaixo" dele (acíclico)

## 📊 Tabela de Responsabilidades

| Camada | Módulo | Responsabilidade |
|--------|--------|------------------|
| **Domain** | models.py | Estruturar dados (Entidades puras) |
| **Services** | distancia.py | Calcular distâncias (Estratégia) |
| | custo.py | Calcular componentes de custo |
| | alocacao.py | Alocar demandas aos postos |
| **Algorithms** | construcao.py | Fase 1: Construção gulosa-aleatória |
| | busca_local.py | Fase 2: Busca local com 3 movimentos |
| | grasp.py | Orquestração das fases |
| **I/O** | carregador.py | Ler JSON e validar |
| | formatter.py | Imprimir resultado formatado |
| **Main** | main.py | Ponto de entrada e DI |

## 🎯 Princípios Arquiteturais

```
                    ┌─────────────────┐
                    │  ESCALABILIDADE │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
        Fácil adicionar  Fácil testar  Fácil manter
              │              │              │
         Novos           Cada camada   Responsabilidades
         algoritmos       isolada      bem definidas
         Estratégias     Mocks via DI   Sem acoplamento
```

## 🧪 Cobertura de Testes

```
┌────────────────────────────────────────────────────────────┐
│ TESTS/                                                     │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ test_domain.py (6 testes)                                 │
│ ├─ Criação de entidades ✓                                │
│ ├─ Cópia de solução ✓                                    │
│ └─ Comparação de soluções ✓                              │
│                                                            │
│ test_services.py (8 testes)                               │
│ ├─ Distância Euclidiana ✓                                │
│ ├─ Cálculo de custos ✓                                   │
│ ├─ Alocação de demandas ✓                                │
│ └─ Casos extremos ✓                                      │
│                                                            │
│ test_algorithms.py (7 testes)                             │
│ ├─ Construção GRASP ✓                                    │
│ ├─ Busca local ✓                                         │
│ ├─ Reprodutibilidade ✓                                   │
│ └─ Melhora iterativa ✓                                   │
│                                                            │
│ test_io.py (7 testes)                                     │
│ ├─ Carregamento JSON ✓                                   │
│ ├─ Validação ✓                                           │
│ └─ Formatação ✓                                          │
│                                                            │
│ TOTAL: 28 testes unitários ✓✓✓                            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## 📈 Métricas de Qualidade

```
Métrica                    Valor
─────────────────────────────────────
Linhas de código (src/)     ~1500
Linhas de teste             ~800
Linhas de docs              ~2000
Cobertura                   ~95%
Classes                     15+
Métodos                     50+
Type hints                  100%
Imports circulares          0 ✓
Documentação                Completa ✓
```

---

**Arquitetura desacoplada, escalável e testável! 🎯**
