# Prueba y verificación

La prueba y la verificación aportan evidencias diferentes sobre un algoritmo. Una **prueba** consiste en ejecutar el algoritmo con entradas seleccionadas y comparar los resultados obtenidos con los establecidos por la especificación. Cada ejecución aporta evidencia sobre una instancia particular, pero superar un conjunto de casos de prueba no garantiza la corrección del algoritmo [@dale2023programming].

La **verificación** examina si el algoritmo produce el resultado especificado para todas las entradas admitidas y si termina. Las ejecuciones manuales y las tablas de seguimiento permiten analizar casos particulares. El razonamiento algebraico permite justificar propiedades generales del procedimiento [@cormen2022algorithms]. La insuficiencia de las pruebas para demostrar la ausencia de defectos fue formulada clásicamente por @dijkstra1969structured.

## Diseño de casos de prueba

Los casos de prueba se derivan del dominio establecido en la especificación y se registran en un plan que incluye valores representativos, valores límite y, cuando existan recorridos diferentes, entradas que permitan examinar cada uno. Los datos no admitidos se registran por separado para revisar la delimitación del dominio; solo forman parte del plan de pruebas si la especificación determina el comportamiento esperado ante ellos [@dale2023programming]. La partición del dominio permite seleccionar estos valores de manera sistemática [@ammann2017software]. Antes de ejecutar el algoritmo, el resultado esperado debe obtenerse mediante un cálculo independiente del procedimiento evaluado.

La selección de datos se rige por criterios complementarios, que pueden coincidir en una misma entrada:

- **Casos representativos:** entradas admitidas seleccionadas para examinar el funcionamiento ordinario del algoritmo.
- **Casos límite:** entradas admitidas situadas en los extremos determinados por las restricciones.
- **Datos no admitidos:** valores que incumplen alguna restricción y sirven para revisar la delimitación del dominio. No constituyen casos de ejecución mientras la especificación no establezca un resultado para ellos.

Una entrada situada en un límite también puede examinar una propiedad particular del resultado. Por esta razón, la selección debe justificarse por el aspecto que permite comprobar y no solo por una etiqueta.

## Ejecución manual y tabla de seguimiento

Una **ejecución manual** (*hand tracing*, *dry run* o *desk checking*) consiste en seleccionar una entrada y recorrer las operaciones de un algoritmo en el orden establecido, a partir de su representación y sin necesidad de implementarlo. Este procedimiento produce una **traza de ejecución**, formada por la secuencia ordenada de las operaciones realizadas y los valores obtenidos. La **tabla de seguimiento** (*trace table* o *hand-trace chart*) organiza esa traza en filas y columnas. Una columna identifica la operación ejecutada, las demás corresponden a los valores de entrada, los resultados intermedios y la salida, y cada fila muestra los valores definidos después de una operación [@gaddis2023programming; @hanly2016problem; @watson2021computer]. El resultado final se compara con el establecido por la especificación. Si ambos difieren, la tabla permite localizar la primera operación a partir de la cual la ejecución se aparta del cálculo esperado.

En una tabla de seguimiento en modalidad detallada, cada operación ejecutada ocupa una fila identificada mediante su número o descripción [@dean2014introduction]. En esta fila solo se registran los valores obtenidos, modificados o producidos por la operación correspondiente. Las demás celdas se dejan vacías. Para determinar el valor vigente de un dato en un paso determinado, se localiza su último registro no vacío en las filas anteriores. La salida se anota en la fila correspondiente a la operación que la produce. Esta disposición permite reconstruir la secuencia de ejecución e identificar la operación que origina cada cambio.

::::{hint} Ejemplo de casos de prueba: precio con descuento. 
:label: ejemplo-traza-descuento

De acuerdo con la [especificación del problema](#ejemplo-especificacion-descuento), los datos para el diseño casos de prueba se derivan de las restricciones $P\geq0$ y $0\leq d\leq100$. En la [](#tab-pruebas-descuento), los casos A-D pertenecen al dominio. El caso A contiene valores interiores representativos, los casos B–D cubren los límites definidos por $P=0$, $d=0$ y $d=100$ y permiten examinar propiedades particulares del resultado. El caso E se incluye únicamente para revisar la restricción sobre $d$.

::: {table} Casos de prueba.
:label: tab-pruebas-descuento
:align: center

| Caso | Tipo                 | $P$ | $d$ | Resultado esperado |
|:-----|:---------------------|:---:|:---:|:------------------:|
| A    | Representativo       | 80  | 25  |         60         |
| B    | Límite               | 80  |  0  |         80         |
| C    | Límite               | 80  | 100 |         0          |
| D    | Límite               |  0  | 25  |         0          |
| E    | Revisión del dominio | 80  | 120 |     no aplica      |

:::

Antes de ejecutar el algoritmo, se determinan los resultados esperados de los casos A–D mediante la [relación entrada-salida](#eq-precio-final-descuento) establecida en la [especificación](#ejemplo-especificacion-descuento). Después se realiza la ejecución manual del [algoritmo diseñado](#ejemplo-diseno-descuento) con las mismas entradas y se registra el resultado obtenido. La prueba es satisfactoria para un caso cuando el resultado obtenido coincide con el esperado. El caso E no pertenece al dominio especificado y, por tanto, no se ejecuta como caso de prueba, ya que la especificación no establece el comportamiento del algoritmo para $d>100$.

La [](#tab-tabla-seguimiento) registra la ejecución manual (tabla de seguimiento) del [caso de prueba A](#tab-pruebas-descuento).

:::{table} Tabla de seguimiento caso A.
:label: tab-tabla-seguimiento

| # | $P$ | $d$ | $D$ | $F$ | Salidas |
|:--|:---:|:---:|:---:|:---:|:-------:|
| 1 | 80  |     |     |     |         |
| 2 |     | 25  |     |     |         |`
| 3 |     |     | 20  |     |         |`
| 4 |     |     |     | 60  |         |
| 5 |     |     |     |     |   60    |
:::

::::

## Diagnóstico y corrección de defectos

Cuando el resultado obtenido difiere del esperado, la tabla de seguimiento permite localizar la primera discrepancia observable de la ejecución. El diagnóstico y la corrección siguen el siguiente procedimiento:

1. registrar los datos de entrada,
2. determinar el resultado esperado a partir de la especificación,
3. ejecutar el algoritmo y registrar los valores obtenidos,
4. localizar en la tabla de seguimiento la primera operación cuyo resultado difiere del esperado,
5. analizar si la discrepancia procede de esa operación o de una relación establecida en una etapa anterior,
6. proponer una modificación y comprobar su correspondencia con la especificación,
7. repetir el caso que reveló el defecto y los demás casos que puedan verse afectados.

La primera discrepancia identifica el punto donde el comportamiento observado comienza a apartarse del previsto, pero no determina por sí sola la causa del defecto. Esta puede encontrarse en la operación señalada, en un resultado intermedio anterior o en el propio diseño del algoritmo. La modificación solo se acepta cuando restablece la correspondencia con la especificación y supera las pruebas pertinentes.

El diseño de caso de pruebas resulta insuficiente si emplea únicamente entradas semejantes, omite los límites del dominio o determina el resultado esperado mediante las mismas operaciones del algoritmo evaluado. Tampoco corresponde ejecutar un caso con datos no admitidos y evaluar su resultado si la especificación no establece el comportamiento requerido para ese dato. La ausencia de discrepancias en los casos ejecutados solo permite concluir que esos casos no revelaron defectos.


::::{hint} Ejemplo de diagnóstico: precio con descuento. 
:label: ejemplo-diagnostico-descuento

Considérese un algoritmo que calcula incorrectamente:

$$D=P\cdot d$$ 

en lugar de,

$$D=P\cdot \frac{d}{100}$$

Para $P=80$ y $d=25$, la especificación establece un precio final de $60$ ([caso A](#tab-pruebas-descuento)). Sin embargo, la ejecución produce la siguiente tabla de seguimiento:

:::{table}

| # | $P$ | $d$ | $D$  |  $F$  | Salidas |
|:--|:---:|:---:|:----:|:-----:|:-------:|
| 1 | 80  |     |      |       |         |
| 2 |     | 25  |      |       |         |`
| 3 |     |     | 2000 |       |         |`
| 4 |     |     |      | -1920 |         |
| 5 |     |     |      |       |  -1920  |
:::

La tabla de seguimiento sitúa la primera discrepancia observable en el cálculo de $D$. La revisión de esa operación permite identificar la omisión de la división por$~100$. Después de corregirla, deben repetirse los casos representativos y límite.

::::