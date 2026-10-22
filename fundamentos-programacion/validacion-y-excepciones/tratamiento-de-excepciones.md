---
title: Tratamiento de excepciones
bibliography:
  - referencias.bib
---

Durante la ejecución, una operación puede encontrar una situación que impida obtener su resultado. Por ejemplo, un texto puede no representar un número entero o una división puede tener un divisor igual a cero. Python señala estas situaciones mediante excepciones, que interrumpen el recorrido ordinario de las instrucciones. Su tratamiento permite establecer una respuesta y, cuando corresponda, continuar la ejecución [@severance2024python].

Cada excepción tiene un tipo que permite identificar la situación producida. A continuación se presentan tres tipos y operaciones que los generan [@pythonTiposExcepciones]:

| Tipo de excepción   | Situación                                                                            | Ejemplo                                                      |
|:--------------------|:-------------------------------------------------------------------------------------|:-------------------------------------------------------------|
| `ValueError`        | Una operación recibe un argumento de un tipo admitido, pero con un valor inadecuado. | `int("cinco")`: el texto no representa un entero.            |
| `ZeroDivisionError` | Una división o una operación de resto utiliza un divisor igual a cero.               | `20 / 0`: la división no está definida.                      |
| `TypeError`         | Una operación se aplica a un objeto de un tipo inadecuado.                           | `"20" / 4`: la división no admite una cadena como dividendo. |
|                     |                                                                                      |                                                              |

La estructura `try–except` permite establecer una respuesta ante una excepción prevista (ver [](#fig-flujo-try-except)). Primero se ejecuta el bloque `try`. Si termina sin excepción, se omiten los bloques `except`. Si ocurre una excepción, se abandonan las instrucciones pendientes de `try` y se ejecuta el primer **manejador** compatible con su tipo: el bloque `except` que contiene la respuesta correspondiente. Una misma estructura puede incluir varios manejadores [@pythonSentencias].

Cuando el manejador termina de forma normal, el flujo de ejecución continúa inmediatamente después de la estructura, como se muestra en  [](#fig-flujo-try-except)). Si ninguna parte del programa trata la excepción, la ejecución termina e informa del error [@pythonSentencias].

:::{figure} ../../assets/images/fundamentos-programacion/try-except.png
:alt: Diagrama de flujo estructura try-except.
:width: 150px
:align: left
:label: fig-flujo-try-except

Diagrama conceptual del flujo de la estructura `try-except`.
:::


El siguiente ejemplo, el programa estima el tiempo necesario para descargar un archivo de 120 MB a partir de la velocidad de descarga ingresada por el usuario. Si $s$ representa el tamaño del archivo en megabytes y $v > 0$ la velocidad de descarga en megabytes por segundo (MB/s), que se supone constante, el tiempo estimado $t$, expresado en segundos, se calcula mediante:

$$ t = \frac{s}{v} $$

:::{code-block} python
:linenos: true

s = 120
texto = input("Velocidad de descarga (MB/s): ")
t = None

try:
    v = float(texto)
    t = s / v
except ValueError:
    print("La velocidad debe ingresarse como un número.")
except ZeroDivisionError:
    print("No se puede estimar el tiempo con una velocidad igual a cero.")

if t is not None:
    if t > 0:
        print(f"Tiempo estimado: {t:.1f} segundos.")
    else:
        print("La velocidad no puede ser negativa.")
:::

El bloque `try` contiene únicamente la conversión y la división: 
- Si se ingresa `"100,2"` o `"rapido"`, la conversión genera una excepción de tipo `ValueError` y la división no se ejecuta. 
- Si se ingresa `"0"`, la conversión se completa, pero la división genera una excepción de tipo `ZeroDivisionError`. 
- Si se ingresa `"8"`, el tiempo estimado es de 15 segundos. 
- La asignación `t = None` permite identificar que no se obtuvo un resultado cuando alguna operación falló.

La excepción `ZeroDivisionError` puede evitarse comprobando que el divisor sea distinto de cero antes de efectuar la división, por tanto, no siempre es necesario utilizar `try–except` para responder a esta situación. Esta validación rechazaría tanto el cero como las velocidades negativas y haría innecesario el uso del manejador `ZeroDivisionError`.
