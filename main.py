#from gurobipy import Model, quicksum
from json import load as json_load
from parameters import ParametersContainer
#from variables import VariablesContainer


M = 1000000
periods = 12

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
    model.addConstr((quicksum(
        parameters['products'][pid].volume_m2 * variables['storage'][
            pid, sid, t] for pid in parameters['products']) <=
                     variables['storage'][pid, sid, t].capacity_m2 for sid in
                     variables['storage'] for t in range(periods) for pid in
                     parameters['products']), 'C2')
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
    model.addConstrs((variables['transportation'][i, j, k, u, t] <=
        variables['binary'][j, k, u, t] * M
        for i in parameters['products']
        for j in parameters['stores']
        for k in parameters['stores']
        for u in parameters['transportation']
        for t in range(periods)
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
