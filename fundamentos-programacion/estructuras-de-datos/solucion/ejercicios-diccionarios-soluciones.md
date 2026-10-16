
# Ejercicios Uso de diccionarios

**DCT-001.** Una agenda (diccionario) relaciona nombres con teléfonos. Implemente la función `registrar_contacto(agenda, nombre, telefono)` para agregar un contacto solo si su nombre no aparece como clave. Si ya existe, conservar su teléfono.

La agenda relaciona nombres de contacto con teléfonos representados como cadenas. `nombre` y `telefono` son cadenas no vacías. Cada nombre identifica un contacto de manera única. La función modifica el diccionario recibido y devuelve `True` si inserta la entrada o `False` si el nombre ya existe.

:::{dropdown} Solución

Comprobar la pertenencia antes de asignar. La presencia conduce al retorno inmediato. la ausencia permite insertar.

```python
def registrar_contacto(agenda, nombre, telefono):
    
    if nombre in agenda:
        return False
    
    agenda[nombre] = telefono
    
    return True


agenda = {"Ana": "5551000"}
print(registrar_contacto(agenda, "Luis", "5552000"))    # True
print(registrar_contacto(agenda, "Ana", "5553000"))     # False
print(agenda)  # {'Ana': '5551000', 'Luis': '5552000'}
```

La única asignación se alcanza cuando la clave está ausente. Por tanto, nunca sustituye una entrada previa.
:::


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

:::{dropdown} Solución

Cada función recorre solo los componentes que necesita: claves para la lista, valores para la suma y pares para la selección.

```python
def obtener_estaciones(precipitaciones):
    codigos = []
    for codigo in precipitaciones.keys():
        codigos.append(codigo)
    return codigos


def sumar_lecturas(precipitaciones):
    total = 0
    for codigo, _, _, lectura in precipitaciones.items():
        total = total + lectura
    return total


def seleccionar_bajas(precipitaciones, umbral):
    seleccion = {}
    for codigo, _, _, lectura in precipitaciones.items():
        if lectura <= umbral:
            seleccion[codigo] = lectura
    return seleccion

```

Cada entrada aporta una vez a cada recorrido. El filtro copia una asociación exactamente cuando satisface el criterio; ninguna función asigna ni elimina entradas del argumento.
:::

(ejdic-04)=


**DCT-003.** Un catálogo bibliográfico relaciona códigos de libros con sus títulos, representados como cadenas. Implemente la función `retirar_libro(catalogo, codigo)` para eliminar la entrada de un libro identificado por su código.

La función modifica el diccionario recibido, devuelve `True` si elimina una entrada y `False` si el código estaba ausente. Los códigos son cadenas no vacías.

:::{dropdown} Solución

La ausencia determina que no hay nada que eliminar. En el otro caso se elimina una única entrada y se informa el cambio.

```python
def retirar_libro(catalogo, codigo):
    if codigo not in catalogo:
        return False
    del catalogo[codigo]
    return True


catalogo = {"L01": "Algoritmos", "L02": "Álgebra"}
print(retirar_libro(catalogo, "L02"))  # True
print(retirar_libro(catalogo, "L02"))  # False
print(catalogo)  # {'L01': 'Algoritmos'}
```

La comprobación determina si existe el código antes de eliminarlo. Los títulos de los demás libros no se consultan ni se modifican.
:::

(ejdic-05)=
**DCT-004.** Implemente `contar_respuestas(respuestas)` que cuenta la cantidad de veces que aparece cada respuesta de una encuesta.

El parámetro es una lista de cadenas no vacías. Las cadenas se comparan exactamente: `"Sí"` y `"sí"` son categorías distintas. La función devuelve un diccionario con cada respuesta y su frecuencia positiva, sin modificar la lista. Un argumento vacío retorna un diccionario vacío.

Por ejemplo, la llamada a la función con el argumento `['sí', 'no', 'sí', 'sí', 'no']` retorna `{'sí': 3, 'no': 2}`.

:::{dropdown} Solución

Comenzar con un diccionario vacío. Para cada respuesta, crear la cantidad uno si no está registrada o aumentar la cantidad existente.

```python
def contar_respuestas(respuestas):
    frecuencias = {}
    for respuesta in respuestas:
        if respuesta in frecuencias:
            frecuencias[respuesta] = frecuencias[respuesta] + 1
        else:
            frecuencias[respuesta] = 1
    return frecuencias


print(contar_respuestas(["sí", "no", "sí", "sí", "no"]))
# {'sí': 3, 'no': 2}
```
:::

(ejdic-06)=
**DCT-005.** Mesas electorales registran los votos obtenidos por cada candidatura. 

1. Implemente `consolidar_votos(primera, segunda)` para reunir los resultados (acumular los votos) de la primera y la segunda mesa. Las candidaturas presentes en ambas deben acumular votos, las que aparecen en una sola conservan su cantidad. Cada mesa es un diccionario con nombres de candidaturas como claves de tipo cadena y cantidades de votos. La función devuelve un nuevo diccionario. Para cada nombre presente en alguna de las mesas, el resultado contiene la suma de sus cantidades, considerando cero en la mesa donde esté ausente.

2. Redacte un párrafo breve con la estrategía implementada.

:::{dropdown} Solución
:class: dropdown

Copiar el primer diccionario y recorrer los pares del segundo diccionario. Sumar para las claves ya presentes e insertar las nuevas.

```python
def consolidar_votos(primera, segunda):
    combinado = primera.copy()
    for candidatura, cantidad in segunda.items():
        if candidatura in combinado:
            combinado[candidatura] = combinado[candidatura] + cantidad
        else:
            combinado[candidatura] = cantidad
    return combinado


a = {"Azul": 3, "Verde": 0}
b = {"Azul": 4, "Roja": 2}
print(consolidar_votos(a, b))
# {'Azul': 7, 'Verde': 0, 'Roja': 2}
print(a)  # {'Azul': 3, 'Verde': 0}
print(b)  # {'Azul': 4, 'Roja': 2}
```

:::

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

:::{dropdown} Solución

**Análisis del fallo:** El fragmento cambia el tamaño del diccionario mientras recorre su vista de entradas; con esos datos se produce `RuntimeError`. Agregar o eliminar entradas durante estos recorridos puede producir una excepción o un recorrido incompleto; no debe basarse el algoritmo en ese comportamiento [@ejdicpsfoperaciones].

**Solución.** Recorrer el original, que permanece estable, y eliminar las claves seleccionadas únicamente de la copia.

```python
def depurar_sensores(sensores):
    depurado = sensores.copy()
    for codigo, cantidad in sensores.items():
        if cantidad == 0:
            del depurado[codigo]
    return depurado

sensores = {"S01": 0, "S02": 4, "S03": 0}
print(depurar_sensores(sensores))  # {'S02': 4}
print(sensores)  # {'S01': 0, 'S02': 4, 'S03': 0}
```

Cada clave se examina en el original y solo se elimina de la copia si su cantidad es cero. El recorrido no cambia de tamaño. Actualizar el valor de una clave existente y agregar o eliminar claves son cambios distintos; este ejercicio trata los segundos.
:::

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

:::{dropdown} Solución

Recorrer las recetas, copiar sus atributos y sustituir en esa copia la lista de ingredientes por una copia nueva. Incorporar cada ficha al resultado.

```python
def copiar_recetario(recetario):
    resultado = {}
    for identificador, ficha in recetario.items():
        nueva_ficha = ficha.copy()
        nueva_ficha["ingredientes"] = ficha["ingredientes"].copy()
        resultado[identificador] = nueva_ficha
    return resultado


# Crea una copia
copia = copiar_recetario(recetario)

# Modifica el nombre y los ingredientes únicamente en la copia.
copia["R01"]["nombre"] = "Sopa de verduras con zapallo"
copia["R01"]["ingredientes"].append("zapallo")

print(recetario["R01"])
# {'nombre': 'Sopa de verduras',
#  'ingredientes': ['agua', 'papa', 'zanahoria', 'sal']}

print(copia["R01"])
# {'nombre': 'Sopa de verduras con zapallo',
#  'ingredientes': ['agua', 'papa', 'zanahoria', 'sal', 'zapallo']}
```

Cada asociación y cada lista mutable susceptible de cambiar quedan en contenedores nuevos. El procedimiento resuelve esta estructura concreta; no es una copia general para cualquier número de capas.
:::


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

Implementar `agrupar_por_destino(envios)` que devuelve un diccionario que asocie cada destino con la lista de identificadores de paquetes enviados a dicho destino.

:::{dropdown} Solución

Recorrer los pares paquete–destino. Crear una lista nueva cuando aparezca un destino por primera vez y agregar el identificador a su lista.

```python
def agrupar_por_destino(envios):
    grupos = {}
    for identificador, destino in envios.items():
        if destino not in grupos:
            grupos[destino] = []
        grupos[destino].append(identificador)
    return grupos


grupos = agrupar_por_destino(envios)
print(grupos)
# {
#     "Santiago": ["ENV001", "ENV004", "ENV008"],
#     "Valparaíso": ["ENV002", "ENV006"],
#     "Concepción": ["ENV003", "ENV007"],
#     "Temuco": ["ENV005"],
# }
```
:::


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


:::{dropdown} Solución

**Diseño.** Recorrer la lista y asignar a cada código una copia de su ficha. Las apariciones posteriores sustituyen la ficha anterior del mismo código.

```python
def organizar_peliculas(fichas):
    peliculas = {}
    for ficha in fichas:
        codigo = ficha["codigo"]
        peliculas[codigo] = ficha.copy()
    return peliculas


peliculas = organizar_peliculas(fichas)

print(len(peliculas))               # 3
print(peliculas["PEL-002"])         # Conserva la última ficha de ese código.
# {'codigo': 'PEL-002', 'titulo': 'WALL-E', 'duracion': 100}

# Modificar el resultado no debe alterar las fichas originales.
peliculas["PEL-001"]["duracion"] = 130

print(peliculas["PEL-001"]["duracion"])  # 130
print(fichas[0]["duracion"])             # 125
```

:::



(ejdic-13)=
**DCT-010.** Un almacén necesita procesar los pedidos recibidos durante una jornada y determinar sus existencias finales. El inventario relaciona códigos de productos con cantidades enteras no negativas. Cada pedido se representa mediante un diccionario con los campos `"codigo"` y `"cantidad"`.

Desarrolle un programa modular cuya función principal sea `procesar_pedidos(inicial, pedidos)`. Los pedidos deben procesarse en el orden recibido. Un pedido se atiende únicamente cuando el producto está registrado y dispone de unidades suficientes. En ese caso se descuenta la cantidad solicitada, en caso contrario, las existencias permanecen iguales. El rechazo de un pedido no impide procesar los posteriores. Los productos cuyo saldo llega a cero deben conservarse en el inventario.

La función debe devolver un diccionario con las siguientes entradas:

- `"inventario"`: existencias finales.
- `"resultados"`: lista de diccionarios, uno por pedido y en el mismo orden, con los campos `"codigo"`, `"cantidad"` y `"estado"`. Los estados posibles son `"atendido"`, `"producto ausente"` y `"cantidad insuficiente"`.

Los argumentos recibidos no deben modificarse. Determine qué funciones auxiliares necesita y establezca sus responsabilidades.

A continuación se muestra un ejemplo de datos y llamada a la función principal:

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

:::{dropdown} Solución

La función principal decide si un pedido puede descontarse del estado actual. La coordinación copia el inventario y la invoca una vez por pedido, guardando una ficha nueva por resultado. El resumen recorre esas fichas y cuenta los estados.

```python
def atender_pedido(inventario, pedido):
    codigo = pedido["codigo"]
    cantidad = pedido["cantidad"]
    if codigo not in inventario:
        return "producto ausente"
    if cantidad > inventario[codigo]:
        return "cantidad insuficiente"
    inventario[codigo] = inventario[codigo] - cantidad
    return "atendido"


def procesar_pedidos(inicial, pedidos):
    inventario = inicial.copy()
    resultados = []
    for pedido in pedidos:
        estado = atender_pedido(inventario, pedido)
        resultados.append({
            "codigo": pedido["codigo"],
            "cantidad": pedido["cantidad"],
            "estado": estado,
        })
    return {"inventario": inventario, "resultados": resultados}


def resumir_pedidos(resultados):
    resumen = {
        "atendido": 0,
        "producto ausente": 0,
        "cantidad insuficiente": 0,
    }
    for resultado in resultados:
        estado = resultado["estado"]
        resumen[estado] = resumen[estado] + 1
    return resumen

```

La comprobación independiente de `atender_pedido` debe cubrir las tres salidas y el consumo exacto. La comprobación de integración debe incluir pedidos consecutivos del mismo código: cada uno debe utilizar el saldo dejado por los anteriores. `resumir_pedidos` recibe únicamente resultados con los tres estados establecidos.

Cada pedido genera una ficha y modifica existencias solo en el caso autorizado. Así, después de cada paso, el inventario representa los pedidos atendidos de la parte procesada y la lista contiene sus resultados, incluidos los rechazos. Al terminar se cumplen ambas partes de la especificación. Los valores del inventario son enteros y las fichas de resultado son nuevas, de modo que el proceso no modifica los argumentos.

:::

(ejdic-14)=
**DCT-011.** Una institución necesita incorporar nuevas calificaciones a su registro académico y obtener un informe actualizado por estudiante. El registro relaciona números de matrícula de estudiantes con fichas que contienen los campos `"nombre"` y `"notas"`, una lista de calificaciones en escala de 1.0 a 7.0. Un estudiante puede tener una lista de notas vacía. Se considera aprobada una calificación mayor o igual a 4.0.

Desarrolle un programa modular cuya función principal sea `actualizar_registro(original, solicitudes)`. Cada solicitud contiene los campos `"matricula"` y `"nota"`.

Una solicitud se acepta cuando el estudiante está registrado y la nota pertenece al intervalo permitido. En ese caso, la nota se agrega al final de su lista. Si alguna condición no se cumple, la solicitud se rechaza sin incorporar cambios. Las solicitudes posteriores deben procesarse aunque existan rechazos.

La función debe devolver un diccionario con las siguientes entradas:

- `"registro"`: registro académico actualizado.
- `"solicitudes"`: diccionario con las cantidades `"aceptadas"` y `"rechazadas"`.
- `"informe"`: diccionario cuyas claves son los números de matrícula de estudiantes. Cada valor contiene `"nombre"`, `"cantidad"` de notas y `"aprobadas"`, correspondiente a las notas mayores o iguales a 4.0.

Los argumentos recibidos no deben modificarse. Además, modificar posteriormente los nombres o las listas de notas del registro devuelto no debe afectar al original. Identifique las funciones auxiliares que necesita implementar y establezca sus responsabilidades.

A continuación se muestra un ejemplo de datos y llamada a la función principal:

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

Salidas esperada:

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

:::{dropdown} Solución

La coordinación copia todas las capas mutables conforme al modelo. Cada solicitud se comprueba antes de agregar la nota. Las cantidades de aceptación y rechazo se actualizan según el booleano devuelto. El informe se construye después, recorriendo el registro final y resumiendo cada lista.

```python
def copiar_registro(registro):
    copia = {}

    for matricula, ficha in registro.items():
        nueva_ficha = ficha.copy()
        nueva_ficha["notas"] = ficha["notas"].copy()
        copia[matricula] = nueva_ficha

    return copia


def incorporar_nota(registro, solicitud):
    matricula = solicitud["matricula"]
    nota = solicitud["nota"]

    if matricula not in registro:
        return False

    if nota < 1.0 or nota > 7.0:
        return False

    registro[matricula]["notas"].append(nota)
    return True


def contar_aprobadas(notas):
    cantidad = 0

    for nota in notas:
        if nota >= 4.0:
            cantidad = cantidad + 1

    return cantidad


def crear_informe(registro):
    informe = {}

    for matricula, ficha in registro.items():
        informe[matricula] = {
            "nombre": ficha["nombre"],
            "cantidad": len(ficha["notas"]),
            "aprobadas": contar_aprobadas(ficha["notas"]),
        }

    return informe


def actualizar_registro(original, solicitudes):
    registro = copiar_registro(original)
    resumen = {"aceptadas": 0, "rechazadas": 0}

    for solicitud in solicitudes:
        if incorporar_nota(registro, solicitud):
            resumen["aceptadas"] = resumen["aceptadas"] + 1
        else:
            resumen["rechazadas"] = resumen["rechazadas"] + 1

    return {
        "registro": registro,
        "solicitudes": resumen,
        "informe": crear_informe(registro),
    }
```

Las pruebas independientes deben comprobar la separación de capas en `copiar_registro`, los dos motivos de rechazo de `incorporar_nota` y el conteo de notas en el umbral de `contar_aprobadas`. Las pruebas de integración deben comprobar que el informe utiliza el registro actualizado y que los rechazos no agregan notas.

Cada solicitud se procesa una vez y aumenta exactamente uno de los dos conteos. Solo las solicitudes aceptadas agregan una nota, y lo hacen en una lista de la copia. Al terminar, el registro contiene exactamente las incorporaciones admitidas. El informe recorre ese registro y cuenta sus notas; por tanto, sus cantidades corresponden al estado final. La independencia respecto del original se obtiene al copiar el diccionario exterior, cada ficha y cada lista de notas.
:::
