from search import depthFirstSearch, breadthFirstSearch
import time 

class HanoiSearchProblem:
    def __init__(self, num_discos, num_pinos=3):
        self.num_discos = num_discos
        self.num_pinos = num_pinos
        
        # Cria o primeiro pino com os discos: (3, 2, 1)
        pino_cheio = tuple(range(num_discos, 0, -1))
        
        # Cria os outros pinos vazios: ()
        pinos_vazios = [tuple() for _ in range(num_pinos - 1)]
        
        # Junta tudo: ((3, 2, 1), (), ())
        self.start_state = (pino_cheio,) + tuple(pinos_vazios)

    def getStartState(self):
        return self.start_state

    def isGoalState(self, state):
        # O objetivo é o ÚLTIMO pino (state[-1]) ter todos os discos
        return len(state[-1]) == self.num_discos

    def getSuccessors(self, state):
        successors = []
        num_pinos = len(state)
        
        for i in range(num_pinos):
            for j in range(num_pinos):
                if i == j: continue
                
                pino_origem = state[i]
                pino_destino = state[j]
                
                if pino_origem: # Tem disco para mover?
                    disco = pino_origem[-1]
                    
                    # Regra: Destino vazio ou disco no topo é maior que o atual
                    if not pino_destino or disco < pino_destino[-1]:
                        # Criar cópia para modificar
                        novo_estado_lista = [list(pino) for pino in state]
                        novo_estado_lista[i].pop()
                        novo_estado_lista[j].append(disco)
                        
                        proximo_estado = tuple(tuple(pino) for pino in novo_estado_lista)
                        acao = f"Mover {disco} de pino {i} para {j}"
                        successors.append((proximo_estado, acao, 1))
                        
        return successors


# EXecução do código para resolver o problema de Hanoi com 4 discos e 3 pinos
problema = HanoiSearchProblem(num_discos=4, num_pinos=3)

# Chamando o DFS do search.py para resolver o problema
solucao = depthFirstSearch(problema)

if solucao:
    print("\n--- Resultado do DFS ---")
    print(f"O DFS encontrou uma solução!")
    print(f"Total de movimentos: {len(solucao)}")
    # Se quiser ver os primeiros 5 movimentos:
    for m in solucao:
        print(m)
    print("")    
else:
    print("Nenhuma solução encontrada.")

# Chamando o BFS do search.py para resolver o problema
solucao = breadthFirstSearch(problema)

if solucao:
    print("\n--- Resultado do BFS ---")
    print(f"O BFS encontrou uma solução!")
    print(f"Total de movimentos do BFS: {len(solucao)}")
    # Se quiser ver os primeiros 5 movimentos:
    for m in solucao:
        print(m)
    print("")    
else:
    print("Nenhuma solução encontrada.")    
