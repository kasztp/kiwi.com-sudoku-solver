# Sudoku solver for code.kiwi.com February 2020 challenge
# Original version for 9*9 sudoku here: https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
# 1st Optimization try: changed list operations to set.
# 2nd Optimiztion try: rewrite for numpy.

import numpy as np
from numba import jit, njit
from math import sqrt
from time import time


board = np.loadtxt(open('9x9.csv', 'rb'), delimiter=",", dtype=np.uint8)
print('Board loaded successfully.')
size = int(len(board[0]))
print(size)
print('Board size detected: {0}x{1}'.format(str(size), str(size)))
if size != 16 and size != 9:
    print('Unsupported board size detected, exiting. (Only 9x9 or 16x16 is supported as of now.)')
    exit(1)


start_time = time()


def solve(bo, size):
    if size == 16:
        start = 0
        end = 16
    else:
        start = 1
        end = 10
    box_size = int(sqrt(size))
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(start, end):
        #print("Place: " + str(bo[row, col]) + " Number to check: " + str(i) + "")
        if valid(bo, i, (row, col), box_size):
            bo[row, col] = i
            #print(str(i) + " saved to place.")
            #print(bo[row, col])
            if solve(bo, size):
                return True
            #print("Backtracking...")
            bo[row, col] = 21

    return False


def valid(bo, num, pos, box_size):
    #print(num)
    # Check row
    if num in bo[pos[0]]:
        return False

    # Check column
    #print(bo[:, pos[1]])
    if num in bo[:, pos[1]]:
        return False

    # Check box
    box_x = pos[0] // box_size
    box_y = pos[1] // box_size
    #print(bo[(box_x * 4):(box_x * 4 + 4), (box_y * 4):(box_y * 4 + 4)])
    if num in bo[(box_x * box_size):(box_x * box_size + box_size), (box_y * box_size):(box_y * box_size + box_size)]:
        return False

    return True



def print_board(bo, size):
    box_size = int(sqrt(size))
    for i in range(len(bo)):
        if i % box_size == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % box_size == 0 and j != 0:
                print(" | ", end="")

            if j == (size - 1):
                print(bo[i, j])
            else:
                print(str(bo[i, j]) + " ", end="")


@jit
def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i, j] == 21:
                return (i, j)  # row, col

    return None


print_board(board, size)
solve(board, size)
print("___________________")
print_board(board, size)

end_time = time()
print(end_time-start_time)