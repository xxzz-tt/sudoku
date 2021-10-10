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
        self.inferences = {}

    def solve(self):
        # TODO: Write your code here
        # self.ans is a list of lists
        # return self.ans
        return self.backtrackingSearchWithInference()

    def backtrackingSearch(self):
        if self.allVarAssigned():
            return self.ans
        row, col = self.pickUnassignedVar()
        domain = self.computeDomain(row, col)
        for val in domain:
            if self.valConsistentWithAssign(val, row, col):
                self.ans[row][col] = val
                result = self.backtrackingSearch()
                if len(result) != 0:
                    return self.ans
                self.ans[row][col] = 0
        return []

    def backtrackingSearchWithInference(self):
        if self.allVarAssigned():
            return self.ans
        row, col = self.pickUnassignedVar()
        domain = self.computeDomain(row, col)
        for val in domain:
            if self.valConsistentWithAssign(val, row, col):
                self.ans[row][col] = val

                inference = self.infer(row, col, val)
                if len(inference) != 0:
                    result = self.backtrackingSearch()
                    if len(result) != 0:
                        return self.ans
                # remove inference if not true
                self.inferences[(row, col)] = []
                self.ans[row][col] = 0
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
        unassigned = []
        for i in range(9):
            for j in range(9):
                if self.ans[i][j] == 0:
                    unassigned.append((i, j))
        minVar = unassigned[0]
        domainSize = len(self.computeDomain(minVar[0], minVar[1]))
        size = len(unassigned)
        for k in range(1, size):
            var = unassigned[k]
            newDomainSize = len(self.computeDomain(var[0], var[1]))
            if newDomainSize < domainSize:
                minVar = var
                domainSize = newDomainSize
        return minVar

    def allVarAssigned(self):
        for i in range(9):
            for j in range(9):
                if self.ans[i][j] == 0:
                    return False
        return True

    def infer(self, row, col, val):
        for i in range(9):
            if i != row:
                s = self.computeDomain(i, col)
                for val in s:
                    if self.ans[i][col] == val:
                        if (i, col) in self.inferences:
                            inference = self.inferences.get(i, col)
                            inference.append(val)
                            self.inferences[(i, col)] = inference
                        else:
                            inference = [val]
                            self.inferences.update({(i, col): inference})
                t = self.computeDomain(i, col)
                if len(t) == 0:
                    return False
            if i != col:
                s = self.computeDomain(row, i)
                for val in s:
                    if self.ans[row][i] == val:
                        if (row, i) in self.inferences:
                            inference = self.inferences.get(row, i)
                            inference.append(val)
                            self.inferences[(row, i)] = inference
                        else:
                            inference = [val]
                            self.inferences.update({(row, i): inference})
                t = self.computeDomain(row, i)
                if len(t) == 0:
                    return {}
            for j in range(0, 3):
                for k in range(0, 3):
                    newRow = j + row // 3 * 3
                    newCol = k + col // 3 * 3

                    if newRow != row and newCol != col:
                        s = self.computeDomain(row, i)
                        for val in s:
                            if self.ans[j][k] == val:
                                if (j, k) in self.inferences:
                                    inference = self.inferences[(j, k)]
                                    inference.append(val)
                                    self.inferences[(j, k)] = inference
                                else:
                                    inference = [val]
                                    self.inferences.update({(j, k): inference})
                        t = self.computeDomain(j, k)
                        if len(t) == 0:
                            return {}
        return self.inferences

    def computeDomain(self, row, col):
        domain = list(range(1, 10))
        if (row, col) in self.inferences:
            invalidVals = self.inferences.get((row, col))
            for val in invalidVals:
                if val in domain:
                    domain.remove(val)
        return domain

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
