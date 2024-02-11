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
    """Solve the APPLE + GRAPE = CHEERY cryptarithm."""
    # Constraint programming engine
    model = cp_model.CpModel()

    base = 10

    a = model.NewIntVar(1, base - 1, "A")
    p = model.NewIntVar(0, base - 1, "P")
    l = model.NewIntVar(0, base - 1, "L")
    e = model.NewIntVar(0, base - 1, "E")
    g = model.NewIntVar(1, base - 1, "G")
    r = model.NewIntVar(0, base - 1, "R")
    c = model.NewIntVar(1, base - 1, "C")
    h = model.NewIntVar(0, base - 1, "H")
    y = model.NewIntVar(0, base - 1, "Y")

    # We need to group variables in a list to use the constraint AllDifferent.
    letters = [a, p, l, e, g, r, c, h, y]

    # Verify that we have enough digits.
    assert base >= len(letters)

    # Define constraints.
    model.AddAllDifferent(letters)

    # APPLE + GRAPE = CHEERY
    model.Add(
        a * base ** 4 + p * base ** 3 + p * base ** 2 + l * base + e +
        g * base ** 4 + r * base ** 3 + a * base ** 2 + p * base + e ==
        c * base ** 5 + h * base ** 4 + e * base ** 3 + e * base ** 2 + r * base + y
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
