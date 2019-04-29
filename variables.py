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
                'outlet': set()  # from port to outlet
            },
            'warehouse': {
                'warehouse': set(),  # from warehouse to warehouse
                'store': set(),  # from warehouse to store
                'outlet': set()  # from warehouse to outlet
            },
            'store': {
                'warehouse': set(),  # from store to warehouse
                'store': set(),  # from store to store
                'outlet': set()  # from store to outlet
            }}
        self['storage'] = {
            'stores': set(),
            'warehouse': set()}

    def set_all(self, model: Model, periods: int=12):
        '''
        Add all variables to model.
        '''
        for _, method in filter(lambda x: x[0][:4] == '_set',
                                VariablesContainer.__dict__.items()):
            method(self, model, periods)

    def _set_tranportation(self, model: Model, _: int):
        for p in self.parameters['products'].values():
            for t in self.parameters['transportation'].values():
                name = 'transport_{0}_from_{1}_to_{2}_using_{3}'.format(
                    p.id_,
                    t.from_,
                    t.to,
                    t.id_)
                self['transportation'][t.from_][t.to] = model.addVar(
                    vtype=GRB.INTEGER, lb=0, name=name)

    def _set_storage(self, model: Model, periods: int):
        for i in range(periods):
            for p in self.parameters['products'].values():
                for s in self.parameters['stores'].values():
                    name = 'stock_{0}_at_{1}_in_{2}'.format(
                        p.id_,
                        s.id_,
                        i)
                    self['storage']['stores'] = model.addVar(
                        vtype=GRB.INTEGER, lb=0, name=name)
                name = 'stock_{0}_at_warehouse_in_{1}'.format(
                    p.id_,
                    i)
                self['storage']['warehouse'] = model.addVar(
                    vtype=GRB.INTEGER, lb=0, name=name)


if __name__ == "__main__":
    with open('data/PATHS.json') as file:
        PATHS = json_load(file)

    parameters = ParametersContainer(PATHS)
    variables = VariablesContainer(parameters)
    model = Model()
    variables.set_all(model, 12)
    model.update()
    print(len(model.getVars()))
