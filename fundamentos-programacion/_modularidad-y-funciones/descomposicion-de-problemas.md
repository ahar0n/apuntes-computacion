# Descomposición de problemas

## Complejidad de una solución monolítica

A medida que aumenta el número de operaciones y de relaciones entre los datos, también se incrementa la dificultad para controlar la complejidad de un programa. La **modularidad** permite abordar este problema mediante la organización de la solución en unidades con responsabilidades delimitadas e interfaces explícitas. La calidad de esta descomposición no depende únicamente del número o del tamaño de las unidades, sino de los criterios empleados para distribuir las responsabilidades y determinar la información que cada una necesita conocer [@parnas1972criteria].

Una solución **monolítica** concentra en una única unidad las operaciones necesarias para resolver el problema. Esta organización no es necesariamente incorrecta en algoritmos pequeños. Sin embargo, cuando una misma secuencia realiza tareas diferentes, resulta más difícil delimitar responsabilidades, reutilizar operaciones y aislar el origen de un resultado defectuoso.

:::{hint} Ejemplo de solución monolítica.
:label: ejemplo-solucion-monolitica

<div id="enunciado-solucion-monolitica">

**Problema**. Un sistema registra una serie de observaciones expresadas mediante números enteros positivos. Debido a errores del sensor durante la observación, algunas observaciones pueden registrarse con valores fuera del rango admisible. Se consideran válidos los valores comprendidos entre 0 y 100, incluidos ambos extremos. Los valores restantes deben excluirse del cálculo y contabilizarse como observaciones rechazadas.

A partir de los datos registrados, se requiere determinar la cantidad de observaciones válidas y rechazadas. Si existe al menos una observación válida, también debe calcularse su promedio.

</div>

La siguiente implementación constituye una posible solución monolítica:

```{code-block} python
:linenos:
:emphasize-lines:
:label: ch7-code-solucion-monolitica

cantidad = int(input("Cantidad de observaciones: "))

validas = 0
rechazadas = 0
suma = 0

for n in range(1, cantidad + 1):
    valor = int(input(f"Observación {n}: "))

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
:::

La [implementación](#ch7-code-solucion-monolitica) satisface el comportamiento requerido para las entradas admitidas, pero reúne en una sola secuencia al menos cinco responsabilidades: leer observaciones, determinar su validez, acumular las aceptadas, calcular el promedio y presentar los resultados. La condición `0 <= valor <= 100` queda incorporada directamente en el recorrido, para verificarla de forma aislada habría que reproducirla fuera del programa. El cálculo del promedio también depende de variables definidas durante la iteración, y la lectura de datos está entrelazada con las decisiones de procesamiento.

Estas características no demuestran que la solución sea incorrecta. Indican que su organización ofrece pocos límites para analizar, verificar y modificar por separado las responsabilidades que la componen.

## Descomposición en tareas

Las funciones proporcionan el primer mecanismo de modularidad. Una **función** asigna un nombre a una operación, declara los datos que necesita y puede devolver un resultado. Esta organización permite utilizar la operación a partir de su especificación sin reproducir sus instrucciones internas en cada uso. La separación entre el comportamiento observable y su realización constituye una forma de abstracción procedimental [@abelson1996sicp].

La modularización no consiste en dividir el código cada cierto número de instrucciones. La descomposición debe realizarse a partir del problema y de su especificación, antes de decidir cómo se implementará cada parte.

La **descomposición de un problema** consiste en separarlo en subproblemas relacionados, cada uno con un propósito y límites definidos. La solución completa se obtiene mediante la composición de los resultados o efectos producidos por esas partes. Por consiguiente, una descomposición adecuada debe satisfacer dos condiciones:

1. cada subproblema puede especificarse de manera individual,
2. la composición de sus soluciones preserva la relación entre las entradas y las salidas establecida en la especificación original.

Cada subproblema representa una responsabilidad diferenciada dentro de la solución. Para delimitarlo, deben establecerse: la tarea que realiza, los datos que requiere, el resultado o efecto que produce y sus relaciones con los demás subproblemas.

Dos indicios de una descomposición deficiente son:

1. **Solapamiento de responsabilidades:** dos subproblemas determinan o calculan un mismo aspecto.
2. **Dependencia innecesaria:** una parte requiere información que no interviene en el cumplimiento de su propósito.

Por lo tanto, la calidad de la descomposición depende de las decisiones sobre las responsabilidades, la información y las relaciones asignadas a cada unidad de la solución [@parnas1972criteria].

Por ejemplo, en la [descripción del problema](#enunciado-solucion-monolitica) pueden distinguirse cinco responsabilidades: leer las observaciones, determinar las observaciones válidas, acumularlas, calcular su promedio y presentar los resultados. Estas responsabilidades se derivan de la especificación del problema, no de la división de una secuencia de instrucciones previamente escrita. Sus relaciones y dependencias pueden representarse mediante un [diagrama de descomposición](ver #).

## Abstracción funcional

La **abstracción funcional** representa una operación mediante su propósito, los datos que requiere y el resultado o efecto que produce, sin exigir que cada uso reproduzca sus detalles internos. Asignar un nombre a una operación compuesta permite tratarla como una unidad conceptual y utilizarla a partir de su comportamiento esperado [@abelson1996sicp].

La abstracción no elimina las operaciones necesarias para obtener el resultado. Estas forman parte de la **implementación**, es decir, del algoritmo y de las instrucciones que realizan la tarea. La separación entre el comportamiento esperado y su implementación permite razonar sobre una operación sin examinar simultáneamente todos sus detalles internos.

Por ejemplo, en el [problema presentado anteriormente](#enunciado-solucion-monolitica), la validación de una observación puede representarse mediante la función `es_observacion_valida(valor)`. Para utilizarla, basta con saber que recibe un valor entero y determina si pertenece al intervalo cerrado de `0` a `100`. La expresión empleada para realizar esta comprobación forma parte de su implementación.

Esta separación permite modificar la forma en que se realiza una operación sin alterar necesariamente las partes de la solución que la utilizan. Por ejemplo, el intervalo de validez podría sustituirse posteriormente por otro criterio de aceptación. Mientras se conserve el comportamiento establecido para la operación, las demás responsabilidades no necesitan reproducir ni conocer los detalles de la comprobación.

La abstracción funcional también contribuye a delimitar responsabilidades. Una operación destinada a determinar la validez de una observación no debe leer datos, acumular valores ni presentar resultados, salvo que alguna de esas acciones forme parte expresa de su propósito. Esta delimitación reduce las dependencias entre las unidades de la solución y permite analizarlas por separado.

## Especificación de una función

La **especificación de una función** describe el comportamiento que debe proporcionar una operación con independencia de la implementación utilizada para realizarla [@liskov1986abstraction]. Para expresar con mayor precisión las restricciones aplicables y las propiedades del resultado pueden emplearse precondiciones y postcondiciones [@hoare1969axiomatic]:

- La **precondición** delimita los casos para los cuales se establece su comportamiento. Una ejecución con datos que no satisfacen estas restricciones queda fuera del dominio especificado, salvo que la propia especificación determine cómo deben tratarse.

- La **postcondición** es la propiedad que debe cumplir el resultado. Expresa la relación entre los datos proporcionados y el resultado obtenido, siempre que la precondición se haya satisfecho.

Algunas funciones producen además acciones perceptibles desde otras partes de la solución, como leer un dato o mostrar información. Estas acciones constituyen **efectos observables** y deben declararse cuando formen parte del comportamiento especificado. Una función que solo calcula y entrega un resultado no tiene los mismos efectos que una operación que muestra ese resultado, aunque ambas intervengan en una misma tarea.

::::{hint} Ejemplo de especificación de funciones.
:label: ejemplo-especificacion-funcion

En el [ejemplo](#enunciado-solucion-monolitica), la operación que determina la validez de una observación puede especificarse de la siguiente manera:

:::{table} Especificación de `es_observacion_valida()`.
:label: tab-cap07-especificacion-validacion
:align: center

| Elemento            | Descripción                                                                                                |
|:--------------------|:-----------------------------------------------------------------------------------------------------------|
| Propósito           | Determinar si una observación pertenece al intervalo válido.                                               |
| Datos requeridos    | Una observación entera.                                                                                    |
| Precondición        | La observación es un número entero.                                                                        |
| Resultado           | Un valor booleano.                                                                                         |
| Postcondición       | El resultado es verdadero exactamente cuando la observación pertenece al intervalo cerrado de `0` a `100`. |
| Efectos observables | Ninguno.                                                                                                   |
:::

Los valores enteros inferiores a `0` o superiores a `100` no incumplen la precondición de esta operación. La función debe aceptarlos y producir `False`, porque su propósito consiste precisamente en decidir si una observación pertenece al intervalo válido. En cambio, un dato que no sea entero queda fuera del dominio establecido por esta especificación.

Una segunda responsabilidad consiste en calcular el promedio de las observaciones que ya han sido aceptadas:

:::{table} Especificación de `calcular_promedio()`
:label: tab-cap07-especificacion-promedio
:align: center

| Elemento            | Descripción                                                                            |
|:--------------------|:---------------------------------------------------------------------------------------|
| Propósito           | Calcular el promedio aritmético de las observaciones válidas.                          |
| Datos requeridos    | Lista de números enteros pertenecientes al intervalo de `0` a `100`.                   |
| Precondición        | La lista contiene al menos un elemento y todos sus valores son observaciones válidas.  |
| Resultado           | Un número que representa el promedio aritmético.                                       |
| Postcondición       | El resultado es igual a la suma de las observaciones validas dividida por su cantidad. |
| Efectos observables | Ninguno.                                                                               |
:::

::::

La especificación y la implementación cumplen funciones diferentes. La primera establece el comportamiento requerido, la segunda contiene las instrucciones que lo realizan. Pueden existir implementaciones distintas de una misma especificación, siempre que todas produzcan el resultado y los efectos establecidos para los datos admitidos. Si la precondición se satisface y el resultado no cumple la postcondición, la implementación no satisface la especificación.