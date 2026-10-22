---
title: Restricciones y validación
bibliography:
  - referencias.bib
---

Los datos utilizados en una operación deben cumplir las condiciones establecidas en la especificación del problema. Una **restricción** expresa una de estas condiciones y delimita los valores admitidos o las relaciones que deben satisfacer varios datos. La **validación de datos** consiste en comprobar que los datos cumplen los requisitos establecidos antes de utilizarlos en una operación [@owaspValidacion].

El **diseño de una validación** consiste en determinar la representación de cada dato, los valores aceptados, las relaciones exigidas entre ellos y la respuesta prevista ante cada incumplimiento. A partir de estos elementos se establecen las comprobaciones necesarias y el orden en que deben realizarse. Cada comprobación debe responder a una exigencia identificable del problema, de modo que pueda justificarse su función dentro de la solución.

El diseño de una **función de validación** requiere definir los datos parámetros y las restricciones que debe comprobar. La función devuelve un valor lógico que indica si los datos satisfacen dichas restricciones [@downey2024think]. La condición de aceptación debe ser verdadera para los datos válidos. Si la especificación exige varias propiedades simultáneas, se combinan mediante conjunción (operador `AND` en Python), el incumplimiento de una propiedad impide la aceptación.

La construcción de la función de validación podría adoptar las siguientes fases:

1. Identificar los supuestos sobre los datos recibidos.
2. Traducir cada restricción a una comparación u operación.
3. Combinar las condiciones para obtener el resultado lógico.
4. Comprobar el comportamiento de la función.


:::{note} Ejercicio: Validación

El laboratorio de computación desea implementar un sistema de reservas de sus estaciones de trabajo. Como parte de su desarrollo, requiere resolver la captura y validación del horario solicitado para una estación y una fecha previamente seleccionadas. La disponibilidad se extiende entre `08:00` y `18:30,` y se divide en bloques de `15` minutos. Cada reserva debe comenzar al inicio de un bloque y puede abarcar desde `1` a `6` bloques consecutivos.

Los horarios se ingresan en formato `HH:mm`, con dos dígitos para las horas (`00` a `23`) y dos para los minutos (`00` a `59`), sin espacios ni caracteres adicionales. Cada reserva debe quedar íntegramente dentro del horario de atención y su inicio debe preceder al fin.

Diseñe e implemente la captura y validación de ambos horarios. Ante datos no admitidos, informe del motivo y solicite nuevamente el inicio y el fin, hasta obtener una solicitud que cumpla todas las restricciones.

:::

::::{dropdown} Solución
:open: false

**1. Datos y su representación**

- La estación de trabajo y la fecha ya están seleccionadas. 
- La solución debe capturar el inicio y el fin de la solicitud.

| Dato       | Captura                   | Representación numérica        |
|:-----------|:--------------------------|:-------------------------------|
| `inicio`   | `str`: en formato `HH:mm` | `int`: minutos desde las `00:00` |
| `fin`      | `str`: en formato `HH:mm` | `int`: minutos desde las `00:00` |
| `duracion` | -                         | `int`: datos derivado          |
|            |                           |                                |

La siguiente expresión permite convertir la hora a minutos transcurridos desde las `00:00`:

$$ t_{min} = 60h + m. $$

Por ejemplo, las `08:00` horas corresponde a $ 480$ minutos.

**2. Restricciones**

**Entradas.** La cadena debe contener cinco caracteres. El tercero debe ser `:` y los restantes deben pertenecer al conjunto `"0123456789"`.

**Hora.** Las horas deben estar comprendidas entre $ 0$ y $ 23$, y los minutos, entre $ 0$ y $ 59$. Por ejemplo, `"08:75"` cumple el formato, pero no representa una hora válida.

**Reserva.** Para el inicio $i$ y fin $f$, expresados en minutos, deben satisfacer:

- El inicio debe preceder al fin, y ambos horarios deben pertenecer al intervalo de disponibilidad de horarios:
 $$ 480 \leq i < f \leq 1110 $$
   
- Ambos horarios deben coincidir con límites de bloques de 15 minutos:
 $$ i \bmod 15 = 0, \qquad f \bmod 15 = 0 $$
   
- La duración debe respetar los límites establecidos:
$$ 15 \leq f-i \leq 90. $$

  
$a \bmod b$ representa el resto de dividir el entero $a$ entre el entero positivo $b$. Un resto igual a cero indica que $a$ es múltiplo de $b$.

**3. Respuestas**

La solución informa de la primera inconsistencia detectada y solicita nuevamente ambos horarios. El orden de comprobación es: formato, validez de la hora, horario de atención, precedencia del inicio, alineación con los bloques y duración.

| Situación                       | Respuesta                                                         |
|:--------------------------------|:------------------------------------------------------------------|
| Formato incorrecto              | Identificar el dato e informar formato exigido.                   |
| Hora inexistente                | Identificar el dato e informar intervalos permitidos.             |
| Horario fuera de atención       | Informar disponibilidad `08:00` a `18:30`.                        |
| Inicio igual o posterior al fin | Informar que inicio debe preceder al fin.                         |
| Inicio/fin fuera de intervalo   | Informar que hora ingresada no se ajusta a bloque de `15` minutos |
| Duración fuera de límite        | Informar límites de `15` y `90`.                                  |
| Entradas válidas                | Conservar horarios, calcular la duración y terminar la captura.   |
|                                 |                                                                   |

- Cada intento comprende un par `inicio` y `fin`. 
- La finalización depende de que se ingresen entradas válidas.

**4. Descomposición**

Las funciones retornan valores que permiten informar y continuar el flujo de validación de los datos: 

| Función               | Parámetros                | Retorno                                       | Responsabilidad                                                                                                                                                                    |
|:----------------------|:--------------------------|:----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `interpretar_hora()`  | hora: `str`               | `tuple`: minutos(`int`/`None`), motivo(`str`) | Verifica el formato y los intervalos de horas y minutos. Si la entrada es válida, la convierte a minutos con origen en `00:00`, en caso contrario, devuelve el motivo del rechazo. |
| `verificar_reserva()` | inicio: `int`, fin: `int` | motivo: `str`                                 | Verifica las restricciones de la reserva. Devuelve el primer motivo de rechazo o una cadena vacía si se cumplen todas.                                                             |
| `solicitar_horario()` | -                         | `tuple:` minutos(`int`), minutos(`int`)       | Captura horarios, coordina las comprobaciones, informa de los rechazos y repite la solicitud hasta devolver inicio y fin válido en minutos.                                        |
|                       |                           |                                               |                                                                                                                                                                                    |

Casos de prueba:

| Caso                                    |  Inicio |     Fin | Esperado                                |
|:----------------------------------------|--------:|--------:|:----------------------------------------|
| Duración mínima de quince minutos.      | `08:00` | `08:15` | Finaliza y retorna inicio y fin.        |
| Duración máxima y término en el cierre. | `17:00` | `18:30` | Finaliza y retorna inicio y fin.        |
| Formato hora de inicio erróneo.         |  `8:00` | `09:00` | Informa error y solicita nueva entrada. |
| Hora de fin inválida                    | `08:00` | `09:75` | Informa error y solicita nueva entrada. |
| Horario fuera de rango.                 | `07:45` | `08:30` | Informa error y solicita nueva entrada. |
| Orden de horas invertido.               | `10:00` | `09:00` | Informa error y solicita nueva entrada. |
| Elección de bloque inexistente.         | `08:10` | `09:10` | Informa error y solicita nueva entrada. |
| Duración fuera de rango.                | `08:00` | `09:45` | Informa error y solicita nueva entrada. |
|                                         |         |         |                                         |

**5. Implementación**


:::{code-block} python
:linenos: true

def interpretar_hora(hora):
    """Valída una hora y devuelve su equivalente en minutos con origen 00:00.

    Args:
        hora (str): Texto que se desea validar como una hora en formato HH:mm.

    Returns:
        tuple: Minutos y mensaje de rechazo. Si la entrada es válida,
        devuelve los minutos y una cadena vacía. En caso contrario,
        devuelve None y el motivo.
    """
    if len(hora) != 5 or hora[2] != ":":
        return None, "Debe ingresar hora en formato HH:mm."

    for digito in hora[:2] + hora[3:]:
        if digito not in "0123456789":
            return None, "Horas y minutos deben ser dígitos."

    horas = int(hora[:2])
    minutos = int(hora[3:])

    if horas > 23 or minutos > 59:
        return None, "Horas debe estar entre 00-23 y minutos entre 00-59."

    return horas * 60 + minutos, ""


def verificar_reserva(inicio, fin):
    """Verifica el cumplimiento de las restricciones de una reserva.

    Args:
        inicio (int): Inicio en minutos con origen en 00:00.
        fin (int): Fin en minutos con origen en 00:00.

    Returns:
        str: Primer motivo de rechazo detectado o una cadena vacía si la 
        reserva cumple todas las restricciones.
    """
    duracion = fin - inicio

    if not 15 <= duracion <= 90:
        return "La duración debe estar entre 15 y 90 minutos."

    if inicio < 480 or fin > 1110:
        return "El horario disponible es entre las 08:00 y las 18:30."

    if inicio % 15 != 0 or duracion % 15 != 0:
        return "El inicio y el fin deben coincidir con límites de bloques."

    return ""


def solicitar_horario():
    """Solicita hora de inicio y fin obtener una reserva válida.

    Returns:
        tuple[int, int]: Inicio y fin válidos, expresados en minutos con
        origen en 00:00.
    """
    while True:
        texto_inicio = input("Inicio (HH:mm): ")
        texto_fin = input("Fin (HH:mm): ")

        inicio, motivo = validar_hora(texto_inicio)
        if motivo != "":
            print("Inicio:", motivo)
            continue

        fin, motivo = validar_hora(texto_fin)
        if motivo != "":
            print("Fin:", motivo)
            continue

        motivo = motivo_rechazo_reserva(inicio, fin)
        if motivo != "":
            print(motivo)
            continue

        return inicio, fin
:::

::::