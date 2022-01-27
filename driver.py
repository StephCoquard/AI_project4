import sys
from sudoku import Sudoku


def ac3(sudoku):
    queue = list(sudoku.constraints)
    while queue:
        xi, xj = queue.pop(0)
        if sudoku.revise(xi, xj):
            if len(sudoku.domains[xi]) == 0:
                return False
            for xk in sudoku.neighbors[xi]:
                if xk != xi:
                    queue.append([xk, xi])
    return True


def backtrack(assignment, sudoku):
    if len(assignment) == len(sudoku.variables):
        return assignment
    var = sudoku.select_unassigned_variable(assignment)
    for value in sudoku.order_domain_values(var):
        if sudoku.consistent(assignment, var, value):
            sudoku.assign(var, value, assignment)
            result = backtrack(assignment, sudoku)
            if result:
                return result
            sudoku.unassign(var, assignment)
    return False


def main():
    grid = sys.argv[1].lower()

    sudoku = Sudoku(grid)

    solution = None
    ac3(sudoku)
    if sudoku.solved():
        solution = sudoku.extract_solution() + " AC3"
    else:
        assignment = sudoku.build_assignment()
        if assignment:
            backtrack(assignment, sudoku)
            for d in sudoku.domains:
                sudoku.domains[d] = assignment[d] if len(d) > 1 else sudoku.domains[d]
            solution = sudoku.extract_solution() + " BTS"

    if solution:
        fo = open("output.txt", 'w')
        fo.write(solution)
        fo.close()


if __name__ == "__main__":
    main()
