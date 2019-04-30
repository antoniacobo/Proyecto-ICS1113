from parameters import ParametersContainer
from gurobipy import Model, GRB
from json import load as json_load


class VariablesContainer(dict):
    def __init__(self, parameters: ParametersContainer):
        super().__init__()
        self.parameters = parameters
        self['transportation'] = dict()
        self['storage'] = dict()
        self['outlet'] = dict()

    def set_all(self, model: Model, periods: int=12):
        '''
        Add all variables to model.
        '''
        for _, method in filter(lambda x: x[0][:4] == '_set',
                                VariablesContainer.__dict__.items()):
            method(self, model, periods)

    def set_binary(self, model: Model, _: int):
        for t in self.parameters['transportation'].values():
            for time in range(12):
                name = 'transport_from_{0}_to_{1}_using_{2}_in{3}'.format(
                    t.from_,
                    t.to,
                    t.id_,
                    time)
                self['binary'][t.from_, t.to, t.id_, time] = model.addVar(
                    vtype=GRB.BINARY, lb=0, name=name)

    def _set_transportation(self, model: Model, _: int):
        for p in self.parameters['products'].values():
            for t in self.parameters['transportation'].values():
                for time in range(12):
                    if t.to != 'outlet':
                        name = 'transport_{0}_from_{1}_to_{2}_using_{3}_in{4}'.format(
                            p.id_,
                            t.from_,
                            t.to,
                            t.id_,
                            time)
                        self['transportation'][t.from_,
                                               t.to,
                                               t.id_,
                                               p.id_,
                                               time] = model.addVar(
                            vtype=GRB.INTEGER, lb=0, name=name)

    def _set_storage(self, model: Model, periods: int):
        for i in range(periods):
            for p in self.parameters['products'].values():
                for s in self.parameters['stores'].values():
                    name = 'stock_{0}_at_{1}_in_{2}'.format(
                        p.id_,
                        s.id_,
                        i)
                    self['storage'][p.id_,
                                    s.id_,
                                    i] = model.addVar(
                        vtype=GRB.INTEGER, lb=0, name=name)

    def _set_outlet(self, model: Model):
        for p in self.parameters['products'].values():
            for t in self.parameters['transportation'].values():
                for time in range(12):
                    if t.to == 'outlet':
                        name = f"transport_{p.id_}_from_{t.from_}_to{t.to}_" \
                               f"using_{t.id_}_in_{time}"
                        self['outlet'][p.id_,
                                       t.from_,
                                       t.id_,
                                       time] = model.addVar(
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
