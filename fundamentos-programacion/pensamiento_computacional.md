# Pensamiento computacional

## Resolución algorítmica

La resolución algorítmica de un problema comienza con su delimitación y con el diseño de un procedimiento que produzca el resultado especificado. El pensamiento computacional proporciona recursos para analizar el problema, abstraer la información relevante y organizar una solución precisa. Una vez diseñado, el algoritmo debe someterse a pruebas y razonamientos que permitan evaluar su correspondencia con la especificación. Su implementación en un lenguaje de programación constituye una etapa posterior. Este enfoque coincide con las orientaciones propuestas para estudiar los fundamentos algorítmicos con independencia del lenguaje, el paradigma y el hardware utilizados [@kumar2024cs2023].

Un **algoritmo** es un procedimiento finito y preciso que transforma datos de entrada en resultados de salida mediante una secuencia de operaciones aplicable a todas las instancias admitidas del problema. Un **programa**, en cambio, expresa uno o más algoritmos en un lenguaje de programación y permite que un computador los ejecute [@cormen2022algorithms; @kumar2024cs2023].

La resolución se organiza en cuatro etapas:

1. **Análisis y especificación:** delimitar el problema y establecer sus entradas, salidas, restricciones, supuestos y relación entrada-salida.
2. **Diseño y representación:** construir el algoritmo y expresarlo mediante una representación que permita examinar sus operaciones y su correspondencia con la especificación.
3. **Prueba y verificación:** ejecutar el algoritmo con casos seleccionados, comparar los resultados con los esperados y justificar, cuando sea posible, que satisface la especificación para todas las entradas admitidas.
4. **Implementación:** expresar el algoritmo en un lenguaje de programación, manteniendo la correspondencia con el diseño previamente verificado.

## Problemas e instancias

En el diseño de algoritmos, un **problema** establece la relación requerida entre unos datos de entrada y un resultado. Una **instancia** es un caso concreto del problema, determinado por valores de entrada particulares [@cormen2022algorithms]. Por ejemplo, «calcular el área de un rectángulo» es un problema; calcular el área de un rectángulo de lados 7 y 4 es una instancia.

Resolver un problema de forma algorítmica exige formular un procedimiento que pueda aplicarse a todas las instancias admitidas, no solo a un ejemplo particular. El resultado producido para una instancia durante una ejecución es distinto del algoritmo general que lo produce.

## Prácticas de pensamiento computacional

El pensamiento computacional reúne prácticas para formular problemas y diseñar soluciones precisas mediante conceptos fundamentales de la informática, entre los que destacan la descomposición, la abstracción y el diseño de algoritmos [@wing2006computational; @shute2017computational]. Sobre esta base, este libro propone un conjunto articulado de prácticas para organizar el análisis y el diseño de soluciones:

- **Descomposición:** dividir un problema en partes manejables que puedan examinarse por separado.
- **Reconocimiento de patrones:** identificar regularidades, semejanzas y diferencias entre instancias o partes del problema.
- **Abstracción:** seleccionar la información que determina la solución y excluir los detalles irrelevantes.
- **Diseño algorítmico:** organizar las operaciones resultantes en un procedimiento preciso y verificable.

Estas prácticas no constituyen etapas secuenciales, ya que sus resultados pueden exigir la revisión de decisiones adoptadas previamente.

## Razonamiento lógico

El razonamiento lógico permite relacionar afirmaciones, derivar conclusiones y comprobar que estas no contradigan las condiciones de un problema. Una **afirmación** expresa una propiedad que puede evaluarse respecto de los datos disponibles. Una **inferencia** es el razonamiento mediante el cual se obtiene una conclusión a partir de una o más afirmaciones. La **conclusión** es la propiedad resultante. Una inferencia se considera justificada cuando la relación entre las afirmaciones iniciales y la conclusión puede explicarse mediante los datos, las restricciones o una relación matemática explícita [@beall2024logical].

La **consistencia** indica que un conjunto de afirmaciones puede mantenerse sin contradicción. Dos afirmaciones son **incompatibles** cuando no pueden cumplirse simultáneamente. Por ejemplo, si de las condiciones de un problema se concluye que un resultado debe ser no negativo, obtener un valor negativo contradice esa conclusión. La ausencia de contradicciones, sin embargo, no basta para justificar una inferencia. También debe explicarse cómo se deriva la conclusión.

Una **afirmación general** atribuye una propiedad a todas las instancias de un dominio. Un **contraejemplo** es una instancia admitida cuya existencia demuestra que esa afirmación es falsa [@beall2024logical]. Por ejemplo, si se sostiene que «el costo total siempre es mayor que cero», una compra de cero artículos constituye un contraejemplo cuando esa cantidad está permitida. Un solo contraejemplo basta para invalidar una afirmación general, mientras que varios casos favorables no permiten demostrarla. La capacidad de traducir enunciados en relaciones y secuencias es relevante en el aprendizaje de programación [@mayer1992cognitive].

:::{hint} Ejemplo: Aplicación del pensamiento computacional.
:label: ejemplo-pensamiento_computacional

Una actividad cobra un precio fijo por entrada. Se requiere determinar el costo total correspondiente a un grupo.

1. **Descomposición.** El problema se divide en la obtención de la cantidad de entradas, la determinación del precio unitario, el cálculo del costo total y la comunicación del resultado. 
2. **Reconocimiento de patrones.** La relación entre la cantidad de entradas y el costo se mantiene para cualquier grupo, esto es, cada entrada adicional incrementa el total en una cantidad igual al precio unitario. 
3. **Abstracción.** La solución requiere la cantidad de entradas y el precio unitario. Los nombres de las personas, el orden de ingreso y otras características del grupo no modifican el resultado y, por tanto, se excluyen del modelo. 
4. **Diseño del algoritmo.** Relación entrada-salida. Si $n$ representa la cantidad de entradas, $p$ el precio unitario y $C$ el costo total, la relación queda definida por
$$C = n \cdot p$$

A partir de esta relación, el procedimiento debe obtener $n$ y $p$, calcular su producto y comunicar el valor de $C$. El diseño se considera inicial porque todavía deben precisarse las condiciones que determinan las entradas admitidas.

**Razonamiento lógico**

- Inferencia: Si se establece que $n\geq0$ y $p\geq0$, de la relación $C=n\cdot p$ se concluye que $C\geq0$. La conclusión se deriva de las condiciones asignadas a los datos y de la relación que define el resultado.
- Comprobación de consistencia. Un valor $C < 0$ contradice la conclusión anterior y sería incompatible con las condiciones y la relación establecidas. Esta incompatibilidad indicaría un defecto en los datos, en el cálculo o en la formulación del problema.
- Contraejemplo. Si la compra de cero entradas está admitida, la instancia $n=0$ produce $C=0$ y demuestra que la afirmación «el costo total siempre es mayor que cero» es falsa. El contraejemplo no contradice que el costo sea no negativo, pues $C=0$ satisface la condición $C\geq0$.

El análisis aún debe determinar si $n$ puede ser cero, si debe ser un número entero, qué valores de $p$ están admitidos y qué conceptos incluye el precio unitario. La formulación explícita de estas condiciones corresponde a la especificación del problema.
:::

## Errores de análisis

Un análisis es incorrecto si confunde el resultado de una instancia con una solución general, si conserva detalles narrativos que no afectan el resultado o si formula operaciones antes de precisar qué debe calcularse. Un algoritmo tampoco requiere ser implementado y ejecutado automática para ser analizado, puede ejecutarse manualmente durante su análisis.