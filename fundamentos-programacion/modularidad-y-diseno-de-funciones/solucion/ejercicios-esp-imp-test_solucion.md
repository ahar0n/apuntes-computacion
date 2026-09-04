# Ejercicios: Diseño de funciones


(df-001)=
**DF-001.** A partir de la siguiente descripción: «la función `esta_en_rango(valor)` indica si un valor está en el rango permitido». Determine qué información falta para que la función pueda implementarse y probarse sin decisiones adicionales. Redacte una especificación que utilice el intervalo cerrado de `10` a `50` y que admita argumentos enteros.

:::{solution} df-001
:class: dropdown

La descripción inicial no identifica los límites, el tipo de dato admitido, la naturaleza del resultado ni los efectos observables. Una especificación suficiente es:

| Elemento            | Descripción |
|---------------------|---|
| Propósito           | Determinar si un entero pertenece al intervalo cerrado de `10` a `50`. |
| Datos requeridos    | `valor`: número entero. |
| Precondición        | `valor` es entero. |
| Resultado           | Valor booleano. |
| Postcondición       | El resultado es `True` exactamente cuando `10 <= valor <= 50`. |
| Efectos observables | Ninguno. |

Una implementación posible es:

```python
def esta_en_rango(valor):
    """Indica si valor pertenece al intervalo cerrado [10, 50]."""
    return 10 <= valor <= 50
```
:::



**DF-002.** Especifique la función `contar_observaciones_validas(observaciones)`. La lista puede estar vacía y puede contener enteros situados dentro o fuera del intervalo de `0` a `100`. La función debe retornar la cantidad de observaciones válidas sin modificar la lista. Después de escribir la especificación, determine los resultados esperados para `[]`, `[40]`, `[-1, 0, 50, 100, 101]` y `[120, -8]`.

:::{solution} Solucion
:class: dropdown
:open: 

| Elemento            | Descripción |
|---------------------|---|
| Propósito           | Contar las observaciones pertenecientes al intervalo cerrado de `0` a `100`. |
| Datos requeridos    | `observaciones`: lista de números enteros. |
| Precondición        | Todos los elementos de la lista son enteros; la lista puede estar vacía. |
| Resultado           | Número entero. |
| Postcondición       | El resultado es la cantidad de elementos `valor` para los cuales se cumple `0 <= valor <= 100`. |
| Efectos observables | Ninguno; la lista recibida no se modifica. |

Los resultados esperados son:

| Argumento | Resultado esperado |
|---|---:|
| `[]` | `0` |
| `[40]` | `1` |
| `[-1, 0, 50, 100, 101]` | `3` |
| `[120, -8]` | `0` |

Una implementación posible es:

```python
def contar_observaciones_validas(observaciones):
    """Devuelve la cantidad de observaciones del intervalo [0, 100]."""
    cantidad_validas = 0

    for valor in observaciones:
        if 0 <= valor <= 100:
            cantidad_validas += 1

    return cantidad_validas
```
:::





**DF-003.** Especifique e implemente la función `limitar_al_intervalo(valor, limite_inferior, limite_superior)` a partir de la siguientes antecedentes:
- los tres argumentos son enteros y `limite_inferior <= limite_superior`,
- si `valor` es menor que el límite inferior, se retorna el límite inferior,
- si `valor` es mayor que el límite superior, se retorna el límite superior,
- en cualquier otro caso, se retorna `valor`,
- la función no produce efectos observables.
- Utilice condicionales y una única sentencia `return` al final de la función. 


Además, compruebe aisladamente la implementación con un valor inferior, uno interior, ambos límites y un valor superior.


:::{solution} Solución
:class: dropdown
:open: 

```python
def limitar_al_intervalo(valor, limite_inferior, limite_superior):
    """Devuelve valor limitado al intervalo cerrado indicado."""
    if valor < limite_inferior:
        resultado = limite_inferior
    elif valor > limite_superior:
        resultado = limite_superior
    else:
        resultado = valor

    return resultado
```

Para el intervalo `[10, 50]`, un conjunto de comprobación es:

| Argumentos | Criterio | Resultado esperado |
|---|---|---:|
| `5, 10, 50` | Valor inferior | `10` |
| `30, 10, 50` | Valor interior | `30` |
| `10, 10, 50` | Límite inferior | `10` |
| `50, 10, 50` | Límite superior | `50` |
| `70, 10, 50` | Valor superior | `50` |
:::


**DF-004.** Considere la función implementada en el siguiente código fuente:

:::{code-block} python
:linenos:

def calcular_cambio(valor_inicial, valor_final):
    """Devuelve el valor final menos el valor inicial."""
    return valor_final - valor_inicial

calcular_cambio(25, 40)
calcular_cambio(40, 25)
calcular_cambio(valor_final=40, valor_inicial=25)
calcular_cambio(25, valor_final=40)
:::

Antes de ejecutar el código, determine el resultado de cada llamada y registre la asociación entre argumentos y parámetros. Luego, ejecute las llamadas y compare los resultados obtenidos con los esperados.

:::{solution} Solución
:class: dropdown
:open: 

| Llamada | Asociación | Resultado esperado |
|---|---|---:|
| `calcular_cambio(25, 40)` | `valor_inicial=25`, `valor_final=40` | `15` |
| `calcular_cambio(40, 25)` | `valor_inicial=40`, `valor_final=25` | `-15` |
| `calcular_cambio(valor_final=40, valor_inicial=25)` | Asociación determinada por los nombres | `15` |
| `calcular_cambio(25, valor_final=40)` | Posicional para `valor_inicial`; palabra clave para `valor_final` | `15` |
:::


**DF-005.** La implementación siguiente muestra el resultado, pero no lo entrega al contexto de la llamada:

:::{code-block} python
:linenos:

def obtener_doble(valor):
    doble = valor * 2
    print(doble)

resultado = obtener_doble(7)
:::

Determine qué valor queda vinculado con `resultado` después de ejecutar la llamada a la función. Modifique la función para que satisfaga la siguiente postcondición: «el valor retornado es igual al doble de `valor`». La función corregida no debe producir operaciones de salida.

:::{solution} Solución
:class: dropdown
:open:
La llamada muestra `14`, pero la función termina sin un `return` explícito. Por ello, `resultado` queda vinculado con `None`. La corrección es:

```python
def obtener_doble(valor):
    """Devuelve el doble de valor."""
    doble = valor * 2
    return doble
```

Después de `resultado = obtener_doble(7)`, `resultado` contiene `14` y la función no produce salida.
:::





**DF-006.** Diseñe un conjunto de pruebas aisladas para `esta_en_rango(valor)`, especificada en la actividad DF-07. Para cada caso registre argumento, criterio de selección y resultado esperado. El conjunto debe incluir un valor interior, ambos límites y los enteros inmediatamente exteriores al intervalo.

Ejecute posteriormente la función y añada el resultado obtenido y la conclusión. No cambie los resultados esperados después de observar la ejecución.


:::{solution} Solución
:class: dropdown
:open:


| Argumento | Criterio | Resultado esperado |
|:---------:|---|:---:|
|   `30`    | Valor interior | `True` |
|   `10`    | Límite inferior | `True` |
|   `50`    | Límite superior | `True` |
|    `9`    | Entero inmediatamente inferior | `False` |
|   `51`    | Entero inmediatamente superior | `False` |

Todos los argumentos son enteros y satisfacen la precondición. Los dos últimos pertenecen al dominio de la función aunque no pertenezcan al intervalo examinado.
:::




**DF-007.** La siguiente implementación pretende calcular el promedio de una lista no vacía:

```python
def calcular_promedio_defectuoso(valores):
    suma = 0
    cantidad = 1

    for valor in valores:
        suma += valor
        cantidad += 1

    return suma / cantidad
```

Antes de ejecutar la función, determine los resultados esperados para `[80]`, `[0, 100]` y `[20, 40, 60]`. Luego, ejecute los casos, identifique la instrucción que origina las diferencias y corrija la implementación sin cambiar su especificación.


:::{solution} Solución
:class: dropdown
:open:

Los resultados esperados, obtenidos de la especificación, son:

| Argumento | Resultado esperado | Resultado defectuoso aproximado |
|---|---:|---:|
| `[80]` | `80.0` | `40.0` |
| `[0, 100]` | `50.0` | `33.33` |
| `[20, 40, 60]` | `40.0` | `30.0` |

El defecto se origina en `cantidad = 1`. Como el recorrido aumenta la cantidad una vez por cada elemento, el contador debe comenzar en cero:

```python
def calcular_promedio(valores):
    """Devuelve el promedio de una lista no vacía."""
    suma = 0
    cantidad = 0

    for valor in valores:
        suma += valor
        cantidad += 1

    return suma / cantidad
```
:::



**DF-008.** Considere la función:

```python
def reemplazar_negativos(valores):
    for posicion in range(len(valores)):
        if valores[posicion] < 0:
            valores[posicion] = 0
```

Especifique la función, incluyendo el efecto observable sobre la lista y el valor retornado por Python al terminar sin un `return` explícito. Diseñe pruebas aisladas para una lista sin negativos, una con algunos negativos, una formada solo por negativos y una lista vacía. En cada caso registre el estado esperado de la lista después de la llamada.

:::{solution} Solución
:class: dropdown
:open:

La precondición establece que `valores` es una lista de números. Al terminar, cada elemento originalmente negativo ha sido sustituido por `0` y los demás conservan su valor. La función modifica la lista recibida y, al no ejecutar un `return` explícito, retorna `None`.

| Lista antes de la llamada | Lista esperada después de la llamada | Retorno esperado |
|---|---|:---:|
| `[2, 5, 8]` | `[2, 5, 8]` | `None` |
| `[-2, 5, -8]` | `[0, 5, 0]` | `None` |
| `[-3, -1]` | `[0, 0]` | `None` |
| `[]` | `[]` | `None` |

:::



## Contexto 1

Una línea aérea permite transportar una maleta sin recargo hasta cierto peso. Por
cada kilogramo adicional (incluida una fracción) cobra una tarifa fija. Si el
límite es `23` kg, una maleta de `23.2` kg paga un kilogramo adicional y una de
`24.0` kg también paga uno.



**DF-009.** Diseñe la función:

```python
calcular_recargo_equipaje(peso_kg, limite_kg=23, tarifa_por_kg=6000)
```

1. Complete la especificación de la función.

| Elemento            | Descripción |
|:--------------------|:------------|
| Propósito           |             |
| Datos requeridos    |             |
| Precondición        |             |
| Resultado           |             |
| Postcondición       |             |
| Efectos observables |             |

2. Diseñe pruebas para una maleta bajo el límite, en el límite, apenas sobre el
   límite y varios kilogramos sobre él.
3. Incluya una prueba que cambie la tarifa mediante un argumento por palabra
   clave y otra que cambie el límite.
4. Implemente y pruebe la función aisladamente.

| Caso | Llamada | Esperado | Obtenido | Conclusión |
| :--- | :--- | :---: | :---: | :--- |
| Bajo el límite |  |  |  |  |
| En el límite |  |  |  |  |
| Fracción sobre el límite |  |  |  |  |
| Exceso de varios kg |  |  |  |  |
| Tarifa especial |  |  |  |  |
| Equipaje de cabina |  |  |  |  |

:::{solution} Ans
:class: dropdown
:open:

| Elemento | Descripción                                                                                                                                |
| :--- |:-------------------------------------------------------------------------------------------------------------------------------------------|
| Propósito | Calcular el recargo asociado al exceso de peso de una maleta.                                                                              |
| Datos requeridos | El peso de la maleta, el límite sin recargo y la tarifa por cada kilogramo adicional.                                                      |
| Precondición | `peso_kg` es un número mayor o igual que cero; `limite_kg` es mayor que cero; `tarifa_por_kg` es un entero mayor o igual que cero.         |
| Resultado | Un número entero mayor o igual que cero, expresado en pesos.                                                                               |
| Poscondición | Si `peso_kg` es menor o igual que `limite_kg`, el resultado es `0`. En otro caso, es el redondeo de `(peso_kg - limite_kg) * tarifa_por_kg`. |
| Efectos observables | Ninguno.                                                                                                                                   |

```python

def calcular_recargo_equipaje(peso_kg, limite_kg=23, tarifa_por_kg=6000):
    exceso_kg = peso_kg - limite_kg
    if exceso_kg <= 0:
        return 0

    kilogramos_cobrados = int(exceso_kg)
    if exceso_kg > kilogramos_cobrados:
        kilogramos_cobrados += 1

    return kilogramos_cobrados * tarifa_por_kg
```

| Caso | Llamada | Resultado esperado |
| :--- | :--- | ---: |
| Bajo el límite | `calcular_recargo_equipaje(18)` | `0` |
| En el límite | `calcular_recargo_equipaje(23)` | `0` |
| Fracción sobre el límite | `calcular_recargo_equipaje(23.2)` | `6000` |
| Exceso de varios kg | `calcular_recargo_equipaje(26.1)` | `24000` |
| Tarifa especial | `calcular_recargo_equipaje(24.2, tarifa_por_kg=7500)` | `15000` |
| Equipaje de cabina | `calcular_recargo_equipaje(9.4, limite_kg=8)` | `12000` |

Las cuatro primeras llamadas usan los valores predeterminados. Las dos últimas
modifican solamente el parámetro identificado por su nombre.

:::



**DF-010.** Diseñe el procedimiento:

```python
mostrar_etiqueta_equipaje(codigo, peso_kg, recargo)
```

A partir de su argumento, debe mostrar tres líneas. Por ejemplo:

```text
Equipaje: LA1842
Peso: 24.5 kg
Recargo: $12000
```

1. Especifique el procedimiento.
2. Explique qué se debe observar para diseñar las pruebas. 
3. Implemente el procedimiento y pruebe un equipaje sin recargo y otro con recargo.

:::{solution} Ans.
:class: dropdown

| Elemento | Descripción |
| :--- | :--- |
| Propósito | Mostrar una etiqueta con la identificación, el peso y el recargo de un equipaje. |
| Datos requeridos | Un código, su peso en kilogramos y el recargo en pesos. |
| Precondición | `codigo` es una cadena no vacía; `peso_kg` es un número mayor o igual que cero; `recargo` es un entero mayor o igual que cero. |
| Resultado | Ninguno (`None`). |
| Poscondición | El procedimiento termina sin retornar información. |
| Efectos observables | Muestra tres líneas con el formato indicado y los datos recibidos. |

```python
def mostrar_etiqueta_equipaje(codigo, peso_kg, recargo):
    print(f"Equipaje: {codigo}")
    print(f"Peso: {peso_kg} kg")
    print(f"Recargo: ${recargo}")
```

```python
mostrar_etiqueta_equipaje("LA1842", 18, 0)
```

```text
Equipaje: LA1842
Peso: 18 kg
Recargo: $0
```

```python
mostrar_etiqueta_equipaje("LA2075", 24.5, 12000)
```

```text
Equipaje: LA2075
Peso: 24.5 kg
Recargo: $12000
```

Aquí la prueba compara la **salida mostrada** con los efectos observables de la
especificación. Comprobar solamente que el resultado sea `None` no verifica el
comportamiento principal del procedimiento.
:::




## Contexto 2

Un centro comunitario dispone de cierta cantidad de canastas. Las familias son atendidas en
el orden de una lista. Por equidad se entregan como máximo dos canastas por
familia. Las solicitudes iguales o menores que cero son errores y se rechazan.
Si una familia pide más que el máximo, su entrega se reduce. Cuando se agota el
stock, la atención termina.


**DF-011.** Diseñe la función para determinar una entrega individual:

```python
calcular_entrega(solicitadas, disponibles, max_por_familia=2)
```

Esta función no modifica el stock, solo retorna cuántas canastas corresponde entregar. 

1. Especifíque la función
2. Diseñe pruebas de solicitudes menor, igual y mayor que el máximo, stock insuficiente y agotado, y para un máximo excepcional de tres canastas.

:::{solution} Ans
:class: dropdown

| Elemento | Descripción |
| :--- | :--- |
| Propósito | Determinar cuántas canastas se pueden entregar según la solicitud, el stock y el máximo permitido. |
| Datos requeridos | Cantidad solicitada, cantidad disponible y máximo permitido por familia. |
| Precondición | Los argumentos son enteros; `solicitadas` es mayor que cero, `disponibles` es mayor o igual que cero y `max_por_familia` es mayor que cero. |
| Resultado | Un número entero mayor o igual que cero. |
| Poscondición | El resultado es el menor valor entre `solicitadas`, `disponibles` y `max_por_familia`. |
| Efectos observables | Ninguno. |

```python
def calcular_entrega(solicitadas, disponibles, max_por_familia=2):
    return min(solicitadas, disponibles, max_por_familia)
```

| Caso | Llamada | Resultado esperado |
| :--- | :--- | ---: |
| Menor que el máximo | `calcular_entrega(1, 10)` | `1` |
| Igual al máximo | `calcular_entrega(2, 10)` | `2` |
| Mayor que el máximo | `calcular_entrega(5, 10)` | `2` |
| Stock insuficiente | `calcular_entrega(2, 1)` | `1` |
| Stock agotado | `calcular_entrega(2, 0)` | `0` |
| Máximo especial | `calcular_entrega(4, 10, max_por_familia=3)` | `3` |

`calcular_entrega(0, 10)` viola la precondición. La función que procesa la
lista será responsable de reconocer ese registro erróneo.
:::

**DF-012.** Diseñe la función que procesa la jornada de entrega:

```python
procesar_solicitudes(solicitudes, stock_inicial, max_por_familia=2)
```

Debe retornar una tupla con la lista de entregas, la cantidad de solicitudes 
no positivas rechazadas y el stock restante. Utilice la función `calcular_entrega`, `continue`
para omitir errores y `break` cuando no queden canastas.

1. Especifique la función.
2. Diseñe las pruebas de los casos identificados en la tabla.
3. Implemente y ejecute los casos de prueba.


| Caso | Argumentos | Esperado | Obtenido | Conclusión |
| :--- | :--- | :--- | :--- | :--- |
| Solicitudes normales |  |  |  |  |
| Errores intercalados |  |  |  |  |
| Stock agotado durante la jornada |  |  |  |  |
| Stock inicial agotado |  |  |  |  |
| Lista vacía |  |  |  |  |
| Máximo especial |  |  |  |  |


:::{solution} Ans
:class: dropdown

| Elemento | Descripción |
| :--- | :--- |
| Propósito | Procesar en orden las solicitudes, omitiendo registros erróneos y entregando mientras exista stock. |
| Datos requeridos | Una secuencia de cantidades solicitadas, el stock inicial y el máximo permitido por familia. |
| Precondición | Cada solicitud y los otros argumentos son enteros; `stock_inicial` es mayor o igual que cero y `max_por_familia` es mayor que cero. |
| Resultado | Una tupla formada por una lista de enteros y dos enteros no negativos. |
| Poscondición | La lista contiene, en orden, las entregas para las solicitudes positivas procesadas mientras hubo stock. El segundo componente cuenta las solicitudes no positivas encontradas antes de agotarse el stock. El tercero es el stock inicial menos la suma de las entregas. No se examinan solicitudes posteriores al agotamiento. |
| Efectos observables | Ninguno; la secuencia recibida no se modifica. |

```python
def procesar_solicitudes(solicitudes, stock_inicial, max_por_familia=2):
    entregas = []
    rechazadas = 0
    stock = stock_inicial

    for solicitadas in solicitudes:
        if stock == 0:
            break
        if solicitadas <= 0:
            rechazadas += 1
            continue

        cantidad = calcular_entrega(
            solicitadas,
            stock,
            max_por_familia=max_por_familia,
        )
        entregas.append(cantidad)
        stock -= cantidad

    return entregas, rechazadas, stock
```

| Caso | Llamada | Resultado esperado |
| :--- | :--- | :--- |
| Normales | `procesar_solicitudes([1, 2, 1], 10)` | `([1, 2, 1], 0, 6)` |
| Errores intercalados | `procesar_solicitudes([2, 0, -3, 1], 10)` | `([2, 1], 2, 7)` |
| Stock agotado | `procesar_solicitudes([2, 2, 2, -1], 3)` | `([2, 1], 0, 0)` |
| Stock inicial agotado | `procesar_solicitudes([-2, 1], 0)` | `([], 0, 0)` |
| Lista vacía | `procesar_solicitudes([], 8)` | `([], 0, 8)` |
| Máximo especial | `procesar_solicitudes([4, 2], 10, max_por_familia=3)` | `([3, 2], 0, 5)` |

En la tercera prueba, el `-1` no aumenta el contador: está después del
agotamiento y la especificación dice que esas solicitudes no se examinan.
:::
