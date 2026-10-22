---
title: Propagación de excepciones
bibliography:
  - referencias.bib
---

Cuando se produce una **excepción dentro de una función**, si existe un manejador compatible que protege la operación, la excepción se trata allí. En caso contrario, la ejecución de la función se interrumpe y la excepción se transmite al punto donde se realizó la llamada. Este recorrido se denomina **propagación de la excepción** y permite tratarla mediante la estructura `try-except` que contenga la llamada, aunque la operación que falla esté definida en otra función [@pythonSentencias].


En el siguiente ejemplo, la función `leer_notas()` solicita notas y las almacena en una lista:

:::{code-block} python
:linenos:

def leer_notas():
    notas = []

    for n in range(3):
        nota = float(input(f"Nota {n+1}: "))
        notas.append(nota)

    return notas


try:
    notas = leer_notas()
    print(f"Notas ingresadas: {notas}")
except ValueError:
    print("Cada nota debe ingresarse como un número.")

print("Lectura finalizada.")
:::

Si se ingresa `2,1`, la conversión mediante `float()` genera `ValueError` dentro de `leer_notas()`. Debido a que esta función no contiene un manejador, su ejecución se interrumpe sin devolver la lista, aunque ya se hayan leído algunas notas. La excepción se propaga hasta el bloque `try` que contiene la llamada, por lo que la asignación a notas no se completa y se omite el mensaje que mostraría la lista. El manejador informa del problema y, a continuación, se muestra `"Lectura finalizada."`.

Tratar la excepción no reanuda la función interrumpida, tampoco repite una operación. Para realizar otro intento se necesita una nueva llamada. Si tampoco existe un manejador compatible en la llamada, la excepción continúa propagándose por las llamadas anteriores hasta encontrar uno, si ninguno la trata, la ejecución termina e informa del error [@pythonSentencias].
