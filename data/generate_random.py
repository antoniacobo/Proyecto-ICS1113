from sys import argv
from random import randint, choice
from json import load as json_load


def generate_products(products_n: int, season_duration: int):
    with open(PATHS["PRODUCTS"], 'w') as file:
        file.write('id,volume(cm^2),season_duration\n')
        for i in range(products_n):
            file.write(f'p{i},'
                       f'{randint(10, 1000)},'
                       f'{season_duration}\n')


def generate_stores(stores_n: int):
    with open(PATHS["STORES"], 'w') as file:
        file.write('id,capacity(m^2)\n')
        for i in range(stores_n):
            file.write(f's{i},'
                       f'{randint(10, 1000)}\n')


def generate_transportation(transportation_n: int):
    with open(PATHS["TRANSPORTATION"], 'w') as file:
        file.write('id,capacity(m^2),fix_price,var_price,from,to\n')
        for i in range(transportation_n):
            file.write(f't{i},'
                       f'{randint(1, 15)}'
                       f'{randint(1, 20)}'
                       f'{randint(5000, 10000)},'
                       f'{randint(1000, 20000)},'
                       f'{choice(["port", "warehouse", "store"])},'
                       f'{choice(["outlet", "warehouse", "store"])}\n')


def generate_demand(periods_n: int, stores_n: int, products_n: int):
    with open(PATHS["DEMAND"], 'w') as file:
        file.write('period,store_id,product_id,amount\n')
        for i in range(periods_n):
            for j in range(stores_n):
                for k in range(products_n):
                    file.write(f'{i},'
                               f's{j},'
                               f'p{k},'
                               f'{randint(0, 500)}\n')


def generate_arrivals(periods_n: int, products_n: int, season_duration: int):
    with open(PATHS["ARRIVALS"], 'w') as file:
        file.write('period,product_id,amout\n')
        for i in range(periods_n):
            for j in range(products_n):
                amount = 0 if i % season_duration else randint(0, 5000)
                file.write(f'{i},'
                           f'p{j},'
                           f'{amount}\n')


def generate_data(periods_n: int, products_n: int, stores_n: int,
                  transportation_n: int, season_duration: int):
    generate_products(products_n, season_duration)
    generate_stores(stores_n)
    generate_transportation(transportation_n)
    generate_demand(periods_n, stores_n, products_n)
    generate_arrivals(periods_n, products_n, season_duration)


if __name__ == "__main__":
    with open(argv[1], 'r') as file:
        PATHS = json_load(file)
    generate_data(*map(int, argv[2:]))
