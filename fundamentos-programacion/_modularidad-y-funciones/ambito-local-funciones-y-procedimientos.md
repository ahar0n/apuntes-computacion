# Ámbito local, funciones y procedimientos


## Procedimientos y funciones

La distinción entre ambas categorías se establece desde su interfaz observable:

- una función produce un valor que la llamada puede utilizar,
- un procedimiento realiza una operación cuyo resultado principal no se entrega como valor de la llamada.

Esta distinción conceptual debe adaptarse a la terminología del lenguaje. Algunos lenguajes proporcionan construcciones diferenciadas, otros representan ambos comportamientos mediante una sola construcción sintáctica. En este último caso, se denominará **función productiva** (o función de cálculo) a la que devuelve un resultado destinado a usos posteriores y **procedimiento** a la unidad cuyo propósito principal es efectuar una acción.

Python utiliza el mismo constructor `def` para ambos comportamientos. La diferencia se observa en el propósito y en el uso.

:::{hint} Ejemplo de función productiva y procedimiento.
:label: ejemplo-ch7-funcion_vs_procedimiento

Considere el procesamiento que debe clasificar el promedio de las observaciones válidas y presentar un reporte. La clasificación produce un valor que podrá utilizarse posteriormente.

```{code-block}python
:label: code-clasificar_promedio
:linenos: true
:lineno-start: 1
:emphasize-lines: 25-26
:caption:

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

    if cantidad_rechazadas > 0:
        print("Advertencia: se rechazaron observaciones")
    else:
        print("No se rechazaron observaciones")

categoria = clasificar_promedio(76.5)
mostrar_informe(validas=8, rechazadas=2, promedio=76.5, clasificacion=categoria)
```
La función `clasificar_promedio()` asigna la categoría correspondiente a la variable local `clasificacion` y retorna ese valor (línea 25). Luego, `categoria` contiene la cadena `"alta"`, que será usada en la llamada a la función `mostrar_reporte()` (línea 26).

:::

En el [ejemplo](#ejemplo-ch7-funcion_vs_procedimiento), ambas funciones contienen instrucciones, variables y decisiones. La diferencia no depende de la extensión del cuerpo ni de las estructuras de control empleadas. `clasificar_promedio()` es una función productiva porque retorna un valor que la llamada  puede utilizar. `mostrar_reporte()` actúa como procedimiento porque su resultado consiste en mostrar información, al terminar sin un `return` explícito, su llamada devuelve el valor `None` [@python314simple].

Una operación puede diseñarse para retornar un valor o para comunicarlo directamente mediante una salida. Retornar el resultado facilita su composición con otras funciones y su prueba independiente o mostrarlo vincula la operación con un mecanismo específico de salida. La elección depende de la responsabilidad asignada, una función productiva produce un valor para usos posteriores, mientras que un procedimiento realiza principalmente una acción observable.