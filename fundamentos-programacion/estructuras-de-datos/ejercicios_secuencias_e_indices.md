
# Ejercicios: Tratamiento de secuencia mediante índices

Diseñe e implemente funciones que procesen listas y tuplas utilizando índices para acceder a sus elementos, compare posiciones y actualice datos cuando corresponda.

- Implemente cada solución como una función con parámetros y retorno. Evite usar `input()` dentro de las funciones.
- Escriba un `docstring` que describa argumento, retornos y si modifica la lista recibida.
- Para practicar el procesamiento por índices, no utilice recorridos directos sobre elementos, recorra las secuencias accediendo a sus elementos mediante su índice.
- Puede utilizar `len()`, `range()`, `append()` y `tuple()`.
- Realice pruebas aisladas de las funciones y genere la tabla de seguimiento manual.

**IDX-001.** Un instrumento registra una secuencia de mediciones. Se considera que existe un descenso cuando una medición es menor que la inmediatamente anterior.

Por ejemplo:

```python
mediciones = [18, 21, 19, 19, 16, 20]
```

Existen descensos en los índices `2` y `4`:

- En el índice `2`, la medición cambia de `21` a `19`.
- En el índice `4`, la medición cambia de `19` a `16`.


Implemente la función:

```python
analizar_descensos(mediciones)
```

- Recibe una lista o tupla de números.
- Retorna una tupla con dos números: cantidad de descensos y una lista con los índices donde ocurren.
- La función no modifica la secuencia recibida.
- Si la secuencia está vacía o tiene un solo elemento, retorna `(0, [])`.

:::{dropdown} Solución
:open: false

**1. identidicar las posiciones que se comparan**

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

```python
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
```

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

### Preguntas

1. ¿Qué problema conceptual aparece si el recorrido comienza en `0`?
2. ¿Por qué el último índice que visita el recorrido es válido?
3. ¿Por qué la misma función trata con una lista y con una tupla?
4. ¿Qué modificaría para detectar aumentos?
5. ¿Cuál es efecto si se reemplaza `<` por `<=`?

:::


**IDX-002.** Implemente,

```python
posiciones_de(secuencia, buscado)
```

- Recibe una lista o tupla.
- Retorna una lista con **todos los índices** donde aparece `buscado`. 
- No modifica la entrada. 
- Una secuencia vacía retorna `[]`.

Por ejemplo,

```python
posiciones_de([4, 7, 4, 9, 4], 4)   # [0, 2, 4]
posiciones_de(("a", "b", "a"), "a") # [0, 2]
posiciones_de([2, 3], 8)            # []
```


**IDX-003.** Implemente,

```python
seleccionar_mayores(secuencia, limite)
```

Recibe una lista o tupla de números y retorna una lista de tuplas `(indice, valor)` para los elementos estrictamente mayores que `limite`. Conserva el orden original, no modificar la entrada y una secuencia vacía retorna `[]`.

Ejemplos,

```python
seleccionar_mayores([12, 7, 15, 10], 10)    # [(0, 12), (2, 15)]
seleccionar_mayores((3, 3, 3), 3)           # []
```



**IDX-004.** Implemente,

```python
alternar_signos(secuencia)
```

Recibe una lista o tupla de números y retorna una **lista nueva**. En los índices pares conserva el valor original, en los índices impares cambia su signo. No modificar la entrada y una secuencia vacía produce `[]`.

Por ejemplo,

```python
alternar_signos([5, 8, -3, -6, 2])  # [5, -8, -3, 6, 2]
alternar_signos((4,))               # [4]
```



**IDX-005.** Implemente,

```python
reemplazar_negativos(datos)
```

Recibe una lista de números, reemplaza cada número negativo por `0` en la misma lista y retorna la cantidad de reemplazos. Usar asignación por índice y una lista vacía retorna `0`.

Por ejemplo,

```python
datos = [3, -2, 0, -5]
cantidad = reemplazar_negativos(datos)  # cantidad: 2
# datos: [3, 0, 0, 0]
```

Antes de ejecutar lo siguiente, evalúe el valor esperado esperas de cada variable:

```python
original = [3, -2, 0, -5]
copia_original = original

cantidad = reemplazar_negativos(copia_original)

print(original)
print(copia_original)
```

**Preguntas:**

1. ¿Por qué ambas variables permiten observar los cambios?
2. ¿Se podría utilizar la misma asignación por índice si la entrada fuera una tupla?

### Ejercicio 5. Intercambiar posiciones de una lista

Implementa:

```python
intercambiar(datos, i, j)
```

Recibe una lista y dos índices válidos. Intercambia los elementos de esas posiciones, modifica la lista recibida y retorna `None`.

```python
datos = [10, 20, 30, 40]
intercambiar(datos, 0, 3)

# datos: [40, 20, 30, 10]
```

Primero realiza el intercambio con una variable auxiliar. Luego escribe una segunda versión mediante asignación múltiple.

**Casos que debes probar:**

- Intercambiar el primer y el último elemento.
- Intercambiar dos posiciones interiores.
- Utilizar el mismo índice para `i` y `j`.

**Pregunta:** ¿por qué dos asignaciones consecutivas sin una variable auxiliar pueden perder uno de los valores?

### Ejercicio 6. Construir una tupla de diferencias

Implementa:

```python
diferencias_consecutivas(secuencia)
```

Recibe una lista o tupla de números y retorna una **tupla nueva** con la diferencia entre cada elemento y el anterior.

```python
diferencias_consecutivas((10, 13, 12, 18))
# (3, -1, 6)

diferencias_consecutivas([5, 5, 2])
# (0, -3)
```

**Condiciones:** no modificar la entrada. Con cero o un elemento, retornar `()`.

Puedes acumular las diferencias en una lista auxiliar y convertirla en tupla al finalizar.

**Preguntas:**

1. Si la entrada tiene `n` elementos y `n >= 1`, ¿cuántos elementos tiene el resultado?
2. ¿Qué relación existe entre un resultado negativo y los descensos del ejercicio guiado?

### Ejercicio 7. Encontrar el máximo y su primera posición

Implementa:

```python
maximo_y_posicion(secuencia)
```

Recibe una lista o tupla **no vacía** de números y retorna una tupla `(valor_maximo, indice)`.

Si el máximo aparece varias veces, retorna el índice de su **primera aparición**.

```python
maximo_y_posicion([6, 9, 4, 9])
# (9, 1)

maximo_y_posicion((-8, -3, -5))
# (-3, 1)

maximo_y_posicion([7])
# (7, 0)
```

**Condiciones:** no modificar la entrada. No utilizar `max()` ni `.index()`.

**Pista:** utiliza el elemento del índice `0` como candidato inicial.

**Pregunta:** ¿por qué inicializar el máximo en `0` daría un resultado incorrecto para algunas entradas?

### Ejercicio 8. Integración: actualizar una lista de tuplas

Un inventario se representa mediante una lista de tuplas:

```python
inventario = [
    ("cuaderno", 12),
    ("lapiz", 30),
    ("goma", 8)
]
```

Cada tupla contiene `(nombre, cantidad)`. Supón que los nombres son únicos y las cantidades son enteros no negativos. `nueva_cantidad` también debe ser un entero no negativo.

Implementa dos funciones:

```python
buscar_producto(inventario, nombre)
```

Retorna el índice del producto, o `-1` si no existe.

```python
actualizar_cantidad(inventario, nombre, nueva_cantidad)
```

Utiliza `buscar_producto()`. Si encuentra el producto, reemplaza la tupla de esa posición por una nueva y retorna `True`. Si no lo encuentra, retorna `False` y deja el inventario sin cambios.

```python
buscar_producto(inventario, "lapiz")
# 1

actualizar_cantidad(inventario, "lapiz", 25)
# True

# inventario:
# [("cuaderno", 12), ("lapiz", 25), ("goma", 8)]

actualizar_cantidad(inventario, "regla", 10)
# False
```

**Condiciones:**

- Recorrer el inventario mediante índices.
- Acceder a los campos mediante `inventario[i][0]` e `inventario[i][1]`.
- No agregar productos nuevos.
- Reemplazar la tupla completa al actualizar la cantidad.
- Un inventario vacío produce `-1` en la búsqueda y `False` en la actualización.

**Preguntas:**

1. ¿Por qué se puede reemplazar `inventario[i]`, aunque ese elemento sea una tupla?
2. ¿Por qué no se puede asignar directamente un valor a `inventario[i][1]`?
3. ¿Por qué es necesario comprobar el resultado de la búsqueda antes de utilizarlo como índice?

