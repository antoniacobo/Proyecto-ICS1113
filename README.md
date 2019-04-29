# Proyecto-ICS1113 (Python-Gurobi)

Proyecto de optimización de la cadena de suministro de _Guess_.

### Crear un modelo de optimización.

```python
model = Model('nombre_modelo')
```

### Cargar parámetros.

```python
with open('data/PATHS.json') as file:
  PATHS = json.load(file)

parameters = ParametersContainer(PATH)
```

### ¿Dónde están las instancias?

```python
parameters['nombre_clase']  # este es un `dict` con todas las instancias de dicha clase
```

### Cargar las variables.

Las variables pueden ser determinadas a partir de las instancias.

```python
variables = VariablesContainer(parameters)  # esto es un contenedor vacío
variables.set_all(model)  # esto crea las variables y las agrega tanto a `variables` como a `model`

model.addVar(variable)  # esto es lo que hace `VariablesContainer` para añadir cada una de las variables al modelo
```

### ¿Dónde están las variables?

```python
variables['transportation']  # acá se encuentran las variables que indican cuánto producto se transporta de un lugar a otro
variables['storage']  # acá se enceuntran las variables que indican cuánto producto se almacena en cada lugar

variables['transportation']['desde']['hasta']  # esto es un ejemplo
```

### Añadir restricciones.

```python
for restricción in restricciones:  # una opción
  model.addConstr(restricción)

model.addConstrs((restricción for restricción in restricciones))  # otra opción
```

### Actualizar modelo y optimizar.

```python
model.update()
model.optimize()
```
