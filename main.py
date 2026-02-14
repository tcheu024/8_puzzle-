import heapq
import time 

#The goal state for 3x3 puzzle
goal_state = (1,2,3
              ,4,5,6
              ,7,8,0)

#Returns a puzzle based on the user's choice of depth
#Also allows the user to create their own unique puzzle if they want to
#The puzzles are from the project specifictions
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

#Allows the user to create their own puzzle, using a 0 to represent the blank tile
def custom_puzzle():
    print("Create puzzle, using a 0 to represent the blank tile.")
    dimension = int(input("How many rows and columns does your puzzle have? "))

    nums = []
    #Get the numbers for each row of the puzzle from the user, and add them to a list
    for i in range(dimension):
        row = input("Enter the numbers for " + str(i+1) + " row, with spaces between the numbers: ")
        row_nums = row.split()

        for num in row_nums:
            nums.append(int(num))
    #Check if the numbers entered are valid for the given dimension of the puzzle
    if sorted(nums) != list(range(dimension*dimension)):
        print("There should be only 1 of each number, Retry.")
        return None

    return tuple(nums)

# Prints detailed information about a node being expanded during search
#Mostly used for debugging in the beginning
def print_node(state, g_n, h_n, f_n, number):
    print("Expansion #", number)
    print("Path Cost:", g_n)
    print("Heuristic:", h_n)
    print("Total Cost:", f_n)
    
    for i in range(0, len(state), 3):
        print(state[i:i+3])
    
    print(" ")

#Reconstructs and prints the solution path from initial state to goal.
def print_solution(goal_state_final, parent_map):
    path = []
    current = goal_state_final  # Start from the goal state
    
    # Follow parent pointers backwards
    while current is not None:
        path.append(current)
        current = parent_map.get(current)
    
    # Reverse to get path from start to goal
    path.reverse()

    print(" ")
    print("SOLUTION PATH")
    print(" ")
    for i, state in enumerate(path):
        print("Step", i)
        for j in range(0, len(state), 3):
            print(state[j:j+3])
        if i < len(path) - 1:  
            print(" ")

#General search algorithm that implements both UCS and A* algorithms
def general_search(initial_state, QUEUING_FUNCTION):
    #creates a priority queue to store the nodes to be expanded
    nodes = []
    
    initial_children = [(0, initial_state, 0, None)]
    nodes = QUEUING_FUNCTION(nodes, initial_children)
    # Initialize g(n) for the initial state
    g_score = {initial_state: 0}  
    # tracks parent of each state for path reconstruction
    parent_map = {initial_state: None} 
    nodes_expanded = 0
    max_queue_size = 1

    # Loop until there are no more nodes to expand
    while True:
        #If the queue is empty, return failure
        if not nodes:
            return "failure"
        #Update the maximum queue size
        max_queue_size = max(max_queue_size, len(nodes)) 
        #remove-front (nodes)
        f_n, state, g_n, parent = heapq.heappop(nodes)
        # Skip this node if there is a better path to this state
        if g_n > g_score.get(state, float('inf')):
            continue
        
        h_n = f_n - g_n
        print_node(state, g_n= g_n, h_n= h_n, f_n= f_n, number= nodes_expanded + 1)
        
        #Check if the current state is the goal state
        if goal_state == state:   
            print_solution(state, parent_map)
            print(" ")
            print("Total nodes expanded:", nodes_expanded + 1)
            print("Depth:", g_n)
            print("Max queue size:", max_queue_size)
            print("Elapsed time(ms):", (time.time() - start)*1000)
            print("")
           
            return {
                'depth': g_n,
                'nodes_expanded': nodes_expanded + 1,
                'max_queue_size': max_queue_size
            }

        nodes_expanded += 1
        # Generate children states
        children = expand(state)
        childrens = []
        #For each child state, calculate g(n) and update the queue and parent map 
        for child in children:
            new_gn = g_n + 1

            if child not in g_score or new_gn < g_score[child]:
                g_score[child] = new_gn
                parent_map[child] = state
                childrens.append((0, child, new_gn, state))
        
        nodes = QUEUING_FUNCTION(nodes, childrens)

#Uniform Cost Search implementation of the queuing function
#h(n) is 0 for all nodes, so f(n) = g(n)
def uniform_cost_search(nodes, children):
    # children is a list of tuples (cost, state, depth, parent)
    for child in children:
        f_n, state, g_n, parent = child
        f_n = g_n
        heapq.heappush(nodes, (f_n, state, g_n, parent))

    return nodes

#expand function generates the child states of a given state by moving the blank tile (0) in all possible directions
# returns a list of the resulting states.
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

#Find the numberof misplaced tiles
def misplaced_tiles_h(state):
    count = 0
    for i in range(len(state)):
        if state[i] != 0 and state[i] != goal_state[i]:
            count += 1
    return count

#Calculate f(n) for each child node using the misplaced tiles heuristic 
def misplaced_tiles_queueing(nodes, children):
    for child in children: 
        f_n, state, g_n, parent = child
        h_n = misplaced_tiles_h(state)
        f_n = g_n + h_n
        heapq.heappush(nodes, (f_n, state, g_n, parent))

    return nodes

#Calculate the Manhattan distance for each tile 
#find the current position of the current tile and goal tile and 
#Calculate the distance by finding the difference in rows and columns 
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

#Calculate f(n) for each child node using the Manhattan distance heuristic
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
    
        
elif choice == '2':
    start= time.time()
    result = general_search(puzzle, misplaced_tiles_queueing)
    elapsed = (time.time() - start)*1000
    
        
elif choice == '3':
    start= time.time()
    result = general_search(puzzle, manhattan_distance_queueing)
    elapsed = (time.time() - start)*1000
else:
    print("Invalid choice. Please select 1, 2, or 3.")