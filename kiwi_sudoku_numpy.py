# Sudoku solver for code.kiwi.com February 2020 challenge
# Original version for 9*9 sudoku here: https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
# 1st Optimization try: changed list operations to set.
# 2nd Optimiztion try: rewrite for numpy.

import numpy as np


board = [
    [7,"X",15,"X","X",10,1,"X",6,"X","X",14,2,0,"X","X"],
    ["X",8,"X",6,4,"X","X",7,5,"X","X","X",12,"X",1,"X"],
    [12,"X","X","X","X",5,6,"X",3,"X","X","X","X","X","X","X"],
    [3,10,5,14,"X",0,8,12,4,"X","X","X",13,"X","X","X"],
    ["X",1,10,"X","X","X",3,15,8,"X","X",12,"X","X",13,7],
    [2,"X","X","X","X",12,13,"X","X","X","X",1,"X","X","X",15],
    ["X",9,"X",12,"X",4,"X","X","X",6,"X","X",0,"X","X",2],
    ["X","X",7,15,"X","X",10,"X","X",3,"X","X","X",9,8,"X"],
    ["X","X",13,"X","X",1,"X","X","X",8,"X","X","X","X",6,"X"],
    [6,"X",2,"X","X","X","X",10,"X",13,"X",5,"X","X","X","X"],
    ["X",4,"X",5,11,"X","X","X","X","X",6,"X",1,13,"X","X"],
    [11,"X",8,"X","X","X",9,0,"X","X","X",10,5,"X",2,4],
    [0,"X",4,10,12,"X","X",13,15,"X","X","X","X",11,"X","X"],
    ["X","X",14,"X","X","X","X",3,"X",9,1,11,"X","X","X","X"],
    ["X",5,"X","X",15,"X","X",2,14,12,"X","X",6,"X","X","X"],
    ["X","X",3,11,7,"X",4,"X","X","X",10,8,"X",12,"X","X"]
]
board = np.array(board)


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(0,16):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = "X"

    return False


def valid(bo, num, pos):
    # Check row
    if num in bo[pos[0]]:
        return False

    # Check column
    if num in bo[:, pos[1]]:
        return False

    # Check box
    box_x = pos[1] // 4
    box_y = pos[0] // 4
    if num in bo[box_x * 4:box_x*4 + 4, box_y * 4:box_y * 4 + 4]:
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
                return (i, j)  # row, col

    return None

print_board(board)
solve(board)
print("___________________")
print_board(board)