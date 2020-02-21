# Sudoku solver for code.kiwi.com February 2020 challenge
# Original version for 9*9 sudoku here: https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
# 1st Optimization try: changed list operations to set.
# 2nd Optimiztion try: rewrite for numpy.

import numpy as np


board = [
    [7,-1,15,-1,-1,10,1,-1,6,-1,-1,14,2,0,-1,-1],
    [-1,8,-1,6,4,-1,-1,7,5,-1,-1,-1,12,-1,1,-1],
    [12,-1,-1,-1,-1,5,6,-1,3,-1,-1,-1,-1,-1,-1,-1],
    [3,10,5,14,-1,0,8,12,4,-1,-1,-1,13,-1,-1,-1],
    [-1,1,10,-1,-1,-1,3,15,8,-1,-1,12,-1,-1,13,7],
    [2,-1,-1,-1,-1,12,13,-1,-1,-1,-1,1,-1,-1,-1,15],
    [-1,9,-1,12,-1,4,-1,-1,-1,6,-1,-1,0,-1,-1,2],
    [-1,-1,7,15,-1,-1,10,-1,-1,3,-1,-1,-1,9,8,-1],
    [-1,-1,13,-1,-1,1,-1,-1,-1,8,-1,-1,-1,-1,6,-1],
    [6,-1,2,-1,-1,-1,-1,10,-1,13,-1,5,-1,-1,-1,-1],
    [-1,4,-1,5,11,-1,-1,-1,-1,-1,6,-1,1,13,-1,-1],
    [11,-1,8,-1,-1,-1,9,0,-1,-1,-1,10,5,-1,2,4],
    [0,-1,4,10,12,-1,-1,13,15,-1,-1,-1,-1,11,-1,-1],
    [-1,-1,14,-1,-1,-1,-1,3,-1,9,1,11,-1,-1,-1,-1],
    [-1,5,-1,-1,15,-1,-1,2,14,12,-1,-1,6,-1,-1,-1],
    [-1,-1,3,11,7,-1,4,-1,-1,-1,10,8,-1,12,-1,-1]
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

            bo[row][col] = -1

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
            if bo[i][j] == -1:
                return (i, j)  # row, col

    return None

print_board(board)
solve(board)
print("___________________")
print_board(board)