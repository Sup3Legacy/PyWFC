#Résolution d'un sudoku par l'algorithme WFC
import numpy as np
import random

class Sudoku:
    def __init__(self):
        self.stated = np.zeros((9, 9), dtype = np.int8)
        self.entropy = np.full((9, 9), 8)
        self.possibles = np.empty((9, 9), dtype = np.object)
        for i in range(9):
            for j in range(9):
                self.possibles[i, j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.solvedCells = 0
        self.startCells = []

    def sudoToMatrix(self, i, j):
        return (3 * (i % 3) + j % 3, 3 * (i // 3) + j // 3)

    def matrixToSudo(self, x, y):
        return (3 * (y // 3) + (x // 3), 3 * (y % 3) + (x % 3))

    def fix(self, x, y, e): #En coordonnées matrix
        self.stated[x, y] = e
        self.entropy[x, y] = 0
        self.solvedCells += 1
        self.induct(x, y)

    def fixList(self, list):
        for i in range(9):
            for j in range(9):
                if list[i][j] > 0:
                    self.fix(i, j, list[i][j])
                    self.startCells.append((i, j, list[i][j]))

    def restart(self):
        self.stated = np.zeros((9, 9), dtype = np.int8)
        self.entropy = np.full((9, 9), 8)
        self.possibles = np.empty((9, 9), dtype = np.object)
        for i in range(9):
            for j in range(9):
                self.possibles[i, j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.solvedCells = 0
        for (x, y, e) in self.startCells:
            self.fix(x, y, e)

    def induct(self, x, y):
        if self.entropy[x, y] > 1:
            print("Cannot induct from. None-zero entropy case.")
            return False
        for i in range(9):
            if self.stated[i, y] == 0 and self.stated[x, y] in self.possibles[i, y]:
                self.possibles[i, y].remove(self.stated[x, y])
                self.entropy[i, y] = max(len(self.possibles[i, y]), 1)
        for j in range(9):
            if self.stated[x, j] == 0 and self.stated[x, y] in self.possibles[x, j]:
                self.possibles[x, j].remove(self.stated[x, y])
                self.entropy[x, j] = max(len(self.possibles[x, j]), 1)
        (case, _) = self.matrixToSudo(x, y)
        for i in range(9):
            a, b = self.sudoToMatrix(case, i)
            if self.stated[a, b] == 0 and self.stated[x, y] in self.possibles[a, b]:
                self.possibles[a, b].remove(self.stated[x, y])
                self.entropy[a, b] = max(len(self.possibles[a, b]), 1)

    def get_least_entropy(self):
        mini = 9
        x0, y0 = -1, -1
        for i in range(9):
            for j in range(9):
                if self.entropy[i, j] > 0 and self.entropy[i, j] < mini:
                    mini = self.entropy[i, j]
                    x0, y0 = i, j
        if mini == 9:
            return (None, None)
        else:
            return (x0, y0)

    def collapse(self, x, y):
        if self.stated[x, y] != 0:
            self.entropy[x, y] = 0
            return True
        else:
            if len(self.possibles[x, y]) == 0:
                return False
            else:
                self.stated[x, y] = random.choice(self.possibles[x, y])
                self.possibles[x, y] = []
                self.entropy[x, y] = 0
                self.solvedCells += 1
                self.induct(x, y)
                return True

    def solveOnce(self):
        res = True
        while res and self.solvedCells < 81:
            (x, y) = self.get_least_entropy()
            if x != None:
                res = self.collapse(x, y)
        return res

    def solve(self, numberOfTries):
        i = 0
        while (not self.solveOnce()) and i < numberOfTries:
            i += 1
            self.restart()
        print("Youpii en " + str(i) if i < numberOfTries else "Hmhmm")
        return i < numberOfTries


    def print_grid(self):
        for i in range(9):
            res = ""
            if i % 3 == 0 and i > 0:
                print("---+---+---")
            for j in range(9):
                if j % 3 == 0 and j > 0:
                    res += '|'
                if self.stated[i, j] == 0:
                    carac = '#'
                else:
                    carac = str(self.stated[i, j])
                res += carac
            print(res)

sudo = Sudoku()
afix = [
    [0, 0, 9, 0, 3, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 7, 9, 0],
    [0, 6, 0, 0, 0, 1, 0, 0, 4],
    [0, 0, 0, 4, 0, 0, 8, 0, 5],
    [0, 0, 0, 7, 5, 6, 0, 0, 0],
    [4, 0, 5, 0, 0, 3, 0, 0, 0],
    [9, 0, 0, 2, 0, 0, 0, 5, 0],
    [0, 7, 4, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 7, 0, 1, 0, 0]
]
afix2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 9, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
sudo.fixList(afix)
sudo.solve(5000)
