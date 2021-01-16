# Sudoku solver for code.kiwi.com February 2020 challenge
# Original version for 9x9 sudoku here: https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
#
# Optimizations:
# 1. Changed most for loops to list slicing & comprehension.
# 2. Changed for cycles to "in" for membership tests.
# 3. Moved size/box_size/etc constant calculations outside of for loops.
#
# New features:
# 1. Added ability to import csv
# 2. Added ability to solve both 9x9 & 16x16 sudoku puzzles
# 3. Added basic runtime timing for performance evaluation
# 4. Added logging for better performance evaluation
import logging
from time import time
from math import sqrt
from csv import reader


logging.basicConfig(filename="kiwi_sudoku.log", level=logging.INFO)


def load_board(filename):
    board = []
    with open(filename) as csvDataFile:
        csvReader = reader(csvDataFile)
        for row in csvReader:
            board.append([int(numeric_string) for numeric_string in row])
    print('Board loaded successfully.')
    size = int(len(board[0]))
    box_size = int(sqrt(size))
    if size == 16:
        start = 1
        end = 17
    else:
        start = 1
        end = 10
    dimensions = (start, end)
    print(size)
    print('Board size detected: {0}x{1}'.format(str(size), str(size)))
    if size != 16 and size != 9:
        print('Unsupported board size detected, exiting. (Only 9x9 or 16x16 is supported as of now.)')
        return None
    return tuple((board, size, box_size, dimensions))


def print_board(board_array):
    bo = board_array[0]
    size = board_array[1]
    box_size = board_array[2]
    for i in range(size):
        if i % box_size == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(size):
            if j % box_size == 0 and j != 0:
                print(" | ", end="")

            if j == (size - 1):
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def solve(board_array):
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

        for i in range(box_y * box_size, box_y * box_size + box_size):
            if num in bo[i][box_x * box_size: box_x * box_size + box_size] and (i, bo[i].index(num)) != pos:
                return False

        return True

    def find_empty(bo, size):
        for i in range(size):
            if 0 in bo[i]:
                return i, bo[i].index(0)  # row, col
        return None

    bo = board_array[0]
    size = board_array[1]
    box_size = board_array[2]
    dimensions = board_array[3]

    find = find_empty(bo, size)

    if not find:
        return True
    else:
        row, col = find

    for i in range(dimensions[0], dimensions[1]):
        if valid(bo, i, (row, col), box_size):
            bo[row][col] = i

            if solve((bo, size, box_size, dimensions)):
                return True

            bo[row][col] = 0

    return False


challenge = load_board('9x9.csv')
print_board(challenge)
start_time = time()

solve(challenge)
execution_time = time() - start_time

print("___________________\n")
print_board(challenge)
print(execution_time)

logging.info(f'{time()}: {execution_time}')
