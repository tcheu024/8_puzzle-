import heapq
import time 

#The goal state for 3x3 puzzle
goal_state = (1,2,3
              ,4,5,6
              ,7,8,0)

#Hardcoded default puzzle for testing purposes
def test_puzzle(choice):
    puzzle = choice
    if puzzle == 1:
        return (1,2,3
                ,4,5,6
                ,7,8,0)
    if puzzle == 2:
        return (1,2,3
                ,4,5,6
                ,0,7,8)
    if puzzle == 3:
        return (1,2,3
                ,5,0,6
                ,4,7,8)
    if puzzle == 4:
        return (1,3,6
                ,5,0,2
                ,4,7,8)
    if puzzle == 5:
        return (1,3,6
                ,5,0,7
                ,4,8,2)
    if puzzle == 6:
        return (1,6,7
                ,5,0,3
                ,4,8,2)
    if puzzle == 7:
        return (7,1,2
                ,4,8,5
                ,6,3,0)
    if puzzle == 8:
        return (0,7,2
                ,4,6,1
                ,3,5,8)
    if puzzle == 9:
        return custom_puzzle()
    else:
        return None

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
        return None

    return tuple(nums)

def print_node(state, g_n, h_n, f_n, number):
    print("Expansion #", number)
    print("Path Cost:", g_n)
    print("Heuristic:", h_n)
    print("Total Cost:", f_n)
    

    for i in range(0, len(state), 3):
        print(state[i:i+3])
    
    print(" ")


def general_search(initial_state, QUEUING_FUNCTION):
    #create a initial node with the initial state
    nodes = []
    
    #heapq.heappush(nodes, (0, initial_state, 0, None))

    initial_children = [(0, initial_state, 0, None)]
    nodes = QUEUING_FUNCTION(nodes, initial_children)
    
    g_score = {initial_state: 0}  # Initialize g(n) for the initial state
    nodes_expanded = 0
    max_queue_size = 1

    while True:
        if not nodes:
            return "failure"
        
        max_queue_size = max(max_queue_size, len(nodes))
        
        #remove-front (nodes)
        f_n, state, g_n, parent = heapq.heappop(nodes)

        if g_n > g_score.get(state, float('inf')):
            continue

        h_n = f_n - g_n
        print_node(state, g_n= g_n, h_n= h_n, f_n= f_n, number= nodes_expanded + 1)
        if goal_state == state:
            print("Found goal state!")
            print("Total nodes expanded:", nodes_expanded)
            print("Depth:", g_n)
            print("Max queue size:", max_queue_size)
            print("")
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

def manhattan_distance_h(state):
    distance = 0
    for i in range(len(state)):
        if state[i] != 0:
            current_row = i // 3
            current_col = i % 3

            goal_index = goal_state.index(state[i])
            goal_row = goal_index // 3
            goal_col = goal_index % 3
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def manhattan_distance_queueing(nodes, children):
    #f(n) = g(n) + h(n)
    for child in children:
        f_n, state, g_n, parent = child
        h_n = manhattan_distance_h(state)
        f_n = g_n + h_n
        heapq.heappush(nodes, (f_n, state, g_n, parent))
    return nodes



#MAIN FUNCTION
print("Choose the depth of the puzzle you want to solve")
print("1. Depth 0 (Already solved)")
print("2. Depth 2")
print("3. Depth 4")
print("4. Depth 8")
print("5. Depth 12")
print("6. Depth 16")
print("7. Depth 20")
print("8. Depth 24")
print("9. Create your own puzzle")

choice2 = int(input("Enter the number of your choice: "))
puzzle = test_puzzle(choice2)

print("Select which algorithm to use:")
print("1. Uniform Cost Search")
print("2. A* with Misplaced Tiles Heuristic")
print("3. A* with Manhattan Distance Heuristic")

choice = input("Enter the number of your choice: ")

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
elif choice == '3':
    start= time.time()
    result = general_search(puzzle, manhattan_distance_queueing)
    elapsed = (time.time() - start)*1000
    print("Result:", result)
    print("Elapsed time(ms):", elapsed)
else:
    print("Invalid choice. Please select 1, 2, or 3.")