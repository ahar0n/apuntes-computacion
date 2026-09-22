---
title: "Descomposición y abstracción funcional"
bibliography:
  - ../referencias_capitulo_07.bib
---

## Complejidad de una solución monolítica

Una solución monolítica reúne en una sola unidad las operaciones necesarias 
para resolver un problema. En programas de escasa complejidad, esta 
organización puede resultar suficiente. Sin embargo, a medida que aumenta el 
número de operaciones y de relaciones entre los datos, resulta más difícil 
controlar la complejidad del programa. Cuando tareas diferentes permanecen 
concentradas en una misma secuencia, se dificulta analizarlas y modificarlas 
por separado.

(ch7-problema-conductor)=
Considere el siguiente problema. Un sistema registra una serie de observaciones 
representadas mediante números enteros. Debido a errores del sensor, algunas 
pueden contener valores fuera del rango admisible. Se consideran válidas las 
observaciones cuyos valores están comprendidos entre 0 y 100, incluidos ambos 
extremos, las restantes deben excluirse del cálculo y contabilizarse como 
observaciones rechazadas. A partir de los datos registrados, se debe determinar 
la cantidad de observaciones válidas y rechazadas y, si existe al menos una 
observación válida, calcular el promedio de sus valores.

Una implementación posible para resolver el problema, concentra todas las 
operaciones en una secuencia:

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

Esta solución integra en una misma secuencia, la lectura, la validación, la acumulación, el cálculo y la 
presentación. Por ejemplo, la detección de observaciones válidas solo puede 
examinarse dentro del iterador o reproduciendo la condición en otro contexto. 
El cálculo del promedio depende de datos acumulados en esa misma iteración y la 
presentación está ligada inmediatamente al cálculo. La solución monolítica no 
es incorrecta, el problema es que su organización no establece límites 
explícitos entre las tareas.

La modularidad permite abordar esta dificultad mediante una organización de la 
solución en unidades con responsabilidades delimitadas e interfaces explícitas. 
La calidad de la descomposición no depende únicamente del número o del tamaño 
de esas unidades, sino de los criterios empleados para distribuir responsabilidades 
y determinar la información que cada una necesita conocer [@parnas1972criteria; @guttag2021introduction].


## Descomposición en responsabilidades

La **descomposición** identifica subproblemas con propósitos, datos requeridos 
y resultados o efectos delimitados. Su punto de partida es la especificación 
global, y su calidad se examina comprobando que la combinación de las partes 
conserve el comportamiento requerido. La organización de funciones a partir de 
tareas reconocibles es una estrategia de programación introductoria [@guttag2021introduction; @felleisen2018design].

Dos indicios de una descomposición deficiente son el **solapamiento**, cuando 
distintas unidades determinan el mismo aspecto, y la 
**dependencia innecesaria**, cuando una unidad recibe información que no 
interviene en su propósito [@parnas1972criteria].

Por ejemplo, en el [problema](#ch7-problema-conductor) se identifican cinco responsabilidades:

(ch7-ex-descomposicion)=
1. Coordinar el procesamiento
2. Leer cada observación
3. Determinar si la observación es válida
4. Calcular el promedio de las observaciones válidas
5. Presentar el resumen

La acumulación de observaciones válidas es una operación interna de la 
coordinación y no una sexta unidad independiente.

## Abstracción funcional y especificación de funciones

Las funciones constituyen un mecanismo para construir soluciones modulares. 
Permite representar una operación por su propósito, sus datos y su resultado 
o efecto, manteniendo sus instrucciones internas en otro nivel de detalle. 
La **interfaz** indica cómo utilizarla, la **especificación** establece el 
comportamiento que debe cumplir para las entradas admitidas, y la 
**implementación** contiene las instrucciones que lo realizan. Una interfaz 
bien delimitada permite sustituir una implementación por otra que conserve el 
comportamiento especificado [@guttag2021introduction; @downey2024think].

La especificación puede expresar restricciones mediante una **precondición** y 
propiedades exigidas al terminar mediante una **postcondición**. Si una llamada 
satisface la precondición, su resultado y sus efectos observables deben 
satisfacer lo establecido por la postcondición [@hoare1969axiomatic; @liskov1986abstraction; @downey2024think].

Algunas operaciones además pueden producir **efectos observables** desde otras 
partes de la solución, tales como, leer un dato, mostrar información o modificar 
una colección recibida. Estos efectos observables deben declararse como parte 
de la especificación, debido a determinan lo que puede percibir el contexto que 
utiliza la función además de su valor de retorno.

Por ejemplo, la función `es_observacion_valida(valor)` podría representar la 
operación que detecta una observación válida. Para utilizarla es necesario 
saber qué dato recibe y qué resultado produce, la expresión empleada para 
realizar la comprobación pertenece a su implementación. Esta expresión puede 
sustituirse por otra equivalente sin afectar a quienes utilizan la función.

Por ejemplo, a partir de la [descomposición](#ch7-ex-descomposicion), formulada 
es posible especificar dos de sus funciones.

:::{table} Especificación de `es_observacion_valida()`.
:label: cap07-tab-esp-es-observacion-valida
:align: center

| Elemento            | Descripción                                                  |
|:--------------------|:-------------------------------------------------------------|
| Propósito           | Determinar si una observación pertenece al intervalo válido. |
| Datos requeridos    | `valor`: observación entera.                                 |
| Precondición        | `valor` es un número entero.                                 |
| Resultado           | Un valor booleano.                                           |
| Postcondición       | Retorna `True` si y solo si `0 <= valor <= 100`.             |
| Efectos observables | Ninguno.                                                     |
:::

:::{table} Especificación de `calcular_promedio()`.
:label: cap07-tab-esp-calcular-promedio
:align: center

| Elemento            | Descripción                                                                  |
|:--------------------|:-----------------------------------------------------------------------------|
| Propósito           | Calcular el promedio aritmético de las observaciones válidas.                |
| Datos requeridos    | `observaciones_validas`: lista de enteros.                                   |
| Precondición        | La lista no vacía y todos pertenecen al intervalo cerrado `[0, 100]`.        |
| Resultado           | Un número que representa el promedio aritmético.                             |
| Postcondición       | Retorna la suma suma de los elementos dividida por su cantidad.              |
| Efectos observables | Ninguno. La lista recibida no se modifica.                                   |
:::

Ambas funciones tienen dominios diferentes. La primera examina cualquier entero, 
la segunda requiere valores previamente validados y al menos uno de ellos. 
Corresponde a la coordinación satisfacer esa precondición antes de llamar a 
`calcular_promedio()`.

