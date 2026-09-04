# Implementación y llamada de funciones

## Definición y llamada de funciones

La definición de una función introduce en el programa una operación identificada por un nombre. Consta de dos partes principales:

- el **encabezado**, que declara el nombre de la función y sus parámetros; 
- el **cuerpo**, que contiene las instrucciones mediante las cuales se implementa la operación.

La definición debe corresponder con la especificación de la función. El nombre identifica la operación, los parámetros representan los datos que esta requiere, las instrucciones implementan el comportamiento especificado, y, cuando corresponde, el retorno proporciona un resultado al contexto que utiliza la función.

En Python, una función se define mediante la sentencia def [@python314compound]. Su forma general es la siguiente:

```{code-block}python
:label: ch7-code-funcion-forma_general
:linenos: true
:lineno-start: 1
:emphasize-lines: 6
:caption:

def nombre_funcion(parametros):
    """Descripción de la función."""
    # instrucciones
    return resultado

nombre_funcion(argumentos)
```
En esta estructura:

- la palabra clave `def` señala el comienzo de la definición,
- `nombre_funcion` es un identificador válido [@python314lexical],
- la lista situada entre paréntesis declara los parámetros y puede estar vacía,
- los dos puntos (`:`) señala el final del encabezado,
- el cuerpo forma un bloque con indentación respecto del encabezado,
- una cadena literal situada como primera instrucción del cuerpo constituye la cadena de documentación (_docstring_) y permite describir el propósito de la función [@pep257];
- la sentencia `return` termina la ejecución de la función y, si incluye una expresión, proporciona su valor al contexto que realizó la llamada. Una sentencia `return` sin expresión y la terminación del cuerpo sin ejecutar un `return` producen el valor `None` [@python314simple].

Definir una función no provoca la ejecución inmediata de su cuerpo. Para ejecutarla se debe realizar una **llamada**, formada por el nombre de la función seguido de los argumentos escritos entre paréntesis (ver [forma general](#ch7-code-funcion-forma_general) línea 6).

:::{figure} ../../assets/images/fundamentos-programacion/function_flow.png
:alt: Flujo de control de la llamada a una función.
:width: 210px
:align: left
:label: ch7-figure-fx-flujo_de_control_llamada

Flujo de control da la llamada a una función.
:::

Mientras la definición describe una operación general, cada llamada inicia una ejecución particular como se muestra en [](#ch7-figure-fx-flujo_de_control_llamada). Primero se evalúan los argumentos y sus valores se asocian con los parámetros correspondientes. A continuación, el control se transfiere al cuerpo de la función. Cuando la ejecución termina, el control regresa al punto de llamada y, si se produjo un valor de retorno, la expresión de llamada adopta ese valor [@python314expressions; @python314execution].

::::{hint} Ejemplo de implementación de funciones.
:label: ch7-ejemplo-funciones-implementacion

```{code-block}python
:label: ch7-code-ex-implementacion
:linenos: true
:lineno-start: 1
:emphasize-lines: 18, 19
:caption:

def es_observacion_valida(valor):
    """Indica si valor pertenece al intervalo cerrado [0, 100]."""
    observacion_valida = 0 <= valor <= 100
    return observacion_valida

def calcular_promedio(observaciones_validas):
    """Devuelve el promedio de las observaciones válidas."""
    suma = 0
    cantidad = 0

    for valor in observaciones_validas:
        suma = suma + valor
        cantidad = cantidad + 1

    promedio = suma / cantidad
    return promedio

aceptada = es_observacion_valida(72)
promedio = calcular_promedio([80, 60, 100])
```

- La línea 1 muestra el encabezado de la función `es_observacion_valida()`, se identifica su nombre y declara su parámetro tal como establece los datos requeridos de su  [especificación](#tab-cap07-especificacion-validacion). La expresión relacional implementa la condición indicada en la postcondición y `return` entrega un valor booleano. La cadena de documentación resume su propósito.

- La línea 6 muestra el encabezado de la función `calcular_promedio()` que, de acuerdo con su  [especificación](#tab-cap07-especificacion-promedio), tiene como parámetro las observaciones válidas en forma de una lista de números enteros. En su cuerpo, realiza el recorrido necesario para obtener la suma y la cantidad de observaciones. Las variables `suma`, `cantidad` y `promedio` permiten implementar la relación establecida por la postcondición.

- En la llamada a la función `es_observacion_valida(valor)` (línea 18), Python evalúa primero el argumento `72`, lo asocia con `valor`, ejecuta el cuerpo y sustituye la expresión de llamada por el valor retornado, `True`. Mediante la operación asignación este valor es almacenado en la variable `aceptada`.

- Utilizando el mismo mecanismo, en la línea 19, la lista se evalúa como argumento de la función, se asocia con `observaciones_validas` y la expresión de llamada adopta el valor retornado, `80.0`. La asignación a la variable `promedio` conserva este resultado.

::::

## Parámetros y argumentos

Un **parámetro** es un nombre declarado en la definición de una función para representar uno de los datos que esta requiere. Un **argumento** es el valor obtenido al evaluar una expresión incluida en una llamada. Cuando se ejecuta la llamada, los argumentos se asocian con los parámetros correspondientes, cuyos nombres quedan vinculados a esos valores durante la ejecución de la función.

En la línea 18 del [ejemplo](ch7-code-ex-implementacion), `72` es el argumento, mientras que `valor` es el parámetro de la función. Los nombres no deben confundirse aunque una llamada emplee una variable con un nombre coincidente.

En Python, los argumentos pueden asociarse con los parámetros por su posición o mediante el nombre del parámetro. Por ello, una llamada debe respetar la cantidad de argumentos requerida, la forma de asociación y las restricciones establecidas por la especificación de la función. Las expresiones usadas como argumentos se evalúan antes de ejecutar el cuerpo y los valores resultantes se asocian con nombres locales de la función [@python314expressions].

### Asociación por posición

En una llamada con **argumentos posicionales**, la posición de cada argumento determina el parámetro con el que se asocia. Para observar el efecto del orden, considérese una operación auxiliar que calcula la variación entre dos observaciones, recibe dos números y retorna el valor final menos el valor inicial:

```{code-block}python
:label: ch7-code-calcular_variacion
:linenos: true
:emphasize-lines: 6-7

def calcular_variacion(valor_inicial, valor_final):
    """Devuelve la diferencia entre los valores final e inicial."""
    variacion = valor_final - valor_inicial
    return variacion
    
variacion = calcular_variacion(40, 70)
variacion = calcular_variacion(70, 40)
variacion = calcular_variacion(valor_final=70, valor_inicial=40)
```
En el ejemplo, 
- En la llamada (línea 6), `40` se asocia con `valor_inicial` y `70` con `valor_final`. El valor retornado es `30`. 
- En la segunda llamada (línea 7) utiliza los mismos valores, pero invierte sus asociaciones y retorna `-30`. Cuando los parámetros representan responsabilidades diferentes, el orden de los argumentos forma parte de la corrección de la llamada.


### Asociación por palabra clave

Python también permite escribir un argumento mediante el nombre del parámetro con el que debe asociarse. En un **argumento por palabra clave** (_keywords_), la asociación se determina por ese nombre y no por la posición escrita [@python314expressions]:

En la [línea 8 del ejemplo](#ch7-code-calcular_variacion), la llamada retorna nuevamente `30`, aunque `valor_final` aparezca primero. Las llamadas posicionales y por palabra clave utilizan la misma definición de la función, lo que cambia es la forma de asociar los argumentos con sus parámetros. En ambos casos deben proporcionarse los datos obligatorios y respetarse las restricciones establecidas por la especificación.

### Parámetros con valores predeterminados

Un parámetro puede declarar un **valor predeterminado**, que se utiliza cuando la llamada no proporciona el argumento correspondiente. En Python, los parámetros obligatorios deben aparecer antes que los parámetros con valores predeterminados [@python314compound].

Por ejemplo, la siguiente implementación, la función determina si una observación pertenece a un intervalo. `valor` es un parámetro obligatorio, `limite_inferior` y `limite_superior` tienen valores predeterminados:

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

- La llamada (línea 6), omite los argumentos correspondientes a los parámetros con valores predeterminados, y retorna `True`. 
- La llamada (línea 7) sustituye uno de los valores predeterminados mediante un argumento por palabra clave. Como `72` no pertenece al intervalo cerrado de `0` a `70`, la función retorna `False`. 
- También es posible sustituir ambos valores predeterminados (línea 8). En este caso, la función evalúa si `72` pertenece al intervalo cerrado de `60` a `80` y retorna `True`.

Otras posibilidades en Python, comprende parámetros exclusivamente posicionales, parámetros exclusivamente por palabra clave y mecanismos para recibir cantidades variables de argumentos. Estas formas quedan fuera del alcance del desarrollo actual porque no son necesarias para diseñar las interfaces estudiadas.

## Valores de retorno

El **valor de retorno** es el valor que una función proporciona al contexto desde el cual fue llamada. En Python, la ejecución de una sentencia return termina la función y, cuando la sentencia incluye una expresión, la expresión de llamada adopta el valor resultante de evaluarla [@python314simple; @python314expressions].

El valor retornado puede almacenarse en una variable, intervenir en una expresión o utilizarse como argumento de otra llamada. Esta posibilidad permite componer funciones, pues el resultado producido por una de ellas puede constituir un dato de entrada para otra. Si la función termina sin ejecutar una sentencia `return` con una expresión, la llamada produce el valor `None`.

Las dos funciones definidas en el [ejemplo](ch7-code-ex-implementacion) producen valores de distinta naturaleza. `es_observacion_valida()` retorna un valor booleano que permite decidir si una observación puede incorporarse al procesamiento. `calcular_promedio()` retorna un valor numérico obtenido a partir de la lista recibida. En esta última, `suma` y `cantidad` son resultados intermedios de la implementación, mientras que `promedio` contiene el resultado que se entrega a la llamada.

La precondición en la [especificación](#tab-cap07-especificacion-promedio) garantiza que la lista no está vacía y, por tanto, que la variable `cantidad` en la [implementación](#ch7-code-ex-implementacion) será mayor que cero al finalizar el recorrido. La sentencia `return` termina la ejecución de la función y entrega el valor de su expresión.

## Variables locales y ámbito

Una **variable local** es un nombre vinculado a un valor dentro del **ámbito** de una función. Los parámetros y los nombres asignados en su cuerpo son locales a esa función, salvo que una declaración del lenguaje establezca otro ámbito. Esta localidad reduce las dependencias con otras partes del programa y permite emplear un mismo nombre en funciones diferentes sin que represente necesariamente la misma variable.

El **ámbito** de un nombre es la región del programa en la que ese nombre puede utilizarse para referirse a una entidad determinada. En un sistema de ámbito léxico, esta región se determina a partir de la estructura del código y del bloque en el que se establece la vinculación.

Python emplea reglas de ámbito léxico para resolver nombres en ámbitos locales, no locales, globales e incorporados [@python314execution]. El tratamiento inicial se limita a los parámetros y las variables locales, con el propósito de determinar qué nombres pueden utilizarse dentro y fuera del cuerpo de una función.

En el [ejemplo](#ch7-code-ex-implementacion),

- Cada función establece su propio ámbito local. En `es_observacion_valida()`, el parámetro `valor` y la variable `observacion_valida` son nombres locales. En `calcular_promedio()`, son locales el parámetro `observaciones_validas` y las variables `suma`, `cantidad`, `valor` y `promedio`.
- `valor` aparece en ambas funciones, pero corresponde a variables diferentes porque cada aparición pertenece a un ámbito local distinto. La ejecución de una función no modifica la variable local homónima de la otra. 
- También existen dos variables llamadas `promedio`, una es local a `calcular_promedio()` y la otra pertenece al ámbito desde el cual se realiza la llamada. La sentencia `return` proporciona el valor de la primera, y la asignación exterior vincula la segunda con ese valor. Aunque ambas contienen `80.0` durante esta ejecución, no representan la misma variable.

Después de finalizar las llamadas, el ámbito exterior puede utilizar aceptada y promedio, pero no puede acceder directamente a nombres locales como observacion_valida, suma o cantidad. Por ejemplo, print(suma) produciría un error porque suma no está definido en ese ámbito.
