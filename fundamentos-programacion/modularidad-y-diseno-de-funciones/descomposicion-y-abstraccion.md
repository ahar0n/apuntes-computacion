---
title: "Descomposición y abstracción funcional"
bibliography:
  - ../referencias_capitulo_07.bib
---

## Complejidad de una solución monolítica

Una solución monolítica reúne en una sola unidad las operaciones necesarias para resolver un problema. En programas de escasa complejidad, esta organización puede resultar suficiente. Sin embargo, a medida que aumenta el número de operaciones y de relaciones entre los datos, resulta más difícil controlar la complejidad del programa. Cuando tareas diferentes permanecen concentradas en una misma secuencia, se dificulta analizarlas y modificarlas por separado.

(ch7-problema-conductor)=
Considere el siguiente problema. Un sistema registra una serie de observaciones representadas mediante números enteros. Debido a errores del sensor, algunas pueden contener valores fuera del rango admisible. Se consideran válidas las observaciones cuyos valores están comprendidos entre 0 y 100, incluidos ambos extremos, las restantes deben excluirse del cálculo y contabilizarse como observaciones rechazadas. A partir de los datos registrados, se debe determinar la cantidad de observaciones válidas y rechazadas y, si existe al menos una observación válida, calcular el promedio de sus valores.

La siguiente implementación constituye una posible solución monolítica:

```{code-block} python
:label: cap07-code-solucion-monolitica
:linenos:

cantidad = int(input("Cantidad de observaciones: "))

validas = 0
rechazadas = 0
suma = 0

for posicion in range(1, cantidad + 1):
    valor = int(input(f"Observación {posicion}: "))

    if 0 <= valor <= 100:
        suma += valor
        validas += 1
    else:
        rechazadas += 1

print("Observaciones válidas:", validas)
print("Observaciones rechazadas:", rechazadas)

if validas > 0:
    promedio = suma / validas
    print("Promedio:", promedio)
else:
    print("Promedio no calculado: sin observaciones válidas")
```
En esta solución, la lectura, la validación, la acumulación, el cálculo y la presentación están entrelazados. Por ejemplo, la detección de observaciones válidas solo puede examinarse dentro del iterador o reproduciendo la condición en otro contexto. El cálculo del promedio depende de datos acumulados en esa misma iteración y la presentación está ligada inmediatamente al cálculo. La solución monolítica no es incorrectas, el problema es que su organización no establece límites explícitos entre las tareas.

La modularidad permite abordar esta dificultad mediante una organización de la solución en unidades con responsabilidades delimitadas e interfaces explícitas. La calidad de la descomposición no depende únicamente del número o del tamaño de esas unidades, sino de los criterios empleados para distribuir responsabilidades y determinar la información que cada una necesita conocer [@parnas1972criteria]

## Descomposición en responsabilidades

La **descomposición de un problema** consiste en separarlo en subproblemas relacionados, cada uno con un propósito y límites definidos. La solución completa se obtiene mediante la composición de sus resultados o efectos. De esta forma, cada subproblema debe especificarse individualmente y su composición debe preservar la relación entradas-salidas establecida en el problema original.

La descomposición se deriva del problema y de su especificación, no de divisiones realizadas cada cierto número de instrucciones. Para delimitar una responsabilidad deben establecerse la tarea que realiza, los datos que requiere, el resultado o efecto que produce y sus relaciones con las demás responsabilidades. 

Dos indicios de una descomposición deficiente son el **solapamiento**, cuando distintas unidades determinan el mismo aspecto, y la **dependencia innecesaria**, cuando una unidad recibe información que no interviene en su propósito [@parnas1972criteria].

Por ejemplo, en el [problema](#ch7-problema-conductor) se identifican cinco responsabilidades:

<div id="ch7-ex-descomposicion">

1. Coordinar el procesamiento
2. Leer cada observación
3. Determinar si la observación es válida
4. Calcular el promedio de las observaciones válidas
5. Presentar el resumen

La acumulación de observaciones válidas es una operación interna de la coordinación y no una sexta unidad independiente.

</div>

## Abstracción funcional y especificación de funciones

Las funciones constituyen un mecanismo para construir soluciones modulares. Mediante una abstracción funcional, una operación se representa por su propósito, los datos que requiere y el resultado o efecto que produce, sin que sea necesario reproducir sus instrucciones internas cada vez que se utiliza. Asignar un nombre a esta operación permite tratarla como una unidad conceptual. La separación entre su comportamiento observable y su implementación constituye una forma de abstracción procedimental [@abelson1996sicp].

La **interfaz** reúne la información necesaria para utilizar una función, como su nombre, los datos que requiere y la forma en que produce su resultado o efecto. La **especificación** establece el comportamiento requerido para las entradas admitidas, mientras que la **implementación** contiene el algoritmo y las instrucciones que realizan ese comportamiento. Pueden existir implementaciones diferentes de una misma especificación, siempre que produzcan los resultados y efectos establecidos [@liskov1986abstraction].

Por ejemplo, la función `es_observacion_valida(valor)` podría representar la operación que identifica una observación válida. Para utilizarla es necesario saber qué dato recibe y qué resultado produce; la expresión empleada para realizar la comprobación pertenece a su implementación. Esa expresión puede sustituirse por otra equivalente sin afectar a quienes utilizan la función. Cambiar el intervalo válido de 0 a 100, en cambio, modificaría el comportamiento especificado y no constituiría solamente un cambio de implementación.

La especificación puede expresar las restricciones sobre los datos y las propiedades del resultado mediante una precondición y una postcondición. La **precondición** delimita las llamadas para las cuales se establece el comportamiento de la función. Una llamada cuyos argumentos no satisfacen esas restricciones queda fuera del dominio especificado, salvo que la propia especificación determine cómo tratarla. La **postcondición** establece la propiedad que debe cumplir el resultado cuando se satisface la precondición [@hoare1969axiomatic; @liskov1986abstraction].

Algunas operaciones también producen **efectos observables** desde otras partes de la solución, como leer un dato, mostrar información o modificar una colección recibida. Estos efectos observables deben declararse como parte de la especificación, debido a determinan lo que puede percibir el contexto que utiliza la función además de su valor de retorno.

Por ejemplo, a partir de la [descomposición del problema](#ch7-ex-descomposicion), se pueden especificar dos de sus funciones.

:::{table} Especificación de `es_observacion_valida()`.
:label: cap07-tab-especificacion-validacion
:align: center

| Elemento            | Descripción                                                  |
|:--------------------|:-------------------------------------------------------------|
| Propósito           | Determinar si una observación pertenece al intervalo válido. |
| Datos requeridos    | `valor`: una observación entera.                             |
| Precondición        | `valor` es un número entero.                                 |
| Resultado           | Un valor booleano.                                           |
| Postcondición       | El resultado es `True` para `0 <= valor <= 100`.             |
| Efectos observables | Ninguno.                                                     |
:::

Los enteros inferiores a `0` o superiores a `100` pertenecen al dominio de esta función: debe aceptarlos y retornar `False`. Un argumento no entero queda fuera del dominio establecido.

:::{table} Especificación de `calcular_promedio()`.
:label: cap07-tab-especificacion-promedio
:align: center

| Elemento            | Descripción                                                                |
|:--------------------|:---------------------------------------------------------------------------|
| Propósito           | Calcular el promedio aritmético de las observaciones válidas.              |
| Datos requeridos    | `observaciones_validas`: lista de enteros del intervalo de `0` a `100`.    |
| Precondición        | La lista contiene al menos un elemento y todos sus valores son válidos.    |
| Resultado           | Un número que representa el promedio aritmético.                           |
| Postcondición       | El resultado equivale a la suma de los elementos dividida por su cantidad. |
| Efectos observables | Ninguno. La lista recibida no se modifica.                                 |
:::

Ambas funciones poseen dominios distintos porque cumplen responsabilidades diferentes. La validación examina cualquier entero, el promedio opéra únicamente sobre una colección no vacía de observaciones ya validadas.

