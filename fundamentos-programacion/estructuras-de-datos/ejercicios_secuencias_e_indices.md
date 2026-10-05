
# Ejercicios: Tratamiento de secuencia mediante índices

Diseñe e implemente funciones que procesen listas y tuplas utilizando índices para acceder a sus elementos.

- Implemente cada solución como una función con parámetros y retorno. 
- Para estos ejercicios, las funciones no se deben capturar entradas `input()`.
- Escriba un `docstring` que describa el propósito de la función, su argumento, retornos y si modifica el valor recibido.
- No utilice recorridos directos sobre elementos, recorra las secuencias accediendo a sus elementos mediante su índice.
- Puede usar `len()`, `range()`, `append()` y `tuple()`.
- Realice pruebas aisladas de las funciones y genere las tablas de seguimiento manual.

**IDX-001.** Un instrumento registra una secuencia de mediciones. Se considera que existe un descenso cuando una medición es menor que la inmediatamente anterior.

Por ejemplo:

```python
mediciones = [18, 21, 19, 19, 16, 20]
```

Existen descensos en los índices `2` y `4`:

- En el índice `2`, la medición cambia de `21` a `19`.
- En el índice `4`, la medición cambia de `19` a `16`.


Implemente la función `analizar_descensos(mediciones)` que recibe una lista o tupla de números, y retorna una tupla que contiene la cantidad de descensos y una lista con los índices donde estos ocurren. Esta función no modifica la secuencia recibida y, si la secuencia está vacía o tiene un solo elemento, retorna `(0, [])`.

**Responda:**

1. ¿Cómo influye el índice inicial del recorrido en el resultado de la función?
2. ¿Son correctos los límites del recorrido? Justifique.
3. ¿Qué tipos de secuencias admite la función? Fundamente su respuesta.
4. ¿Cómo adaptaría la función para identificar otro tipo de cambio entre mediciones consecutivas?
5. ¿Cómo influye el operador de comparación en los cambios que detecta la función?

::::{dropdown} Solución
:open: false

**1. identificar las posiciones que se comparan**

- Para cada índice `i`, debe comparar:

```python
mediciones[i] < mediciones[i - 1]
```

- El recorrido comienza en `1`, porque el primer elemento no tiene un elemento anterior.

```python
for i in range(1, len(mediciones)):
    actual = mediciones[i]
    anterior = mediciones[i - 1]
```

**2. seguir manualmente el recorrido**

|  #  | `i` | actual | anterior |
|:---:|----:|-------:|---------:|
|  1  |     |        |          |  
|  2  |     |        |          |  
|  :  |     |        |          |


**3. implementar la función**

:::{code-block} python
:linenos:

def analizar_descensos(mediciones):
    """Retorna la cantidad de descensos y sus índices.

    - Recibe una lista o tupla de números.
    - No modifica la secuencia recibida.
    """
    indices = []

    for i in range(1, len(mediciones)):
        if mediciones[i] < mediciones[i - 1]:
            indices.append(i)

    return len(indices), indices
:::

La expresión del `return` construye una tupla. Sus dos componentes se pueden recuperar mediante desempaquetado:

```python
cantidad, posiciones = analizar_descensos([18, 21, 19, 19, 16, 20])
print(cantidad)    # 2
print(posiciones)  # [2, 4]
```

**4. comprobar con casos de prueba**

|       Argumento       | Caso                     |  Esperado   |   Obtenido   |
|:---------------------:|:-------------------------|:-----------:|:------------:|
| `[18,21,19,19,16,20]` | Representativo con lista | `(2,[2,4])` |              |
|      `(9, 7, 5)`      | Representativo con tupla | `(2,[1,2])` |              |
|      `[4, 4, 4]`      | Sin descensos            |  `(0, [])`  |              |
|          `:`          | :                        |     `:`     |              |

Se recomienda realizar el seguimiento manual.

::::


**IDX-002.** Implemente la función `posiciones_de(secuencia, buscado)` que recibe como argumento una lista o tupla, y retorna una lista con todos los índices donde aparece `buscado`. La función no modifica la entrada, y Uua secuencia vacía retorna `[]`.

Por ejemplo,

```python
posiciones_de([4, 7, 4, 9, 4], 4)   # [0, 2, 4]
posiciones_de(("a", "b", "a"), "a") # [0, 2]
posiciones_de([2, 3], 8)            # []
```


**IDX-003.** Implemente `seleccionar_mayores(secuencia, limite)` que recibe como argumento una lista o tupla de números y retorna una lista de tuplas `(indice, valor)` para los elementos mayores que `limite`. Esta función conserva el orden original, no modifica la entrada y una secuencia vacía retorna `[]`.

Ejemplos de llamadas,

```python
seleccionar_mayores([12, 7, 15, 10], 10)    # [(0, 12), (2, 15)]
seleccionar_mayores((3, 3, 3), 3)           # []
```



**IDX-004.** Implemente la función `alternar_signos(secuencia)` que recibe una lista o tupla de números y retorna una lista nueva. En los índices pares conserva el valor original, en los índices impares cambia su signo. No modifica la entrada y una secuencia vacía retorna `[]`.

Por ejemplo,

```python
alternar_signos([5, 8, -3, -6, 2])  # [5, -8, -3, 6, 2]
alternar_signos((4,))               # [4]
```



**IDX-005.** Implemente `reemplazar_negativos(datos)` que recibe como argumento una lista de números, reemplaza cada número negativo por `0` y retorna la cantidad de valores reemplazados. Una lista vacía retorna `0`.

Por ejemplo,

```python
datos = [3, -2, 0, -5]
cantidad = reemplazar_negativos(datos)  # cantidad: 2
# datos: [3, 0, 0, 0]
```

Antes de ejecutar lo siguiente, evalúe el valor esperado de cada variable en el siguiente fragmento:

:::{code-block} python
:linenos:

original = [3, -2, 0, -5]
copia_original = original

cantidad = reemplazar_negativos(copia_original)

print(original)
print(copia_original)
:::

**Responda:**

- ¿Ambas variables permiten observar los cambios? ¿Por qué?
- ¿Se puede utilizar la misma asignación por índice si la entrada es una tupla?




**IDX-006.** Implemente la función `intercambiar(datos, i, j)`, que recibe una lista y dos índices válidos. La función debe intercambiar los elementos de estas posiciones, modificar la lista recibida y retornar `None`. Por ejemplo,

```python
datos = [10, 20, 30, 40]
intercambiar(datos, 0, 3)       # datos: [40, 20, 30, 10]
```
Escriba dos versiones de esta función:
- Una que realice el intercambio con una variable auxiliar. 
- Otra versión mediante asignación múltiple.

Casos de prueba sugeridos:

| Argumento | Caso                                         | Esperado |   Obtenido   |
|:---------:|:---------------------------------------------|:--------:|:------------:|
|           | Intercambiar el primer y el último elemento. |          |              |
|           | Intercambiar dos posiciones interiores.      |          |              |
|           | Utilizar el mismo índice para `i` y `j`      |          |              |
|           | :                                            |          |              |




**IDX-007.** Implemente la función `diferencias_consecutivas(secuencia)` que recibe como argumento una lista o tupla de números y retorna una tupla nueva con la diferencia entre cada elemento y el anterior. Esta función no modifica la entrada, y con cero o un elemento, retornar `()`. Por ejemplo,

```python
diferencias_consecutivas((10, 13, 12, 18))  # (3, -1, 6)
diferencias_consecutivas([5, 5, 2])         # (0, -3)
```

**Responda:**

¿Qué relación existe entre la cantidad de elementos de la entrada y la del retorno? Justifique.



**IDX-008.** Implemente la función `maximo_y_posicion(secuencia)` que recibe como argumento una lista o tupla no vacía de números y retorna una tupla `(valor_maximo, indice)`. Si el máximo aparece varias veces, retorna el índice de su primera ocurrencia. La función no modifica la entrada. Por ejemplo,

```python
maximo_y_posicion([6, 9, 4, 9])     # (9, 1)
maximo_y_posicion((-8, -3, -5))     # (-3, 1)
maximo_y_posicion([7])              # (7, 0)
```



**IDX-009.** Un inventario se representa mediante una lista de tuplas, por ejemplo,

```python
inventario = [("teclado", 12), ("mouse", 30), ("monitor", 8)]
```

- Cada tupla contiene `(nombre, cantidad)`.
- Los nombres son únicos y las cantidades son enteros no negativos.

Implementa dos funciones:

- `buscar_producto(inventario, nombre)`: retorna el índice del producto, o `-1` si no existe.
- `actualizar_cantidad(inventario, nombre, nueva_cantidad)`: agrega un nuevo producto con un su respectiva cantidad. `nueva_cantidad` también es un entero no negativo. Esta función debe llamar a `buscar_producto()`. Si encuentra el producto, reemplaza la tupla de esa posición por una nueva compuesta por `(nombre, nueva_cantidad)` (argumento) y retorna `True`. Si no lo encuentra, retorna `False` y deja el inventario sin cambios.

Ejemplo de llamadas:
```python
buscar_producto(inventario, "teclado")              # 1
actualizar_cantidad(inventario, "teclado", 25)      # True
# inventario: [("teclado", 25), ("mouse", 30), ("monitor", 8)]

actualizar_cantidad(inventario, "silla", 10)        # False
```


**Responda:**
1. ¿Qué modificaciones permite la estructura de datos utilizada para representar el inventario? Justifique su respuesta.
2. ¿Qué podría ocurrir si se utiliza directamente el resultado de buscar_producto() para actualizar el inventario? Analice los posibles casos.



**IDX-009.** Un instrumento registra mediciones en una lista o tupla. Para observar su comportamiento se desea calcular el promedio de cada grupo (ventana) de `k` mediciones consecutivas.

Implemente dos funciones,

- `promedio_ventana(secuencia, inicio, k)` retorna el promedio de los `k` elementos que comienzan en `inicio`. Suponga que `k` es un entero positivo y que `0 <= inicio` e `inicio + k <= len(secuencia)`.
- `promedios_moviles(secuencia, k)` recibe una lista o tupla de números y un entero positivo `k`. Retorna una tupla con los promedios de todas las ventanas completas, en orden. Debe utilizar la función auxiliar. Si no cabe una ventana completa, retorna `()`.
- Ninguna función modifica la entrada.


Ejemplos de llamadas a las funciones:

```python
promedio_ventana([10, 14, 18, 22, 26], 1, 3)        # 18.0

promedios_moviles([10, 14, 18, 22, 26], 3)          # (14.0, 18.0, 22.0)
promedios_moviles((4, 8), 1)                        # (4.0, 8.0)
promedios_moviles([4, 8], 3)                        # ()
```