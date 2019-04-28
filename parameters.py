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


class ParameterContainer(dict):
    def __init__(self):
        super().__init__()
        self['products'] = []
        self['stores'] = []
        self['transportation'] = []
        self['demand'] = []
        self['products'] = []
        self['arrivals'] = []

    def load_all(self, PATHS: dict):
        for name, path in PATHS.items():
            with open(path, 'r') as file:
                for line in file.readlines():
                    self[name.lower()] = self._new_parameter(name, line)

    @staticmethod
    def _new_parameter(name: str, csv_line: str):
        data = map(lambda x: int(x) if x.isdecimal() else x,
                   csv_line.strip().split(','))

        if name == 'PRODUCTS':
            return Product(*data)
        elif name == 'STORES':
            return Store(*data)
        elif name == 'TRANSPORTATION':
            return Transportation(*data)
        elif name == 'DEMAND':
            return Demand(*data)
        elif name == 'ARRIVALS':
            return Arrival(*data)

        raise TypeError(f"invalid parameter of type '{name}'")


if __name__ == "__main__":
    parameters = ParameterContainer()
    with open('data/PATHS.json') as file:
        PATHS = json_load(file)
    parameters.load_all(PATHS)
