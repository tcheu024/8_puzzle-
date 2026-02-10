def default_puzzle():
    return (1,2,3
            ,4,5,6
            ,7,8,0)

def custom_puzzle():
    print("Create your own puzzle, using a 0 to represent the blank tile.")
    nums = []
    rows = ["first", "second", "third"]

    for i in range(3):
        row = input ("Enter the " + rows[i] + " row, with spaces between the numbers: ")
        row_nums = row.split()

        nums.append(int(row_nums[0]))
        nums.append(int(row_nums[1]))
        nums.append(int(row_nums[2]))
    
    

    return tuple(nums)


puzzle = custom_puzzle()
print("Puzzle tuple:", puzzle)

