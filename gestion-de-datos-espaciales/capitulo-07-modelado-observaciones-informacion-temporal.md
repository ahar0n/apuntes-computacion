# Capítulo 7. Modelado de observaciones e información temporal

## Objetivos de aprendizaje

Al finalizar el capítulo, el estudiante será capaz de:

1. modelar una observación mediante fuente, variable, valor, unidad, tiempo, ubicación y calidad;
2. distinguir dispositivo físico, fuente lógica y registro de observación;
3. diferenciar evento, estado, instante e intervalo;
4. separar tiempo de ocurrencia o validez de tiempo de carga en la base de datos;
5. explicar por qué un instante de carga no constituye por sí solo historial transaccional completo;
6. seleccionar conscientemente entre `DATETIME` y `TIMESTAMP` en MySQL 8.0;
7. representar vigencias mediante intervalos semiabiertos `[desde,hasta)`;
8. conservar cambios de estado sin sobrescribir la historia anterior;
9. cargar un CSV desde Python mediante conversión, validación, transacción y reporte de rechazos;
10. formular controles de recuento, unicidad, unidad, calidad y procedencia.

Estos objetivos desarrollan R1–R4 y establecen la base para las consultas espacio-temporales del capítulo 8.

## Introducción

Hasta ahora, ObservaSur ha respondido principalmente preguntas de ubicación: dónde está una estación, en qué zona se encuentra y qué objetos están próximos. El siguiente problema es temporal: **¿qué se observó, por medio de qué fuente y cuándo ocurrió?**

El esquema inicial contenía una tabla sencilla:

```text
observacion(id, estacion, instante, variable, valor, unidad)
```

Esta estructura permite comenzar, pero deja preguntas abiertas. ¿La variable `nivel` significa siempre lo mismo? ¿La unidad corresponde a la esperada? ¿Qué dispositivo produjo el valor? ¿El instante describe la medición o la carga? ¿La estación estaba operativa entonces? ¿Qué ocurre si el archivo llega con retraso?

Los sensores se abordarán exclusivamente como **fuentes de observaciones**. No se estudiará su física. Para la base de datos importan su identidad, variable observada, unidad, tiempo, ubicación asociada, calidad declarada y problemas de carga.

La progresión será:

```text
valor aislado
    → observación contextualizada
    → instante de ocurrencia y carga
    → estado con vigencia
    → carga reproducible y trazable
```

---

## 1. La observación como hecho contextualizado

### 1.1 Un número no constituye una observación completa

El valor `12.4` admite múltiples significados. Podría ser nivel en centímetros, temperatura en grados Celsius, voltaje o una puntuación de calidad. Para interpretarlo se requiere un contexto mínimo:

\[
O=(fuente, variable, valor, unidad, tiempo, ubicación, calidad).
\]

La ubicación puede obtenerse mediante la estación vinculada, siempre que se conozca qué ubicación era válida al momento de observar. Este último problema se desarrollará en el capítulo 8.

### 1.2 Dispositivo y fuente

Un **dispositivo** es un objeto físico o lógico que produce datos. Una **fuente de observación** es la identidad que el sistema utiliza para atribuir registros. Pueden coincidir, pero no necesariamente:

- un dispositivo puede ser reemplazado conservando el código de una fuente lógica;
- un archivo manual puede actuar como fuente sin ser sensor;
- un dispositivo puede producir varias variables;
- varias fuentes pueden observar la misma variable.

El esquema debe representar la granularidad que la organización puede mantener. Inventar números de serie inexistentes no mejora la trazabilidad.

### 1.3 Variable y unidad

La variable define qué propiedad se observó. La unidad define cómo se expresa el valor. Almacenar ambas como texto libre en cada fila permite variantes como `cm`, `centímetro` y `CMS`, que dificultan controles y agregaciones.

En el núcleo se utiliza un catálogo de variables con una unidad canónica:

```text
variable: nivel
unidad canónica: cm
```

La carga conserva también la unidad recibida. Si no coincide con la canónica, la fila no se convierte automáticamente sin una regla de transformación explícita.

### 1.4 Calidad

La calidad no se reducirá a una certeza estadística que los estudiantes aún no pueden evaluar. Se utilizarán códigos operativos comprensibles:

- `VALIDA`: superó los controles definidos;
- `SOSPECHOSA`: puede utilizarse solo con advertencia;
- `FALTANTE`: no existe valor interpretable;
- `RECHAZADA`: no debe promoverse al conjunto operacional.

El código registra una decisión y sus reglas; no demuestra por sí solo exactitud física.

## 2. Evento, estado, instante e intervalo

### 2.1 Evento

Un **evento** representa algo que ocurre. Para el modelo, puede asociarse a un instante, aunque en la realidad tenga duración. Una observación puntual se trata como evento registrado en `instante_observado`.

Ejemplos:

- se obtuvo una lectura;
- llegó un archivo;
- una estación cambió a estado inactivo;
- se corrigió un dato.

### 2.2 Estado

Un **estado** describe una condición que se mantiene durante un intervalo:

```text
EST-N01 estuvo OPERATIVA desde t1 hasta t2.
```

Sobrescribir `estado='INACTIVA'` en la fila de estación conserva solo la situación actual y elimina cuándo fue operativa. Para responder preguntas históricas se deben conservar versiones o intervalos.

### 2.3 Instante

Un instante identifica una posición en el eje temporal. En la implementación se representa con fecha y hora a una precisión acordada. Dos cadenas iguales no necesariamente representan el mismo instante si sus zonas horarias son distintas.

```text
2026-08-01T09:00:00-04:00
2026-08-01T13:00:00Z
```

Las dos expresiones representan el mismo instante. El proceso de carga normalizará los tiempos recibidos con desplazamiento a UTC.

### 2.4 Intervalo

Un intervalo posee límites. El núcleo utiliza intervalos semiabiertos:

\[
[desde,hasta)=\{t\mid desde\leq t<hasta\}.
\]

El extremo inicial se incluye y el final se excluye. Así, dos estados consecutivos pueden escribirse:

```text
[2026-08-01 00:00, 2026-08-10 12:00)
[2026-08-10 12:00, ∞)
```

sin que ambos sean válidos exactamente a las 12:00 del 10 de agosto.

### 2.5 Intervalo abierto vigente

`hasta = NULL` representará “sin término conocido todavía”, no “tiempo desconocido” en general. Es una convención del modelo:

```text
valido_hasta IS NULL → versión vigente hasta nuevo aviso
```

La consulta debe tratarla explícitamente. El capítulo 8 formalizará pertenencia y solapamiento de intervalos.

## 3. Dimensiones temporales de un dato

### 3.1 Tiempo válido

El **tiempo válido** indica cuándo un hecho es verdadero en la realidad modelada. Para una observación puntual, `instante_observado_utc` representa cuándo se atribuye la lectura. Para un estado, `[valido_desde,valido_hasta)` representa su vigencia.

La terminología temporal distingue el tiempo válido del tiempo en que la base conserva un hecho [@jensen1992; @jensen1998].

### 3.2 Tiempo de carga

`instante_carga` indica cuándo el registro ingresó al sistema. Puede ser posterior al tiempo observado:

```text
observado: 2026-08-01 13:00 UTC
cargado:   2026-08-03 10:15 UTC
```

La diferencia permite detectar retrasos y reconstruir lotes.

### 3.3 Tiempo de transacción y límite de esta implementación

En teoría temporal, el tiempo de transacción describe cuándo un hecho está presente en la base. Para representarlo plenamente se necesitan límites de inicio y fin administrados por el sistema o una estrategia de versionado. Un único `instante_carga` solo registra entrada; no conserva cuándo una fila fue corregida o dejó de considerarse vigente en la base.

Por rigor, el capítulo denomina la columna **tiempo de carga**, no “tiempo de transacción completo”. La bitemporalidad queda como profundización.

### 3.4 Dato tardío

Una observación tardía llega después de su tiempo válido. No debe reemplazarse el instante observado por el de carga para ordenar el archivo. Ambos tiempos responden preguntas diferentes:

- `instante_observado_utc`: ¿cuándo se atribuye la observación?;
- `instante_carga`: ¿cuándo estuvo disponible en la base?

Este contraste prepara el flujo ETL y la trazabilidad analítica posteriores.

## 4. Tipos temporales en MySQL 8.0

### 4.1 `DATE`, `TIME`, `DATETIME` y `TIMESTAMP`

MySQL dispone de tipos temporales distintos. Para este capítulo interesan principalmente:

- `DATE`: fecha sin hora;
- `TIME`: hora o duración dentro de su rango;
- `DATETIME`: fecha y hora sin conversión automática de zona por sesión;
- `TIMESTAMP`: instante almacenado con conversión entre la zona de la sesión y UTC.

`DATETIME` posee un rango mucho más amplio; `TIMESTAMP` en MySQL 8.0 tiene un rango aproximado desde 1970 hasta enero de 2038 [@mysqlDatetime2026]. La selección debe responder a semántica y rango, no a preferencia estética.

### 4.2 Convención del curso

Se adopta:

```text
instante_observado_utc → DATETIME(6), normalizado explícitamente a UTC
instante_carga         → TIMESTAMP(6), DEFAULT CURRENT_TIMESTAMP(6)
```

`DATETIME` no contiene una etiqueta de zona horaria. El sufijo `_utc`, el diccionario y el proceso de carga forman parte del contrato. Python recibe una marca ISO 8601 con desplazamiento, la convierte a UTC y entrega un `datetime` normalizado.

### 4.3 Precisión fraccional

MySQL admite precisión fraccional de hasta seis dígitos para `TIME`, `DATETIME` y `TIMESTAMP` [@mysqlFractional2026]. Usar `(6)` no demuestra que la fuente mida microsegundos. Se conserva capacidad técnica, mientras el diccionario declara la resolución real de cada fuente.

### 4.4 Valores automáticos

`DEFAULT CURRENT_TIMESTAMP(6)` registra el instante de inserción cuando no se proporciona otro valor. MySQL permite inicialización y actualización automáticas para `TIMESTAMP` y `DATETIME` si se declaran explícitamente [@mysqlTimestampInitialization2026]. Para `instante_carga` se usa inicialización, no `ON UPDATE`, porque una edición posterior no debe reescribir silenciosamente el momento de carga original.

## 5. Esquema relacional de observaciones

### 5.1 Catálogos

```sql
CREATE TABLE fuente_observacion (
    id_fuente SMALLINT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    tipo ENUM('SENSOR','ARCHIVO','MANUAL') NOT NULL,
    descripcion VARCHAR(120) NOT NULL
) ENGINE = InnoDB;

CREATE TABLE variable_observada (
    id_variable SMALLINT PRIMARY KEY,
    codigo VARCHAR(30) NOT NULL UNIQUE,
    nombre VARCHAR(80) NOT NULL,
    unidad_canonica VARCHAR(20) NOT NULL
) ENGINE = InnoDB;

CREATE TABLE calidad_observacion (
    id_calidad TINYINT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    descripcion VARCHAR(160) NOT NULL,
    utilizable BOOLEAN NOT NULL
) ENGINE = InnoDB;
```

Los catálogos evitan repetir significado y permiten claves foráneas. No describen física del sensor ni estadística de calidad.

### 5.2 Tabla de hechos operacionales

```sql
CREATE TABLE observacion_temporal (
    id_observacion BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_estacion INT NOT NULL,
    id_fuente SMALLINT NOT NULL,
    id_variable SMALLINT NOT NULL,
    instante_observado_utc DATETIME(6) NOT NULL,
    valor DECIMAL(14,4) NOT NULL,
    unidad_recibida VARCHAR(20) NOT NULL,
    id_calidad TINYINT NOT NULL,
    instante_carga TIMESTAMP(6) NOT NULL
        DEFAULT CURRENT_TIMESTAMP(6),
    archivo_origen VARCHAR(160) NOT NULL,
    fila_origen INT NOT NULL,
    CONSTRAINT fk_obs_temporal_estacion
        FOREIGN KEY (id_estacion)
        REFERENCES estacion_espacial (id_estacion),
    CONSTRAINT fk_obs_temporal_fuente
        FOREIGN KEY (id_fuente)
        REFERENCES fuente_observacion (id_fuente),
    CONSTRAINT fk_obs_temporal_variable
        FOREIGN KEY (id_variable)
        REFERENCES variable_observada (id_variable),
    CONSTRAINT fk_obs_temporal_calidad
        FOREIGN KEY (id_calidad)
        REFERENCES calidad_observacion (id_calidad),
    CONSTRAINT uq_obs_temporal_origen
        UNIQUE (archivo_origen, fila_origen)
) ENGINE = InnoDB;
```

La restricción de origen evita cargar dos veces la misma fila del mismo archivo. No impide dos observaciones legítimas con igual estación, variable e instante provenientes de fuentes distintas.

### 5.3 Grano

El grano se declara antes de consultar:

> Cada fila representa una observación de una variable, atribuida a una fuente y estación, ocurrida en un instante UTC, recibida con una unidad y calidad determinadas, y trazable a una fila de archivo.

Este enunciado evita interpretar una fila como resumen diario o estado continuo.

## 6. Historial simple de estados

### 6.1 Esquema

```sql
CREATE TABLE historial_estado_estacion (
    id_historial BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_estacion INT NOT NULL,
    estado ENUM('OPERATIVA','INACTIVA','MANTENCION') NOT NULL,
    valido_desde DATETIME(6) NOT NULL,
    valido_hasta DATETIME(6) NULL,
    registrado_en TIMESTAMP(6) NOT NULL
        DEFAULT CURRENT_TIMESTAMP(6),
    CONSTRAINT fk_historial_estado_estacion
        FOREIGN KEY (id_estacion)
        REFERENCES estacion_espacial (id_estacion),
    CONSTRAINT ck_historial_intervalo
        CHECK (valido_hasta IS NULL OR valido_hasta > valido_desde)
) ENGINE = InnoDB;
```

La restricción evita intervalos vacíos o invertidos. No evita solapamientos entre filas de una estación; ese control requiere comparar filas y se desarrollará en el capítulo 8.

### 6.2 Actualizar destruyendo historia

Este patrón es insuficiente:

```sql
UPDATE estacion_espacial
SET estado = 'INACTIVA'
WHERE codigo = 'EST-N01';
```

Solo conserva el último valor. El patrón histórico cierra la versión vigente e inserta una nueva dentro de una transacción:

```sql
START TRANSACTION;

UPDATE historial_estado_estacion
SET valido_hasta = '2026-08-10 16:00:00.000000'
WHERE id_estacion = 1
  AND valido_hasta IS NULL;

INSERT INTO historial_estado_estacion
    (id_estacion, estado, valido_desde, valido_hasta)
VALUES
    (1, 'MANTENCION', '2026-08-10 16:00:00.000000', NULL);

COMMIT;
```

La transacción evita dejar un intervalo cerrado sin sucesor si la inserción falla.

### 6.3 Prueba de pérdida y recuperación

El contraste pedagógico consiste en:

1. sobrescribir un estado en una tabla de ensayo;
2. intentar responder cuándo cambió;
3. comprobar que la respuesta se perdió;
4. repetir con historial;
5. reconstruir la secuencia completa.

Este ciclo hace visible por qué “actualización → historial” es un puente central del curso.

## 7. Carga de observaciones desde CSV

### 7.1 Contrato del archivo

```text
codigo_estacion,codigo_fuente,codigo_variable,instante_iso,valor,unidad,calidad
EST-N01,SEN-N01,NIVEL,2026-08-01T09:00:00-04:00,12.40,cm,VALIDA
```

El archivo incluye desplazamiento horario. La carga no presume que una fecha sin zona sea UTC.

### 7.2 Conversión mínima en Python

```python
from datetime import timezone
from decimal import Decimal, InvalidOperation


def convertir_fila(fila):
    instante = datetime.fromisoformat(fila["instante_iso"])
    if instante.tzinfo is None:
        raise ValueError("TIEMPO_SIN_ZONA")
    instante_utc = instante.astimezone(timezone.utc).replace(tzinfo=None)

    try:
        valor = Decimal(fila["valor"])
    except InvalidOperation as error:
        raise ValueError("VALOR_NO_NUMERICO") from error

    return instante_utc, valor
```

Se usa Python básico: lectura de diccionarios, conversión de fecha y `Decimal`. No se requiere pandas.

### 7.3 Resolución de claves

Los códigos externos deben resolverse a identificadores internos mediante consultas parametrizadas. Si no existe estación, fuente, variable o calidad, la fila se rechaza con una categoría estable. No se crean catálogos automáticamente a partir de errores tipográficos.

### 7.4 Unidad canónica

La consulta de variable devuelve `id_variable` y `unidad_canonica`. Si `unidad_recibida` difiere:

- se rechaza como `UNIDAD_INCOMPATIBLE`; o
- se transforma solo si existe una regla declarada y probada.

El núcleo elige rechazo explicable. Las conversiones se incorporarán posteriormente al ETL.

### 7.5 Inserción parametrizada

```python
INSERCION = """
    INSERT INTO observacion_temporal
        (id_estacion, id_fuente, id_variable,
         instante_observado_utc, valor, unidad_recibida,
         id_calidad, archivo_origen, fila_origen)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
```

Connector/Python admite ejecutar una operación para una secuencia de parámetros mediante `executemany()` [@mysqlConnectorExecutemany2026]. Para poder explicar rechazos por fila, la práctica procesa y valida primero, acumula filas aceptables y luego inserta el lote dentro de una transacción.

### 7.6 `LOAD DATA` como referencia, no prerrequisito

MySQL ofrece `LOAD DATA` para leer archivos de texto y permite configurar separadores, comillas, líneas y columnas [@mysqlLoadData2026]. Su uso depende de permisos, `LOCAL`, configuración y política de errores. Python se mantiene como ruta nuclear porque permite diagnóstico por fila con conocimientos previos; `LOAD DATA` queda como alternativa técnica.

## 8. Controles y evidencia de carga

### 8.1 Reconciliación

```text
filas leídas = filas aceptadas + filas rechazadas
filas aceptadas = filas insertadas o ya identificadas como duplicadas
```

Un duplicado de procedencia no debe contarse simultáneamente como nueva inserción y rechazo genérico.

### 8.2 Controles SQL

```sql
SELECT archivo_origen, COUNT(*) AS filas
FROM observacion_temporal
GROUP BY archivo_origen;

SELECT v.codigo, o.unidad_recibida, COUNT(*) AS filas
FROM observacion_temporal AS o
JOIN variable_observada AS v
  ON v.id_variable = o.id_variable
GROUP BY v.codigo, o.unidad_recibida;

SELECT
    MIN(instante_observado_utc) AS primera_observacion,
    MAX(instante_observado_utc) AS ultima_observacion,
    MIN(instante_carga) AS primera_carga,
    MAX(instante_carga) AS ultima_carga
FROM observacion_temporal;
```

### 8.3 Latencia de llegada

La diferencia entre carga y observación puede calcularse, con cuidado respecto de la convención UTC:

```sql
SELECT id_observacion,
       TIMESTAMPDIFF(
           SECOND,
           instante_observado_utc,
           CAST(instante_carga AS DATETIME)
       ) AS retraso_segundos
FROM observacion_temporal;
```

La sesión debe estar configurada coherentemente en UTC para interpretar el `TIMESTAMP` convertido. El laboratorio fija y registra esa condición.

### 8.4 Evidencia

La entrega incluye:

- diccionario de fuente, variable, unidad, tiempo y calidad;
- script SQL;
- archivo CSV preparado;
- programa Python de carga;
- bitácora de aceptaciones y rechazos;
- reconciliación de recuentos;
- historial con dos estados consecutivos;
- demostración de la historia que se pierde al sobrescribir.

## 9. Síntesis del núcleo obligatorio

```text
sensor o fuente
    → produce o entrega observaciones

observación
    → variable + valor + unidad + tiempo + estación + calidad

tiempo válido
    → cuándo ocurrió o fue verdadero

tiempo de carga
    → cuándo ingresó a la base

estado
    → hecho válido durante [desde,hasta)

historial
    → conserva cambios sin sobrescribir
```

Hasta aquí es obligatorio distinguir observación de valor aislado, tiempo observado de tiempo cargado y estado actual de historia.

## 10. Ejercicios y casos prácticos

### Ejercicio 1. Nivel básico: completar una observación

Se recibe `12.4` desde `SEN-N01` a las `2026-08-01T09:00:00-04:00`. Indique qué información falta para formar una observación interpretable.

#### Resolución paso a paso

**Paso 1. Fuente.** `SEN-N01` identifica una fuente, pero debe existir en catálogo.

**Paso 2. Variable.** Falta declarar qué se observó, por ejemplo `NIVEL`.

**Paso 3. Unidad.** Falta `cm` u otra unidad compatible.

**Paso 4. Ubicación.** Debe vincularse a una estación cuya posición corresponda al instante.

**Paso 5. Calidad.** Debe existir un código y criterio de calidad.

**Paso 6. Procedencia.** Para carga reproducible faltan archivo y fila.

### Ejercicio 2. Nivel básico–intermedio: normalizar un instante

Convierta `2026-08-01T09:00:00-04:00` a UTC y explique qué se almacena.

#### Resolución paso a paso

**Paso 1. Interpretar desplazamiento.** `-04:00` está cuatro horas detrás de UTC.

**Paso 2. Sumar cuatro horas.** El resultado es `2026-08-01 13:00:00 UTC`.

**Paso 3. Almacenar.** Se inserta `2026-08-01 13:00:00.000000` en `instante_observado_utc DATETIME(6)`.

**Paso 4. Documentar.** La columna no transporta la zona; el sufijo, diccionario y carga garantizan la convención.

### Ejercicio 3. Nivel intermedio: representar un cambio de estado

`EST-N01` estuvo operativa desde el 1 de agosto y entró en mantención el 10 de agosto a las 16:00 UTC. Represente ambos estados sin solapamiento.

#### Resolución paso a paso

**Paso 1. Primer intervalo.**

```text
OPERATIVA: [2026-08-01 00:00, 2026-08-10 16:00)
```

**Paso 2. Segundo intervalo.**

```text
MANTENCION: [2026-08-10 16:00, ∞)
```

**Paso 3. Implementar transaccionalmente.** Se cierra la fila vigente y se inserta la nueva antes de confirmar.

**Paso 4. Interpretar el límite.** Exactamente a las 16:00 solo está vigente `MANTENCION`.

### Ejercicio 4. Nivel avanzado: reconciliar una carga

Un CSV tiene diez filas. Se insertan siete, una ya había sido cargada desde el mismo archivo y fila, una tiene unidad incompatible y otra carece de zona horaria. Diseñe el resumen.

#### Resolución paso a paso

**Paso 1. Leídas.** 10.

**Paso 2. Nuevas aceptadas e insertadas.** 7.

**Paso 3. Duplicada identificada.** 1; no se reinserta.

**Paso 4. Rechazadas.** 2: `UNIDAD_INCOMPATIBLE=1`, `TIEMPO_SIN_ZONA=1`.

**Paso 5. Reconciliar.**

```text
10 leídas = 7 insertadas + 1 duplicada + 2 rechazadas
```

**Paso 6. Informar.** El reporte conserva archivo, fila, categoría y mensaje controlado para cada no insertada.

## 11. Temas de profundización

### 11.1 Tiempo de transacción y bitemporalidad

Un modelo bitemporal combina tiempo válido y tiempo de transacción, permitiendo preguntar qué se consideraba cierto en la base en un momento respecto de otro momento del dominio. Su implementación completa excede el núcleo y no debe fingirse con una sola fecha de carga.

### 11.2 Resolución y granularidad temporal

Guardar microsegundos no implica que la fuente los distinga. La resolución de captura, la precisión del tipo y la frecuencia de observación son propiedades diferentes.

### 11.3 Series de tiempo

Una serie de tiempo organiza observaciones de una variable a través de instantes ordenados. Este curso no desarrolla análisis estadístico de series; utiliza la estructura para almacenar, consultar y preparar datos correctamente.

## 12. Referencia técnica

- `DATETIME(6)`: fecha y hora sin conversión automática por zona de sesión.
- `TIMESTAMP(6)`: conversión asociada a la zona de sesión y rango menor.
- `DEFAULT CURRENT_TIMESTAMP(6)`: inicialización automática explícita.
- Intervalo nuclear: `[desde,hasta)`; `NULL` final significa abierto según convenio.
- Tiempo observado/validez y tiempo de carga son atributos distintos.
- `csv.DictReader`, `datetime.fromisoformat`, `timezone.utc` y `Decimal` bastan para la carga nuclear.
- `LOAD DATA` queda como alternativa condicionada por configuración y permisos.
- Recursos ejecutables: [`semana07_observaciones_temporales.sql`](../observasur/sql/semana07_observaciones_temporales.sql), [`semana07_cargar_observaciones.py`](../observasur/python/semana07_cargar_observaciones.py) y [`semana07_observaciones.csv`](../observasur/datos/semana07_observaciones.csv).

El capítulo 8 utilizará estos tiempos e intervalos para consultar vigencias, detectar solapamientos y recuperar la ubicación válida cuando ocurrió cada observación.

## 13. Referencias bibliográficas

Jensen, C. S., Clifford, J., Gadia, S. K., Segev, A. y Snodgrass, R. T. (1992). A glossary of temporal database concepts. *ACM SIGMOD Record, 21*(3), 35–43. https://doi.org/10.1145/136985.136988

Jensen, C. S., Dyreson, C. E., Böhlen, M., Clifford, J., Elmasri, R., Gadia, S. K., Grandi, F., Hayes, P., Jajodia, S., Käfer, W., Kline, N., Lorentzos, N., Mitsopoulos, Y., Montanari, A., Nonen, D., Peressi, E., Pernici, B., Roddick, J. F., Sarda, N. L., ... Wiederhold, G. (1998). The consensus glossary of temporal database concepts—February 1998 version. En O. Etzion, S. Jajodia y S. Sripada (Eds.), *Temporal databases: Research and practice* (LNCS 1399, pp. 367–405). Springer. https://doi.org/10.1007/BFb0053710

MySQL. (2026). *MySQL 8.0 Reference Manual: Automatic initialization and updating for TIMESTAMP and DATETIME*. https://dev.mysql.com/doc/refman/8.0/en/timestamp-initialization.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Fractional seconds in time values*. https://dev.mysql.com/doc/refman/8.0/en/fractional-seconds.html

MySQL. (2026). *MySQL 8.0 Reference Manual: LOAD DATA statement*. https://dev.mysql.com/doc/refman/8.0/en/load-data.html

MySQL. (2026). *MySQL 8.0 Reference Manual: The DATE, DATETIME, and TIMESTAMP types*. https://dev.mysql.com/doc/refman/8.0/en/datetime.html

MySQL. (2026). *MySQL Connector/Python Developer Guide: MySQLCursor.executemany() method*. https://dev.mysql.com/doc/connectors/en/connector-python-api-mysqlcursor-executemany.html
