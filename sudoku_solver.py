import pandas as pd
import numpy as np
import random


class SolutionFound(Exception):
    pass


def csv_to_array(filename, puzzle_limit):
    df = pd.read_csv(filename)
    puzzle = []
    cheat = []
    limit = puzzle_limit
    while puzzle_limit > 0:
        i = random.randint(0, limit)
        puzzle_list = list(map(int, df.loc[i][0]))
        puzzle_arr = np.array(puzzle_list).reshape(9, 9)
        puzzle.append(puzzle_arr)
        cheat_list = list(map(int, df.loc[i][1]))
        cheat_arr = np.array(cheat_list).reshape(9, 9)
        cheat.append(cheat_arr)
        puzzle_limit -= 1
    return puzzle, cheat


def recursive_solver(array, row, col):
    if col == 9:
        row += 1
        col = 0
    if row == 9:
        raise SolutionFound(array)
    if array[row][col] != 0:
        recursive_solver(array, row, col + 1)
        return
    row_values = set(array[row])
    col_values = set(array[:, col])
    grid_values = set(array[row-row % 3:(row + 3)-row % 3
                            , col-col % 3:(col + 3)-col % 3].flatten())
    valid_values = set(range(1, 10))-row_values-col_values-grid_values
    for value in valid_values:
        array_copy = array.copy()
        array_copy[row][col] = value
        try:
            recursive_solver(array_copy, row, col + 1)
        except SolutionFound as e:
            raise SolutionFound(e.args[0])


limit = int(input("How many puzzles to be solved(max = 100): "))
if(limit > 0 and limit < 100):
    puzzlelist, cheatlist = csv_to_array("sudoku_chunk.csv", limit)
    for i in range(limit):
        try:
            array_copy = puzzlelist[i].copy()
            solution = recursive_solver(array_copy, 0, 0)
        except SolutionFound as e:
            with open("solutions.txt", "a") as file:
                file.writelines(f"Puzzle {i}.\n")
                for x in range(9):
                    file.writelines(f"{e.args[0][x]}\n")
                file.writelines(f"\n")
                file.writelines(f"\n")
                for x in range(9):
                    file.writelines(f"{cheatlist[i][x]}\n")
                file.writelines(f"\n")
