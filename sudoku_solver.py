# Sudoku solver for code.kiwi.com February 2020 challenge
# Original version for 9x9 sudoku here:
# https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
#
# Optimizations:
# 1. Changed most for loops to list slicing & comprehension.
# 2. Changed for cycles to "in" for membership tests.
# 3. Moved size/box_size/etc constant calculations outside of for loops.
# 4. Added mask with possible valid values
# 5. Added board preprocessing based on valid value mask
# 6. Extended preprocessing with mask_update method
#
# New features:
# 1. Added ability to import csv
# 2. Added ability to solve both 9x9 & 16x16 sudoku puzzles
# 3. Added basic runtime timing for performance evaluation
# 4. Added logging for better performance evaluation

import logging
import platform
from copy import deepcopy
from csv import reader
from math import sqrt
from time import time, localtime, strftime

interpreter = f'{platform.python_implementation()} {platform.python_version()}'
logging.basicConfig(filename='./logs/kiwi_sudoku.log', level=logging.INFO)


class Board:
    def __init__(self, board, size, box_size, dimensions):
        self.board = board
        self.size = size
        self.box_size = box_size
        self.dimensions = dimensions
        self.iterations = 0
        self.mask = self.create_mask()

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
            if num in self.board[i][box_x * self.box_size: box_x * self.box_size + self.box_size] \
                    and (i, self.board[i].index(num)) != pos:
                return False

        return True

    def find_empty(self):
        for i, row in enumerate(self.board):
            if 0 in row:
                return i, row.index(0)  # row, col
        return None

    def create_mask(self):
        mask = deepcopy(self.board)
        for i, row in enumerate(mask):
            if 0 in row:
                while 0 in row:
                    zero_index = row.index(0)
                    mask[i][zero_index] = set()
                    for number in range(self.dimensions[0], self.dimensions[1]):
                        if self.valid(number, (i, zero_index)):
                            mask[i][zero_index].add(number)
            else:
                for number in row:
                    if number != 0:
                        mask[i][row.index(number)] = {number}
        return mask

    def update_mask(self):
        def masking(item):
            return bool(isinstance(item, set) and len(item) > 1)

        for i, row in enumerate(self.mask):
            for numbers in filter(masking, row):
                x_pos = row.index(numbers)
                to_remove = set()
                for number in numbers:
                    if not self.valid(number, (i, x_pos)):
                        to_remove.add(number)
                for num in to_remove:
                    self.mask[i][x_pos].remove(num)

    def update_board(self):
        def masking(item):
            return bool(isinstance(item, set) and len(item) == 1)

        for i, row in enumerate(self.mask):
            for number in filter(masking, row):
                x_pos = row.index(number)
                num = number.pop()
                self.board[i][x_pos] = num
                self.mask[i][x_pos] = num

    def preprocess_board(self):
        temp_board = deepcopy(self)
        temp_board.mask = None
        passes = 0
        while temp_board.mask != self.mask:
            passes += 1
            temp_board = deepcopy(self)
            self.update_board()
            self.update_mask()
        return passes

    def solve(self):
        self.iterations += 1

        if not self.find_empty():
            return True
        else:
            row, col = self.find_empty()

        for i in self.mask[row][col]:
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
    if size not in (9, 16):
        print('Unsupported board size detected, exiting. (Only 9x9 or 16x16 is supported as of now.)')
        return None
    box_size = int(sqrt(size))
    if size == 16:
        start = 1
        end = 17
    else:
        start = 1
        end = 10
    dimensions = (start, end)
    print(f'Board size detected: {size}x{size}')
    return Board(board, size, box_size, dimensions)


filename = './sudokus/9x9.csv'
challenge = load_board(filename)

print('________________________\n')
print(challenge)

start_time = time()

# Preprocess board based on mask:
preprocess_passes = challenge.preprocess_board()
print(f'Preprocessing passes: {preprocess_passes}')

# Solve board:
challenge.solve()

execution_time = time() - start_time

print('________________________\n')
print(challenge)
print(execution_time)

logging.info(f'{strftime("%d %b %Y %H:%M:%S", localtime())}: '
             f'Iterations: {challenge.iterations}, Preprocessing passes: {preprocess_passes} '
             f'Time Taken: {execution_time}, File: {filename}, Interpreter: {interpreter}')
