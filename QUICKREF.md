# Quick Reference - Guia Rápido

## 🚀 Começar em 30 Segundos

```bash
# 1. Navegue até a pasta
cd metaheurisitcas

# 2. Execute (instância padrão)
python run.py
```

## 📚 Comandos Principais

### Executar

```bash
# Instância padrão
python run.py

# Instância customizada
python run.py data/instancia_pequena.json

# Com parâmetros GRASP
python run.py data/instancia.json 0.5 100 42
#                                  ↑   ↑   ↑
#                              alpha   iterações  seed
```

### Testar

```bash
# Todos os testes
python -m unittest discover tests/ -v

# Testes específicos
python -m unittest tests.test_services -v
python -m unittest tests.test_domain.TestSolucao -v
```

### Via Módulo

```bash
python -m src.main data/instancia.json
```

## 🎛️ Parâmetros GRASP

| Parâmetro | Intervalo | Padrão | Efeito |
|-----------|-----------|--------|--------|
| alpha (α) | 0 - 1 | 0.3 | 0=guloso, 1=aleatório |
| iterações | 1 - ∞ | 50 | Mais iterações = melhor (mais lento) |
| seed | 0 - 2^32 | aleatório | Reproduzir resultados |

### Recomendações

```bash
# Rápido (< 5s)
python run.py data/instancia.json 0.3 10

# Balanceado (recomendado)
python run.py data/instancia.json 0.3 50

# Exploração profunda (> 30s)
python run.py data/instancia.json 0.5 200

# Guloso puro (determinístico)
python run.py data/instancia.json 0.0 1 42
```

## 📁 Estrutura Essencial

```
src/
  ├── domain/       → Modelos (Posto, Demanda, Solucao)
  ├── services/     → Serviços (Distância, Custo, Alocação)
  ├── algorithms/   → Algoritmos (Construção, BL, GRASP)
  ├── io/          → I/O (Carregamento, Formatação)
  └── main.py      → Ponto de entrada

data/
  └── instancia.json → Dados de entrada

tests/
  ├── test_domain.py
  ├── test_services.py
  ├── test_algorithms.py
  └── test_io.py
```

## 🔍 Entender a Saída

```
iter   1 | construção:    15000.00 | após BL:     14500.00 | melhor:     14500.00 ◀ novo melhor
         ↑                 ↑                          ↑
    Iteração        Custo construção          Melhor global
                                          ◀ Indicador de novo melhor
```

**Custos:**
- Abertura: Custo de abrir cada posto
- Distância: Custo de transporte (população × km × custo_por_km)
- Não-atendimento: Demanda não coberta × custo_nao_atendimento

## ⚙️ Personalizar JSON

Edite `data/instancia.json`:

```json
{
  "parametros": {
    "custo_por_km": 2.5,              ← Ajuste conforme necessário
    "custo_nao_atendimento": 500      ← Mais = penaliza não-atendimento
  },
  "postos": [
    {
      "id": 1,
      "nome": "Seu Posto",
      "capacidade": 800,              ← Máximo de pessoas
      "custo_abertura": 3000,         ← Custo fixo
      "x": 5.0,                       ← Coordenada X
      "y": 5.0                        ← Coordenada Y
    }
  ],
  "demandas": [
    {
      "id": 1,
      "nome": "Seu Bairro",
      "populacao": 700,               ← Pessoas a vacinar
      "x": 5.0,
      "y": 5.5
    }
  ]
}
```

## 🧪 Testar Sua Implementação

```bash
# 1. Verifique imports
python -c "from src.algorithms import GRASP; print('OK')"

# 2. Rode testes
python -m unittest tests.test_domain -v

# 3. Execute programa
python run.py

# 4. Reproduza resultado
python run.py data/instancia.json 0.3 50 42
```

## 🐛 Problemas Comuns

| Problema | Solução |
|----------|---------|
| Python não encontrado | Instale Python e adicione ao PATH |
| ModuleNotFoundError | Execute do diretório raiz (`metaheurisitcas/`) |
| FileNotFoundError | Crie `data/instancia.json` ou especifique caminho |
| JSON inválido | Valide em [jsonlint.com](https://www.jsonlint.com/) |

## 📊 Exemplo: Comparar Soluções

```bash
# Guloso puro
python run.py data/instancia.json 0.0 1 42

# GRASP recomendado
python run.py data/instancia.json 0.3 50 42

# Mais exploração
python run.py data/instancia.json 0.7 100 42
```

Compare os custos finais para entender o impacto de α.

## 💾 Adicionar Nova Instância

1. Crie `data/minha_instancia.json`
2. Garanta formato correto
3. Execute: `python run.py data/minha_instancia.json`

## 📖 Documentação

- **README.md** - Visão geral e uso
- **INSTALL.md** - Setup e instalação
- **DESIGN.md** - Arquitetura e padrões
- **CHECKLIST.md** - O que foi implementado
- **data/README.md** - Dados e instâncias

## 🎓 Aprenda Mais

```bash
# Ver código de distância
cat src/services/distancia.py

# Ver testes de algoritmo
cat tests/test_algorithms.py

# Ver estrutura de dados
cat src/domain/models.py
```

## ⏱️ Performance

```bash
# Instância pequena (5 postos, 5 demandas)
python run.py data/instancia_pequena.json 0.3 50
# ~ 0.5 segundos

# Instância média (10 postos, 10 demandas)
python run.py data/instancia.json 0.3 50
# ~ 5-10 segundos

# Instância grande (50+ postos)
python run.py data/instancia_grande.json 0.3 100
# ~ 30-60 segundos
```

## 🔗 Fluxo Rápido

```
Carregar JSON
    ↓
Criar Serviços (DI)
    ↓
Para cada iteração:
  └─ Construir solução inicial (GRASP)
  └─ Melhorar com Busca Local
  └─ Atualizar melhor global
    ↓
Imprimir resultado
```

---

**Dúvidas? Veja os arquivos de documentação completos!** 📚
