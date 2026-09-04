---
title: "Variables locales, ámbito, procedimientos y funciones"
bibliography:
  - ../referencias_capitulo_07.bib
---

## Variables locales y ámbito

Una **variable local** es un nombre vinculado dentro del ámbito de una función. Los parámetros y los nombres asignados en el cuerpo son locales, salvo que una declaración del lenguaje establezca otro ámbito. Esta localidad reduce dependencias y permite usar el mismo nombre en funciones diferentes sin que represente necesariamente la misma variable.

El **ámbito** de un nombre es la región del programa en la que puede utilizarse para referirse a una entidad determinada. Python utiliza reglas de ámbito léxico: la resolución de un nombre depende de la estructura del código [@python314execution; @scott2016plp].

En el [código](#cap07-code-funciones-elementales), en la función `es_observacion_valida()`, `valor` y `observacion_valida` son locales. En `calcular_promedio()`, son locales `observaciones_validas`, `suma`, `cantidad`, `valor` y `promedio`. Aunque `valor` aparece en las dos funciones, cada aparición pertenece a un ámbito distinto.

En el [código](#cap07-code-funciones-elementales), la variable local `promedio` contiene el resultado antes de ejecutar `return`. La asignación exterior vincula otro nombre con el valor producido por la llamada (línea 20). Que ambos nombres contengan `80.0` no los convierte en la misma variable.

El ámbito tampoco debe confundirse con la **duración de una ejecución**. Dos llamadas sucesivas establecen ejecuciones independientes de los nombres locales. Por ejemplo, en el [código](#cap07-code-funciones-elementales), después de las llamadas a las funciones pueden utilizarse `valida` y `promedio`, pero el ámbito exterior no puede acceder directamente a `suma` o `cantidad`.

## Procedimientos y funciones

La distinción entre funciones y procedimientos se establece aquí desde su comportamiento observable:

- una **función de cálculo** produce un valor destinado a usos posteriores;
- un **procedimiento** realiza una operación cuyo resultado principal no se entrega como valor de la llamada.

Algunos lenguajes ofrecen construcciones diferentes para ambas categorías. Python representa los dos tipos de comportamientos mediante `def`. La diferencia depende del propósito y del uso, no de una construcción sintáctica distinta [@scott2016plp].

:::{code-block} python
:label: cap07-code-funcion-y-procedimiento
:linenos:

def clasificar_promedio(promedio):
    """Devuelve la categoría correspondiente al promedio."""
    if promedio < 40:
        clasificacion = "baja"
    elif promedio < 70:
        clasificacion = "media"
    else:
        clasificacion = "alta"

    return clasificacion

def mostrar_reporte(validas, rechazadas, promedio, clasificacion):
    """Muestra el informe del procesamiento de observaciones."""
    print("Reporte de observaciones")
    print("Observaciones válidas:", validas)
    print("Observaciones rechazadas:", rechazadas)
    print("Promedio:", promedio)
    print("Clasificación:", clasificacion)

    if rechazadas > 0:
        print("Advertencia: se rechazaron observaciones")
    else:
        print("No se rechazaron observaciones")

categoria = clasificar_promedio(76.5)
mostrar_reporte(
    validas=8,
    rechazadas=2,
    promedio=76.5,
    clasificacion=categoria,
)
:::

En este código:
- `clasificar_promedio()` es una función de cálculo porque retorna una categoría reutilizable. 
- `mostrar_reporte()` actúa como procedimiento porque su propósito principal es producir salida, al terminar sin un `return` explícito, su llamada produce `None`.

