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
    """Solve the BASE + BALL = GAMES cryptarithm."""
    # Constraint programming engine
    model = cp_model.CpModel()

    base = 10

    B = model.NewIntVar(1, base - 1, "B")
    A = model.NewIntVar(0, base - 1, "A")
    S = model.NewIntVar(0, base - 1, "S")
    E = model.NewIntVar(0, base - 1, "E")
    L = model.NewIntVar(1, base - 1, "L")
    G = model.NewIntVar(0, base - 1, "G")
    M = model.NewIntVar(0, base - 1, "M")

    # We need to group variables in a list to use the constraint AllDifferent.
    letters = [B, A, S, E, L, G, M]

    # Verify that we have enough digits.
    assert base >= len(letters)

    # Define constraints.
    model.AddAllDifferent(letters)

    # BASE + BALL = GAMES
    model.Add(
        B * base ** 3 + A * base ** 2 + S * base + E +
        B * base ** 3 + A * base ** 2 + L * base + L ==
        G * base ** 4 + A * base ** 3 + M * base ** 2 + E * base + S
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
