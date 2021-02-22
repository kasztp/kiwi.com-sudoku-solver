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
# 5. Added capability to save solutions to disk
# 6. Added concurrent batch processing capability

import argparse
from concurrent.futures import ProcessPoolExecutor
import logging
import platform
from time import time, localtime, strftime
from tqdm import tqdm
from sudoku_solver import batch_preprocess, batch_solve
from utility_functions import load_from_dataset, load_from_csv, save_solved_dataset

parser = argparse.ArgumentParser()
parser.add_argument("input_file",
                    help="Sudoku input file to solve (CSV or Flatfile).")
parser.add_argument("output_file",
                    help="Desired output file to save solution.")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()
FILENAME = args.input_file
RESULT_FILE = args.output_file
BATCH_MODE = False
INTERPRETER = f'{platform.python_implementation()} {platform.python_version()}'
logging.basicConfig(filename='./logs/kiwi_sudoku.log', level=logging.INFO)


if __name__ == '__main__':
    try:
        with open(FILENAME) as test_run:
            first_line = test_run.readline().strip()
        if ',' in first_line:
            challenge = load_from_csv(FILENAME)
            if args.verbose:
                print(challenge)
        else:
            BATCH_MODE = True
            challenges = load_from_dataset(FILENAME)
            kwargs = {
                'total': len(challenges),
                'unit': ' board',
                'unit_scale': True,
                'leave': True
            }
            if args.verbose:
                for board in challenges:
                    print(board)

        start_time = time()

        # Preprocess board based on mask:
        print('Preprocessing...')
        if BATCH_MODE:
            with ProcessPoolExecutor(max_workers=8) as executor:
                preprocessed = list(tqdm(executor.map(batch_preprocess, challenges,
                                                      chunksize=len(challenges)//8), **kwargs))

            for index, item in enumerate(preprocessed):
                challenges[index] = item[2]
        else:
            preprocess_passes = challenge.preprocess_board()
            if args.verbose:
                print(f'Preprocessing passes: {preprocess_passes}')
        print('________________________\n')

        # Solve board:
        print('Solving...')
        if BATCH_MODE:
            with ProcessPoolExecutor(max_workers=7) as executor:
                solved = list(tqdm(executor.map(batch_solve, challenges, chunksize=10), **kwargs))

            for index, item in enumerate(solved):
                challenges[index] = item[1]
        else:
            challenge.solve()

        execution_time = time() - start_time

        print('________________________\n')
        print(f'Execution Time: {execution_time}')

        # Write solutions to disk:
        if BATCH_MODE:
            save_solved_dataset(FILENAME, RESULT_FILE, challenges)
        else:
            output = ''
            for line in challenge.board:
                output += ','.join(map(str, line)) + '\n'
            print('Output file generated successfully.')
            print(f'Saving file: {RESULT_FILE}')
            with open(RESULT_FILE, 'w') as output_file:
                output_file.writelines(output)

        # Write to log:
        if BATCH_MODE:
            logging.info('-----------------------------------------------------------------------')
            logging.info(f'{strftime("%d %b %Y %H:%M:%S", localtime())}: '
                         f'Solved Challenges: {len(challenges)}, '
                         f'Avg. Time/Sudoku: {execution_time / len(challenges)} '
                         f'Overall Time Taken: {execution_time}, '
                         f'File: {FILENAME}, '
                         f'Interpreter: {INTERPRETER}')
            logging.info('-----------------------------------------------------------------------')
            per_sudoku_details = ''
            for data in tqdm(list(zip(preprocessed, solved, challenges)), **kwargs):
                pp, times, challenge = data[0], data[1], data[2]
                to_log = (f'Iterations: {challenge.iterations}, '
                          f'Preprocessing passes: {pp[0]} '
                          f'Cues: {challenge.cues} '
                          f'Time Taken: {pp[1] + times[0]}, '
                          f'File: {FILENAME}')
                logging.info(to_log)
        else:
            logging.info(f'{strftime("%d %b %Y %H:%M:%S", localtime())}: '
                         f'Iterations: {challenge.iterations}, '
                         f'Preprocessing passes: {preprocess_passes} '
                         f'Cues: {challenge.cues} '
                         f'Time Taken: {execution_time}, '
                         f'File: {FILENAME}, '
                         f'Interpreter: {INTERPRETER}')

    except (IOError, OSError) as ex:
        print(f"Caught the Error: {ex}")
        logging.info(f'Error: {ex}')
