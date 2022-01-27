import itertools

rows = 'ABCDEFGHI'
columns = '123456789'


def combine(array1, array2):
    return [a + b for a in array1 for b in array2]


def permutate(iterable):
    result = list()
    for L in range(0, len(iterable) + 1):
        if L == 2:
            for subset in itertools.permutations(iterable, L):
                result.append(subset)
    return result


class Sudoku:
    def __init__(self, grid):
        self.variables = list()
        self.domains = dict()
        self.constraints = list()
        self.neighbors = dict()
        self.pruned = dict()
        self.prepare(grid)

    def prepare(self, grid):
        game = list(grid)
        self.variables = combine(rows, columns)
        self.domains = {v: list(range(1, 10)) if game[i] == '0' else [int(game[i])] for i, v in
                        enumerate(self.variables)}
        self.pruned = {v: list() if game[i] == '0' else [int(game[i])] for i, v in enumerate(self.variables)}
        self.build_constraints()
        self.build_neighbors()

    def build_constraints(self):
        blocks = (
                [combine(rows, number) for number in columns] +
                [combine(character, columns) for character in rows] +
                [combine(character, number) for character in ('ABC', 'DEF', 'GHI') for number in ('123', '456', '789')]
        )
        for block in blocks:
            combinations = permutate(block)
            for combination in combinations:
                if [combination[0], combination[1]] not in self.constraints:
                    self.constraints.append([combination[0], combination[1]])

    def revise(self, xi, xj):
        revised = False
        for x in self.domains[xi]:
            if not any([x != y for y in self.domains[xj]]):
                self.domains[xi].remove(x)
                revised = True
        return revised

    def select_unassigned_variable(self, assignment):
        unassigned = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def order_domain_values(self, var):
        if len(self.domains[var]) == 1:
            return self.domains[var]
        return sorted(self.domains[var], key=lambda val: self.conflicts(var, val))

    def conflicts(self, var, val):
        count = 0
        for n in self.neighbors[var]:
            if len(self.domains[n]) > 1 and val in self.domains[n]:
                count += 1
        return count

    def build_neighbors(self):
        for x in self.variables:
            self.neighbors[x] = list()
            for c in self.constraints:
                if x == c[0]:
                    self.neighbors[x].append(c[1])

    def solved(self):
        for v in self.variables:
            if len(self.domains[v]) > 1:
                return False

        return True

    def complete(self, assignment):
        for x in self.variables:
            if len(self.domains[x]) > 1 and x not in assignment:
                return False

        return True

    def consistent(self, assignment, var, value):
        consistent = True
        for key, val in assignment.items():
            if val == value and key in self.neighbors[var]:
                consistent = False
        return consistent

    def assign(self, var, value, assignment):
        assignment[var] = value
        self.forward_check(var, value, assignment)

    def unassign(self, var, assignment):
        if var in assignment:
            for (D, v) in self.pruned[var]:
                self.domains[D].append(v)
            self.pruned[var] = []
            del assignment[var]

    def forward_check(self, var, value, assignment):
        for neighbor in self.neighbors[var]:
            if neighbor not in assignment:
                if value in self.domains[neighbor]:
                    self.domains[neighbor].remove(value)
                    self.pruned[var].append((neighbor, value))

    def build_assignment(self):
        assignment = {}
        for x in self.variables:
            if len(self.domains[x]) == 1:
                assignment[x] = self.domains[x][0]
        return assignment

    def extract_solution(self):
        solution = ""
        for var in self.variables:
            solution += str(self.domains[var])
        return solution
