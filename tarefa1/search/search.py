# search.py
# ---------
# Informações de Licenciamento: Você é livre para usar ou estender estes projetos para
# fins educacionais, desde que (1) você não distribua ou publique
# soluções, (2) você retenha este aviso, e (3) você forneça clara
# atribuição à UC Berkeley, incluindo um link para http://ai.berkeley.edu.
#
# Informações de Atribuição: Os projetos de IA do Pacman foram desenvolvidos na UC Berkeley.
# Os projetos principais e os corretores automáticos foram criados principalmente por John DeNero
# (denero@cs.berkeley.edu) e Dan Klein (klein@cs.berkeley.edu).
# A correção automática do lado do estudante foi adicionada por Brad Miller, Nick Hay, e
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
Em search.py, você implementará algoritmos de busca genéricos que são chamados por
agentes do Pacman (em searchAgents.py).
"""

import util

class SearchProblem:
    """
    Esta classe descreve a estrutura de um problema de busca, mas não implementa
    nenhum dos métodos (em terminologia orientada a objetos: uma classe abstrata).

    Você não precisa alterar nada nesta classe, nunca.
    """

    def getStartState(self):
        """
        Retorna o estado inicial para o problema de busca.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Estado de busca

        Retorna True se e somente se o estado for um estado objetivo válido.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Estado de busca

        Para um estado dado, isso deve retornar uma lista de triplas, (successor,
        action, stepCost), onde 'successor' é um sucessor do estado atual,
        'action' é a ação necessária para chegar lá, e 'stepCost' é
        o custo incremental de expandir para esse sucessor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: Uma lista de ações a serem tomadas

        Este método retorna o custo total de uma sequência particular de ações.
        A sequência deve ser composta de movimentos legais.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Retorna uma sequência de movimentos que resolve tinyMaze. Para qualquer outro labirinto, a
    sequência de movimentos estará incorreta, então use apenas para tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# obtém o último elemento na lista do nó = node.STATE
def getState(node: list):
    if type(node) is list:
        node = node[1]
    return node

def depthFirstSearch(problem: SearchProblem):
    debug = False
    
    # Pilha (Stack) para DFS: Último a entrar, primeiro a sair (LIFO)
    fronteira = util.Stack()
    no_inicio = problem.getStartState()
    
    # Inicializa com (estado_atual, caminho_ate_aqui)
    fronteira.push((no_inicio, []))
    visitados = set()

    interacao = 0
    while not fronteira.isEmpty():
        if debug:
            print(f'\n Iteração: {interacao}')
            interacao += 1    

        # Seleciona e remove o elemento do TOPO da pilha
        estado_atual, caminho = fronteira.pop()
        
        if debug:   
            print(f'    - Nó analisado: {estado_atual}')
            print(f'    - Caminho acumulado: {caminho}')

        # Se alcançou o objetivo, retorna a lista de direções
        if problem.isGoalState(estado_atual):
            if debug: print(">>> Caminho encontrado!", caminho)
            return caminho

        # Só expandimos o nó se ele ainda não foi explorado por outro caminho
        if estado_atual not in visitados:
            if debug:    
                print(f'    - Registrando no set de visitados: {estado_atual}')
            
            visitados.add(estado_atual)
            sucessores = problem.getSuccessors(estado_atual)

            # Percorre os sucessores (estado, acao, custo)
            for proximo_estado, acao, custo in sucessores:
                if proximo_estado not in visitados:
                    novo_caminho = caminho + [acao]
                    
                    if debug:
                        print(f'         + Direção [{acao}] -> Próximo: {proximo_estado}')
                    
                    fronteira.push((proximo_estado, novo_caminho))

    return [] # Falha


def breadthFirstSearch(problem: SearchProblem):
    """
    Busca em Largura (BFS) que encontra o caminho mais curto.
    - Utiliza uma Fila (FIFO) para expansão em camadas.
    - Garante a solução ótima em termos de número de passos.
    """
    from util import Queue

    # Ativa e desativa debugs detalhados para acompanhar o processo de busca
    debug=True

    # 1. INICIALIZAÇÃO
    # Usamos uma Fila para garantir que os nós mais rasos sejam processados primeiro
    fronteira = util.Queue()
    no_inicio = problem.getStartState()
    
    # A fronteira armazena o estado atual e a lista de ações para chegar até ele
    fronteira.push((no_inicio, []))
    
    # O 'set' de visitados evita ciclos e redundância (Busca em Grafo)
    # Na BFS, marcamos como visitado logo na inserção para economizar memória
    visitados = set()
    visitados.add(no_inicio)
    
    nos_expandidos = 0
    
    if debug:
        print(f"\n[INÍCIO] Partindo de: {no_inicio}")

    # 2. LOOP DE BUSCA
    while not fronteira.isEmpty():
        # Remove o nó mais antigo da fila (Princípio FIFO)
        estado_atual, caminho = fronteira.pop()
        nos_expandidos += 1
        
        if debug:
            print(f"  > [{nos_expandidos}] Analisando nó: {estado_atual}")
            print(f"    Caminho até aqui: {caminho}")

        # 3. TESTE DE OBJETIVO
        # Verificamos se o estado retirado da fila é a meta
        if problem.isGoalState(estado_atual):
            if debug:
                print(f"!!! OBJETIVO ENCONTRADO em {nos_expandidos} expansões !!!")
                print(f"Caminho para o objetivo: {caminho}")
            return caminho

        # 4. EXPANSÃO DE SUCESSORES
        # Obtemos os vizinhos: (próximo_estado, ação_necessária, custo_do_passo)
        for proximo_estado, acao, custo in problem.getSuccessors(estado_atual):
            
            # Só adicionamos à fila se o estado ainda não foi "visto" por nenhum caminho
            if proximo_estado not in visitados:
                # Marcamos imediatamente para evitar que outros caminhos o adicionem de novo
                visitados.add(proximo_estado)
                
                # Criamos o novo caminho acumulado
                novo_caminho = caminho + [acao]
                fronteira.push((proximo_estado, novo_caminho))
                
                if debug:
                    print(f"    + Adicionado à fila: {proximo_estado} via {acao}")

    # 5. FINALIZAÇÃO (Caso a fila esvazie sem encontrar o objetivo)
    if debug:
        print(f"[FALHA] Todos os {nos_expandidos} nós acessíveis foram explorados.")
    return []


def uniformCostSearch(problem: SearchProblem, debug=True):
    from util import PriorityQueue

    # 1. INICIALIZAÇÃO
    # Usamos uma Fila de Prioridade: o item com menor custo acumulado sai primeiro
    fronteira = util.PriorityQueue()
    no_inicio = problem.getStartState()
    
    # Na PriorityQueue do util.py, passamos: push(item, prioridade)
    # Item: (estado, caminho, custo_acumulado) | Prioridade: custo_acumulado
    fronteira.push((no_inicio, [], 0), 0)
    
    # Conjunto para busca rápida O(1)
    visitados = set()
    nos_expandidos = 0

    if debug: 
        print(f"\n[INÍCIO UCS] Partindo de: {no_inicio}")

    # 2. LOOP DE BUSCA
    while not fronteira.isEmpty():
        # Remove o nó com o MENOR custo acumulado g(n)
        estado_atual, caminho, custo_total = fronteira.pop()

        # Importante para UCS: Se já visitamos este estado por um caminho mais barato,
        # ignoramos esta expansão.
        if estado_atual in visitados:
            continue
            
        nos_expandidos += 1
        
        if debug:
            print(f"  > [{nos_expandidos}] Expandindo: {estado_atual} | Custo: {custo_total}")

        # 3. TESTE DE OBJETIVO
        if problem.isGoalState(estado_atual):
            if debug: print(f"--- Sucesso! Objetivo encontrado ---")
            print(f"  - Nós expandidos: {nos_expandidos}")
            print(f"  - Custo total: {custo_total}")
            return caminho

        # 4. MARCAR COMO VISITADO
        # Na UCS, marcamos no POP para garantir que encontramos o custo mínimo
        visitados.add(estado_atual)

        # 5. EXPANSÃO DE SUCESSORES
        for proximo_estado, acao, custo_passo in problem.getSuccessors(estado_atual):
            if proximo_estado not in visitados:
                novo_custo = custo_total + custo_passo
                novo_caminho = caminho + [acao]
                
                # A prioridade na fila é o novo custo acumulado
                fronteira.push((proximo_estado, novo_caminho, novo_custo), novo_custo)
                
                if debug:
                    print(f"    + Na fila: {proximo_estado} (Custo: {novo_custo})")

    return []


def nullHeuristic(state, problem=None):
    """
    Uma função heurística estima o custo do estado atual até o objetivo mais próximo
    no SearchProblem fornecido. Esta heurística é trivial.-
    """
    return 0



def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    # Usamos o PriorityQueue da util.py fornecida
    fronteira = util.PriorityQueue()
    start_state = problem.getStartState()
    
    # Armazenamos (estado, caminho, custo_g)
    # Nota: passamos o caminho como lista, mas evitamos operações pesadas nele
    fronteira.push((start_state, [], 0), heuristic(start_state, problem))
    
    # 'visitados' armazena o menor custo g(n) encontrado para cada estado
    visitados = {} 

    iteracao = 0    
    while not fronteira.isEmpty():
        state, path, cost_g = fronteira.pop()

        # Se já chegamos aqui com um custo menor ou igual, ignoramos a expansão
        if state in visitados and visitados[state] <= cost_g:
            continue
            
        visitados[state] = cost_g

        if problem.isGoalState(state):
            return path

        for next_state, action, step_cost in problem.getSuccessors(state):
            new_g = cost_g + step_cost
            
            # Só colocamos na fila se for um caminho potencialmente melhor
            if next_state not in visitados or visitados[next_state] > new_g:
                # h(n) é calculado aqui
                new_f = new_g + heuristic(next_state, problem)
                # Criar a nova lista de ações apenas no push
                fronteira.push((next_state, path + [action], new_g), new_f)

    return []


# Abreviações
dfs = depthFirstSearch
bfs = breadthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch
