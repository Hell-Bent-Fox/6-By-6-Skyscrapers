import copy

class SudokuSolver:
    def solve(puzzle, hint):
        solution = copy.deepcopy(puzzle)
        if SudokuSolver.solveHelper(solution, hint):
            return solution
        return None

    def solveHelper(solution, hint):
        while True:
            minPossibleValueCountCell = None
            len_minPossibleValueCountCell = 100
            for rowIndex in range(6):
                for columnIndex in range(6):
                    if solution[rowIndex][columnIndex] != 0:
                        continue
                    possibleValues = SudokuSolver.findPossibleValues(rowIndex, columnIndex, solution, hint)
                    possibleValueCount = len(possibleValues)
                    if possibleValueCount == 0:
                        return False
                    if possibleValueCount == 1:
                        solution[rowIndex][columnIndex] = possibleValues.pop()
                        mass1 = solution[rowIndex]
                        mass2 = [solution[i][columnIndex] for i in range(6)]
                        if 0 not in mass1 or 0 not in mass2:
                            if SudokuSolver.check(solution, hint, mass1, mass2, rowIndex, columnIndex) == False:
                                return False
                    if not minPossibleValueCountCell or possibleValueCount < len_minPossibleValueCountCell:
                        minPossibleValueCountCell = ((rowIndex, columnIndex), possibleValues)
                        len_minPossibleValueCountCell = len(minPossibleValueCountCell[1])
            if not minPossibleValueCountCell:
                return True
            elif 1 < len_minPossibleValueCountCell:
                break

        r, c = minPossibleValueCountCell[0]
        for v in minPossibleValueCountCell[1]:
            solutionCopy = copy.deepcopy(solution)
            solutionCopy[r][c] = v
            if SudokuSolver.solveHelper(solutionCopy, hint):
                for r in range(6):
                    for c in range(6):
                        solution[r][c] = solutionCopy[r][c]
                return True
        return False

    def findPossibleValues(rowIndex, columnIndex, puzzle, hint):
        values = {1,2,3,4,5,6}
        values -= SudokuSolver.getRowValues(rowIndex, puzzle)
        values -= SudokuSolver.getColumnValues(columnIndex, puzzle)
        if len(values)>1:
            values -= SudokuSolver.getBlockValues(rowIndex, columnIndex, hint)
        return values

    def getRowValues(rowIndex, puzzle):
        return set(puzzle[rowIndex][:])

    def getColumnValues(columnIndex, puzzle):
        return {puzzle[r][columnIndex] for r in range(6)}

    def getBlockValues(rowIndex, columnIndex, hint):
        line_left = hint[23-rowIndex]
        line_right = hint[6+rowIndex]
        column_top = hint[columnIndex]
        column_down = hint[17-columnIndex]
        if line_left+line_right+column_top+column_down==0:
            return {0}
        values = {1,2,3,4,5,6}
        values -= {v for v in range(1, 7) if (v <= 6 - line_left + columnIndex + 1) and (v <= 6 + (6 - columnIndex - 1) - line_right + 1) and (v <= 6 - column_top + rowIndex + 1) and (v <= 6 + (6 - rowIndex - 1) - column_down + 1)}
        return values

    def check(solution, hint, mass1, mass2, rowIndex, columnIndex):
        if 0 not in mass1:
            line_left = hint[23 - rowIndex]
            line_right = hint[6 + rowIndex]
            if line_left != 0 or line_right != 0:
                max1 = mass1[0]
                kol1 = 1
                max2 = mass1[-1]
                kol2 = 1
                for i in range(len(mass1)):
                    if mass1[i] > max1:
                        max1 = mass1[i]
                        kol1 += 1
                    if mass1[len(mass1) - i - 1] > max2:
                        max2 = mass1[len(mass1) - i - 1]
                        kol2 += 1
                if (kol1 != line_left and line_left != 0) or (kol2 != line_right and line_right != 0):
                    return False
        if 0 not in mass2:
            column_top = hint[columnIndex]
            column_down = hint[17 - columnIndex]
            if column_top != 0 or column_down != 0:
                max1 = mass2[0]
                kol1 = 1
                max2 = mass2[-1]
                kol2 = 1
                for i in range(len(mass2)):
                    if mass2[i] > max1:
                        max1 = mass2[i]
                        kol1 += 1
                    if mass2[len(mass2) - i - 1] > max2:
                        max2 = mass2[len(mass2) - i - 1]
                        kol2 += 1
                if (kol1 != column_top and column_top != 0) or (kol2 != column_down and column_down != 0):
                    return False
        return True


def solve_puzzle (clues):
    puzzle = [
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]
    ]
    solution = SudokuSolver.solve(puzzle, clues)
    for i in range(len(solution)):
        solution[i]=tuple(solution[i])
    solution = tuple(solution)
    return solution