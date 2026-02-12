import heapq

#The goal state for 3x3 puzzle
goal_state = (1,2,3
              ,4,5,6
              ,7,8,0)

#Hardcoded default puzzle for testing purposes
def default_puzzle():
    return (1,2,0
            ,4,5,3
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
    explored = set()
    

    while True:
        if not nodes:
            return "failure"
        
        cost, state, depth, parent = heapq.heappop(nodes)
        explored.add(state) 
        #remove-front (nodes)
        h_n = cost - depth
        print("Initial state:", state, "Cost:", cost, "Depth:", depth, "h(n):", h_n)

        if goal_state == state:
            print("Found goal state!")
            return (cost, state, depth, parent)
        
        children = expand(state)
        childrens = []

        for child in children:
            if child not in explored:
                childrens.append((cost + 1, child, depth + 1, state))

        nodes = QUEUING_FUNCTION(nodes, state, childrens, parent, cost)

    parent = state
    pass

def QUEUING_FUNCTION(nodes, state, children, parent, best_cost):
    for child in children:
        heapq.heappush(nodes, child)
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



puzzle = default_puzzle()
result = general_search(puzzle, QUEUING_FUNCTION)
print("Result:", result)

##puzzle = custom_puzzle()
##print("Puzzle tuple:", puzzle)
