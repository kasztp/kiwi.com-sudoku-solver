# Sudoku solver for code.kiwi.com February 2020 challenge
# Original version for 9x9 sudoku here: https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/

from time import time
from csv import reader

board = []
with open('9x9.csv') as csvDataFile:
    csvReader = reader(csvDataFile)
    for row in csvReader:
        board.append([int(numeric_string) for numeric_string in row])
print('Board loaded successfully.')
size = int(len(board[0]))
print('Board size detected: {0}x{1}'.format(str(size), str(size)))
if size != 16 and size != 9:
    print('Unsupported board size detected, exiting. (Only 9x9 or 16x16 is supported as of now.)')
    exit(1)


start_time = time()


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 21

    return False


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 21:
                return (i, j)  # row, col

    return None

print_board(board)
solve(board)
print("___________________")
print_board(board)

end_time = time()
print(end_time-start_time)