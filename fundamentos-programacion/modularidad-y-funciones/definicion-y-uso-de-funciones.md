# Definición y uso de funciones

## Definición de una función

La **definición de una función** incorpora al programa una unidad identificada por un nombre:

- su **encabezado** declara la información requerida por el lenguaje,
- su **cuerpo** contiene las instrucciones que realizan la tarea.

La definición establece qué debe ocurrir cuando se produzca una llamada, pero escribirla no equivale a ejecutar inmediatamente todas las instrucciones de su cuerpo.

La correspondencia con la especificación debe ser explícita. El **nombre** expresa la operación, los **parámetros** representan los datos de entrada, las **instrucciones** implementan la relación especificada, y el **retorno** entrega el resultado a la operación invocada.

En Python [@python314compound]:

- La sentencia `def` marca el comienzo del encabezado de la función.
- El nombre de la función es un identificador exclusivo.
- El argumento de la función `()`, contiene los parámetros a través de los cuales se pasan los valores a una función. Son opcionales.
- Los dos puntos (`:`) marcan el final de la cabecera de la función.
- El `docstring` [@pep257] permite describir lo que hace la función.
- El cuerpo forma un bloque con indentación.
- Una sentencia `return` (opcional) devuelve un valor desde la función.

::::{hint} Ejemplo de función: `es_observacion_valida`
:label: ejemplo-funcion

La [especificación](#tab-cap07-especificacion-validacion) admite la siguiente implementación:

```{code-block}python
:label: code-es_observacion_valida
:linenos: true
:lineno-start: 1
:emphasize-lines:
:caption:

def es_observacion_valida(valor):
    """Indica si valor pertenece al intervalo cerrado [0, 100]."""
    observacion_valida = 0 <= valor <= 100
    return observacion_valida
```

El encabezado identifica la operación y declara su parámetro, de acuerdo con los datos requeridos de la [especificación](#tab-cap07-especificacion-validacion). La expresión relacional implementa la condición indicada en la poscondición y `return` entrega el valor booleano. La cadena de documentación resume el propósito; no reemplaza la especificación completa, pues no expresa por sí sola todas las restricciones del dominio.

La otra [especificación](#tab-cap07-especificacion-promedio) se traduce en una segunda definición.

```{code-block}python
:label: code-calcular_promedio
:linenos: true
:lineno-start: 1
:emphasize-lines:
:caption:

def calcular_promedio(observaciones_validas):
    """Devuelve el promedio de las observaciones válidas."""
    suma = 0
    cantidad = 0

    for valor in observaciones_validas:
        suma = suma + valor
        cantidad = cantidad + 1

    promedio = suma / cantidad
    return promedio
```

La función tiene como parámetro la lista declarada en datos de requeridos de la [especificación](#tab-cap07-especificacion-promedio). Realiza internamente el recorrido necesario para obtener la suma y la cantidad. Las variables `suma`, `cantidad` y `promedio` permiten implementar la relación establecida por la poscondición.

::::


## Llamada de una función

Una **llamada** solicita la ejecución de una función y proporciona los datos concretos que esta requiere. Mientras que la definición describe una operación general, cada llamada inicia una ejecución particular con argumentos determinados. Durante esa ejecución, el control se transfiere desde el punto de llamada al cuerpo de la función y, cuando esta termina, regresa al punto inmediatamente posterior a la llamada:

```{figure} ../../assets/images/fundamentos-programacion/function_flow.png
:alt: Flujo de control de la llamada a una función.
:width: 200px
:align: left

Flujo de control da la llamada a una función.
```

Si la función retorna un valor, la expresión de llamada adopta ese valor y puede utilizarse como parte de otra expresión.

::::{hint} Ejemplo de llamada a una función.

Considere la llamada a la [función](#code-es_observacion_valida):

```{code-block}python
:label: code-llamada_a_es_observacion_valida
:linenos: false
:lineno-start: 
:emphasize-lines:
:caption:

aceptada = es_observacion_valida(72)

```

Python evalúa primero el argumento `72`, lo asocia con `valor`, ejecuta el cuerpo y sustituye la expresión de llamada por el valor retornado, `True` [@python314execution]. La asignación almacena después ese valor en la variable `aceptada`.


Se realiza la siguiente llamada a la [segunda función](#code-calcular_promedio) se llama mediante el mismo mecanismo:

```{code-block}python
:label: code-llamada_a_promedio
:linenos: false
:lineno-start: 
:emphasize-lines:
:caption:

promedio = calcular_promedio([80, 60, 100])
```

En este caso, la lista se evalúa como argumento, se asocia con `observaciones_validas` y la expresión de llamada adopta el valor retornado, `80.0`. La asignación a la variable `promedio` conserva este resultado.

::::

## Parámetros y argumentos

Un **parámetro** es un nombre declarado en la definición de una función para representar uno de los datos que esta requiere. Un **argumento** es el valor obtenido al evaluar una expresión incluida en una llamada. Cuando se ejecuta la llamada, los argumentos se asocian con los parámetros correspondientes, cuyos nombres quedan vinculados a esos valores durante la ejecución de la función.

En el [ejemplo](#code-llamada_a_es_observacion_valida), `72` es el argumento, mientras que `valor` es el parámetro (ver [definicion de la función](#code-es_observacion_valida)). Los nombres no deben confundirse aunque una llamada emplee una variable con un nombre coincidente. Por ejemplo,

```{code-block}python
:label: code-llamada_a_promedio
:linenos: true
valor = 72
aceptada = es_observacion_valida(valor)
```

En segundo caso, [`calcular_promedio`](code-calcular_promedio) tiene un parámetro cuyo argumento es una lista. En la [llamada](code-llamada_a_promedio), `[80, 60, 100]` es el argumento y `observaciones_validas` es el parámetro. La [especificación](#tab-cap07-especificacion-promedio) establece que la función utiliza sus elementos, pero indica que se modifica la lista.

En Python, los argumentos pueden asociarse con los parámetros por su posición o mediante el nombre del parámetro. Por ello, una llamada debe respetar la cantidad de argumentos requerida, la forma de asociación y las restricciones establecidas por la especificación de la función. Las expresiones usadas como argumentos se evalúan antes de ejecutar el cuerpo y los valores resultantes se asocian con nombres locales de la función [@python314expressions].

### Asociación por posición

En una llamada con **argumentos posicionales**, la posición de cada argumento determina el parámetro con el que se asocia. Para observar el efecto del orden, considérese una operación auxiliar que calcula la variación entre dos observaciones, recibe dos números y retorna el valor final menos el valor inicial:

```{code-block}python
:label: code-ch7-calcular_variacion
:linenos: true
:emphasize-lines: 6-7

def calcular_variacion(valor_inicial, valor_final):
    """Devuelve la diferencia entre los valores final e inicial."""
    variacion = valor_final - valor_inicial
    return variacion
    
variacion = calcular_variacion(40, 70)
variacion = `calcular_variacion(70, 40)
```

En la llamada (línea 6), `40` se asocia con `valor_inicial` y `70` con `valor_final`. El valor retornado es `30`. 

En la segunda llamada (línea 7) utiliza los mismos valores, pero invierte sus asociaciones y retorna `-30`. Cuando los parámetros representan responsabilidades diferentes, el orden de los argumentos forma parte de la corrección de la llamada.


### Asociación por palabra clave

Python también permite escribir un argumento mediante el nombre del parámetro con el que debe asociarse. En un **argumento por palabra clave** (_keywords_), la asociación se determina por ese nombre y no por la posición escrita [@python314expressions]:

```{code-block}python
:label: code-ch7-llamada_calcular_variacion
:linenos: false
:emphasize-lines: 

variacion = calcular_variacion(valor_final=70, valor_inicial=40)
```

En el [ejemplo](#code-ch7-llamada_calcular_variacion), la llamada retorna nuevamente `30`, aunque `valor_final` aparezca primero. Las llamadas posicionales y por palabra clave utilizan la misma definición de `calcular_variacion`, lo que cambia es la forma de asociar los argumentos con sus parámetros. En ambos casos deben proporcionarse los datos obligatorios y respetarse las restricciones establecidas por la especificación.

### Parámetros con valores predeterminados

Un parámetro puede declarar un valor predeterminado, que se utiliza cuando la llamada no proporciona el argumento correspondiente. En Python, los parámetros obligatorios deben aparecer antes que los parámetros con valores predeterminados [@python314compound].

Por ejemplo, la siguiente función determina si una observación pertenece a un intervalo. `valor` es un parámetro obligatorio, `limite_inferior` y `limite_superior` tienen valores predeterminados:

```{code-block}python
:label: code-ch7-funcion_parametros_predeterminados
:linenos: true
:emphasize-lines: 6-8

def pertenece_al_intervalo(valor, limite_inferior=0, limite_superior=100,):
    """Indica si valor pertenece al intervalo cerrado especificado."""
    pertenece = limite_inferior <= valor <= limite_superior
    return pertenece

resultado = pertenece_al_intervalo(72)
resultado = pertenece_al_intervalo(72, limite_superior=70)
resultado = pertenece_al_intervalo(72, limite_inferior=60, limite_superior=80)
```
En el [ejemplo](#code-ch7-funcion_parametros_predeterminados), 

1. La llamada (línea 6), omite los argumentos correspondientes a los parámetros con valores predeterminados, y retorna `True`. 
2. La llamada (línea 7) sustituye uno de los valores predeterminados mediante un argumento por palabra clave. Como `72` no pertenece al intervalo cerrado de `0` a `70`, la función retorna `False`. 
3. También es posible sustituir ambos valores predeterminados (línea 8). En este caso, la función evalúa si `72` pertenece al intervalo cerrado de `60` a `80` y retorna `True`.

Otras posibilidades en Python, comprende parámetros exclusivamente posicionales, parámetros exclusivamente por palabra clave y mecanismos para recibir cantidades variables de argumentos. Estas formas quedan fuera del alcance del desarrollo actual porque no son necesarias para diseñar las interfaces estudiadas.

## Valores de retorno

El **valor de retorno** es el resultado que una función entrega a la llamada. Calcular un valor, retornarlo y mostrarlo son acciones distintas. Una función puede calcular un resultado intermedio sin retornarlo; puede retornar un valor sin mostrarlo; y una operación de salida puede comunicar un dato sin convertirlo en el valor de la llamada.

La separación resulta decisiva para la composición. Si una función retorna un número, otra expresión puede utilizarlo como argumento, combinarlo con otro valor o almacenarlo. Si la función se limita a mostrar ese número, su representación visual no queda disponible automáticamente para nuevos cálculos.

Las dos funciones ya definidas producen valores de distinta naturaleza. [`es_observacion_valida`](#code-es_observacion_valida) retorna un valor booleano (`bool`) que permite decidir si una observación puede incorporarse al procesamiento. [`calcular_promedio`](#code-calcular_promedio) retorna un valor numérico obtenido a partir de la lista recibida. En esta última función, `suma` y `cantidad` son resultados intermedios de la implementación, mientras que `promedio` contiene el resultado que se entrega a la llamada.

La precondición de [`calcular_promedio`](#tab-cap07-especificacion-promedio) garantiza que la lista no está vacía y, por tanto, que `cantidad` será mayor que cero al finalizar el recorrido. La sentencia `return` termina la ejecución de la función y entrega el valor de su expresión. Si una función termina sin ejecutar una sentencia `return` con una expresión, Python produce el valor `None` [@python314simple]. Este comportamiento del lenguaje no convierte una operación de salida en un retorno.