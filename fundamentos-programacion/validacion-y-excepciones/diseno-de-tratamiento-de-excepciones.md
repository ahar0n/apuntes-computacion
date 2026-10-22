---
title: Diseño del tratamiento de excepciones
bibliography:
  - referencias.bib
---

Para diseñar el tratamiento, se debe identificar las operaciones que pueden provocar un fallo, el tipo de excepción esperado y la respuesta requerida. El bloque `try` delimita las operaciones a tratar, evitando incluir instrucciones ajenas al problema previsto. Los cálculos que dependen de una conversión deben realizarse solamente si esta ha terminado correctamente [@severance2024python].

La ubicación del tratamiento depende de la respuesta requerida. Una función puede tratar una excepción cuando dispone de los elementos necesarios para responder. Si la respuesta consiste en solicitar nuevamente los datos o reiniciar un procedimiento, el tratamiento puede situarse en la función que coordina dichas acciones. De esta forma, la función que realiza el cálculo conserva su responsabilidad, mientras quien la llama decide la forma de continuar cuando no se obtiene un resultado.

El tratamiento de excepciones no sustituye la validación de las restricciones de un problema. Por ejemplo, `int("-3")` produce el entero `-3` sin generar una excepción, pero este valor no es una cantidad válida. La conversión verifica si el texto puede interpretarse como entero, una condición posterior podría determinar si el entero obtenido satisface los requisitos.



::::{note} Ejercicio: Tratamiento de excepciones.

El siguiente programa calcula cuánto debe pagar cada persona al dividir por igual la cuenta de un restaurante. Solicita el total de la cuenta en pesos y la cantidad de personas, y muestra el monto individual. La propina ya está incluida en el total.

:::{code-block} python
:linenos: true
:emphasize-lines:

def leer_datos():
    """Solicita el total de la cuenta y la cantidad de personas."""
    total = int(input("Total de la cuenta: "))
    personas = int(input("Cantidad de personas: "))
    return total, personas


def calcular_pago(total, personas):
    """Calcula el valor individual de cada persona."""
    return total / personas


def dividir_la_cuenta():
    """Solicita los datos y muestra el pago individual."""
    while True:
        total, personas = leer_datos()

        if total <= 0:
            print("El total de la cuenta debe ser mayor que cero.")
            continue

        if personas < 0:
            print("La cantidad de personas no puede ser negativa.")
            continue

        pago = calcular_pago(total, personas)
        print(f"Cada persona debe pagar: ${pago:.2f}")
        return


dividir_la_cuenta()
:::

1. Analice el código e identifique las excepciones que pueden producirse. 
2. Genere los casos de prueba que provoquen dichas excepciones e identifique la operación y la función donde se originan. 
3. Incorpore el tratamiento de cada excepción identificada usando la estructura `try–except`, conservando las tres funciones. El programa deberá informar del motivo y solicitar nuevamente los datos. Mantenga las validaciones existentes.

::::

::::{dropdown} Solución
:open: false

**1. Identificación de las excepciones**

El programa puede producir dos tipos de excepción relacionados con los datos ingresados: 
- `ValueError`, cuando un texto no puede convertirse a entero, y 
- `ZeroDivisionError`, cuando se intenta dividir la cuenta entre cero personas.

Notar que, un valor negativo no produce por sí mismo ninguna excepción. Su conversión puede completarse correctamente, pero las condiciones de `dividir_la_cuenta()` lo rechazan por incumplir las restricciones.

**2. Casos de prueba**

Los siguientes datos permiten provocar cada fallo y establecer la respuesta requerida:

| `total`        | `personas`      | Comportamiento actual                              | Comportamiento requerido                                                       |
|:---------------|:----------------|:---------------------------------------------------|:-------------------------------------------------------------------------------|
| `"veinte mil"` | No se solicita. | `ValueError` al convertir el total.                | Informar del error y solicitar nuevamente los datos.                           |
| `"20000"`      | `"tres"`        | `ValueError` al convertir la cantidad de personas. | Informar del error y solicitar nuevamente los datos.                           |
| `"20000"`      | `"2.5"`         | `ValueError` el texto no representa un entero.     | Informar del error y solicitar nuevamente los datos.                           |
| `"20000"`      | `"0"`           | `ZeroDivisionError` al calcular el pago.           | Informar que debe haber al menos una persona y solicitar nuevamente los datos. |
|                |                 |                                                    |                                                                                |

**3. Diseño e implementación del tratamiento**

- El tratamiento se incorpora en `dividir_la_cuenta()`, debido a que esta función coordina los intentos de entrada y puede solicitar nuevamente los datos. 
- Se utilizan dos bloques `try:` uno alrededor de la llamada a `leer_datos()` y otro alrededor de la llamada a `calcular_pago()`. 
- Cada manejador muestra el motivo del rechazo y ejecuta `continue` para comenzar un nuevo intento. 
- Las validaciones existentes permanecen entre ambas operaciones. 
- El resultado se muestra cuando la lectura, las validaciones y el cálculo terminan correctamente.

:::{code-block} python
:linenos: true
:emphasize-lines: 3-5, 17-21

def dividir_la_cuenta():
    while True:
        try:
            total, personas = leer_datos()
        except ValueError:
            print("Total de la cuenta y la cantidad de personas deben ser como números enteros.")
            continue

        if total <= 0:
            print("El total de la cuenta debe ser mayor que cero.")
            continue

        if personas < 0:
            print("La cantidad de personas no puede ser negativa.")
            continue

        try:
            pago = calcular_pago(total, personas)
        except ZeroDivisionError:
            print("La cantidad de personas debe ser mayor que cero.")
            continue

        print(f"Cada persona debe pagar: ${pago:.0f}")
        return


dividir_la_cuenta()
:::

Aunque las excepciones se originan dentro de `leer_datos()` y `calcular_pago()`, en el ejemplo, son tratadas en los bloques que contienen sus llamadas. Si una conversión falla, `leer_datos()` no llega a devolver los datos, si falla la división, `calcular_pago()` no devuelve un resultado. En ambos casos, la sentencia `continue` del manejador evita usar variables no asignadas y reinicia la captura.

::::