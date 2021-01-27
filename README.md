# Sudoku solver originally prepared for Kiwi.com coding challenge

Sudoku solver for 9x9 16x16 size.

Based on:
https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/

Current speedup compared to original code (depending on size, and hardness of sudoku): ~50-67000x

Optimizations compared to original code from above:
1. Changed most for loops to list slicing & comprehension.
2. Changed for cycles to "in" for membership tests.
3. Moved size/box_size/etc constant calculations outside of for loops.
4. Added mask with possible valid values
5. Added board preprocessing based on valid values mask

New features:
1. Added ability to import csv
2. Added ability to solve both 9x9 & 16x16 sudoku puzzles
3. Added basic runtime timing for performance evaluation
4. Added logging for better performance evaluation

Todo:
1. Optimize further for speed? OR Write efficient parallel python code based on this paper: https://shawnjzlee.me/dl/efficient-parallel-sudoku.pdf
2. Test PyPy speedup?
3. Generalize for all possible sudoku sizes.
4. OCR
5. Multiplatform GUI with Kivy
