---
title: "Implementación y llamada de funciones"
bibliography:
  - ../referencias_capitulo_07.bib
---

## Definición de una función

La definición de una función introduce en el programa una operación identificada por un nombre. Consta de un **encabezado**, que declara el nombre y los parámetros, y un **cuerpo**, que contiene las instrucciones que implementan la operación. La definición debe corresponder con la especificación: el nombre identifica la operación, los parámetros representan los datos requeridos y, cuando corresponde, el retorno proporciona el resultado.

En Python, una función se define mediante la sentencia `def` [@python314compound]. Su forma general es la siguiente:

```{code-block} python
:label: cap07-code-forma-general-funcion
:linenos:

def nombre_funcion(parametros):
    """Descripción de la función."""
    instrucciones

nombre_funcion(argumentos)
```

- La palabra clave `def` señala el comienzo de la definición
- `nombre_funcion` es un identificador válido [@python314lexical].
- La lista situada entre paréntesis declara los parámetros y puede estar vacía.
- Los dos puntos (`:`) señala el final del encabezado.
- El cuerpo forma un bloque con indentación respecto del encabezado.
- Una cadena literal situada como primera instrucción del cuerpo constituye la cadena de documentación (_docstring_) y permite describir el propósito de la función [@pep257], pero no sustituye su especificación.
- Una sentencia `return` terminaría la ejecución de la función y, si incluye una expresión, proporciona su valor al contexto que realizó la llamada. Una sentencia `return` sin expresión y la terminación del cuerpo sin ejecutar un `return` producen el valor `None` [@python314simple].

Los nombres de las funciones y variables de los ejemplos siguen la convención de minúsculas con palabras separadas mediante guiones bajos [@pep8].

Las especificaciones previas para las funciones [`es_observacion_valida()`](#cap07-tab-especificacion-validacion) y [`calcular_promedio()`](#cap07-tab-especificacion-promedio) admiten las siguientes implementaciones, respectivamente:

:::{code-block} python
:label: cap07-code-funciones-elementales
:linenos:

def es_observacion_valida(valor):
    """Indica si valor pertenece al intervalo cerrado [0, 100]."""
    observacion_valida = 0 <= valor <= 100
    return observacion_valida


def calcular_promedio(observaciones_validas):
    """Devuelve el promedio de una lista no vacía de observaciones válidas."""
    suma = 0
    cantidad = 0

    for valor in observaciones_validas:
        suma += valor
        cantidad += 1

    promedio = suma / cantidad
    return promedio

valida = es_observacion_valida(72)
promedio = calcular_promedio([80, 60, 100])
:::

En la primera función, la expresión relacional implementa la postcondición de la validación. En la segunda, el recorrido calcula la suma y la cantidad requeridas por la postcondición del promedio. La división es válida porque la precondición exige una lista no vacía.

## Llamada y transferencia del control

Definir una función no ejecuta inmediatamente su cuerpo. Una **llamada** solicita su ejecución mediante el nombre de la función y los argumentos escritos entre paréntesis. Primero se evalúan las expresiones empleadas como argumentos y sus valores se asocian con los parámetros (líneas [19](#cap07-code-funciones-elementales) y [20](#cap07-code-funciones-elementales)). Después, el control se transfiere al cuerpo ([](#ch7-figure-fx-flujo_de_control_llamada)). Cuando la ejecución termina, el control regresa al punto de llamada y, si existe un retorno, la expresión adopta ese valor [@python314expressions; @python314execution].

:::{figure} ../../assets/images/fundamentos-programacion/function_flow.png
:alt: Flujo de control de la llamada a una función.
:width: 220px
:align: left
:label: ch7-figure-fx-flujo_de_control_llamada

Flujo de control da la llamada a una función.
:::

En la [implementación](#cap07-code-funciones-elementales), la primera llamada produce `True`, la segunda produce `80.0`. Las asignaciones conservan esos resultados en el ámbito desde el cual se efectuaron las llamadas.

## Parámetros y argumentos

Un **parámetro** es un nombre declarado en la definición para representar uno de los datos requeridos. Un **argumento** es el valor obtenido al evaluar una expresión incluida en una llamada. En `es_observacion_valida(72)`, `valor` es el parámetro y `72` es el argumento.

En una llamada con **argumentos posicionales**, la posición determina la asociación con los parámetros:

:::{code-block} python
:label: cap07-code-parametros-posicionales
:linenos:

def calcular_variacion(valor_inicial, valor_final):
    """Devuelve el valor final menos el inicial."""
    variacion = valor_final - valor_inicial
    return variacion

aumento = calcular_variacion(40, 70)
variacion = calcular_variacion(70, 40)
aumento = calcular_variacion(valor_final=70, valor_inicial=40)
:::

En este ejemplo, 
- En la llamada (línea 6), `40` se asocia con `valor_inicial` y `70` con `valor_final`. El valor retornado es `30`. 
- En la segunda llamada (línea 7) utiliza los mismos valores, pero invierte sus asociaciones y retorna `-30`. Cuando los parámetros representan responsabilidades diferentes, el orden de los argumentos forma parte de la corrección de la llamada.

Python también admite **argumentos por palabra clave**, cuya asociación se determina mediante el nombre del parámetro. La tercera llamada (línea [8](#cap07-code-parametros-posicionales)) retorna `30`, aunque `valor_final` aparezca primero [@python314expressions]:

Un parámetro puede declarar un **valor predeterminado**, utilizado cuando la llamada omite el argumento correspondiente. Los parámetros obligatorios deben aparecer antes que aquellos que poseen valores predeterminados [@python314compound].

:::{code-block} python
:label: cap07-code-fx-pertenece
:linenos:

def pertenece_al_intervalo(valor, limite_inferior=0, limite_superior=100):
    """Indica si valor pertenece al intervalo cerrado especificado."""
    pertenece = limite_inferior <= valor <= limite_superior
    return pertenece

resultado_1 = pertenece_al_intervalo(72)
resultado_2 = pertenece_al_intervalo(72, limite_superior=70)
resultado_3 = pertenece_al_intervalo(72, limite_inferior=60, limite_superior=80)
:::

En este código,
- La llamada (línea 6), omite los argumentos correspondientes a los parámetros con valores predeterminados, y retorna `True`. 
- La llamada (línea 7) sustituye uno de los valores predeterminados mediante un argumento por palabra clave. Como `72` no pertenece al intervalo cerrado de `0` a `70`, la función retorna `False`. 
- También es posible sustituir ambos valores predeterminados (línea 8). En este caso, la función evalúa si `72` pertenece al intervalo cerrado de `60` a `80` y retorna `True`.

Otras alternativas en Python, comprende parámetros exclusivamente posicionales, parámetros exclusivamente por palabra clave y mecanismos para recibir cantidades variables de argumentos. Estas formas quedan fuera del alcance del desarrollo actual porque no son necesarias para diseñar las interfaces estudiadas.

## Valores de retorno

El **valor de retorno** es el valor que una función proporciona al contexto desde el cual fue llamada. La sentencia `return` termina la ejecución de la función y, cuando contiene una expresión, la llamada adopta el valor resultante. Una sentencia `return` sin expresión y la terminación del cuerpo sin ejecutar un `return` producen `None` [@python314simple; @python314expressions].

Un valor retornado puede almacenarse en una variable, intervenir en una expresión o utilizarse como argumento de otra llamada. Esta propiedad permite componer expresiones:

```python
print(calcular_promedio([80, 60, 100]))
```

En esta expresión, el valor producido por `calcular_promedio()` se convierte en argumento de `print()`. Retornar un valor no equivale a mostrarlo: `return` entrega un dato al contexto llamador, mientras que `print()` produce un efecto de salida y su propio valor de retorno es `None`.

## Vinculación de parámetros y objetos mutables

Durante una llamada, los parámetros se vinculan con los objetos obtenidos al evaluar los argumentos. Python no crea automáticamente una copia independiente de cada objeto [@python314execution]. Si una función modifica un objeto mutable mediante un parámetro, el cambio puede observarse después de la llamada:

```python
def registrar_observacion(observaciones, valor):
    """Agrega valor a la lista observaciones."""
    observaciones.append(valor)

datos = [80, 60]
registrar_observacion(datos, 100)
print(datos)
```
La ejecución dl código fuente anterior, generará la salida `[80, 60, 100]`.

La modificación de la lista constituye un efecto observable y debe declararse en la especificación.
