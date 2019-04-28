from gurobipy import Model, GRB
from json import load as json_load
from parameters import ParametersContainer
from variables import VariablesContainer


def set_restrictions(model: Model):
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
    No llegan productos a una bodega desde otra si no se utiliz ́o transporte.
    '''


if __name__ == "__main__":
    with open('data/PATHS.json') as file:
        PATHS = json_load(file)

    parameters = ParametersContainer(PATHS)
    variables = VariablesContainer(parameters)

    model = Model('Guess')
    variables.set_all(model)

    model.update()
    model.optimize()
