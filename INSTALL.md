# Guia de Instalação e Setup

## 🐍 Instalação do Python

### Windows

1. Acesse [python.org](https://www.python.org/downloads/)
2. Baixe Python 3.9 ou superior
3. **Importante**: Marque "Add Python to PATH" durante instalação
4. Verifique:
   ```bash
   python --version
   ```

### macOS

```bash
# Com Homebrew
brew install python3

# Ou baixe de python.org
```

### Linux

```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# Fedora
sudo dnf install python3

# Arch
sudo pacman -S python
```

## 📦 Setup do Projeto

### 1. Clone ou baixe o projeto

```bash
cd metaheurisitcas/
```

### 2. (Opcional) Crie ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale dependências (opcional)

```bash
# Sem dependências externas - só usa stdlib!
# Mas se quiser rodar testes com pytest:
pip install pytest
```

## 🚀 Executar o Programa

### Opção 1: Script Python

```bash
# Windows/Linux/Mac
python run.py

# Com parâmetros
python run.py data/instancia.json 0.5 100 42
```

### Opção 2: Script Nativo (Windows)

```bash
# No PowerShell ou CMD
.\run.bat
.\run.bat data/instancia.json 0.5 100 42
```

### Opção 3: Script Shell (Linux/Mac)

```bash
# Dar permissão e executar
chmod +x run.sh
./run.sh
./run.sh data/instancia.json 0.5 100 42
```

### Opção 4: Módulo Python

```bash
python -m src.main data/instancia.json 0.3 50
```

## 🧪 Rodar Testes

```bash
# Com unittest (nativa)
python -m unittest discover tests/ -v

# Com pytest (mais legível)
pytest tests/ -v

# Teste específico
python -m unittest tests.test_services.TestCalculadoraCusto -v
```

## 📊 Verificar Instalação

```bash
# Verifica se todos os módulos podem ser importados
python -c "from src.algorithms import GRASP; print('✓ Importação OK')"

# Lista estrutura de arquivos
ls -la src/
```

## ⚠️ Problemas Comuns

### "Python não encontrado"
- Windows: Reinstale Python e marque "Add to PATH"
- Linux: `sudo apt-get install python3`
- Mac: `brew install python3`

### "ModuleNotFoundError"
- Execute do diretório raiz do projeto
- Verifique que `src/__init__.py` existe

### "JSON não encontrado"
- Crie `data/instancia.json` ou especifique o caminho
- Verifique permissões de leitura

## 💡 Dicas

- Use `python -m src.main` sem argumentos para usar instância padrão
- Use seed para reproduzir resultados: `python run.py data/instancia.json 0.3 50 42`
- Aumente iterações para instâncias maiores: `python run.py data/instancia.json 0.5 200`
