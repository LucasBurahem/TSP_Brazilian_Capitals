import pyomo.environ as pyomo_model
from catalog import Solver


def objective_function(model):
    return sum(model.x[i, j] * model.c[i, j] for i in model.N for j in model.M)


def mtz_model(distance_matrix):
    n = len(distance_matrix)

    # MODEL
    model = pyomo_model.ConcreteModel()

    # INDEXES FOR
    model.M = pyomo_model.RangeSet(n)
    model.N = pyomo_model.RangeSet(n)

    # DECISION VARIABLES
    model.x = pyomo_model.Var(model.M, model.N, within=pyomo_model.Binary)

    # AUXILIAR VARIABLE
    model.Z = pyomo_model.RangeSet(2, n)

    # AUXILIAR VARIABLES Z
    model.u = pyomo_model.Var(model.M, within=pyomo_model.NonNegativeIntegers, bounds=(0, n - 1))

    # DISTANCE MATRIX
    model.c = pyomo_model.Param(model.N, model.M, initialize=lambda model, i, j: distance_matrix[i - 1][j - 1])

    model.objective = pyomo_model.Objective(rule=objective_function, sense=pyomo_model.minimize)

    def come_to_constraint(model, N):
        return sum(model.x[N, j] for j in model.M if j != N) == 1

    model.const1 = pyomo_model.Constraint(model.N, rule=come_to_constraint)

    def go_to_constraint(model, M):
        return sum(model.x[i, M] for i in model.N if i != M) == 1

    model.const2 = pyomo_model.Constraint(model.M, rule=go_to_constraint)

    def eliminate_subtour(model, i, j):
            return model.u[i] - model.u[j] + model.x[i, j] * len(model.u) <= len(model.u) - 1

    model.const3 = pyomo_model.Constraint(model.Z, model.M, rule=eliminate_subtour)

    solver = pyomo_model.SolverFactory(Solver.SolverName)

    result = solver.solve(model)

    return result, model