# Ejercicios: Diseño de funciones


**DF-001.** A partir de la siguiente descripción: 

«la función `esta_en_rango(valor)` indica si un valor está en el rango permitido»

1. Indique la información faltante para que la función pueda implementarse y 
probarse sin decisiones adicionales. 
2. Especifique la función para que considere el intervalo cerrado de `10` a `50` 
y que admita argumentos enteros.

::::{dropdown} Solución

La descripción inicial no identifica:
- los límites, 
- el tipo de dato admitido, 
- la naturaleza del resultado,
- los efectos observables. 

Especificación:

| Elemento             | Descripción                                                            |
|:---------------------|:-----------------------------------------------------------------------|
| Propósito            | Determinar si un entero pertenece al intervalo cerrado de `10` a `50`. |
| Datos requeridos     | `valor`: número entero.                                                |
| Precondición         | `valor` es entero.                                                     |
| Resultado            | Valor booleano.                                                        |
| Postcondición        | El resultado es `True` cuando `10 <= valor <= 50`.                     |
| Efectos observables  | Ninguno.                                                               |

Implementación conforme con esta especificación:

:::{code-block} python
:linenos:```python
def esta_en_rango(valor):
    """Indica si valor pertenece al intervalo cerrado [10, 50]."""
    return 10 <= valor <= 50
:::
::::


**DF-002.** Especifique la función `contar_observaciones_validas(observaciones)`. 
Observaciones es una lista puede estar vacía o puede contener enteros situados 
dentro o fuera del intervalo de `0` a `100`. La función debe retornar la 
cantidad de observaciones válidas sin modificar la lista. Adicionalmente, 
determine los resultados esperados para `[]`, `[40]`, `[-1, 0, 50, 100, 101]` y
`[120, -8]`.


::::{dropdown} Solución

| Elemento            | Descripción                                                                  |
|---------------------|:-----------------------------------------------------------------------------|
| Propósito           | Contar las observaciones pertenecientes al intervalo cerrado de `0` a `100`. |
| Datos requeridos    | `observaciones`: lista de números enteros.                                   |
| Precondición        | Todos los elementos de la lista son enteros, la lista puede estar vacía.     |
| Resultado           | Número entero.                                                               |
| Postcondición       | Cantidad de elementos `valor` que cumplen con `0 <= valor <= 100`.           |
| Efectos observables | Ninguno.                                                                     |

Los resultados esperados son:

|        Argumento         | Resultado esperado |
|:------------------------:|:------------------:|
|           `[]`           |        `0`         |
|          `[40]`          |        `1`         |
| `[-1, 0, 50, 100, 101]`  |        `3`         |
|       `[120, -8]`        |        `0`         |

Una implementación conforme con la especificación es:

:::{code-block}python
:linenos:
def contar_observaciones_validas(observaciones):
    """Devuelve la cantidad de observaciones del intervalo [0, 100]."""
    cantidad_validas = 0

    for valor in observaciones:
        if 0 <= valor <= 100:
            cantidad_validas += 1

    return cantidad_validas
:::

::::


**DF-003.** Especifique e implemente la función 
`limitar_al_intervalo(valor, limite_inferior, limite_superior)` a partir de la 
siguientes antecedentes:

- los tres argumentos son enteros y `limite_inferior <= limite_superior`,
- si `valor` es menor que el límite inferior, se retorna el límite inferior,
- si `valor` es mayor que el límite superior, se retorna el límite superior,
- en cualquier otro caso, se retorna `valor`,
- la función no produce efectos observables.
- utilice condicionales y una única sentencia `return` al final de la función. 

Además, compruebe aisladamente la implementación con un valor inferior, uno 
interior, ambos límites y un valor superior.

::::{dropdown} Solución

Especificación

| Elemento            | Descripción                                                                                                                                                                                         |
|:--------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Propósito           | Devolver el valor más cercano al valor que pertenezca al intervalo cerrado `[linite_inferior, limite_superior]`                                                                                      |
| Datos requeridos    | `valor`: número a limitar, `limite_inferior`: límite inferior, `limite_superior`: límite superior.                                                                                                  |
| Precondición        | Tres argumentos enteros, `limite_inferior <= limite_superior`.                                                                                                                                      |
| Resultado           | Número entero que pertenece al intervalo cerrado `[limite_inferior, limite_superior]`                                                                                                               |
| Postcondición       | Si `valor < limite_inferior`, resultado es `limite_inferior`, si `valor > limite_superior`, resultado es `limite_superior`, si `limite_inferior <= valor <= limite_superior`, resultado es `valor`. |
| Efectos observables | Ninguno.                                                                                                                                                                                            |


:::{code-block} python
:linenos:
def limitar_al_intervalo(valor, limite_inferior, limite_superior):
    """Devuelve valor limitado al intervalo cerrado indicado."""
    if valor < limite_inferior:
        resultado = limite_inferior
    elif valor > limite_superior:
        resultado = limite_superior
    else:
        resultado = valor

    return resultado
:::

Para el intervalo `[5, 8]`, un conjunto de comprobación es:

| Argumentos | Criterio        | Resultado esperado |
|:-----------|:----------------|:------------------:|
| `1,5,8`    | Valor inferior  |        `5`         |
| `6,5,8`    | Valor interior  |        `6`         |
| `5,5,8`    | Límite inferior |        `5`         |
| `8,5,8`    | Límite superior |        `8`         |
| `9,5,8`    | Valor superior  |        `8`         |
::::


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

Antes de ejecutar el código, determine el resultado de cada llamada y registre 
la asociación entre argumentos y parámetros. Luego, ejecute las llamadas y 
compare los resultados obtenidos con los esperados.


**DF-005.** La implementación siguiente muestra el resultado, pero no lo 
entrega al contexto de la llamada:

:::{code-block} python
:linenos:

def obtener_doble(valor):
    doble = valor * 2
    print(doble)

resultado = obtener_doble(7)
:::

Determine qué valor queda vinculado con `resultado` después de ejecutar la 
llamada a la función. Modifique la función para que satisfaga la siguiente 
postcondición: «el valor retornado es igual al doble de `valor`». La función 
corregida no debe producir operaciones de salida.

::::{dropdown} Solución

La llamada a la función muestra `14`, pero la función termina sin un `return` explícito. Por ello, `resultado` queda vinculado con `None`. 

Función corregida:

:::{code-block} python
:linenos:
def obtener_doble(valor):
    """Devuelve el doble de valor."""
    doble = valor * 2
    return doble
:::

Después de `resultado = obtener_doble(7)`, `resultado` contiene `14` y la función no produce salida.
::::


**DF-006.** Diseñe un conjunto de pruebas aisladas para `esta_en_rango(valor)`, 
especificada en la actividad DF-01. Para cada caso registre argumento, criterio 
de selección y resultado esperado. El conjunto debe incluir un valor interior, 
ambos límites y los enteros inmediatamente exteriores al intervalo.

Ejecute posteriormente la función y añada el resultado obtenido y la 
conclusión. No cambie los resultados esperados después de observar la 
ejecución.



**DF-007.** La siguiente implementación pretende calcular el promedio de una 
lista no vacía:

:::{code-block} python
:linenos:
def calcular_promedio_defectuoso(valores):
    suma = 0
    cantidad = 1

    for valor in valores:
        suma += valor
        cantidad += 1

    return suma / cantidad
:::

Antes de ejecutar la función, determine los resultados esperados para 
`[80]`, `[0, 100]` y `[20, 40, 60]`. Luego, ejecute los casos, identifique la 
instrucción que origina las diferencias y corrija la implementación sin cambiar 
su especificación.

::::{dropdown} Solución

Los resultados esperados y obtenidos, son:

|    Argumento    | Resultado esperado | Resultado defectuoso aproximado |
|:---------------:|:------------------:|:-------------------------------:|
|     `[80]`      |       `80.0`       |             `40.0`              |
|   `[0, 100]`    |       `50.0`       |             `33.33`             |
| `[20, 40, 60]`  |       `40.0`       |             `30.0`              |

Si `cantidad` tiene el rol de contador de valores de la lista, esta debe 
inicializarse en `0`, ya que el recorrido se inicia junto con el iterador.
El defecto se origina en la inicialización `cantidad = 1` (línea 3).

:::{code-block} python
:linenos:
def calcular_promedio(valores):
    """Devuelve el promedio de una lista no vacía."""
    suma = 0
    cantidad = 0

    for valor in valores:
        suma += valor
        cantidad += 1

    return suma / cantidad
:::
::::



**DF-008.** Considere la función:

:::{code-block} python
:linenos:
def reemplazar_negativos(valores):
    for posicion in range(len(valores)):
        if valores[posicion] < 0:
            valores[posicion] = 0
:::

Especifique la función, incluyendo el efecto observable sobre la lista y el 
valor retornado por Python al terminar sin un `return` explícito. Diseñe 
pruebas aisladas para una lista sin negativos, una con algunos negativos, una 
formada solo por negativos y una lista vacía. En cada caso registre el estado 
esperado de la lista después de la llamada.

:::{dropdown} Solución

Análisis:

- La precondición establece que `valores` es una lista de números (valores comparables con `0`). 
- Al terminar, cada elemento negativo ha sido sustituido por `0` y los demás conservan su valor. 
- La función modifica la lista recibida y, al no contener sentencia `return`, devuelve `None`.

Especificación:

| Elemento            | Descripción                                                                                                                                                                                          |
|:--------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Propósito           | Reemplazar por `0` todos los valores negativos contenidos en una lista.                                                                                                                              |
| Datos requeridos    | Una lista de valores numéricos.                                                                                                                                                                      |
| Precondición        | `valores` es una lista cuyos elementos son números comparables con cero.                                                                                                                             |
| Resultado           | Ninguno (`None`).                                                                                                                                                                                    |
| Poscondición        | Para cada posición de la lista, si el valor original era negativo, el valor final es `0`. Si el valor original era mayor o igual que cero, permanece sin cambios. La longitud de la lista no cambia. |
| Efectos observables | La lista recibida mediante `valores` es modificada directamente.                                                                                                                                     |

Casos de prueba:

| Lista (argumento) | Lista después de la llamada | Retorno esperado  |
|:-----------------:|:---------------------------:|:-----------------:|
|    `[2, 5, 8]`    |         `[2, 5, 8]`         |      `None`       |
|   `[-2, 5, -8]`   |         `[0, 5, 0]`         |      `None`       |
|    `[-3, -1]`     |          `[0, 0]`           |      `None`       |
|       `[]`        |            `[]`             |      `None`       |

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

| Caso                     | Llamada | Esperado | Obtenido | Conclusión |
|:-------------------------|:--------|:--------:|:--------:|:-----------|
| Bajo el límite           |         |          |          |            |
| En el límite             |         |          |          |            |
| Fracción sobre el límite |         |          |          |            |
| Exceso de varios kg      |         |          |          |            |
| Tarifa especial          |         |          |          |            |
| Equipaje de cabina       |         |          |          |            |



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




## Contexto 2

Un centro comunitario dispone de cierta cantidad de canastas. Las familias son 
atendidas en el orden de una lista. Por equidad se entregan como máximo dos 
canastas por familia. Las solicitudes iguales o menores que cero son errores y 
se rechazan. Si una familia pide más que el máximo, su entrega se reduce. 
Cuando se agota el stock, la atención termina.


**DF-011.** Diseñe la función para determinar una entrega individual:

```python
calcular_entrega(solicitadas, disponibles, max_por_familia=2)
```

Esta función no modifica el stock, solo retorna cuántas canastas corresponde entregar. 

1. Especifíque la función
2. Diseñe pruebas de solicitudes menor, igual y mayor que el máximo, stock insuficiente y agotado, y para un máximo excepcional de tres canastas.



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


| Caso                             | Argumentos | Esperado | Obtenido | Conclusión |
|:---------------------------------| :--- | :--- | :--- | :--- |
| Solicitudes normales             |  |  |  |  |
| Errores intercalados             |  |  |  |  |
| Stock agotado durante la jornada |  |  |  |  |
| Stock inicial agotado            |  |  |  |  |
| Lista vacía                      |  |  |  |  |
| Máximo excepcional               |  |  |  |  |

