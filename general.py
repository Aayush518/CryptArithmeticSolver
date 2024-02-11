from ortools.sat.python import cp_model

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.solutions = []
        self.statistics = {}

    def on_solution_callback(self):
        solution = ''
        for v in self.__variables:
            solution += f"{v}={self.Value(v)} "
        self.solutions.append(solution)

    def solution_count(self):
        return len(self.solutions)

def solve_cryptarithmetic(first_string, second_string, third_string):
    """Solve the cryptarithmetic puzzle."""
    # Constraint programming engine
    model = cp_model.CpModel()

    # Get unique letters from all strings
    all_letters = set(first_string + second_string + third_string)
    letters = {}
    for letter in all_letters:
        letters[letter] = model.NewIntVar(0, 9, letter)

    # Convert strings to variables
    first_num = sum(letters[letter] * 10**i for i, letter in enumerate(reversed(first_string)))
    second_num = sum(letters[letter] * 10**i for i, letter in enumerate(reversed(second_string)))
    third_num = sum(letters[letter] * 10**i for i, letter in enumerate(reversed(third_string)))

    # Define constraints
    model.Add(first_num + second_num == third_num)

    # Ensure each letter corresponds to a unique value
    model.AddAllDifferent(list(letters.values()))

    # Ensure the first letter of the result string (carryover) is not zero
    model.Add(letters[third_string[0]] != 0)

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(list(letters.values()))
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True
    # Solve.
    status = solver.Solve(model, solution_printer)

    # Statistics
    statistics = {
        "status": solver.StatusName(status),
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "wall_time": solver.WallTime(),
        "sol_found": solution_printer.solution_count()
    }

    return solution_printer.solutions, statistics
