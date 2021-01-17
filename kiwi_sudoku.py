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


logging.basicConfig(filename='kiwi_sudoku.log', level=logging.INFO)


class Board:
    def __init__(self, board, size, box_size, dimensions):
        self.board = board
        self.size = size
        self.box_size = box_size
        self.dimensions = dimensions
        self.iterations = 0
        self.mask = list()

    def __repr__(self):
        to_print = str()
        for i in range(self.size):
            if i % self.box_size == 0 and i != 0:
                to_print += '- - - - - - - - - - - -\n'

            for j in range(self.size):
                if j % self.box_size == 0 and j != 0:
                    to_print += ' | '

                if j == (self.size - 1):
                    to_print += str(self.board[i][j]) + '\n'
                else:
                    to_print += str(self.board[i][j]) + ' '
        return to_print

    def valid(self, num, pos):
        # Check row
        if num in self.board[pos[0]]:
            return False

        # Check column
        if num in [item[pos[1]] for item in self.board]:
            return False

        # Check box
        box_x = pos[1] // self.box_size
        box_y = pos[0] // self.box_size

        for i in range(box_y * self.box_size, box_y * self.box_size + self.box_size):
            if num in self.board[i][box_x * self.box_size: box_x * self.box_size + self.box_size]\
                    and (i, self.board[i].index(num)) != pos:
                return False

        return True

    def find_empty(self):
        for i, row in enumerate(self.board):
            if 0 in row:
                return i, row.index(0)  # row, col
        return None

    def solve(self):
        self.iterations += 1

        if not self.find_empty():
            return True
        else:
            row, col = self.find_empty()

        for i in range(self.dimensions[0], self.dimensions[1]):
            if self.valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False


def load_board(filename):
    board = []
    with open(filename) as csvDataFile:
        csv_reader = reader(csvDataFile)
        for row in csv_reader:
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
    print(f'Board size detected: {size}x{size}')
    if size != 16 and size != 9:
        print('Unsupported board size detected, exiting. (Only 9x9 or 16x16 is supported as of now.)')
        return None
    return Board(board, size, box_size, dimensions)


challenge = load_board('9x9.csv')
print(challenge)

start_time = time()

challenge.solve()
execution_time = time() - start_time

print('___________________\n')
print(challenge)
print(execution_time)

logging.info(f'{time()}: Iterations: {challenge.iterations}, Time Taken: {execution_time}')
