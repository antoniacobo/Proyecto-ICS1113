from gurobipy import Model, GRB
from json import load as json_load
from parameters import ParametersContainer
from variables import VariablesContainer


if __name__ == "__main__":
    with open('data/PATHS.json') as file:
        PATHS = json_load(file)

    parameters = ParametersContainer(PATHS)
    variables = VariablesContainer(parameters)

    model = Model('Guess')
    variables.set_all(model)

    model.update()
    model.optimize()

