from ortools.sat.python import cp_model


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print(f"{v}={self.Value(v)}", end=" ")
        print()

    def solution_count(self):
        return self.__solution_count


def main():
    """Solve the RIGHT + RIGHT = WRONG cryptarithm."""
    # Constraint programming engine
    model = cp_model.CpModel()

    base = 10

    R = model.NewIntVar(1, base - 1, "R")
    I = model.NewIntVar(0, base - 1, "I")
    G = model.NewIntVar(0, base - 1, "G")
    H = model.NewIntVar(0, base - 1, "H")
    T = model.NewIntVar(1, base - 1, "T")
    W = model.NewIntVar(1, base - 1, "W")
    O = model.NewIntVar(0, base - 1, "O")
    N = model.NewIntVar(0, base - 1, "N")

    # We need to group variables in a list to use the constraint AllDifferent.
    letters = [R, I, G, H, T, W, O, N]

    # Verify that we have enough digits.
    assert base >= len(letters)

    # Define constraints.
    model.AddAllDifferent(letters)

    # RIGHT + RIGHT = WRONG
    model.Add(
        R * base ** 3 + I * base ** 2 + G * base + H +
        R * base ** 3 + I * base ** 2 + G * base + H ==
        W * base ** 4 + R * base ** 3 + O * base ** 2 + N * base + G
    )

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(letters)
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True
    # Solve.
    status = solver.Solve(model, solution_printer)

    # Statistics.
    print("\nStatistics")
    print(f"  status   : {solver.StatusName(status)}")
    print(f"  conflicts: {solver.NumConflicts()}")
    print(f"  branches : {solver.NumBranches()}")
    print(f"  wall time: {solver.WallTime()} s")
    print(f"  sol found: {solution_printer.solution_count()}")


if __name__ == "__main__":
    main()
