# CS3243 Introduction to Artificial Intelligence
# Project 2

import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        # TODO: Write your code here
        if self.allVarAssigned():
            return self.ans
        row, col = self.pickUnassignedVar()
        for val in range(1, 10):
            if self.valConsistentWithAssign(val, row, col):
                self.ans[row][col] = val
                result = self.solve()
                if len(result) != 0:
                    return self.ans
                self.ans[row][col] = 0
        # self.ans is a list of lists
        # return self.ans
        return []

    def consistentInRow(self, val, row):
        for i in range(9):
            if val == self.ans[row][i]:
                return False
        return True

    def consistentInCol(self, val, col):
        for i in range(9):
            if val == self.ans[i][col]:
                return False;
        return True

    def consistentInBox(self, val, row, col):
        bRow = row // 3
        bCol = col // 3

        startRow = bRow * 3
        startCol = bCol * 3
        for i in range(3):
            for j in range(3):
                if val == self.ans[startRow + i][startCol + j]:
                    return False
        return True

    def valConsistentWithAssign(self, val, row, col):
        return self.consistentInRow(val, row) and self.consistentInCol(val, col) and self.consistentInBox(val, row, col)

    def pickUnassignedVar(self):
        for i in range(9):
            for j in range(9):
                if self.ans[i][j] == 0:
                    return i, j

    def allVarAssigned(self):
        for i in range(9):
            for j in range(9):
                if self.ans[i][j] == 0:
                    return False
        return True

    def infer(self, row, col, val):
        inference = []
        varQueue = [(row, col)]
        while not len(varQueue) == 0:
            y = varQueue.pop(0)
    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_32.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_32.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
