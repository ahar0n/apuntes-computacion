# Análisis y especificación

## Elementos de la especificación

Una **especificación** define las condiciones que deben satisfacer los datos de entrada y los resultados esperados, independiente del procedimiento utilizado para obtenerlos. Esta separación entre condiciones iniciales y propiedades finales se fundamenta en el método axiomático de @hoare1969axiomatic. La especificación se estructura mediante los siguientes elementos:

1. **Entradas:** datos que recibe el algoritmo.
2. **Salidas:** resultados que debe producir.
3. **Restricciones:** condiciones que limitan los datos admitidos o la solución.
4. **Supuestos:** condiciones aceptadas como válidas para acotar el problema.
5. **Relación entrada-salida:** propiedad que debe cumplir el resultado.

Posteriormente, estas ideas podrán formalizarse mediante **precondiciones**, que describen las condiciones previas a la ejecución, y **poscondiciones**, que expresan las propiedades requeridas al finalizar.

El análisis comienza al delimitar el resultado requerido. Después se identifican los datos de entrada, se establecen sus restricciones y se declaran los supuestos que acotan el problema. Con estos elementos se formula la relación matemática o lógica que debe existir entre las entradas y la salida. El procedimiento concluye al comprobar que la especificación permite determinar el resultado esperado para cualquier instancia admitida sin depender de decisiones de implementación.

:::{hint} Ejemplo: Análisis y especificación del problema
:label: ejemplo-analisis_especificacion

Calcular el valor que debe pagar una persona por un producto al que se aplica un descuento porcentual.

1. **Entradas:** precio inicial $P$ y porcentaje de descuento $d$.
2. **Salida:** precio final $F$.
3. **Restricciones:** $P \geq 0$ y $0 \leq d \leq 100$.
4. **Supuesto:** no se consideran impuestos adicionales ni reglas de redondeo monetario.
5. **Relación entrada-salida:** el precio final es el precio inicial menos el importe descontado. Puede expresarse directamente como

```{math}
:label: eq-precio-final-descuento
F = P\left(1-\frac{d}{100}\right)
```

La especificación incluye los casos $d=0$, $d=100$ y $P=0$. Estos valores permiten comprobar que la relación está definida en los extremos del dominio.
:::

## Ambiguedades del problema

Durante el análisis y la especificación del problema debe comprobarse que el enunciado contenga la información necesaria para definir el problema sin ambigüedades. Por ejemplo, la instrucción «calcular el promedio de notas» es insuficiente si no especifica cuántas notas intervienen, qué valores admiten, si todas tienen la misma ponderación y qué resultado corresponde cuando no existen notas.

## Errores de especificación

La especificación pierde precisión cuando confunde un dato con una operación, define una salida sin establecer la propiedad que debe cumplir o incorpora detalles de un lenguaje de programación. También es incorrecto resolver una ambigüedad mediante un supuesto no declarado o excluir datos inválidos solo porque los primeros casos contienen valores admisibles.