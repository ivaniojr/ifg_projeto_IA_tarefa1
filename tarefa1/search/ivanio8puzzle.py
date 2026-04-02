import eightpuzzle
import search
import time 

eightpuzzle.EIGHT_PUZZLE_DATA=[[0,8,7,6,5,4,3,2,1]]  
goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

puzzle = eightpuzzle.loadEightPuzzle(0)
problem = eightpuzzle.EightPuzzleSearchProblem(puzzle)


#Heuristic para o A* que calcule a soma das distâncias de Manhattan de cada peça para sua posição correta   
def manhattan_short(state, problem=None):
    board = state.cells
    pos = {val: (r, c) for r, row in enumerate(goal) for c, val in enumerate(row)}
    return sum(abs(r - pos[v][0]) + abs(c - pos[v][1]) 
               for r, row in enumerate(board) 
               for c, v in enumerate(row) if v != 0)    

time_start = time.time() 
path = search.aStarSearch(problem, heuristic=manhattan_short)
time_end = time.time()

print('-'*200)
print(f'Usando o A* encontrou um caminho de {len(path)} movimentos.')
print(f'Tempo gasto: {time_end - time_start:.4f} segundos.')
print('Este é o caminho: ', str(path))
print('-'*200)    