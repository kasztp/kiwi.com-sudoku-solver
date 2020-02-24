# Sudoku solver for code.kiwi.com February 2020 challenge - 9x9 1..9 version for performance testing.
# Original version for 9*9 sudoku here: https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
# 1st Optimization try: changed list operations to set.
import time

start_time = time.time()

board = [
    [7, "X", 15, "X", "X", 10, 1, "X", 6, "X", "X", 14, 2, 0, "X", "X"],
    ["X", 8, "X", 6, 4, "X", "X", 7, 5, "X", "X", "X", 12, "X", 1, "X"],
    [12, "X", "X", "X", "X", 5, 6, "X", 3, "X", "X", "X", "X", "X", "X", "X"],
    [3, 10, 5, 14, "X", 0, 8, 12, 4, "X", "X", "X", 13, "X", "X", "X"],
    ["X", 1, 10, "X", "X", "X", 3, 15, 8, "X", "X", 12, "X", "X", 13, 7],
    [2, "X", "X", "X", "X", 12, 13, "X", "X", "X", "X", 1, "X", "X", "X", 15],
    ["X", 9, "X", 12, "X", 4, "X", "X", "X", 6, "X", "X", 0, "X", "X", 2],
    ["X", "X", 7, 15, "X", "X", 10, "X", "X", 3, "X", "X", "X", 9, 8, "X"],
    ["X", "X", 13, "X", "X", 1, "X", "X", "X", 8, "X", "X", "X", "X", 6, "X"],
    [6, "X", 2, "X", "X", "X", "X", 10, "X", 13, "X", 5, "X", "X", "X", "X"],
    ["X", 4, "X", 5, 11, "X", "X", "X", "X", "X", 6, "X", 1, 13, "X", "X"],
    [11, "X", 8, "X", "X", "X", 9, 0, "X", "X", "X", 10, 5, "X", 2, 4],
    [0, "X", 4, 10, 12, "X", "X", 13, 15, "X", "X", "X", "X", 11, "X", "X"],
    ["X", "X", 14, "X", "X", "X", "X", 3, "X", 9, 1, 11, "X", "X", "X", "X"],
    ["X", 5, "X", "X", 15, "X", "X", 2, 14, 12, "X", "X", 6, "X", "X", "X"],
    ["X", "X", 3, 11, 7, "X", 4, "X", "X", "X", 10, 8, "X", 12, "X", "X"]
]


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(0, 16):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = "X"

    return False


def valid(bo, num, pos):
    # Check row
    # for i in range(len(bo[0])):
    # if bo[pos[0]][i] == num and pos[1] != i:
    # row = set(bo[pos[0]])
    if num in bo[pos[0]]:
        return False
    # if num in row
    #    return False

    # Check column
    # for i in range(len(bo)):
    #    if bo[i][pos[1]] == num and pos[0] != i:
    column = set()
    for i in range(len(bo)):
        column.add(bo[i][pos[1]])
    if num in column:
        return False

    # Check box
    box_x = pos[1] // 4
    box_y = pos[0] // 4
    box = set()
    for i in range(box_y * 4, box_y * 4 + 4):
        box.add(frozenset(bo[i][box_x * 4: box_x * 4 + 4]))
    # for i in range(box_y*4, box_y*4 + 4):
    #    for j in range(box_x * 4, box_x*4 + 4):
    #        if bo[i][j] == num and (i,j) != pos:
    #            return False
    #print(box)
    if num in box:
        return False

    return True


def print_board(bo):
    for i in range(len(bo)):
        if i % 4 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 4 == 0 and j != 0:
                print(" | ", end="")

            if j == 15:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == "X":
                #print(i, j)
                return (i, j)  # row, col

    return None


print_board(board)
solve(board)
print("___________________")
print_board(board)

end_time = time.time()
print(end_time-start_time)