---
title: Procesamiento de listas y tuplas mediante índices — soluciones
subtitle: Enunciados y soluciones — semanas 7 y 8
---

# Guía de ejercicios: procesamiento de listas y tuplas mediante índices — soluciones

**Asignatura:** Lenguaje de Programación 457847  
**Contenidos:** semanas 7 y 8

## Objetivo

Diseñar e implementar funciones que procesen listas y tuplas utilizando índices para acceder a sus elementos, comparar posiciones y actualizar datos cuando corresponda.

La guía aborda búsqueda, selección, transformación, actualización y referencias compartidas en listas, además de tuplas, inmutabilidad y retorno múltiple.

## Indicaciones generales

- Implementa cada solución como una función con parámetros y retorno. Evita usar `input()` dentro de las funciones.
- Escribe un `docstring` que describa qué recibe la función, qué retorna y si modifica la lista recibida.
- Recorre las secuencias con `for i in range(...)` o con `while`, accediendo a los elementos mediante `secuencia[i]`.
- Para practicar el procesamiento por índices, no utilices recorridos directos sobre elementos, comprensiones, rebanadas, `enumerate()`, `zip()` ni funciones que resuelvan el problema completo, como `sum()`, `min()`, `max()`, `sorted()` o `.index()`.
- Puedes utilizar `len()`, `range()`, `append()` y `tuple()`.
- Supón que las entradas cumplen las condiciones indicadas. Todavía no es necesario trabajar con excepciones.
- Prueba tus funciones con los ejemplos propuestos y con casos adicionales.

**Recuerda:** una secuencia de longitud `n` tiene índices no negativos desde `0` hasta `n - 1`. Una lista permite asignar un nuevo valor a una posición; una tupla no permite reemplazar sus elementos.

## 1. Ejercicio guiado: detectar descensos entre mediciones

Un equipo registra una secuencia de mediciones. Se considera que existe un descenso cuando una medición es menor que la inmediatamente anterior.

Por ejemplo:

```python
mediciones = [18, 21, 19, 19, 16, 20]
```

Existen descensos en los índices `2` y `4`:

- En el índice `2`, la medición cambia de `21` a `19`.
- En el índice `4`, la medición cambia de `19` a `16`.

### Especificación

Implementar:

```python
analizar_descensos(mediciones)
```

La función:

- Recibe una lista o tupla de números.
- Retorna una tupla con dos resultados: la cantidad de descensos y una lista con los índices donde ocurren.
- No modifica la secuencia recibida.
- Si la secuencia está vacía o tiene un solo elemento, retorna `(0, [])`.

### Paso 1: identificar las posiciones que se comparan

Para cada índice `i`, debemos comparar:

```python
mediciones[i] < mediciones[i - 1]
```

El recorrido comienza en `1`, porque el primer elemento no tiene un elemento anterior.

```python
for i in range(1, len(mediciones)):
    # Comparar la medición actual con la anterior.
    pass
```

### Paso 2: seguir manualmente el recorrido

| `i` | Elemento anterior | Elemento actual | ¿Hay descenso? | Índices acumulados |
| ---: | ---: | ---: | :---: | :--- |
| 1 | 18 | 21 | No | `[]` |
| 2 | 21 | 19 | Sí | `[2]` |
| 3 | 19 | 19 | No | `[2]` |
| 4 | 19 | 16 | Sí | `[2, 4]` |
| 5 | 16 | 20 | No | `[2, 4]` |

### Paso 3: implementar la función

```python
def analizar_descensos(mediciones):
    """Retorna la cantidad de descensos y sus índices.

    Recibe una lista o tupla de números.
    No modifica la secuencia recibida.
    """
    indices = []

    for i in range(1, len(mediciones)):
        if mediciones[i] < mediciones[i - 1]:
            indices.append(i)

    return len(indices), indices
```

La expresión del `return` construye una tupla. Sus dos componentes se pueden recuperar mediante desempaquetado:

```python
cantidad, posiciones = analizar_descensos(
    [18, 21, 19, 19, 16, 20]
)

print(cantidad)    # 2
print(posiciones)  # [2, 4]
```

### Paso 4: comprobar casos diferentes

```python
assert analizar_descensos([18, 21, 19, 19, 16, 20]) == (2, [2, 4])
assert analizar_descensos((9, 7, 5)) == (2, [1, 2])
assert analizar_descensos([4, 4, 4]) == (0, [])
assert analizar_descensos([8]) == (0, [])
assert analizar_descensos([]) == (0, [])
```

Cada `assert` comprueba que el resultado obtenido coincide con el esperado. Si no coincide, Python interrumpe la ejecución e informa del fallo.

### Preguntas de comprensión

1. ¿Qué problema conceptual aparece si el recorrido comienza en `0`? Considera qué significa el índice `-1` en Python.
2. ¿Por qué el último índice que visita el recorrido es válido?
3. ¿Por qué la misma función funciona con una lista y con una tupla?
4. ¿Qué habría que cambiar para detectar aumentos?
5. ¿Qué resultado se obtiene si se reemplaza `<` por `<=`?

### Respuestas a las preguntas de comprensión

1. Si el recorrido comenzara en `0`, se compararía la primera medición con la última, porque `mediciones[-1]` accede al último elemento de una secuencia no vacía. Esa comparación no corresponde a dos mediciones consecutivas en el orden del registro.
2. Cuando hay al menos dos elementos, el último índice visitado es `len(mediciones) - 1`, que es válido. Su anterior también lo es porque `i >= 1`. Con cero o un elemento, el recorrido no ejecuta su cuerpo.
3. La función solo utiliza longitud y acceso por índice, operaciones disponibles en listas y tuplas. No asigna valores a sus posiciones.
4. Se reemplazaría `<` por `>`.
5. Se registrarían también las igualdades: se detectarían mediciones que no aumentan. Para el ejemplo guiado, el retorno sería `(3, [2, 3, 4])`.

## 2. Ejercicios de práctica

### Ejercicio 1. Encontrar todas las posiciones

Implementa:

```python
posiciones_de(secuencia, buscado)
```

Recibe una lista o tupla y retorna una lista con **todos los índices** donde aparece `buscado`.

```python
posiciones_de([4, 7, 4, 9, 4], 4)
# [0, 2, 4]

posiciones_de(("a", "b", "a"), "a")
# [0, 2]

posiciones_de([2, 3], 8)
# []
```

**Condiciones:** no modificar la entrada. Una secuencia vacía produce `[]`.

**Prueba adicional:** el valor buscado aparece únicamente en la última posición.

#### Solución

```python
def posiciones_de(secuencia, buscado):
    """Retorna los índices de buscado en una lista o tupla, sin modificarla."""
    posiciones = []
    for i in range(len(secuencia)):
        if secuencia[i] == buscado:
            posiciones.append(i)
    return posiciones


assert posiciones_de([4, 7, 4, 9, 4], 4) == [0, 2, 4]
assert posiciones_de(("a", "b", "a"), "a") == [0, 2]
assert posiciones_de([2, 3], 8) == []
assert posiciones_de([], 4) == []
assert posiciones_de([2, 3, 8], 8) == [2]
```

Se guarda el índice `i` cuando el elemento de esa posición coincide con el valor buscado. La lista de resultados es nueva; la entrada no se modifica.

### Ejercicio 2. Seleccionar elementos y conservar sus índices

Implementa:

```python
seleccionar_mayores(secuencia, limite)
```

Recibe una lista o tupla de números y retorna una lista de tuplas `(indice, valor)` para los elementos estrictamente mayores que `limite`. Conserva el orden original.

```python
seleccionar_mayores([12, 7, 15, 10], 10)
# [(0, 12), (2, 15)]

seleccionar_mayores((3, 3, 3), 3)
# []
```

**Condiciones:** no modificar la entrada. Una secuencia vacía produce `[]`.

**Pregunta:** ¿qué información se perdería si la función retornara solamente los valores seleccionados?

#### Solución

```python
def seleccionar_mayores(secuencia, limite):
    """Retorna pares (índice, valor) para valores mayores que limite.

    Recibe una lista o tupla de números y no la modifica.
    """
    seleccionados = []
    for i in range(len(secuencia)):
        if secuencia[i] > limite:
            seleccionados.append((i, secuencia[i]))
    return seleccionados


assert seleccionar_mayores([12, 7, 15, 10], 10) == [(0, 12), (2, 15)]
assert seleccionar_mayores((3, 3, 3), 3) == []
assert seleccionar_mayores([], 10) == []
assert seleccionar_mayores((11, 11), 10) == [(0, 11), (1, 11)]
```

El recorrido ascendente por índices conserva el orden original. Cada resultado es una tupla dentro de una lista nueva.

**Respuesta:** si se retornaran solamente los valores, se perderían sus posiciones en la secuencia original, especialmente útiles cuando hay valores repetidos.

### Ejercicio 3. Transformar según la posición

Implementa:

```python
alternar_signos(secuencia)
```

Recibe una lista o tupla de números y retorna una **lista nueva**. En los índices pares conserva el valor original; en los índices impares cambia su signo.

```python
alternar_signos([5, 8, -3, -6, 2])
# [5, -8, -3, 6, 2]

alternar_signos((4,))
# [4]
```

**Condiciones:** no modificar la entrada. Una secuencia vacía produce `[]`.

**Pregunta:** ¿cuál es la diferencia entre comprobar `i % 2 == 0` y comprobar `secuencia[i] % 2 == 0`?

#### Solución

```python
def alternar_signos(secuencia):
    """Retorna una lista nueva con el signo cambiado en índices impares.

    Recibe una lista o tupla de números y no la modifica.
    """
    resultado = []
    for i in range(len(secuencia)):
        if i % 2 == 0:
            resultado.append(secuencia[i])
        else:
            resultado.append(-secuencia[i])
    return resultado


datos = [5, 8, -3, -6, 2]
resultado = alternar_signos(datos)
assert resultado == [5, -8, -3, 6, 2]
assert datos == [5, 8, -3, -6, 2]
assert resultado is not datos
assert alternar_signos((4,)) == [4]
assert alternar_signos([]) == []
assert alternar_signos((0, 0, -2, 3)) == [0, 0, -2, -3]
```

**Respuesta:** `i % 2 == 0` comprueba la paridad de la posición; `secuencia[i] % 2 == 0` comprueba la paridad del valor almacenado. La consigna depende de la posición.

### Ejercicio 4. Actualizar una lista y observar las referencias

Implementa:

```python
reemplazar_negativos(datos)
```

Recibe una lista de números, reemplaza cada número negativo por `0` **en la misma lista** y retorna la cantidad de reemplazos.

```python
datos = [3, -2, 0, -5]
cantidad = reemplazar_negativos(datos)

# cantidad: 2
# datos: [3, 0, 0, 0]
```

**Condiciones:** usar asignación por índice. Una lista vacía produce `0`.

Antes de ejecutar lo siguiente, escribe qué esperas que contenga cada variable:

```python
original = [3, -2, 0, -5]
otra_referencia = original

cantidad = reemplazar_negativos(otra_referencia)

print(original)
print(otra_referencia)
```

**Preguntas:**

1. ¿Por qué ambas variables permiten observar los cambios?
2. ¿Se podría utilizar la misma asignación por índice si la entrada fuera una tupla?

#### Solución

```python
def reemplazar_negativos(datos):
    """Reemplaza negativos por cero en la lista y retorna cuántos cambió."""
    reemplazos = 0
    for i in range(len(datos)):
        if datos[i] < 0:
            datos[i] = 0
            reemplazos += 1
    return reemplazos


original = [3, -2, 0, -5]
otra_referencia = original
assert reemplazar_negativos(otra_referencia) == 2
assert original == [3, 0, 0, 0]
assert otra_referencia == [3, 0, 0, 0]
assert original is otra_referencia

sin_negativos = [0, 2, 5]
assert reemplazar_negativos(sin_negativos) == 0
assert sin_negativos == [0, 2, 5]

assert reemplazar_negativos([]) == 0

negativos = [-1, -2]
assert reemplazar_negativos(negativos) == 2
assert negativos == [0, 0]
```

**Respuestas:**

1. Las dos variables hacen referencia a la misma lista. La asignación `otra_referencia = original` no crea una copia. Ambas impresiones muestran `[3, 0, 0, 0]`.
2. Una tupla no admite asignación a sus posiciones. Si se intentara reemplazar un elemento negativo mediante esa asignación, se produciría un `TypeError`.

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

#### Solución con variable auxiliar

```python
def intercambiar(datos, i, j):
    """Intercambia dos posiciones válidas de una lista y retorna None."""
    auxiliar = datos[i]
    datos[i] = datos[j]
    datos[j] = auxiliar
    return None


datos = [10, 20, 30, 40]
assert intercambiar(datos, 0, 3) is None
assert datos == [40, 20, 30, 10]

interiores = [10, 20, 30, 40]
assert intercambiar(interiores, 1, 2) is None
assert interiores == [10, 30, 20, 40]

misma_posicion = [10, 20, 30]
assert intercambiar(misma_posicion, 1, 1) is None
assert misma_posicion == [10, 20, 30]
```

#### Solución con asignación múltiple

Se usa otro nombre para poder comparar ambas versiones en una misma sesión.

```python
def intercambiar_multiple(datos, i, j):
    """Intercambia dos posiciones válidas de una lista y retorna None."""
    datos[i], datos[j] = datos[j], datos[i]
    return None


datos = [10, 20, 30, 40]
assert intercambiar_multiple(datos, 0, 3) is None
assert datos == [40, 20, 30, 10]

interiores = [10, 20, 30, 40]
assert intercambiar_multiple(interiores, 1, 2) is None
assert interiores == [10, 30, 20, 40]

misma_posicion = [10, 20, 30]
assert intercambiar_multiple(misma_posicion, 1, 1) is None
assert misma_posicion == [10, 20, 30]
```

**Respuesta:** al ejecutar primero `datos[i] = datos[j]`, el valor original de `datos[i]` se sobrescribe. Si luego se asigna `datos[j] = datos[i]`, ambas posiciones terminan con el mismo valor cuando sus valores iniciales eran distintos. La variable auxiliar conserva el valor original; en la asignación múltiple se evalúa el lado derecho antes de efectuar las asignaciones.

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

#### Solución

```python
def diferencias_consecutivas(secuencia):
    """Retorna una tupla con las diferencias entre elementos consecutivos.

    Recibe una lista o tupla de números y no la modifica.
    Con cero o un elemento retorna una tupla vacía.
    """
    diferencias = []
    for i in range(1, len(secuencia)):
        diferencias.append(secuencia[i] - secuencia[i - 1])
    return tuple(diferencias)


assert diferencias_consecutivas((10, 13, 12, 18)) == (3, -1, 6)
assert diferencias_consecutivas([5, 5, 2]) == (0, -3)
assert diferencias_consecutivas([]) == ()
assert diferencias_consecutivas([8]) == ()
```

La lista auxiliar permite acumular diferencias con `append()`. Al finalizar, `tuple()` construye la tupla del resultado.

**Respuestas:**

1. Para `n >= 1`, hay `n - 1` diferencias.
2. Cada diferencia negativa indica un descenso. La diferencia almacenada en el índice `k` del resultado corresponde a la comparación entre los índices `k` y `k + 1` de la entrada; el ejercicio guiado registra `k + 1`.

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

#### Solución

```python
def maximo_y_posicion(secuencia):
    """Retorna (máximo, índice de su primera aparición).

    Recibe una lista o tupla no vacía de números y no la modifica.
    """
    maximo = secuencia[0]
    posicion = 0
    for i in range(1, len(secuencia)):
        if secuencia[i] > maximo:
            maximo = secuencia[i]
            posicion = i
    return maximo, posicion


assert maximo_y_posicion([6, 9, 4, 9]) == (9, 1)
assert maximo_y_posicion((-8, -3, -5)) == (-3, 1)
assert maximo_y_posicion([7]) == (7, 0)
assert maximo_y_posicion((4, 4, 4)) == (4, 0)
assert maximo_y_posicion([9, 6, 2]) == (9, 0)
```

El candidato inicial pertenece a la secuencia. La comparación estricta `>` evita cambiar la posición cuando se encuentra otra aparición del mismo máximo.

**Respuesta:** inicializar en `0` daría un máximo inexistente si todos los valores fueran negativos. En `(-8, -3, -5)`, ningún elemento supera `0`, aunque el máximo correcto es `-3`.

La secuencia vacía queda fuera de la precondición; no se solicita validar ese caso.

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

#### Solución

```python
def buscar_producto(inventario, nombre):
    """Retorna el índice del producto o -1 si no existe.

    Recibe una lista de tuplas (nombre, cantidad) con nombres únicos.
    No modifica el inventario.
    """
    for i in range(len(inventario)):
        if inventario[i][0] == nombre:
            return i
    return -1


def actualizar_cantidad(inventario, nombre, nueva_cantidad):
    """Actualiza un producto existente y retorna True; si falta, False.

    Recibe una lista de tuplas (nombre, cantidad) con nombres únicos
    y una nueva cantidad entera no negativa.
    Modifica la lista reemplazando la tupla del producto encontrado.
    """
    posicion = buscar_producto(inventario, nombre)
    if posicion == -1:
        return False
    inventario[posicion] = (inventario[posicion][0], nueva_cantidad)
    return True


inventario = [("cuaderno", 12), ("lapiz", 30), ("goma", 8)]
assert buscar_producto(inventario, "lapiz") == 1
assert buscar_producto(inventario, "cuaderno") == 0
assert buscar_producto(inventario, "goma") == 2
assert buscar_producto(inventario, "regla") == -1
assert buscar_producto([], "lapiz") == -1
assert inventario == [("cuaderno", 12), ("lapiz", 30), ("goma", 8)]

tupla_anterior = inventario[1]
assert actualizar_cantidad(inventario, "lapiz", 25) is True
assert inventario == [("cuaderno", 12), ("lapiz", 25), ("goma", 8)]
assert tupla_anterior == ("lapiz", 30)

assert actualizar_cantidad(inventario, "regla", 10) is False
assert inventario == [("cuaderno", 12), ("lapiz", 25), ("goma", 8)]
assert actualizar_cantidad([], "lapiz", 10) is False

assert actualizar_cantidad(inventario, "goma", 0) is True
assert inventario[2] == ("goma", 0)
```

**Respuestas:**

1. `inventario` es una lista mutable: puede reemplazarse la referencia almacenada en una de sus posiciones. Se crea una nueva tupla y se coloca allí.
2. `inventario[i][1]` designa una posición dentro de una tupla, que no admite asignación. Reemplazar la tupla en la lista no modifica la tupla anterior.
3. En Python, `-1` también es un índice válido para una secuencia no vacía: designa su último elemento. Usarlo sin comprobar la búsqueda podría actualizar el último producto aunque el nombre buscado no exista. En una lista vacía, ese acceso produciría un error.

## 3. Entrega y revisión

Para cada ejercicio, entrega:

1. La función con su `docstring`.
2. Al menos tres pruebas con resultados esperados.
3. Una indicación de si modifica la entrada o construye un resultado nuevo.

En al menos un ejercicio, incluye una tabla de seguimiento con el índice, los elementos consultados y el estado parcial del resultado.

**Criterios de revisión:**

- Utiliza índices válidos y límites de recorrido correctos.
- Distingue índices de valores.
- Cumple el tipo y significado del retorno solicitado.
- Respeta la mutabilidad de listas y la inmutabilidad de tuplas.
- Resuelve correctamente los casos especiales indicados.
- Reutiliza funciones cuando el ejercicio lo solicita.
