#from gurobipy import Model, quicksum
from json import load as json_load
from parameters import ParametersContainer
#from variables import VariablesContainer


M = 1000000

def set_restrictions(model):
    '''
    Set all constrains to model.
    '''
    pass

    '''
    Se debe conservar el flujo de productos las tiendas,
    satisfaciendo, a la vez, la demanda de cada una.
    '''

    '''
    No es posible superar la capacidad m ́axima de cada tienda.
    '''

    '''
    Los medios de transporte no pueden transportar
    m ́as que su capacidad volum ́etrica m ́axima.
    '''

    '''
    Al finalizar cada temporada, los productos deben ser llevados al
    outlet.
    '''

    '''
    No llegan productos a una bodega desde otra si no se utilizó transporte.
    '''
    model.addConstrs((quicksum(
        variables['transportation'][i, j, k, u]
        for i in parameters['products'].values()
        for j in parameters['stores'].values()) <=
        quicksum(variables['binary'][j, k, u] * M
        for j in parameters['stores'].values())
        for k in parameters['stores'].values()
        for u in parameters['transportation'].values()
        ), name="storage_condition")


if __name__ == "__main__":
    with open('data/PATHS.json') as file:
        PATHS = json_load(file)

    parameters = ParametersContainer(PATHS)
    print(parameters['products'])
    variables = VariablesContainer(parameters)

    model = Model('Guess')
    variables.set_all(model)

    model.update()
    model.optimize()
