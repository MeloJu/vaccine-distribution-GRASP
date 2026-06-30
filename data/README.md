# Instâncias

Arquivos JSON com instâncias do problema de alocação de postos de vacinação.

## Arquivos

### `instancia.json` — padrão
- 10 postos candidatos, 10 bairros
- 3.960 pessoas no total
- Tempo estimado: < 5 s (50 iterações)

### `instancia_pequena.json` — reduzida
- 5 postos candidatos, 5 bairros
- Útil para testes rápidos

## Como usar

```bash
# Instância padrão
python run.py

# Instância específica com parâmetros
python -m src.main data/instancia_pequena.json 5 50
```

## Formato

```json
{
  "parametros": {
    "custo_por_km": 2.5,
    "custo_nao_atendimento": 500
  },
  "postos": [
    {"id": 1, "nome": "Posto A", "capacidade": 800, "custo_abertura": 3000, "x": 5.0, "y": 5.0}
  ],
  "demandas": [
    {"id": 1, "nome": "Bairro A", "populacao": 700, "x": 5.0, "y": 5.5}
  ]
}
```

Para adicionar uma nova instância, salve o arquivo em `data/` e passe o caminho como primeiro argumento.
