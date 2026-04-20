# Pasta Data - Instâncias de Teste

Contém arquivos JSON com instâncias do problema de alocação de postos de vacinação.

## 📄 Arquivos Disponíveis

### `instancia.json` (Padrão)
**Recomendada para começar**
- 10 postos de vacinação
- 10 pontos de demanda
- ~5800 pessoas total
- Complexidade: Média
- Tempo estimado: 5-10 segundos (50 iterações)

### `instancia_pequena.json`
**Para testes rápidos**
- 5 postos
- 5 pontos de demanda
- ~5700 pessoas total
- Complexidade: Baixa
- Tempo estimado: < 1 segundo (50 iterações)

## 🔧 Como Usar

### Execução com Instância Padrão
```bash
python run.py
```

### Execução com Instância Específica
```bash
python run.py data/instancia_pequena.json
python run.py data/instancia.json 0.5 100 42
```

## 📋 Formato de Arquivo

Cada arquivo JSON deve ter:

```json
{
  "parametros": {
    "custo_por_km": float,
    "custo_nao_atendimento": float
  },
  "postos": [
    {
      "id": int,
      "nome": string,
      "capacidade": int,
      "custo_abertura": float,
      "x": float,
      "y": float
    }
  ],
  "demandas": [
    {
      "id": int,
      "nome": string,
      "populacao": int,
      "x": float,
      "y": float
    }
  ]
}
```

## ✅ Validação

O programa valida automaticamente:
- ✅ Arquivo existe
- ✅ JSON válido
- ✅ Estrutura completa (parametros, postos, demandas)
- ✅ Tipos corretos para cada campo

Se houver erro, veja a mensagem e corrija o JSON.

## 💡 Criar Nova Instância

1. Copie `instancia.json`
2. Modifique com seus dados
3. Garanta que IDs são únicos
4. Salve em `data/`
5. Execute: `python run.py data/seu_arquivo.json`

### Exemplo Customizado

```json
{
  "parametros": {
    "custo_por_km": 10.0,
    "custo_nao_atendimento": 500
  },
  "postos": [
    {"id": 1, "nome": "Posto A", "capacidade": 500, "custo_abertura": 2000, "x": 0.0, "y": 0.0},
    {"id": 2, "nome": "Posto B", "capacidade": 400, "custo_abertura": 1800, "x": 5.0, "y": 5.0}
  ],
  "demandas": [
    {"id": 1, "nome": "Bairro 1", "populacao": 300, "x": 1.0, "y": 1.0},
    {"id": 2, "nome": "Bairro 2", "populacao": 250, "x": 4.0, "y": 4.0}
  ]
}
```

## 🎯 Dicas

- **Pequenas instâncias**: Use para testar/validar
- **Grandes instâncias**: Aumente `alpha` e iterações
- **Reproduce resultados**: Use a mesma seed
- **Compare soluções**: Rode múltiplas vezes com seeds diferentes
