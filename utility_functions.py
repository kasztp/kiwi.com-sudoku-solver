from csv import reader
from math import sqrt
from tqdm import tqdm
from sudoku_solver import Board


def load_from_csv(filename):
    board = []
    with open(filename) as csv_file:
        csv_reader = reader(csv_file)
        for row in csv_reader:
            board.append([int(numeric_string) for numeric_string in row])
    print('Board loaded successfully.')
    size = int(len(board[0]))
    if size not in (9, 16):
        print('Unsupported board size detected, exiting. (9x9 or 16x16 are supported as of now.)')
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


def load_from_dataset(filename):
    dataset = []
    board = []
    size = 9
    box_size = 3
    dimensions = (1, 10)
    with open(filename) as datafile:
        dataset_length = int(datafile.readline().strip())
        kwargs = {
            'total': dataset_length,
            'unit': ' board',
            'unit_scale': True,
            'leave': True
        }
        print(f'Loading {dataset_length} boards...')
        for line in tqdm(datafile.readlines(), **kwargs):
            row = []
            for i, item in enumerate(line.strip()):
                row.append(int(item))
                if (i + 1) % 9 == 0:
                    board.append(row)
                    row = []
            dataset.append(Board(board, size, box_size, dimensions))
            board = []
    if len(dataset) == dataset_length:
        print(f'Boards loaded successfully: {dataset_length}')
    return dataset


def save_solved_dataset(original_filename, results_file, solved_dataset):
    with open(original_filename) as datafile:
        dataset_length = int(datafile.readline().strip())
        kwargs = {
            'total': dataset_length,
            'unit': ' board',
            'unit_scale': True,
            'leave': True
        }
        output = str(dataset_length) + '\n'
        print(f'Saving {dataset_length} boards...')
        for idx, line in tqdm(enumerate(datafile.readlines()), **kwargs):
            line = line.strip() + ','
            for row in solved_dataset[idx].board:
                for number in row:
                    line += (str(number))
            output += line + '\n'
    print(f'Output file generated successfully for {dataset_length} sudokus.')
    print(f'Saving file: {results_file}')
    with open(results_file, 'w') as output_file:
        output_file.writelines(output)
