# 🚀 Projeto Artemis: Simulador de Resposta a Queimadas PyrosAI

## 🎯 Visão Geral do Projeto

O **Projeto Artemis** é um sistema **simulado** de gerenciamento e resposta a ocorrências de queimadas, desenvolvido para demonstrar a aplicação prática de estruturas de dados e algoritmos. O coração do sistema é a **PyrosAI**, uma inteligência artificial (simulada) responsável por otimizar a detecção, avaliação de risco e alocação de recursos para combater incêndios florestais.

Este projeto visa ilustrar como conceitos de **Grafos (NetworkX)**, **Dicionários**, **Filas de Prioridade (Heapq)**, **Busca Binária** e **Memorização (`functools.lru_cache`)** podem ser integrados para resolver um problema complexo e de grande impacto social, como o combate a queimadas.

## ✨ Destaques Tecnológicos e Conceituais

Este simulador foi cuidadosamente construído para exemplificar os seguintes conceitos:

  * **Dicionários**: Utilizados extensivamente para armazenamento e recuperação eficiente de dados, como as ocorrências ativas (`ocorrencias_ativas`) e mapeamentos de severidade (`SEVERIDADES`). Oferecem acesso de complexidade **O(1)**.
  * **Filas de Prioridade (Heapq)**: Implementadas para gerenciar a ordem de atendimento das queimadas, garantindo que as ocorrências de maior severidade (criticidade) sejam priorizadas. Inserção e remoção em heaps têm complexidade **O(log N)**.
  * **Busca Binária**: Demonstrada na funcionalidade de busca por severidade, mostrando a eficiência de busca em listas ordenadas, com complexidade **O(log N)** (após uma ordenação inicial de **O(N log N)** para fins didáticos).
  * **Modelagem com Grafos (NetworkX.DiGraph)**:
      * As **localizações** (bases de equipes, florestas, vilas) são modeladas como **nós (vértices)**.
      * As **rotas** entre essas localizações são representadas como **arestas (edges) direcionadas** com **pesos (`weight`)**, simulando distâncias ou tempos de viagem. O uso do `DiGraph` (Grafo Direcionado) permite rotas assimétricas.
      * A **PyrosAI** utiliza algoritmos de **caminho mais curto** (Dijkstra, implementado eficientemente pelo NetworkX, com complexidade típica de **O(E log V)**) para determinar a rota mais eficiente da base da equipe até o foco da queimada.
  * **Memorização (`functools.lru_cache`)**:
      * A função `pyrosai_avaliar_criticidade_area` simula o complexo processo de avaliação de risco da PyrosAI, combinando múltiplos fatores (temperatura, umidade do ar e do solo) em um sistema de pontuação.
      * O uso de `@lru_cache` garante que, se a PyrosAI encontrar as **mesmas condições de sensores** múltiplas vezes, o resultado da avaliação de criticidade será retornado **instantaneamente do cache**, evitando recálculos desnecessários e demonstrando uma otimização crucial para sistemas de IA em tempo real.

## ⚙️ Como Rodar o Simulador

Siga os passos abaixo para colocar o Projeto Artemis em funcionamento no seu ambiente.

### Pré-requisitos

Certifique-se de ter o **Python 3.x** instalado.

Você precisará instalar a biblioteca `NetworkX`.

```bash
pip install networkx
```

### Execução

1.  **Clone o repositório** (se aplicável, caso seja um repositório Git) ou **salve o código** em um arquivo Python (ex: `artemis_simulador.py`).

2.  **Abra seu terminal** ou prompt de comando.

3.  **Navegue até o diretório** onde você salvou o arquivo.

4.  **Execute o script Python**:

    ```bash
    python artemis_simulador.py
    ```

5.  O menu interativo do simulador será exibido, permitindo que você interaja com o sistema do Projeto Artemis.

## 🤝 Contribuições

Este projeto é uma **simulação didática**. Contribuições (seja em um ambiente de desenvolvimento real ou para futuras versões acadêmicas) que aprimorem a simulação, adicionem mais algoritmos ou otimizações são sempre bem-vindas\!
