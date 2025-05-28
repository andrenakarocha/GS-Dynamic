import datetime
import random
import heapq
import networkx as nx
from functools import lru_cache

# --- Constantes e Configurações Simuladas (mantidas) ---
SEVERIDADES = {
    "BAIXA": 1,
    "MEDIA": 2,
    "ALTA": 3,
    "CRITICA": 4
}
STATUS_OCORRENCIA = ["DETECTADA", "EM_ATENDIMENTO", "SOB_CONTROLE", "EXTINTA"]

# --- Estruturas de Dados Globais Simuladas (mantidas) ---
ocorrencias_ativas = {} 
fila_prioridade_atendimento = [] 
rede_localizacoes_graph = nx.DiGraph()

# --- Configuração Inicial do Grafo (Simulação) (mantida) ---
def configurar_grafo_localizacoes():
    """
    Simula a configuração dos nós (localizações) e das arestas (rotas com peso)
    em um DiGraph do NetworkX.
    Nós: representam bases de equipes e áreas de interesse para queimadas.
    Arestas: representam rotas direcionadas entre os locais, com o 'weight' (peso)
             simulando a distância ou tempo de deslocamento.
    """
    print("\n--- Simulando Configuração da Rede de Localizações (Grafo) ---")
    nodes = ['Base_Alfa', 'Base_Beta', 'Floresta_Vermelha', 'Bosque_Azul', 
             'Montanha_Verde', 'Rio_Sereno', 'Vila_Clara', 'Pico_Alto', 'Estrada_Principal']
    rede_localizacoes_graph.add_nodes_from(nodes)

    # Arestas simuladas (origem, destino, peso)
    edges = [
        ('Base_Alfa', 'Floresta_Vermelha', 10),
        ('Base_Alfa', 'Montanha_Verde', 25),
        ('Base_Beta', 'Bosque_Azul', 15),
        ('Base_Beta', 'Vila_Clara', 8),
        ('Floresta_Vermelha', 'Bosque_Azul', 12),
        ('Floresta_Vermelha', 'Rio_Sereno', 7),
        ('Bosque_Azul', 'Base_Alfa', 18), 
        ('Bosque_Azul', 'Montanha_Verde', 20),
        ('Montanha_Verde', 'Rio_Sereno', 5),
        ('Rio_Sereno', 'Vila_Clara', 10),
        ('Vila_Clara', 'Floresta_Vermelha', 30),
        ('Vila_Clara', 'Base_Beta', 8),
        ('Estrada_Principal', 'Base_Alfa', 5),
        ('Montanha_Verde', 'Pico_Alto', 15),
        ('Pico_Alto', 'Montanha_Verde', 12) # Diferença de peso na volta simulando subida/descida
    ]
    rede_localizacoes_graph.add_weighted_edges_from(edges)

    print(f"  Rede de Localizações (Grafo DiGraph) simulada com sucesso!")
    print(f"  Nós no grafo: {list(rede_localizacoes_graph.nodes)}")

# --- Nova Função da PyrosAI com Memoization (Simulação de Avaliação de Risco) ---
@lru_cache(maxsize=128) # Cache para até 128 resultados diferentes
def pyrosai_avaliar_criticidade_area(temperatura: int, umidade_ar: int, umidade_solo: int) -> str:
    """
    Simula uma avaliação detalhada da PyrosAI sobre a criticidade de uma micro-área.
    Baseia-se em parâmetros simulados de temperatura, umidade do ar e umidade do solo,
    utilizando um sistema de pontuação para maior variedade e realismo na simulação.
    Esta função usa memoization (`lru_cache`) para otimizar chamadas repetidas
    com os mesmos parâmetros, simulando a eficiência da IA em evitar recálculos.

    Args:
        temperatura (int): Temperatura ambiente simulada (ex: 20-40°C).
        umidade_ar (int): Umidade relativa do ar simulada (ex: 0-100%).
        umidade_solo (int): Percentual de umidade do solo simulado (ex: 0-100%).

    Returns:
        str: Nível de criticidade simulado ('BAIXA', 'MEDIA', 'ALTA', 'CRITICA').
    """
    # Esta linha é visível APENAS quando a função é *realmente* executada (não do cache).
    print(f"  [PyrosAI SIMULANDO Processamento de Criticidade para Temp={temperatura}°C, UmidAr={umidade_ar}%, UmidSolo={umidade_solo}%]")
    
    total_pontos_risco = 0

    # Pontuação da Temperatura
    if temperatura <= 20:
        total_pontos_risco += 0
    elif 20 < temperatura <= 25:
        total_pontos_risco += 1
    elif 25 < temperatura <= 30:
        total_pontos_risco += 2
    elif 30 < temperatura <= 35:
        total_pontos_risco += 3
    else: # temperatura > 35
        total_pontos_risco += 4

    # Pontuação da Umidade do Ar (inversamente proporcional ao risco)
    if umidade_ar > 70:
        total_pontos_risco += 0
    elif 50 < umidade_ar <= 70:
        total_pontos_risco += 1
    elif 30 < umidade_ar <= 50:
        total_pontos_risco += 2
    elif 15 < umidade_ar <= 30:
        total_pontos_risco += 3
    else: # umidade_ar <= 15
        total_pontos_risco += 4

    # Pontuação da Umidade do Solo (inversamente proporcional ao risco)
    if umidade_solo > 60:
        total_pontos_risco += 0
    elif 40 < umidade_solo <= 60:
        total_pontos_risco += 1
    elif 20 < umidade_solo <= 40:
        total_pontos_risco += 2
    elif 10 < umidade_solo <= 20:
        total_pontos_risco += 3
    else: # umidade_solo <= 10
        total_pontos_risco += 4

    # Mapeamento da pontuação total para o nível de criticidade
    if total_pontos_risco <= 3:
        return "BAIXA"
    elif 3 < total_pontos_risco <= 6:
        return "MEDIA"
    elif 6 < total_pontos_risco <= 9:
        return "ALTA"
    else: # total_pontos_risco > 9 (até 12)
        return "CRITICA"

# --- Funções do Simulador (restante do código permanece o mesmo) ---

def gerar_id_ocorrencia():
    """
    Simula a geração de um ID único para cada nova ocorrência de queimada no sistema.
    """
    return len(ocorrencias_ativas) + 1

def inserir_nova_ocorrencia():
    """
    Simula a detecção de uma nova ocorrência de queimada pelo sistema Artemis.
    Coleta dados de sensores simulados e utiliza a `pyrosai_avaliar_criticidade_area`
    (com memoization) para determinar a severidade da ocorrência.
    Registra a ocorrência no dicionário `ocorrencias_ativas` e na fila de prioridade.
    """
    print("\n--- Registrar Nova Ocorrência Simulada ---")
    ocorrencia_id = gerar_id_ocorrencia()

    print(f"  ID da Ocorrência Simulada: {ocorrencia_id}")

    # Simula a leitura de sensores para alimentar a PyrosAI
    print("  Simulando leitura de dados de sensores para avaliação da PyrosAI...")
    temp_sim = random.randint(15, 45) # Maior variação de temperatura
    umid_ar_sim = random.randint(5, 95) # Maior variação de umidade
    umid_solo_sim = random.randint(0, 90) # Maior variação de umidade do solo

    # A PyrosAI avalia a criticidade usando a função memorizada
    severidade_str = pyrosai_avaliar_criticidade_area(temp_sim, umid_ar_sim, umid_solo_sim)
    print(f"  PyrosAI SIMULOU a avaliação de criticidade como: {severidade_str}")


    # Validação de localização (deve ser um nó no nosso grafo simulado)
    localizacao_ocorrencia = ""
    disponivel_locais = list(rede_localizacoes_graph.nodes)
    while localizacao_ocorrencia not in disponivel_locais:
        localizacao_ocorrencia = input(f"  Informe a localização (ex: {', '.join(disponivel_locais)}): ")
        if localizacao_ocorrencia not in disponivel_locais:
            print("  Localização inválida ou não mapeada no sistema simulado. Tente novamente.")

    ocorrencia_details = {
        'ID': ocorrencia_id,
        'severidade': severidade_str,
        'severidade_num': SEVERIDADES[severidade_str],
        'localizacao': localizacao_ocorrencia,
        'status': "DETECTADA",
        'timestamp_deteccao': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'sensor_data_simulated': {'temp': temp_sim, 'umid_ar': umid_ar_sim, 'umid_solo': umid_solo_sim} # Adiciona os dados simulados para referência
    }

    ocorrencias_ativas[ocorrencia_id] = ocorrencia_details
    # Adiciona à fila de prioridade (heapq) para simular o atendimento por prioridade
    heapq.heappush(fila_prioridade_atendimento, (-ocorrencia_details['severidade_num'], ocorrencia_id))

    print(f"Ocorrência {ocorrencia_id} registrada com sucesso: {ocorrencia_details['severidade']} em {ocorrencia_details['localizacao']}.")

def exibir_ocorrencias_ativas():
    """
    Exibe todas as ocorrências de queimada que estão ativas (não extintas) no simulador.
    Itera sobre o dicionário `ocorrencias_ativas`.
    """
    print("\n--- Ocorrências Ativas Simuladas ---")
    if not ocorrencias_ativas:
        print("Nenhuma ocorrência ativa simulada no momento.")
        return

    print(f"{'ID':<5} | {'Severidade':<12} | {'Localização':<20} | {'Status':<15} | {'Detecção':<20}")
    print("-" * 75)
    for id, details in ocorrencias_ativas.items():
        if details['status'] != "EXTINTA":
            print(f"{id:<5} | {details['severidade']:<12} | {details['localizacao']:<20} | {details['status']:<15} | {details['timestamp_deteccao']:<20}")

def buscar_ocorrencia_por_severidade(severidade_alvo: str):
    """
    Simula a busca por ocorrências com uma severidade específica.
    Demonstra o conceito de Busca Binária. Para fins didáticos, uma lista temporária
    é criada e ordenada para permitir a aplicação da busca binária.
    Complexidade: O(N log N) para ordenar a lista + O(log N) para a busca.
    """
    print(f"\n--- Simulando Busca por Ocorrências com Severidade '{severidade_alvo}' ---")
    severidade_alvo_upper = severidade_alvo.upper()
    if severidade_alvo_upper not in SEVERIDADES:
        print("  Severidade alvo inválida.")
        return

    severidade_num_alvo = SEVERIDADES[severidade_alvo_upper]
    
    # Criar uma lista de tuplas (severidade_numerica, ID_ocorrencia) das ocorrências ativas simuladas
    ocorrencias_ordenadas_por_severidade = []
    for id, details in ocorrencias_ativas.items():
        if details['status'] != "EXTINTA": # Considera apenas ocorrências ainda ativas
            ocorrencias_ordenadas_por_severidade.append((details['severidade_num'], id))
    
    # Ordena a lista para permitir a busca binária (O(N log N))
    ocorrencias_ordenadas_por_severidade.sort() 

    # --- Implementação da Busca Binária ---
    low, high = 0, len(ocorrencias_ordenadas_por_severidade) - 1
    primeiro_match_idx = -1

    while low <= high:
        mid = (low + high) // 2
        if ocorrencias_ordenadas_por_severidade[mid][0] >= severidade_num_alvo:
            primeiro_match_idx = mid
            high = mid - 1 # Tenta encontrar uma correspondência mais à esquerda (primeira ocorrência)
        else:
            low = mid + 1
            
    encontradas = []
    if primeiro_match_idx != -1:
        # Percorre a partir do primeiro_match_idx para coletar todas as ocorrências com a severidade exata
        for i in range(primeiro_match_idx, len(ocorrencias_ordenadas_por_severidade)):
            if ocorrencias_ordenadas_por_severidade[i][0] == severidade_num_alvo:
                encontradas.append(ocorrencias_ativas[ocorrencias_ordenadas_por_severidade[i][1]])
            else:
                # Como a lista está ordenada, se a severidade já aumentou, não haverá mais com a severidade alvo
                break 

    if encontradas:
        print(f"{'ID':<5} | {'Severidade':<12} | {'Localização':<20} | {'Status':<15}")
        print("-" * 55)
        for details in encontradas:
            print(f"{details['ID']:<5} | {details['severidade']:<12} | {details['localizacao']:<20} | {details['status']:<15}")
    else:
        print(f"  Nenhuma ocorrência com severidade '{severidade_alvo}' encontrada na simulação.")


def atender_proxima_ocorrencia():
    """
    Simula o atendimento da próxima ocorrência de queimada com maior prioridade (severidade).
    Utiliza a fila de prioridade (`heapq`) e simula a otimização de rota da PyrosAI
    usando algoritmos de caminho mais curto do NetworkX.
    """
    print("\n--- Simulando Atendimento da Próxima Ocorrência (PyrosAI Otimização) ---")
    if not fila_prioridade_atendimento:
        print("  Nenhuma ocorrência na fila simulada para atendimento.")
        return

    # Pega a ocorrência de maior prioridade (menor valor negativo na fila)
    severidade_neg, ocorrencia_id = heapq.heappop(fila_prioridade_atendimento)
    
    # Verifica se a ocorrência ainda existe e não foi extinta por outro meio na simulação
    if ocorrencia_id not in ocorrencias_ativas or ocorrencias_ativas[ocorrencia_id]['status'] == "EXTINTA":
        print(f"  Ocorrência {ocorrencia_id} já foi tratada ou não existe mais. Buscando a próxima na simulação...")
        return atender_proxima_ocorrencia() # Tenta a próxima recursivamente (simulando re-fila)

    ocorrencia = ocorrencias_ativas[ocorrencia_id]
    
    # Simula a "PyrosAI" encontrando a base mais próxima usando o grafo do NetworkX
    bases_disponiveis = [node for node in rede_localizacoes_graph.nodes if node.startswith('Base')]
    
    if not bases_disponiveis:
        print("  Nenhuma base de equipes disponível no grafo simulado.")
        return

    melhor_base = None
    menor_distancia = float('infinity')
    melhor_caminho = None

    print("\n  PyrosAI SIMULANDO cálculo de rota otimizada...")
    for base in bases_disponiveis:
        try:
            # Utiliza o algoritmo de Dijkstra do NetworkX para encontrar o caminho mais curto
            caminho = nx.shortest_path(rede_localizacoes_graph, source=base, target=ocorrencia['localizacao'], weight='weight')
            distancia = nx.shortest_path_length(rede_localizacoes_graph, source=base, target=ocorrencia['localizacao'], weight='weight')
            
            if distancia < menor_distancia:
                menor_distancia = distancia
                melhor_base = base
                melhor_caminho = caminho
        except nx.NetworkXNoPath:
            # Simula a ausência de um caminho direto entre a base e a ocorrência
            continue
        except nx.NodeNotFound:
            # Simula um erro onde um nó (base ou localização) não foi encontrado no grafo
            print(f"  Erro simulado: Nó '{base}' ou '{ocorrencia['localizacao']}' não encontrado no grafo simulado.")
            continue
    
    if melhor_base:
        print(f"  PyrosAI SIMULOU recomendação: equipe da '{melhor_base}' para Ocorrência {ocorrencia_id} (Severidade: {ocorrencia['severidade']}).")
        print(f"  Rota otimizada simulada ({menor_distancia}km): {' -> '.join(melhor_caminho)}")
        
        ocorrencias_ativas[ocorrencia_id]['status'] = "EM_ATENDIMENTO"
        print(f"  Ocorrência {ocorrencia_id} agora está '{ocorrencias_ativas[ocorrencia_id]['status']}' (status simulado).")
    else:
        print(f"  Não foi possível encontrar uma rota simulada para a Ocorrência {ocorrencia_id}. Verifique a conectividade do grafo.")


def atualizar_status_ocorrencia():
    """
    Permite ao usuário simular a atualização do status de uma ocorrência.
    """
    print("\n--- Atualizar Status de Ocorrência Simulada ---")
    try:
        ocorrencia_id = int(input("  Informe o ID da ocorrência para atualizar: "))
    except ValueError:
        print("  ID inválido. Digite um número.")
        return

    if ocorrencia_id not in ocorrencias_ativas:
        print("  Ocorrência não encontrada na simulação.")
        return

    ocorrencia = ocorrencias_ativas[ocorrencia_id]
    print(f"  Status atual da Ocorrência {ocorrencia_id}: {ocorrencia['status']}")
    print(f"  Novos status disponíveis: {', '.join(STATUS_OCORRENCIA)}")

    novo_status = ""
    while novo_status not in STATUS_OCORRENCIA:
        novo_status = input("  Informe o novo status: ").upper().replace(" ", "_")
        if novo_status not in STATUS_OCORRENCIA:
            print("  Status inválido. Tente novamente.")

    ocorrencia['status'] = novo_status
    if novo_status == "EXTINTA":
        print(f"  Ocorrência {ocorrencia_id} marcada como EXTINTA (simulação).")
    
    print(f"  Status da Ocorrência {ocorrencia_id} atualizado para '{novo_status}'.")

def gerar_relatorio_atendimento_por_localizacao():
    """
    Gera um relatório simulado de ocorrências por localização, mostrando o histórico.
    """
    print("\n--- Relatório Simulado de Ocorrências por Localização ---")
    if not ocorrencias_ativas:
        print("  Nenhuma ocorrência registrada na simulação.")
        return

    relatorio = {}
    for id, details in ocorrencias_ativas.items():
        local = details['localizacao']
        if local not in relatorio:
            relatorio[local] = []
        relatorio[local].append(f"ID {id} | Severidade: {details['severidade']} | Status: {details['status']} | Detecção: {details['timestamp_deteccao']}")
    
    for local, ocorrencias in relatorio.items():
        print(f"\n  Localização: {local}")
        for ocorrencia_info in ocorrencias:
            print(f"    - {ocorrencia_info}")

def simular_chamadas_aleatorias():
    """
    Simula a inserção de várias ocorrências aleatórias no sistema.
    A severidade de cada nova ocorrência é determinada pela `pyrosai_avaliar_criticidade_area`,
    simulando detecções do Projeto Artemis e avaliações da PyrosAI.
    """
    print("\n--- Simulação de Novas Detecções Aleatórias ---")
    num_simulacoes = random.randint(3, 7)
    print(f"  Simulando {num_simulacoes} novas detecções de queimadas pelo Projeto Artemis e avaliação da PyrosAI...")
    
    locais_validos = list(rede_localizacoes_graph.nodes) # Usar nós do grafo para simular locais
    
    for i in range(num_simulacoes):
        ocorrencia_id = gerar_id_ocorrencia()
        localizacao_ocorrencia = random.choice(locais_validos)

        # Simula leituras de sensores para a PyrosAI com ranges mais amplos para maior variedade
        temp_sim = random.randint(15, 45)
        umid_ar_sim = random.randint(5, 95)
        umid_solo_sim = random.randint(0, 90)

        # A PyrosAI avalia a criticidade usando a função memorizada (lru_cache)
        severidade_str = pyrosai_avaliar_criticidade_area(temp_sim, umid_ar_sim, umid_solo_sim)
        
        ocorrencia_details = {
            'ID': ocorrencia_id,
            'severidade': severidade_str,
            'severidade_num': SEVERIDADES[severidade_str],
            'localizacao': localizacao_ocorrencia,
            'status': "DETECTADA",
            'timestamp_deteccao': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'sensor_data_simulated': {'temp': temp_sim, 'umid_ar': umid_ar_sim, 'umid_solo': umid_solo_sim}
        }
        ocorrencias_ativas[ocorrencia_id] = ocorrencia_details
        heapq.heappush(fila_prioridade_atendimento, (-ocorrencia_details['severidade_num'], ocorrencia_id))
        print(f"  - Simulação: Ocorrência {ocorrencia_id} ({severidade_str}) em {localizacao_ocorrencia} detectada.")


# --- Menu Principal do Simulador (mantido) ---
def menu():
    """
    Exibe o menu principal do simulador e gerencia as opções do usuário.
    """
    print("\n===== Projeto Artemis: Simulador de Resposta a Queimadas =====")
    print("  1. Registrar Nova Ocorrência (Simulada pela PyrosAI)")
    print("  2. Exibir Ocorrências Ativas Simuladas")
    print("  3. Atender Próxima Ocorrência (PyrosAI Otimização de Rotas)")
    print("  4. Atualizar Status de Ocorrência Simulada")
    print("  5. Gerar Relatório Simulado por Localização")
    print("  6. Simular Novas Detecções Aleatórias (Avaliação PyrosAI)")
    print("  7. Buscar Ocorrência por Severidade (Simulação de Busca Binária)")
    print("  0. Sair do Simulador")
    print("================================================================")

    escolha = input("  Escolha uma opção: ")
    return escolha

# --- Loop Principal da Aplicação ---
if __name__ == "__main__":
    configurar_grafo_localizacoes() # Configura o grafo simulado no início da execução

    while True:
        escolha = menu()

        if escolha == '1':
            inserir_nova_ocorrencia()
        elif escolha == '2':
            exibir_ocorrencias_ativas()
        elif escolha == '3':
            atender_proxima_ocorrencia()
        elif escolha == '4':
            atualizar_status_ocorrencia()
        elif escolha == '5':
            gerar_relatorio_atendimento_por_localizacao()
        elif escolha == '6':
            simular_chamadas_aleatorias()
        elif escolha == '7':
            severidade_busca = input("  Informe a severidade para buscar (BAIXA, MEDIA, ALTA, CRITICA): ")
            buscar_ocorrencia_por_severidade(severidade_busca)
        elif escolha == '0':
            print("Saindo do Simulador do Projeto Artemis. Até mais!")
            break
        else:
            print("  Opção inválida. Por favor, tente novamente.")
        
        input("\n  Pressione Enter para continuar no simulador...") # Pausa para o usuário ler a saída
