# Conceptos básicos

### 1. Observaciones, eventos y estados

Una base de datos permite representar entidades, sus propiedades y las relaciones que mantienen. Sin embargo, muchas de esas propiedades cambian: una estación deja de funcionar, un dispositivo se reemplaza, una instalación cambia de responsable o una unidad territorial modifica sus límites. Cuando estas transformaciones son relevantes para las preguntas que debe responder el sistema, conservar únicamente el último valor resulta insuficiente.

Considére una estación que registra el nivel de agua estático de un pozo. Una lectura de 104 centímetros tiene un significado incompleto si se desconoce cuándo fue obtenida. Su interpretación también puede depender del estado de la estación en ese momento. Si estaba declarada inactiva, la lectura requiere revisión, si estaba operativa, podría incorporarse al análisis bajo las condiciones de calidad establecidas. El estado actual de la estación no permite resolver esa pregunta histórica.

El problema tiene dos componentes. Por una parte, se necesita conservar una secuencia de observaciones. Por otra, es necesario representar las condiciones que tenían vigencia cuando se produjeron. El modelo deberá permitir relacionar cada lectura con el estado correspondiente a su instante de observación.

El diseño debe definir el significado de cada marca temporal. Una columna llamada fecha puede referirse a medición, recepción, inicio de vigencia o corrección. Esa diferencia determina las filas que debe seleccionar una consulta y la información que debe conservar una actualización.

Una **observación** registra un valor asociado a un fenómeno, una entidad y un tiempo. En el caso del pozo, la entidad es una estación, la variable es el nivel de agua y la unidad es el centímetro. Una fila puede expresar que la estación E01 registró un nivel de 100 cm a las 08:00.

Para este modelo, la obtención de una lectura se representa como un **evento** asociado a un instante. Esta elección no implica que el proceso físico de medición sea instantáneo. Significa que basta atribuir el valor a una marca temporal. Si el dato correspondiera al promedio de una hora o a la acumulación durante un día, sería necesario identificar el período de observación y el significado de la agregación.

Un **estado** tiene otra función. La afirmación «la estación estuvo inactiva entre las 10:00 y las 12:00» describe una condición que se considera válida durante un período. Mientras una tabla de lecturas acumula observaciones, una tabla de estados conserva tramos de vigencia.

### 2. Instante, período y duración

Un **instante** identifica una posición temporal. Un **período** delimita una porción de la línea de tiempo, una **duración** expresa su extensión. Estas distinciones son fundamentales en el tratamiento de información temporal (Snodgrass, 2000, caps. 3–4).

Por ejemplo, el valor `2026-10-19 10:00:00` identifica un instante, entre `10:00` y `12:00` del mismo día delimita un período, y 2 horas expresa una duración. La duración, por sí sola, no permite identificar el momento en que ocurrió una inactividad.

La **granularidad temporal** establece el nivel de detalle con que se representa el tiempo. Almacenar horas, minutos y segundos permite distinguir posiciones con una resolución diferente de la que ofrece una fecha. La **frecuencia de observación** indica cada cuánto se espera una medición. Por ejemplo, una estación puede producir un registro por hora y almacenar su instante con resolución de segundos.

Suponga que un esquema contiene `estacion(estacion_id, nombre, estado)`, esta tabla permite representar un estado por estación. Al actualizar `estado`, se conserva el nuevo valor y deja de representar el anterior. Ese diseño es suficiente si solo se requiere mantener un registro del estado actual. Cuando se necesita explicar una observación histórica, deben conocerse los períodos durante los que cada estado fue válido.

La incorporación de la historia cambia la unidad representada por una fila. En la tabla de `estaciones`, una fila identifica una entidad. En una tabla de estados históricos, cada fila describe una versión temporal de uno de sus atributos. La repetición del identificador de estación en varias versiones es necesaria para expresar que la misma entidad tuvo distintos estados.

Esta separación evita confundir identidad y cambio. Una estación que pasa de operativa a inactiva sigue siendo la misma estación. Su historial debe permitir recuperar ambas condiciones y el instante de transición, sin duplicar su identidad ni atribuir el estado nuevo a todas las observaciones anteriores.

### 3. Tiempo observado y tiempo de registro

Suponga que una lectura fue obtenida el 19 de octubre a las 13:00, pero el archivo que la contiene se incorporó al sistema el día siguiente a las 08:00. Ambas marcas son correctas, aunque responden a situaciones distintas:

```text
instante_observado_utc = 2026-10-19 13:00:00
registrado_utc         = 2026-10-20 08:00:00
```

Un informe de las lecturas observadas el día 19 debe incluir esa fila. Un informe de los registros recibidos el día 20 también debe incluirla. El criterio de selección depende del tipo de requerimiento de información.

La literatura distingue el **tiempo válido**, referido al momento de un hecho es verdadero en la realidad modelada, y el **tiempo de transacción**, es referido al momento de una determinada versión de la información. Un modelo que representa ambas dimensiones se denomina bitemporal [@snodgrass2000, ch. 2].

En el ejemplo, el `instante_observado_utc` sitúa temporalmente la medición, la marca `registrado_utc` documenta una incorporación. La diferencia surge al corregir un dato. Si el nivel 104 se reemplaza por 103 mediante `UPDATE`, una fecha de registro no permite reconstruir el valor anterior.

### 4. Referencia horaria y comparabilidad

Antes de comparar marcas temporales debe establecerse una referencia común. El **Tiempo Universal Coordinado (UTC)** es la referencia internacional respecto de la cual se expresan los desplazamientos de las horas locales. Un desplazamiento `-03:00` indica que la hora local está tres horas detrás de UTC. Por esta razón, dos marcas con la misma fecha y hora pueden representar instantes diferentes si utilizan desplazamientos distintos.

Una convención de almacenamiento consiste en expresar todos los instantes en UTC. El sufijo `_utc` permite identificar los campos que siguen esta convención. Si los datos de origen utilizan otra referencia horaria, deben convertirse antes de almacenarse, considerando el desplazamiento correspondiente a la fecha observada.

La referencia horaria también determina los límites de las agregaciones. Antes de calcular un promedio diario, debe definirse la referencia requerida.

Por ejemplo, las `09:00` con desplazamiento `-03:00` y las `12:00` UTC de la misma fecha representan el mismo instante. Con ese desplazamiento, el día local comienza a las `03:00` UTC y termina al comenzar las `03:00` UTC del día siguiente.