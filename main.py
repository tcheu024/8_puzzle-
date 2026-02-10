import heapq
#The goal state for a 3x3 puzzle
goal_state = (1,2,3
              ,4,5,6
              ,7,8,0)

#Hardcoded default puzzle for testing purposes
def default_puzzle():
    return (1,2,3
            ,4,5,6
            ,7,8,0)

# Function for the user to create their own unique puzzle, can be of any size
def custom_puzzle():
    print("Create your own puzzle, using a 0 to represent the blank tile.")
    dimensions = int(input("How many rows and columns does your puzzle have? "))

    nums = []
    for i in range(dimensions):
       
        row = input ("Enter the numbers for " + str(i+1) + " row, with spaces between the numbers: ")
        row_nums = row.split()

        for num in row_nums:
            nums.append(int(num))

    if sorted(nums) != list(range(dimensions*dimensions)):
        print("There should be only 1 of each number, Retry.")
        return 0
    
    return tuple(nums)

def general_search(initial_state):
    nodes = []
    heapq.heappush(nodes, (0, initial_state))  

    explored = set()
    
    pass


puzzle = custom_puzzle()
print("Puzzle tuple:", puzzle)




