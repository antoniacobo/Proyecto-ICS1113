from collections import defaultdict
from json import load as json_load


class Product:
    def __init__(self, id_: str, volume_cm2: int, season_duration: int):
        self.id_ = id_
        self.volume_cm2 = volume_cm2
        self.season_duration = season_duration

    @property
    def volume_m2(self):
        return self.volume_cm2 / (100 ** 2)


class Store:
    def __init__(self, id_: str, capacity_m2: int):
        self.id_ = id_
        self.capacity_m2 = capacity_m2

    @property
    def capacity_cm2(self):
        return self.capacity_m2 * (100 ** 2)


class Transportation:
    def __init__(self, id_: str, capacity_m2: int,
                 fix_price: int, var_price: int, from_: str, to: str):
        self.id_ = id_
        self.capacity_m2 = capacity_m2
        self.fix_price = fix_price
        self.var_price = var_price
        self.from_ = from_
        self.to = to

    @property
    def capacity_cm2(self):
        return self.capacity_m2 * (100 ** 2)


class Demand:
    def __init__(self, period: int, store_id: str, product_id: str,
                 amount: int):
        self.period = period
        self.store_id = store_id
        self.product_id = product_id
        self.amount = amount


class Arrival:
    def __init__(self, period: int, product_id: str, amount: int):
        self.period = period
        self.product_id = product_id
        self.amount = amount


class ParametersContainer(defaultdict):
    def __init__(self, PATHS: dict):
        super().__init__(dict)
        self._load_all(PATHS)

    def _load_all(self, PATHS: dict):
        for name, path in PATHS.items():
            with open(path, 'r') as file:
                file.readline()  # skip header
                for line in file.readlines():
                    self._new_entity(name, line)

    def _new_entity(self, name: str, csv_line: str):
        data = map(lambda x: int(x) if x.isdecimal() else x,
                   csv_line.strip().split(','))

        if name == 'PRODUCTS':
            product = Product(*data)
            self[name.lower()][product.id_] = product
        elif name == 'STORES':
            store = Store(*data)
            self[name.lower()][store.id_] = store
        elif name == 'TRANSPORTATION':
            transportation = Transportation(*data)
            self[name.lower()][transportation.id_] = transportation
        elif name == 'DEMAND':
            demand = Demand(*data)
            self[name.lower()][demand.period,
                               demand.store_id,
                               demand.product_id] = demand
        elif name == 'ARRIVALS':
            arrival = Arrival(*data)
            self[name.lower()][arrival.period,
                               arrival.product_id] = arrival

        else:
            raise TypeError(f"invalid parameter of type '{name}'")


if __name__ == "__main__":
    with open('data/PATHS.json') as file:
        PATHS = json_load(file)

    parameters = ParametersContainer(PATHS)
    print(parameters)
