import heapq
import time 

#The goal state for 3x3 puzzle
goal_state = (1,2,3
              ,4,5,6
              ,7,8,0)

#Hardcoded default puzzle for testing purposes
def default_puzzle():
    return (1,2,3
            ,4,0,5
            ,7,8,6)

#Fuction to create unique puzzle
def custom_puzzle():
    print("Create puzzle, using a 0 to represent the blank tile.")
    dimension = int(input("How many rows and columns does your puzzle have? "))

    nums = []
    for i in range(dimension):
        row = input("Enter the numbers for " + str(i+1) + " row, with spaces between the numbers: ")
        row_nums = row.split()

        for num in row_nums:
            nums.append(int(num))

    if sorted(nums) != list(range(dimension*dimension)):
        print("There should be only 1 of each number, Retry.")
        return 0

    return tuple(nums)

def general_search(initial_state, QUEUING_FUNCTION):
    #create a initial node with the initial state
    nodes = []
    heapq.heappush(nodes, (0, initial_state, 0, None))
    
    g_score = {initial_state: 0}  # Initialize g(n) for the initial state
    nodes_expanded = 0

    while True:
        if not nodes:
            return "failure"
        
        f_n, state, g_n, parent = heapq.heappop(nodes)

        if g_n > g_score.get(state, float('inf')):
            continue
        
        #remove-front (nodes)
        h_n = f_n - g_n
        print("Initial state:", state, "Cost:", f_n, "Depth:", g_n, "h(n):", h_n)

        if goal_state == state:
            print("Found goal state!")
            return (f_n, state, g_n, parent)

        nodes_expanded += 1

        children = expand(state)
        childrens = []

        for child in children:
            new_gn = g_n + 1

            if child not in g_score or new_gn < g_score[child]:
                g_score[child] = new_gn
                childrens.append((0, child, new_gn, state))
        
        nodes = QUEUING_FUNCTION(nodes, childrens)
    
    pass

def uniform_cost_search(nodes, children):
    # children is a list of tuples (cost, state, depth, parent)
    for child in children:
        f_n, state, g_n, parent = child
        f_n = g_n
        heapq.heappush(nodes, (f_n, state, g_n, parent))

    return nodes


def expand(state):
    children = []

    zero =state.index(0)
    row = zero // 3
    col = zero % 3

    # Move up
    if row > 0:  
        new_state = list(state)
        new_state[zero], new_state[zero - 3] = new_state[zero - 3], new_state[zero]
        children.append(tuple(new_state))

    #Move down
    if row < 2:  
        new_state = list(state)
        new_state[zero], new_state[zero + 3] = new_state[zero + 3], new_state[zero]
        children.append(tuple(new_state))

    #Move left
    if col > 0:  
        new_state = list(state)
        new_state[zero], new_state[zero - 1] = new_state[zero - 1], new_state[zero]
        children.append(tuple(new_state))
    
    #Move right
    if col < 2:  
        new_state = list(state)
        new_state[zero], new_state[zero + 1] = new_state[zero + 1], new_state[zero]
        children.append(tuple(new_state))
    return children

def misplaced_tiles_h(state):
    count = 0
    for i in range(len(state)):
        if state[i] != 0 and state[i] != goal_state[i]:
            count += 1
    return count

def misplaced_tiles_queueing(nodes, children):
    for child in children: 
        f_n, state, g_n, parent = child
        h_n = misplaced_tiles_h(state)
        f_n = g_n + h_n
        heapq.heappush(nodes, (f_n, state, g_n, parent))

    return nodes



puzzle = default_puzzle()
print("Select which algorithm to use:")
print("1. Uniform Cost Search")
print("2. A* with Misplaced Tiles Heuristic")
print("3. A* with Manhattan Distance Heuristic")
choice = input("Enter the number of your choice: ")
puzzle = default_puzzle()
if choice == '1':
    start= time.time()
    result = general_search(puzzle, uniform_cost_search)
    elapsed = (time.time() - start)*1000
    print("Result:", result)
    print("Elapsed time(ms):", elapsed)
elif choice == '2':
    start= time.time()
    result = general_search(puzzle, misplaced_tiles_queueing)
    elapsed = (time.time() - start)*1000
    print("Result:", result)
    print("Elapsed time(ms):", elapsed)
else:
    print("Invalid choice. Please select 1, 2, or 3.")


##puzzle = custom_puzzle()
##print("Puzzle tuple:", puzzle)

# def QUEUING_FUNCTION(nodes, state, children, parent, best_cost):
#     for child in children:
#         heapq.heappush(nodes, child)
#     return nodes