# Sudoku solver for code.kiwi.com February 2020 challenge
# Original version for 9x9 sudoku here: https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
#
# Optimizations:
# 1. Changed most for loops to list slicing & comprehension.
# 2. Changed for cycles to in for membership tests.
# 3. Moved size/box_size/etc constant calculations outside of for loops.
#
# New features:
# 1. Added ability to import csv
# 2. Added ability to solve both 9x9 & 16x16 sudoku puzzles
# 3. Added basic runtime timing for performance evaluation

from time import time
from math import sqrt
from csv import reader

board = []
with open('9x9.csv') as csvDataFile:
    csvReader = reader(csvDataFile)
    for row in csvReader:
        board.append([int(numeric_string) for numeric_string in row])
print('Board loaded successfully.')
size = int(len(board[0]))
box_size = int(sqrt(size))
if size == 16:
    start = 0
    end = 16
else:
    start = 1
    end = 10
dimensions = (start, end)
print(size)
print('Board size detected: {0}x{1}'.format(str(size), str(size)))
if size != 16 and size != 9:
    print('Unsupported board size detected, exiting. (Only 9x9 or 16x16 is supported as of now.)')
    exit(1)


start_time = time()


def solve(bo, size, box_size, dimensions):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(dimensions[0], dimensions[1]):
        if valid(bo, i, (row, col), box_size):
            bo[row][col] = i

            if solve(bo, size, box_size, dimensions):
                return True

            bo[row][col] = 21

    return False


def valid(bo, num, pos, box_size):
    # Check row
    if num in bo[pos[0]]:
        return False

    # Check column
    if num in [item[pos[1]] for item in bo]:
        return False

    # Check box
    box_x = pos[1] // box_size
    box_y = pos[0] // box_size

    for i in range(box_y*box_size, box_y*box_size + box_size):
        if num in bo[i][box_x * box_size: box_x*box_size + box_size] and (i,bo[i].index(num)) != pos:
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
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def find_empty(bo):
    for i in range(len(bo)):
        if 21 in bo[i]:
            return (i, bo[i].index(21))  # row, col

    return None


print_board(board, size)
solve(board, size, box_size, dimensions)
print("___________________")
print_board(board, size)

end_time = time()
print(end_time-start_time)