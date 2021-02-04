# Sudoku board Class and solver logic

from time import time
from copy import deepcopy


class Board:
    def __init__(self, board, size, box_size, dimensions):
        self.board = board
        self.size = size
        self.box_size = box_size
        self.dimensions = dimensions
        self.iterations = 0
        self.cues = self.set_cues()
        self.mc_cues = self.set_mc_cues()
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

    def find_min_empty(self):
        def is_list(item):
            return bool(isinstance(item, list))

        min_len_list = [0, [1, 2, 3, 4, 5, 6, 7, 8, 9]]
        for i, row in enumerate(self.mask):
            if len(list(filter(is_list, row))) >= 1:
                sorted_sets = sorted(filter(is_list, row), key=len)
                for j, shortest in enumerate(sorted_sets):
                    if self.board[i][row.index(shortest)] == 0:
                        if len(min_len_list[1]) > len(sorted_sets[j]):
                            min_len_list[0] = i
                            min_len_list[1] = sorted_sets[j]
                            break

        if min_len_list != [0, [1, 2, 3, 4, 5, 6, 7, 8, 9]]:
            return min_len_list[0], self.mask[min_len_list[0]].index(min_len_list[1])  # row, col
        else:
            return self.find_empty()

    def set_cues(self):
        cues = []
        cue_dict = dict()
        for row in self.board:
            for number in row:
                if number != 0:
                    cues.append(number)
        for i in range(self.dimensions[0], self.dimensions[1]):
            cue_dict[i] = cues.count(i)
        return cue_dict

    def set_mc_cues(self):
        mc_cues = []
        for item in sorted(self.cues.items(), key=lambda x: x[1], reverse=True):
            mc_cues.append(item[0])
        if len(mc_cues) < 9:
            missing = set(range(1, self.dimensions[1])).difference(mc_cues)
            print(f"Missing: {missing}")
            mc_cues += missing
        return mc_cues

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

        self.cues = self.set_cues()
        self.mc_cues = self.set_mc_cues()
        for i, row in enumerate(self.mask):
            for numbers in filter(masking, row):
                x_pos = row.index(numbers)
                to_mask = list()
                to_remove = set()
                for number in numbers:
                    if not self.valid(number, (i, x_pos)):
                        to_remove.add(number)
                for num in to_remove:
                    self.mask[i][x_pos].remove(num)
                for num in self.mc_cues:
                    if num in self.mask[i][x_pos]:
                        to_mask.append(num)
                self.mask[i][x_pos] = to_mask

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
        pick = self.find_min_empty()
        if not pick:
            return True
        else:
            row, col = pick

        for i in self.mask[row][col]:
            # ^ Only check for numbers in mask in the order of most common cues
            if self.valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False


def batch_preprocess(item):
    start_time = time()
    passes = item.preprocess_board()
    execution_time = time() - start_time
    return passes, execution_time, item


def batch_solve(challenge):
    start_time = time()
    challenge.solve()
    execution_time = time() - start_time
    return execution_time, challenge
