def get_data():
    # input all lines
    data = []
    with open("advent/input4.txt", "r") as file:
        for line in file:
            data.append(line.strip("\n"))
    # format the bingo numbers
    nums = data[0]
    nums = nums.split(",")
    for i, num in enumerate(nums):
        nums[i] = int(num)
    # format bingo boards
    boards = []
    board = []
    for i in range(2,len(data)):
        if data[i] != "":
            row = data[i].split()
            for j, num in enumerate(row):
                row[j] = int(num)
            board.append(row)
        else:
            boards.append(board[:])
            board = []
    return nums, boards

if __name__ == "__main__":
    nums, boards = get_data()
    print(nums)
    print(boards)