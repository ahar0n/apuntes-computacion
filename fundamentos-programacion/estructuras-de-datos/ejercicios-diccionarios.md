
# Ejercicios: Tratamiento de diccionarios

**DCT-001.** Una agenda (diccionario) relaciona nombres con teléfonos. Implemente la función `registrar_contacto(agenda, nombre, telefono)` para agregar un contacto solo si su nombre no aparece como clave. Si ya existe, conservar su teléfono.

La agenda relaciona nombres de contacto con teléfonos representados como cadenas. `nombre` y `telefono` son cadenas no vacías. Cada nombre identifica un contacto de manera única. La función modifica el diccionario recibido y devuelve `True` si inserta la entrada o `False` si el nombre ya existe.


**DCT-002.** Una red meteorológica mantiene un registro de la precipitación acumulada de cada estación. El diccionario relaciona códigos de estación con milímetros enteros no negativos.

```python
estaciones = {
    # código: (nombre, ubicación, agua caída en mm)
    "180005": ("Chacalluta", "Arica", 0),
    "230001": ("Andrés Sabella", "Antofagasta", 0),
    "290004": ("La Florida", "La Serena", 2),
    "330007": ("Rodelillo", "Valparaíso", 8),
    "330020": ("Quinta Normal", "Santiago", 5),
    "360019": ("Carriel Sur", "Concepción", 18),
    "390006": ("Pichoy", "Valdivia", 32),
    "400009": ("Cañal Bajo", "Osorno", 25),
    "410005": ("El Tepual", "Puerto Montt", 28),
    "520006": ("Carlos Ibáñez", "Punta Arenas", 6),
}
```

Implemente tres funciones: 

- `obtener_estaciones(precipitaciones)` devuelve una lista de los códigos de cada estación. 
- `sumar_lecturas(precipitaciones)`, que suma el agua caída registrada en todas las estaciones. 
- `seleccionar_bajas(precipitaciones, umbral)`, que devuelve otro diccionario con las entradas de lectura menor o igual al umbral especificado.

Los códigos son cadenas no vacías y cada valor es la lectura de una estación. La suma representa la suma de lecturas de las estaciones. El umbral es un entero no negativo. La selección conserva las lecturas originales. En un registro vacío se esperan una lista vacía, cero y un diccionario vacío, respectivamente.


(ejdic-04)=
**DCT-003.** Un catálogo bibliográfico relaciona códigos de libros con sus títulos, representados como cadenas. Implemente la función `retirar_libro(catalogo, codigo)` para eliminar la entrada de un libro identificado por su código.

La función modifica el diccionario recibido, devuelve `True` si elimina una entrada y `False` si el código estaba ausente. Los códigos son cadenas no vacías.



(ejdic-05)=
**DCT-004.** Implemente `contar_respuestas(respuestas)` que cuenta la cantidad de veces que aparece cada respuesta de una encuesta.

El parámetro es una lista de cadenas no vacías. Las cadenas se comparan exactamente: `"Sí"` y `"sí"` son categorías distintas. La función devuelve un diccionario con cada respuesta y su frecuencia positiva, sin modificar la lista. Un argumento vacío retorna un diccionario vacío.

Por ejemplo, la llamada a la función con el argumento `['sí', 'no', 'sí', 'sí', 'no']` retorna `{'sí': 3, 'no': 2}`.



(ejdic-06)=
**DCT-005.** Mesas electorales registran los votos obtenidos por cada candidatura. 

1. Implemente `consolidar_votos(primera, segunda)` para reunir los resultados (acumular los votos) de la primera y la segunda mesa. Las candidaturas presentes en ambas deben acumular votos, las que aparecen en una sola conservan su cantidad. Cada mesa es un diccionario con nombres de candidaturas como claves de tipo cadena y cantidades de votos. La función devuelve un nuevo diccionario. Para cada nombre presente en alguna de las mesas, el resultado contiene la suma de sus cantidades, considerando cero en la mesa donde esté ausente.

2. Redacte un párrafo breve con la estrategía implementada.


(ejdic-07)=
**DCT-006.** Analice el siguiente fragmento de código:

```python
sensores = {"Sensor01": 0, "Sensor02": 4, "Sensor03": 0}
for codigo, cantidad in sensores.items():
    if cantidad == 0:
        del sensores[codigo]
```

El diccionario `sensores` relaciona identificadores de sensores, cadenas no vacías, con cantidades enteras no negativas de lecturas recibidas.

1. Explique por qué no es una solución válida para remover los sensores que no registraron lecturas. 
2. Implemente `depurar_sensores(sensores)` que debe retornar un diccionario sin entradas de cantidad cero y conservar el original.
3. Diseñe y ejecute los casos de prueba que permitan validar la solución implementada.



(ejdic-10)=
**DCT-007.** Un recetario relaciona códigos de recetas con fichas que contienen un nombre y una lista de ingredientes. 

```python

recetario = {
    "R01": {
        "nombre": "Sopa de verduras",
        "ingredientes": ["agua", "papa", "zanahoria", "sal"],
    },
    "R02": {
        "nombre": "Ensalada de tomate",
        "ingredientes": ["tomate", "cebolla", "aceite", "sal"],
    },
    "R03": {
        "nombre": "Arroz con verduras",
        "ingredientes": ["arroz", "agua", "zanahoria", "arvejas"],
    },
    "R04": {
        "nombre": "Tortilla de espinacas",
        "ingredientes": ["huevo", "espinaca", "aceite", "sal"],
    },
}

```
Cada clave exterior es un código de receta. Cada valor es un diccionario con `"nombre"`, una cadena, e `"ingredientes"`, una lista de cadenas no vacías.

Implemente la función `copiar_recetario(recetario)` que genera una copia que permita modificar nombres y listas de ingredientes sin afectar al original.




(ejdic-11)=
**DCT-008.** Una empresa de transporte registra el destino de cada paquete en un diccionario:

```python
envios = {
    "CL-20261016-04821": "Santiago",
    "CL-20261016-04822": "Valparaíso",
    "CL-20261016-04823": "Concepción",
    "CL-20261016-04824": "Santiago",
    "CL-20261016-04825": "Temuco",
    "CL-20261016-04826": "Valparaíso",
    "CL-20261016-04827": "Concepción",
    "CL-20261016-04828": "Santiago",
}
```

Las claves son identificadores de paquetes y los valores son ciudades de destino. Códigos de envío y destinos son cadenas no vacías. Cada paquete tiene un código único, pero varios pueden enviarse al mismo destino. 

Implemente `agrupar_por_destino(envios)` que devuelve un diccionario que asocie cada destino con la lista de identificadores de paquetes enviados a dicho destino.




(ejdic-12)=
**DCT-009.** Un cine recibe una lista de fichas de películas con tres campos `"codigo"`, `"titulo"` y `"duracion"`, todos inmutables. La duración se expresa en minutos.

```python
fichas = [
    {"codigo": "PEL-001", "titulo": "El viaje de Chihiro", "duracion": 125},
    {"codigo": "PEL-002", "titulo": "WALL-E", "duracion": 98},
    {"codigo": "PEL-003", "titulo": "Coco", "duracion": 105},
    {"codigo": "PEL-002", "titulo": "WALL-E", "duracion": 100},
]
```

Códigos y títulos son cadenas no vacías, las duraciones son enteros. Si un código aparece varias veces, debe conservarse la última ficha completa asociada con ese código.

Implemente `organizar_peliculas(fichas)` que retorne un diccionario cuya clave es el código y su valor, una copia de la ficha. El valor devuelto debe permitir cambiar duraciones sin alterar las fichas originales.




(ejdic-13)=
**DCT-010.** Un almacén necesita procesar los pedidos recibidos durante una jornada y determinar sus existencias finales. El inventario relaciona códigos de productos con cantidades enteras no negativas. Cada pedido se representa mediante un diccionario con los campos `"codigo"` y `"cantidad"`.

Desarrolle un programa modular cuya función principal sea `procesar_pedidos(inicial, pedidos)`. Los pedidos deben procesarse en el orden recibido. Un pedido se atiende únicamente cuando el producto está registrado y dispone de unidades suficientes. En ese caso se descuenta la cantidad solicitada, en caso contrario, las existencias permanecen iguales. El rechazo de un pedido no impide procesar los posteriores. Los productos cuyo saldo llega a cero deben conservarse en el inventario.

La función debe devolver un diccionario con las siguientes entradas:

- `"inventario"`: existencias finales.
- `"resultados"`: lista de diccionarios, uno por pedido y en el mismo orden, con los campos `"codigo"`, `"cantidad"` y `"estado"`. Los estados posibles son `"atendido"`, `"producto ausente"` y `"cantidad insuficiente"`.

Los argumentos recibidos no deben modificarse. Determine qué funciones auxiliares necesita y establezca sus responsabilidades.

A continuación se muestran ejemplos de datos y llamada a la función principal:

```python
inventario_inicial = {
    "ALM-001": 12,
    "ALM-002": 0,
    "ALM-003": 8,
}

pedidos = [
    {"codigo": "ALM-001", "cantidad": 5},
    {"codigo": "ALM-003", "cantidad": 10},
    {"codigo": "ALM-009", "cantidad": 2},
    {"codigo": "ALM-001", "cantidad": 7},
    {"codigo": "ALM-002", "cantidad": 1},
]

pedidios_procesados = procesar_pedidos(inventario_inicial, pedidos)

print(pedidios_procesados["inventario"])

for resultado in pedidios_procesados["resultados"]:
    print(resultado)
```

Salida esperada:

```text
{'ALM-001': 0, 'ALM-002': 0, 'ALM-003': 8}
{'codigo': 'ALM-001', 'cantidad': 5, 'estado': 'atendido'}
{'codigo': 'ALM-003', 'cantidad': 10, 'estado': 'cantidad insuficiente'}
{'codigo': 'ALM-009', 'cantidad': 2, 'estado': 'producto ausente'}
{'codigo': 'ALM-001', 'cantidad': 7, 'estado': 'atendido'}
{'codigo': 'ALM-002', 'cantidad': 1, 'estado': 'cantidad insuficiente'}
```

Verifique el comportamiento con una lista de pedidos vacía, un inventario vacío y pedidos que consuman las unidades disponibles. Verifique que los datos originales permanezcan sin modificación.



(ejdic-14)=
**DCT-011.** Una institución necesita incorporar nuevas calificaciones a su registro académico y obtener un informe actualizado por estudiante. El registro relaciona números de matrícula de estudiantes con fichas que contienen los campos `"nombre"` y `"notas"`, una lista de calificaciones en escala de 1.0 a 7.0. Un estudiante puede tener una lista de notas vacía. Se considera aprobada una calificación mayor o igual a 4.0.

Desarrolle un programa modular cuya función principal sea `actualizar_registro(original, solicitudes)`. Cada solicitud contiene los campos `"matricula"` y `"nota"`.

Una solicitud se acepta cuando el estudiante está registrado y la nota pertenece al intervalo permitido. En ese caso, la nota se agrega al final de su lista. Si alguna condición no se cumple, la solicitud se rechaza sin incorporar cambios. Las solicitudes posteriores deben procesarse aunque existan rechazos.

La función debe devolver un diccionario con las siguientes entradas:

- `"registro"`: registro académico actualizado.
- `"solicitudes"`: diccionario con las cantidades `"aceptadas"` y `"rechazadas"`.
- `"informe"`: diccionario cuyas claves son los números de matrícula de estudiantes. Cada valor contiene `"nombre"`, `"cantidad"` de notas y `"aprobadas"`, correspondiente a las notas mayores o iguales a 4.0.

Los argumentos recibidos no deben modificarse. Además, modificar posteriormente los nombres o las listas de notas del registro devuelto no debe afectar al original. Identifique las funciones auxiliares que necesita implementar y establezca sus responsabilidades.

A continuación se muestran ejemplos de datos y llamada a la función principal:

```python
registro_original = {
    "202600184": {
        "nombre": "Camila Rojas",
        "notas": [5.8, 3.6],
    },
    "202600237": {
        "nombre": "Matías Fuentes",
        "notas": [],
    },
    "202600315": {
        "nombre": "Valentina Soto",
        "notas": [4.0, 6.2],
    },
}

solicitudes = [
    {"matricula": "202600237", "nota": 4.0},
    {"matricula": "202600184", "nota": 6.5},
    {"matricula": "202600999", "nota": 5.8},
    {"matricula": "202600184", "nota": 7.3},
    {"matricula": "202600315", "nota": 3.2},
    {"matricula": "202600237", "nota": 7.0},
]

resultado = actualizar_registro(registro_original, solicitudes)

print(resultado["solicitudes"])

for matricula, ficha in resultado["registro"].items():
    print(matricula, ficha)

for matricula, resumen in resultado["informe"].items():
    print(matricula, resumen)
```

Salida esperada:

```text
{'aceptadas': 4, 'rechazadas': 2}
202600184 {'nombre': 'Camila Rojas', 'notas': [5.8, 3.6, 6.5]}
202600237 {'nombre': 'Matías Fuentes', 'notas': [4.0, 7.0]}
202600315 {'nombre': 'Valentina Soto', 'notas': [4.0, 6.2, 3.2]}
202600184 {'nombre': 'Camila Rojas', 'cantidad': 3, 'aprobadas': 2}
202600237 {'nombre': 'Matías Fuentes', 'cantidad': 2, 'aprobadas': 2}
202600315 {'nombre': 'Valentina Soto', 'cantidad': 3, 'aprobadas': 2}
```

Además, verifique su solución con un registro vacío, una lista de solicitudes vacía y notas exactamente iguales a 1.0, 4.0 y 7.0. Incluya solicitudes con notas inferiores a 1.0 y superiores a 7.0. Verifique que los argumentos no cambien y que modificar el registro devuelto no altere el original.


