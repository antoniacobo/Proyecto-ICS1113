from parameters import ParametersContainer
from gurobipy import Model, GRB
from json import load as json_load


class VariablesContainer(dict):
    def __init__(self, parameters: ParametersContainer):
        super().__init__()
        self.parameters = parameters
        self['transportation'] = {
            'port': {
                'warehouse': set(),  # from port to warehouse
                'store': set(),  # from port to store
                'outlet': set(),  # from port to outlet
            },
            'warehouse': {
                'store': set(),  # from warehouse to store
                'outlet': set(),  # from warehouse to outlet
            },
            'store': {
                'warehouse': set(),  # from store to warehouse
                'store': set(),  # from store to store
                'outlet': set(),  # from store to outlet
            },
        }
        self['store_storage'] = set()

    def set_tranportation(self, model: Model):
        for p in self.parameters['products']:
            for t in self.parameters['transportation']:
                name = 'transport_{0}_from_{1}_to_{2}_using_{3}'.format(
                    p.id_,
                    t.from_,
                    t.to,
                    t.id)
                self['transportation'][t.from_][t.to] = model.addVar(
                    vtype=GRB.INTEGER, name=name)


if __name__ == "__main__":
    with open('data/PATHS.json') as file:
        PATHS = json_load(file)

    parameters = ParametersContainer(PATHS)
    variables = VariablesContainer(parameters)
