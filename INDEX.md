# 📑 Índice de Documentação

Bem-vindo ao projeto GRASP Vacinação! Este índice ajuda a encontrar a informação que você precisa.

## 🚀 Primeiros Passos

1. **[QUICKREF.md](QUICKREF.md)** ← **COMECE AQUI** (30 segundos)
   - Comandos rápidos
   - Exemplos básicos
   - Solução de problemas

2. **[INSTALL.md](INSTALL.md)** (5 minutos)
   - Instalação de Python
   - Setup do projeto
   - Verificação

## 📚 Documentação Completa

### Para Usuários
- **[README.md](README.md)** - Visão geral completa
  - Estrutura do projeto
  - Como usar
  - Formato de dados
  - Configuração GRASP
  
- **[QUICKREF.md](QUICKREF.md)** - Referência rápida
  - Comandos principais
  - Parâmetros
  - Recomendações
  
- **[data/README.md](data/README.md)** - Dados e instâncias
  - Instâncias disponíveis
  - Como criar nova instância
  - Validação

### Para Desenvolvedores
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Visão da arquitetura
  - Camadas
  - Fluxo de execução
  - Dependências
  - Responsabilidades

- **[DESIGN.md](DESIGN.md)** - Padrões de Design
  - SOLID principles
  - Design patterns implementados
  - Exemplos de código
  - Como estender

- **[CHECKLIST.md](CHECKLIST.md)** - O que foi implementado
  - Checklist completo
  - Estatísticas
  - Próximos passos

### Para Testes
- **tests/** - Suite completa
  - test_domain.py (6 testes)
  - test_services.py (8 testes)
  - test_algorithms.py (7 testes)
  - test_io.py (7 testes)

## 🗂️ Estrutura de Arquivos

```
metaheurisitcas/
├── 📄 README.md              ← Comece aqui (visão geral)
├── 🚀 QUICKREF.md            ← Referência rápida
├── 💻 INSTALL.md             ← Instalação e setup
├── 🏗️ ARCHITECTURE.md         ← Visão da arquitetura
├── 🎓 DESIGN.md              ← Padrões e exemplos
├── ✅ CHECKLIST.md           ← O que foi feito
│
├── 📁 src/                   ← Código-fonte
│   ├── main.py               ← Ponto de entrada
│   ├── domain/               ← Entidades
│   ├── services/             ← Lógica reutilizável
│   ├── algorithms/           ← Algoritmos GRASP
│   └── io/                   ← I/O (JSON, prints)
│
├── 📁 data/                  ← Dados de entrada
│   ├── instancia.json        ← Instância padrão (10 postos)
│   ├── instancia_pequena.json← Instância pequena (5 postos)
│   └── README.md             ← Documentação de dados
│
├── 🧪 tests/                 ← Testes unitários
│   ├── test_domain.py
│   ├── test_services.py
│   ├── test_algorithms.py
│   └── test_io.py
│
├── 🎬 run.py                 ← Script Python
├── 🪟 run.bat                ← Script Windows
├── 🐧 run.sh                 ← Script Linux/Mac
│
├── 📦 pyproject.toml         ← Metadados do projeto
├── 📋 requirements.txt       ← Dependências
└── .gitignore               ← Configuração Git
```

## 🎯 Navegação por Tarefa

### "Quero executar o programa"
1. [QUICKREF.md](QUICKREF.md#-começar-em-30-segundos)
2. `python run.py`

### "Quero entender a arquitetura"
1. [ARCHITECTURE.md](ARCHITECTURE.md)
2. [DESIGN.md](DESIGN.md)

### "Quero adicionar um novo algoritmo"
1. [DESIGN.md](DESIGN.md#-extensão-adicionar-novo-algoritmo)
2. [ARCHITECTURE.md](ARCHITECTURE.md#-princípios-arquiteturais)

### "Quero modificar os dados"
1. [data/README.md](data/README.md)
2. Edite `data/instancia.json`

### "Quero rodar os testes"
1. [QUICKREF.md](QUICKREF.md#-testar)
2. `python -m unittest discover tests/ -v`

### "Tenho um problema"
1. [QUICKREF.md](QUICKREF.md#-problemas-comuns)
2. [INSTALL.md](INSTALL.md#-problemas-comuns)

## 📊 Mapa Mental

```
                  COMEÇAR AQUI
                      │
        ┌─────────────┼─────────────┐
        │             │             │
    Usuário       Dev/Design     Testes
        │             │             │
    QUICKREF      ARCHITECTURE   tests/
        │             │             │
    run.py         DESIGN       test_*.py
        │             │             │
    data/        code review   Coverage
```

## 🔑 Conceitos-Chave

| Conceito | Onde ler | Para quem |
|----------|----------|----------|
| GRASP | [README.md](README.md) | Todos |
| Arquitetura em Camadas | [ARCHITECTURE.md](ARCHITECTURE.md) | Devs |
| SOLID Principles | [DESIGN.md](DESIGN.md) | Devs |
| Testes Unitários | [CHECKLIST.md](CHECKLIST.md) | QA/Devs |
| Parametrização | [QUICKREF.md](QUICKREF.md) | Usuários |
| Formato JSON | [data/README.md](data/README.md) | Todos |

## 📞 Suporte Rápido

**"Como faço para...?"**

| Pergunta | Documento | Seção |
|----------|-----------|-------|
| ...executar o programa? | QUICKREF | Comandos Principais |
| ...entender o código? | ARCHITECTURE | Fluxo de Execução |
| ...adicionar um novo algoritmo? | DESIGN | Extensão |
| ...mudar os parâmetros? | QUICKREF | Parâmetros GRASP |
| ...rodar testes? | QUICKREF | Testar |
| ...criar nova instância? | data/README | Criar Nova Instância |
| ...instalar Python? | INSTALL | Python |
| ...solucionar um erro? | QUICKREF | Problemas Comuns |

## 🎓 Sequência de Leitura Recomendada

### Para Usuários
1. Este INDEX (você está aqui)
2. [QUICKREF.md](QUICKREF.md) - 5 min
3. [data/README.md](data/README.md) - 2 min
4. [README.md](README.md) - 10 min

### Para Desenvolvedores
1. Este INDEX (você está aqui)
2. [QUICKREF.md](QUICKREF.md) - 5 min
3. [ARCHITECTURE.md](ARCHITECTURE.md) - 15 min
4. [DESIGN.md](DESIGN.md) - 20 min
5. Código em `src/` - 30 min
6. [CHECKLIST.md](CHECKLIST.md) - 5 min

### Para QA/Testes
1. Este INDEX (você está aqui)
2. [QUICKREF.md](QUICKREF.md) - 5 min
3. [CHECKLIST.md](CHECKLIST.md) - 10 min
4. Rodar: `python -m unittest discover tests/ -v` - 5 min

## 🌟 Destaques

✅ **28 Testes Unitários**
✅ **Arquitetura em Camadas**
✅ **Padrões de Design aplicados**
✅ **100% Documentado**
✅ **Totalmente Desacoplado**
✅ **Facilmente Escalável**

## 💬 Dúvidas Frequentes

**"Por onde começar?"**
→ [QUICKREF.md](QUICKREF.md)

**"Como funciona internamente?"**
→ [ARCHITECTURE.md](ARCHITECTURE.md)

**"Como estendo o projeto?"**
→ [DESIGN.md](DESIGN.md)

**"Está completo?"**
→ [CHECKLIST.md](CHECKLIST.md)

---

**Escolha seu caminho acima e bom proveito!** 🚀

*Última atualização: 2026-04-20*
