# Colinha de Apresentacao - Projeto Vacinacao (Busca Tabu)

## 1) Resumo em 20 segundos

Este projeto resolve um problema de localizacao e alocacao de vacinacao.
A ideia e decidir quais postos abrir e como alocar cada demanda para reduzir o custo total.
O metodo principal atual e a **Busca Tabu** (Tabu Search), que avalia a vizinhanca e usa memoria para escapar de otimos locais.

Formula principal:

- custo_total = custo_abertura + custo_distancia + custo_nao_atendimento

## 2) Problema que o projeto resolve

Entrada:

- Postos com: capacidade, custo de abertura e coordenadas
- Demandas com: populacao e coordenadas
- Parametros: custo por km e penalidade por nao atendimento

Saida:

- Quais postos abrir
- Como as demandas foram alocadas
- Quanto ficou cada componente de custo
- Cobertura total da populacao

## 3) Arquitetura (1 slide)

Camadas:

1. Domain: entidades puras
2. Services: distancia, custo e alocacao
3. Algorithms: construcao, busca_local, grasp, e **tabu_search** (novo)
4. IO: carrega JSON e formata resultado
5. Main: orquestracao e injeccao de dependencia

Arquivos importantes:

- src/domain/models.py
- src/services/alocacao.py
- src/algorithms/tabu_search.py (Implementacao da Busca Tabu)
- src/main.py

## 4) Fluxo da execucao (falar como pipeline)

1. Carrega a instancia JSON
2. Monta os servicos e algoritmos via DI
3. Gera Solucao Inicial (via construcao Gulosa)
4. Roda N iteracoes da Busca Tabu:
   - Avalia a vizinhanca completa (Drop, Add, Swap)
   - Verifica Lista Tabu + Criterio de Aspiracao
   - Atualiza para o melhor vizinho validado
   - Registra o movimento invertido na memoria (Lista Tabu)
5. Imprime melhor solucao final

## 5) Como a BUSCA TABU funciona (essencia)

Diferente do GRASP, a Busca Tabu avalia os vizinhos e pode ir para uma solucao com um custo "pior" para nao ficar presa num otimo local.

Movimentos explorados:
- **Drop**: Fechar um posto aberto
- **Add**: Abrir um posto fechado
- **Swap**: Trocar um posto aberto por um fechado

Memoria (Lista Tabu):
- Se eu adicionar um posto, remover ele vira "tabu" (proibido) por *T* iteracoes (Tabu Tenure).
- O mesmo vale para Drop e Swap (guarda os movimentos reversos).

Criterio de Aspiracao:
- Se um movimento e proibido (tabu), mas gera um custo MAIS BARATO que o **melhor global** encontrado ate agora, a proibicao e ignorada.

## 6) Parametros que voce pode justificar

- **modo**: `tabu` (padrão) ou `grasp`.
- **tabu_tenure / alpha**: 
  - Se for "tabu", esse campo indica quantas iteracoes o movimento fica proibido na memoria (padrao 5).
- **iteracoes**:
  - Mais iteracoes -> avalia mais espacos, chance maior de melhora.

Configuracao boa para demo:

- `python run.py data/instancia.json tabu 5 50`

## 7) Como explicar a saida no terminal

Durante iteracoes:

- vz_custo: o custo real do vizinho escolhido nesta rodada
- mov: qual movimento foi feito (add X, drop Y, ou swap X->Y)
- global: o melhor custo absoluto do historico

No final:

- custo total e componentes
- postos abertos
- alocacao de cada demanda
- percentual de cobertura

## 8) Roteiro pronto de fala (5 a 7 minutos)

### Abertura (30s)

Hoje eu vou apresentar um sistema de otimizacao para distribuicao de vacinacao.
Ele decide abertura de postos e alocacao de demanda minimizando custo total.

### Modelagem (1min)

Cada posto tem capacidade, custo fixo e localizacao.
Cada demanda tem populacao e localizacao.
O custo total soma abertura, deslocamento e nao atendimento.

### Metodo (2min)

Nosso motor principal e a **Busca Tabu**.
Para iniciar, geramos uma solucao gulosa (a tentativa mais inteligente partindo do zero).
Depois, exploramos todos os vizinhos validos adicionando, removendo ou trocando postos de vacinacao simultaneamente.
O segredo desse algoritmo contra os convencionais e a *Lista Tabu*: movimentos feitos recentemente sao proibidos de serem desfeitos por algumas iteracoes para forcar a exploracao global e evitar andar em circulos.

### Engenharia de software (1min)

O projeto esta em camadas desacopladas.
A metaheuristica original era GRASP, e a transicao para Tabu Search foi simples gracas ao design.
O dominio e separado de servicos, e o Main faz a orquestracao via Dependency Injection.

### Fechamento (30s)

O resultado final e um sistema performatico, modular, com uma memoria eficaz de heuristica e metricas ricas como cobertura %.
Agradeco e fico aberto a perguntas.

## 9) Perguntas provaveis da banca + resposta curta

1. **Por que Busca Tabu?**
   - Porque evitar ficar iterando no mesmo loop (otimo local) e o maior beneficio usando uma lista de transicoes proibidas temporarias.

2. **Qual a lista tabu?**
   - Um dicionario registrando ate que iteracao o "movimento reverso" ao recem-tomado e proibido.

3. **O que e criterio de aspiracao?**
   - E a excessao: se um movimento era proibido mas quebrar meu recorde de "A Solucao Absoluta", eu acato!

4. **Por que no output o custo vizinho piora (sobe)?**
   - Essa e a principal vantagem do algoritimo. Ele e disfarcado para "subir a montanha" se for o melhor movimento disponivel nao restrito pra depois achar um vale melhor!

## 10) Limites atuais e melhorias futuras

Melhorias:

- Limitar a exploracao de vizinhanca com busca hibrida em bases de dados gigantes.
- Trocar o tamanho da tenure dinamicamente caso o algoritimo encerre preso.

## 11) Comandos rapidos para a apresentacao

- Execucao padrao Tabu:
  - `python run.py data/instancia.json tabu 5 50`

- Voltar pro GRASP tradicional pra explicar mudanca se pedirem:
  - `python run.py data/instancia.json grasp 0.3 50`

## 12) Frase final pronta

Em resumo, o trabalho entrega uma solucao pratica e modular para alocacao de vacinacao,
com GRASP para boa qualidade em tempo viavel, resultados reprodutiveis e arquitetura pronta
para evolucao.

## 13) Guia arquivo por arquivo (implementacao completa)

Esta secao e para voce saber exatamente o papel de cada arquivo.

### Arquivos da raiz

- .gitignore
  - Diz ao Git quais arquivos/pastas nao devem ser versionados (cache, venv, builds etc).

- ARCHITECTURE.md
  - Documento visual da arquitetura em camadas e fluxo de execucao.

- CHECKLIST.md
  - Lista de tudo que foi implementado na refatoracao (camadas, testes, docs, scripts).

- COLINHA_APRESENTACAO.md
  - Sua cola de apresentacao (este arquivo).

- DESIGN.md
  - Explica padroes de design usados (DI, Strategy, SRP) e exemplos de extensao.

- INDEX.md
  - Mapa de navegacao da documentacao do projeto.

- INSTALL.md
  - Passo a passo de instalacao, execucao e troubleshooting.

- QUICKREF.md
  - Comandos rapidos e parametros principais para uso diario.

- README.md
  - Visao geral do projeto: objetivo, estrutura, formato de entrada e como rodar.

- SUMMARY.md
  - Resumo executivo da refatoracao e metricas gerais.

- grasp_vacinacao.py
  - Versao monolitica original do projeto (tudo em um arquivo).
  - Mantido como referencia historica.
  - A implementacao atual em producao esta em src/.

- instancia_exemplo.json
  - Exemplo de instancia legado, usado pelo script monolitico antigo.

- pyproject.toml
  - Metadados do projeto Python (nome, versao, python minimo, build-system).

- requirements.txt
  - Dependencias externas. Hoje praticamente vazio (usa stdlib do Python).

- run.py
  - Script principal recomendado para executar o sistema atual.
  - So repassa para src.main.main().

- run.bat
  - Script de execucao para Windows.
  - Detecta Python no PATH e executa run.py.

- run.sh
  - Script de execucao para Linux/Mac.
  - Detecta python3/python e executa run.py.

### Pasta src/ (codigo atual)

- src/__init__.py
  - Marca src como pacote Python.

- src/main.py
  - Ponto de entrada real da aplicacao.
  - Faz parse de argumentos, carrega instancia, cria dependencias (DI), roda GRASP e imprime resultado.

### Pasta src/domain/

- src/domain/__init__.py
  - Exporta as entidades principais do dominio.

- src/domain/models.py
  - Define os dataclasses do problema:
    - Posto
    - PontoDemanda
    - Solucao
    - ParametrosInstancia
  - Aqui nao tem regra de negocio pesada, apenas estrutura de dados.

### Pasta src/services/

- src/services/__init__.py
  - Exporta os servicos da camada.

- src/services/distancia.py
  - Interface CalculadoraDistancia e implementacao DistanciaEuclidiana.
  - Centraliza calculo geometrico.

- src/services/custo.py
  - Calcula custo de abertura, distancia e nao atendimento.
  - Recalcula custo total de uma Solucao.

- src/services/alocacao.py
  - Faz a alocacao gulosa da demanda para postos abertos com base em distancia e capacidade.
  - Chama calculadora de custo para retornar Solucao completa.

### Pasta src/algorithms/

- src/algorithms/__init__.py
  - Exporta as classes de algoritmo.

- src/algorithms/construcao.py
  - Fase de construcao do GRASP.
  - Avalia candidatos, monta LRC com alpha e escolhe aleatoriamente.

- src/algorithms/busca_local.py
  - Fase de busca local.
  - Testa 3 movimentos (fechar, trocar, abrir) e aceita primeira melhora.

- src/algorithms/grasp.py
  - Orquestra o GRASP completo por iteracoes:
    - construcao
    - busca local
    - atualizacao da melhor solucao global

### Pasta src/io/

- src/io/__init__.py
  - Exporta utilitarios de I/O.

- src/io/carregador.py
  - Le e valida arquivo JSON de entrada.
  - Converte JSON em objetos de dominio.

- src/io/formatter.py
  - Formata e imprime o resultado final no terminal.
  - Mostra custos, postos, alocacoes e cobertura.

### Pasta data/

- data/README.md
  - Documentacao das instancias e formato de dados.

- data/instancia.json
  - Instancia padrao usada por default no run.py.

- data/instancia_pequena.json
  - Instancia menor para testes rapidos.

### Pasta tests/

- tests/__init__.py
  - Marca pasta de testes como pacote.

- tests/test_domain.py
  - Testa entidades do dominio (criacao, copia, comparacao).

- tests/test_services.py
  - Testa distancia, custo e alocacao.

- tests/test_algorithms.py
  - Testa construcao GRASP, busca local, reprodutibilidade e melhora iterativa.

- tests/test_io.py
  - Testa carregamento de JSON, validacoes e formatter.

## 14) Ordem ideal para estudar implementacao (sem se perder)

Se voce nao domina o codigo ainda, siga exatamente esta ordem:

1. src/domain/models.py
2. src/services/distancia.py
3. src/services/custo.py
4. src/services/alocacao.py
5. src/algorithms/construcao.py
6. src/algorithms/busca_local.py
7. src/algorithms/grasp.py
8. src/io/carregador.py
9. src/io/formatter.py
10. src/main.py
11. tests/test_services.py e tests/test_algorithms.py

Com essa ordem, voce entende primeiro os dados, depois a logica, depois o algoritmo completo.

## 15) Quem chama quem (mapa mental rapido)

- run.py -> src/main.py
- src/main.py -> src/io/carregador.py
- src/main.py -> src/algorithms/grasp.py
- src/algorithms/grasp.py -> src/algorithms/construcao.py
- src/algorithms/grasp.py -> src/algorithms/busca_local.py
- construcao/busca_local -> src/services/alocacao.py
- alocacao -> src/services/distancia.py
- alocacao -> src/services/custo.py
- src/main.py -> src/io/formatter.py

## 16) Se te perguntarem "onde fica X?"

- "Entidades do problema" -> src/domain/models.py
- "Calculo de custo" -> src/services/custo.py
- "Alocacao da demanda" -> src/services/alocacao.py
- "Heuristica GRASP" -> src/algorithms/grasp.py
- "Construcao com alpha/LRC" -> src/algorithms/construcao.py
- "Busca local" -> src/algorithms/busca_local.py
- "Leitura de JSON" -> src/io/carregador.py
- "Impressao de resultado" -> src/io/formatter.py
- "Orquestracao e CLI" -> src/main.py
- "Testes" -> tests/

## 17) Frase de seguranca para usar na apresentacao

Se eu tivesse que resumir a implementacao em uma frase:

"O src/main.py so orquestra; a regra de negocio esta separada em services; a metaheuristica esta em algorithms; e tudo e validado por testes em tests/."
### 🗂️ A Regra de «Postos vs Escolas»
Para garantir que o Tabu Search dê prioridade a Postos de Saúde em vez de Escolas:
1. **JSONs e models.py:** Adicionada a propriedade 	ipo (posto_saude ou escola) e prioridade (1 ou 2).
2. **services/custo.py:** O custo de abertura agora é multiplicado pela prioridade. Se tentar abrir uma escola (prioridade 2), o custo real fica o dobro. Assim a Busca Tabu **sempre prefere** Postos de Saúde primeiro.
