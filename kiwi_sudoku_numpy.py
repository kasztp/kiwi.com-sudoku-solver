# Sudoku solver for code.kiwi.com February 2020 challenge
# Original version for 9*9 sudoku here: https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
# 1st Optimization try: changed list operations to set.
# 2nd Optimization try: partially rewrite for numpy.
# 3rd Optimization try: numba njit for find_empty.
# 4th Optimization try: numba jit and numpy for valid.


import numpy as np
from numba import njit
from math import sqrt
from time import time


board = np.loadtxt(open('test_0.csv', 'rb'), delimiter=",", dtype=np.uint8)
print('Board loaded successfully.')
size = int(len(board[0]))
print(size)
print('Board size detected: {0}x{1}'.format(str(size), str(size)))
if size != 16 and size != 9:
    print('Unsupported board size detected, exiting. (Only 9x9 or 16x16 is supported as of now.)')
    exit(1)
if size == 16:
    start = 1
    end = 17
else:
    start = 1
    end = 10
dimensions = (start, end)
box_size = int(sqrt(size))
start_time = time()


def solve(bo, size, box_size, dimensions):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(dimensions[0], dimensions[1]):
        if valid(bo, i, (row, col), box_size):
            bo[row, col] = i
            if solve(bo, size, box_size, dimensions):
                return True
            bo[row, col] = 0

    return False


@njit
def valid(bo, num, pos, box_size):
    # Check row
    print(num, pos, box_size)
    location = np.argwhere(bo[pos[0]] == num)
    print(location)
    if np.any(location):
        return False

    # Check column
    location = np.argwhere(bo[:, pos[1]] == num)
    print(location)
    if np.any(location):
        return False

    # Check box
    box_x = pos[0] // box_size
    box_y = pos[1] // box_size
    location = np.argwhere(bo[(box_x * box_size):(box_x * box_size + box_size), (box_y * box_size):(box_y * box_size + box_size)] == num)
    print(location)
    if np.any(location):
        print("Bennevanmár!")
        return False
    print("Nincsbenne he!")
    return True


def print_board(bo, size, box_size):
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


@njit
def find_empty(bo):
    location = np.argwhere(bo == 0)
    if np.any(location):
        print(location[0][0], location[0][1])
        return location[0][0], location[0][1]  # row, col

    return None


print_board(board, size, box_size)
solve(board, size, box_size, dimensions)
print("___________________")
print_board(board, size, box_size)

end_time = time()
print(end_time - start_time)
