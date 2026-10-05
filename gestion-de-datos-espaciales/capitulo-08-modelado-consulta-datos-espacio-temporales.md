# Capítulo 8. Modelado y consulta de datos espacio-temporales

## Objetivos de aprendizaje

Al finalizar el capítulo, el estudiante será capaz de:

1. explicar por qué una ubicación histórica requiere geometría y vigencia temporal;
2. representar versiones de ubicación mediante intervalos semiabiertos `[desde,hasta)`;
3. formular correctamente la pertenencia de un instante a un intervalo;
4. detectar intervalos solapados, contiguos y separados;
5. recuperar la ubicación válida cuando ocurrió una observación;
6. combinar reunión por claves, condición temporal y predicado espacial en una misma consulta;
7. distinguir la ubicación actual de la ubicación histórica atribuible a un hecho;
8. utilizar `LAG()` o `LEAD()` para auditar secuencias temporales ordenadas;
9. explicar qué integridad puede declararse con `CHECK` y qué requiere comparación entre filas;
10. tratar datos y correcciones tardías mediante transacciones, procedencia y nuevas verificaciones.

Estos objetivos desarrollan R1–R4 e integran los núcleos espacial y temporal de la asignatura.

## Introducción

El capítulo 7 modeló observaciones e historiales de estado. Aún falta resolver una dependencia fundamental: **¿dónde estaba una estación cuando ocurrió una observación?**

Consultar la columna actual `estacion_espacial.ubicacion` puede atribuir una lectura antigua a una posición nueva. El error no está en la geometría ni en la fecha por separado, sino en ignorar su correspondencia temporal. Una base espacio-temporal debe conservar versiones de la propiedad espacial y determinar cuál era válida para el instante consultado.

La consulta completa combina tres relaciones:

```text
observación ──clave──> estación
observación ──tiempo─> versión de ubicación vigente
ubicación   ──espacio> zona que la contiene
```

Este capítulo no introduce modelos especializados de trayectorias ni análisis de movimiento. Utiliza el modelo relacional de MySQL 8.0 para representar historia discreta, consultar vigencias y verificar integridad alcanzable con los recursos del curso.

---

## 1. De la geometría actual a la geometría histórica

### 1.1 El problema de sobrescribir

Si `EST-N01` cambia de `(25,75)` a `(30,70)`, esta actualización conserva solo el último valor:

```sql
UPDATE estacion_espacial
SET ubicacion = ST_PointFromText('POINT(30 70)', 0)
WHERE codigo = 'EST-N01';
```

Después de ejecutarla, una consulta sobre observaciones del 1 de agosto podría asociarlas incorrectamente con `(30,70)`, aunque el traslado ocurrió el 10 de agosto.

### 1.2 Hecho versionado

La propiedad histórica se expresa como:

\[
(estación, ubicación, intervalo\ de\ validez).
\]

Ejemplo:

```text
EST-N01, POINT(25 75), [2026-08-01, 2026-08-10 16:00)
EST-N01, POINT(30 70), [2026-08-10 16:00, ∞)
```

La identidad de la estación permanece; cambia una propiedad a través del tiempo. Este patrón extiende el puente “actualización → historial” introducido en el capítulo 7.

### 1.3 Dato espacio-temporal

En este libro, un dato es espacio-temporal cuando su interpretación depende conjuntamente de geometría y tiempo. No basta que una tabla contenga una columna espacial y otra fecha sin una semántica que las relacione.

Una versión de ubicación afirma:

> La estación identificada poseyó esta posición durante este intervalo válido.

Los modelos temporales distinguen tiempo válido de tiempo de transacción; aquí se implementa principalmente tiempo válido y se registra el instante de carga para trazabilidad [@jensen1998; @snodgrass1999, caps. 2–3].

## 2. Esquema de historial espacial

### 2.1 Tabla de versiones

```sql
CREATE TABLE historial_ubicacion_estacion (
    id_ubicacion_hist BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_estacion INT NOT NULL,
    ubicacion POINT NOT NULL SRID 0,
    valido_desde DATETIME(6) NOT NULL,
    valido_hasta DATETIME(6) NULL,
    registrado_en TIMESTAMP(6) NOT NULL
        DEFAULT CURRENT_TIMESTAMP(6),
    fuente_cambio VARCHAR(160) NOT NULL,
    motivo VARCHAR(240) NOT NULL,
    vigente_unica TINYINT
        GENERATED ALWAYS AS (
            CASE WHEN valido_hasta IS NULL THEN 1 ELSE NULL END
        ) STORED,
    CONSTRAINT fk_hist_ubicacion_estacion
        FOREIGN KEY (id_estacion)
        REFERENCES estacion_espacial (id_estacion),
    CONSTRAINT ck_hist_ubicacion_intervalo
        CHECK (valido_hasta IS NULL OR valido_hasta > valido_desde),
    CONSTRAINT uq_hist_ubicacion_inicio
        UNIQUE (id_estacion, valido_desde),
    CONSTRAINT uq_hist_ubicacion_vigente
        UNIQUE (id_estacion, vigente_unica)
) ENGINE = InnoDB;
```

### 2.2 Qué controla el esquema

- `POINT NOT NULL SRID 0`: tipo, presencia y sistema de referencia;
- `CHECK`: final posterior al inicio o intervalo abierto;
- unicidad de inicio: evita dos versiones con el mismo comienzo para una estación;
- `vigente_unica`: permite como máximo una fila abierta por estación;
- claves y procedencia: mantienen identidad y fuente del cambio.

La columna generada devuelve 1 solo para la versión abierta y `NULL` para las cerradas. Como un índice único admite múltiples `NULL` pero no dos valores `(id_estacion,1)`, se impide más de una versión abierta.

### 2.3 Qué no controla

La tabla todavía puede admitir:

```text
[1 agosto, 15 agosto)
[10 agosto, 20 agosto)
```

Los intervalos tienen inicios distintos, finales válidos y ninguna segunda fila abierta, pero se solapan. Detectarlo exige comparar filas de la misma estación. MySQL restringe expresiones `CHECK` a condiciones de la fila: no permite subconsultas ni columnas de otras tablas [@mysqlCheckConstraints2026].

### 2.4 Índices de apoyo

```sql
CREATE INDEX idx_hist_ubicacion_estacion_tiempo
ON historial_ubicacion_estacion
    (id_estacion, valido_desde, valido_hasta);

CREATE SPATIAL INDEX idx_hist_ubicacion_geometria
ON historial_ubicacion_estacion (ubicacion);
```

El índice compuesto apoya búsquedas por estación y tiempo; el espacial, búsquedas por región. Que ambos existan no significa que una consulta combinada use necesariamente los dos. El plan debe inspeccionarse.

## 3. Pertenencia de un instante a una vigencia

### 3.1 Predicado fundamental

Un instante \(t\) pertenece a `[desde,hasta)` si:

\[
desde\leq t \land (hasta\ es\ nulo \lor t<hasta).
\]

En SQL:

```sql
valido_desde <= %s
AND (valido_hasta IS NULL OR %s < valido_hasta)
```

### 3.2 Por qué no usar `BETWEEN`

`BETWEEN` incluye ambos extremos; equivale a `min <= valor AND valor <= max` [@mysqlComparison2026]. Para intervalos semiabiertos incluiría incorrectamente `valido_hasta`. Además, no resuelve directamente el extremo abierto `NULL`.

Esta expresión es inadecuada:

```sql
instante BETWEEN valido_desde AND valido_hasta
```

La condición explícita comunica la semántica adoptada.

### 3.3 Consulta de una estación en un instante

```sql
SELECT
    e.codigo,
    ST_AsText(h.ubicacion) AS ubicacion_wkt,
    h.valido_desde,
    h.valido_hasta
FROM historial_ubicacion_estacion AS h
JOIN estacion_espacial AS e
  ON e.id_estacion = h.id_estacion
WHERE e.codigo = %s
  AND h.valido_desde <= %s
  AND (h.valido_hasta IS NULL OR %s < h.valido_hasta);
```

El resultado esperado es exactamente una fila. Cero filas revelan una brecha; más de una revela solapamiento.

### 3.4 Casos de frontera temporal

Para `[10:00,11:00)`:

| Instante | Pertenece |
|---|---:|
| 09:59:59 | 0 |
| 10:00:00 | 1 |
| 10:30:00 | 1 |
| 11:00:00 | 0 |

La prueba del extremo final es indispensable. Si la siguiente versión comienza a las 11:00, solo ella debe resultar válida entonces.

## 4. Solapamientos, contigüidad y brechas

### 4.1 Predicado de solapamiento

Dos intervalos semiabiertos finitos \([a_1,a_2)\) y \([b_1,b_2)\) se solapan si:

\[
a_1<b_2 \land b_1<a_2.
\]

Un extremo nulo se interpreta como infinito futuro para esta prueba. En SQL puede utilizarse una fecha centinela solo dentro de la expresión:

```sql
a.valido_desde < COALESCE(b.valido_hasta, '9999-12-31 23:59:59.999999')
AND b.valido_desde < COALESCE(a.valido_hasta, '9999-12-31 23:59:59.999999')
```

La tabla conserva `NULL`; no almacena la fecha centinela como si fuera un hecho real.

### 4.2 Autorreunión para detectar solapamientos

```sql
SELECT
    a.id_estacion,
    a.id_ubicacion_hist AS version_a,
    b.id_ubicacion_hist AS version_b
FROM historial_ubicacion_estacion AS a
JOIN historial_ubicacion_estacion AS b
  ON b.id_estacion = a.id_estacion
 AND b.id_ubicacion_hist > a.id_ubicacion_hist
 AND a.valido_desde < COALESCE(
        b.valido_hasta, '9999-12-31 23:59:59.999999')
 AND b.valido_desde < COALESCE(
        a.valido_hasta, '9999-12-31 23:59:59.999999');
```

La condición de identificadores evita comparar una fila consigo misma y reportar cada pareja dos veces.

### 4.3 Contigüidad

Dos intervalos son contiguos si:

\[
a_2=b_1.
\]

No se solapan y no dejan brecha. La contigüidad es deseable para propiedades que deben tener valor continuo, pero no siempre es obligatoria. Una estación puede carecer de ubicación confiable durante un período; esa brecha debe conservarse en vez de inventar continuidad.

### 4.4 Auditoría con `LEAD()`

`LEAD()` devuelve un valor de una fila posterior dentro de una partición ordenada y resulta útil para comparar versiones adyacentes [@mysqlWindowFunctions2026].

```sql
WITH secuencia AS (
    SELECT
        id_estacion,
        valido_desde,
        valido_hasta,
        LEAD(valido_desde) OVER (
            PARTITION BY id_estacion
            ORDER BY valido_desde
        ) AS siguiente_desde
    FROM historial_ubicacion_estacion
)
SELECT *,
       CASE
           WHEN siguiente_desde IS NULL THEN 'ultima-version'
           WHEN valido_hasta IS NULL THEN 'abierta-antes-de-otra'
           WHEN valido_hasta > siguiente_desde THEN 'solapamiento'
           WHEN valido_hasta < siguiente_desde THEN 'brecha'
           ELSE 'contigua'
       END AS diagnostico
FROM secuencia
ORDER BY id_estacion, valido_desde;
```

La función de ventana no impide el problema; lo hace visible para auditoría.

## 5. Ubicación válida de cada observación

### 5.1 Reunión temporal

```sql
SELECT
    o.id_observacion,
    e.codigo,
    o.instante_observado_utc,
    ST_AsText(h.ubicacion) AS ubicacion_al_observar
FROM observacion_temporal AS o
JOIN estacion_espacial AS e
  ON e.id_estacion = o.id_estacion
JOIN historial_ubicacion_estacion AS h
  ON h.id_estacion = o.id_estacion
 AND h.valido_desde <= o.instante_observado_utc
 AND (
        h.valido_hasta IS NULL
        OR o.instante_observado_utc < h.valido_hasta
     )
ORDER BY o.id_observacion;
```

La reunión combina clave e intervalo. Si el historial es íntegro, cada observación se vincula con una versión.

### 5.2 Auditoría de cardinalidad

```sql
SELECT
    o.id_observacion,
    COUNT(h.id_ubicacion_hist) AS versiones_encontradas
FROM observacion_temporal AS o
LEFT JOIN historial_ubicacion_estacion AS h
  ON h.id_estacion = o.id_estacion
 AND h.valido_desde <= o.instante_observado_utc
 AND (h.valido_hasta IS NULL
      OR o.instante_observado_utc < h.valido_hasta)
GROUP BY o.id_observacion
HAVING COUNT(h.id_ubicacion_hist) <> 1;
```

- 0: observación sin ubicación válida;
- 1: correspondencia esperada;
- más de 1: historial solapado.

Esta consulta convierte una expectativa de modelado en evidencia verificable.

### 5.3 Error de usar la ubicación actual

```sql
-- Incorrecta para preguntas históricas:
SELECT o.id_observacion, ST_AsText(e.ubicacion)
FROM observacion_temporal AS o
JOIN estacion_espacial AS e
  ON e.id_estacion = o.id_estacion;
```

La consulta es relacionalmente válida, pero responde por la ubicación actual. Su error es semántico respecto de la pregunta histórica.

## 6. Consulta integrada espacio-temporal

### 6.1 Zona de la observación

Una vez recuperada la posición válida, puede calcularse la zona actual que contiene esa posición:

```sql
WITH observacion_ubicada AS (
    SELECT
        o.id_observacion,
        o.instante_observado_utc,
        h.ubicacion
    FROM observacion_temporal AS o
    JOIN historial_ubicacion_estacion AS h
      ON h.id_estacion = o.id_estacion
     AND h.valido_desde <= o.instante_observado_utc
     AND (h.valido_hasta IS NULL
          OR o.instante_observado_utc < h.valido_hasta)
)
SELECT
    ou.id_observacion,
    ou.instante_observado_utc,
    z.nombre AS zona_calculada
FROM observacion_ubicada AS ou
JOIN zona_espacial AS z
  ON ST_Within(ou.ubicacion, z.extension)
ORDER BY ou.id_observacion, z.nombre;
```

### 6.2 Límite de la consulta

La consulta usa historia de ubicación de estaciones, pero geometría actual de zonas. Si las zonas también cambian, se necesita `historial_extension_zona` y una segunda condición de vigencia. La respuesta debe declararse como “zona según límites actuales” mientras ese historial no exista.

### 6.3 Tres dimensiones de coherencia

Una observación puede evaluarse respecto de:

1. estación identificada por clave;
2. ubicación válida por tiempo;
3. zona calculada por geometría.

La combinación no convierte la consulta en prueba de exactitud. Sigue dependiendo de procedencia, SRID, calidad y completitud de los historiales.

## 7. Estado válido cuando se observó

La misma condición temporal permite recuperar estado:

```sql
SELECT
    o.id_observacion,
    e.codigo,
    o.instante_observado_utc,
    h.estado
FROM observacion_temporal AS o
JOIN estacion_espacial AS e
  ON e.id_estacion = o.id_estacion
LEFT JOIN historial_estado_estacion AS h
  ON h.id_estacion = o.id_estacion
 AND h.valido_desde <= o.instante_observado_utc
 AND (h.valido_hasta IS NULL
      OR o.instante_observado_utc < h.valido_hasta)
ORDER BY o.id_observacion;
```

El `LEFT JOIN` conserva observaciones sin estado histórico para hacer visible la ausencia. Usar `INNER JOIN` las eliminaría del resultado y podría ocultar el problema.

Una observación producida durante `MANTENCION` no debe eliminarse automáticamente. Puede ser legítima, sospechosa o parte de una prueba. La política de calidad debe declararlo.

## 8. Cambios y datos tardíos

### 8.1 Inserción tardía

Supóngase que el 20 de agosto llega evidencia de que la estación cambió de posición el 5 de agosto. El historial ya contiene una versión `[1 agosto,10 agosto)`. Insertar simplemente `[5 agosto,10 agosto)` crea solapamiento.

### 8.2 División de intervalo

La corrección requiere una transacción:

```text
antes:  A [1 agosto, 10 agosto)

después:
A [1 agosto, 5 agosto)
B [5 agosto, 10 agosto)
```

```sql
START TRANSACTION;

UPDATE historial_ubicacion_estacion
SET valido_hasta = '2026-08-05 12:00:00.000000'
WHERE id_ubicacion_hist = %s;

INSERT INTO historial_ubicacion_estacion
    (id_estacion, ubicacion, valido_desde, valido_hasta,
     fuente_cambio, motivo)
VALUES
    (%s, ST_PointFromText(%s, 0),
     '2026-08-05 12:00:00.000000',
     '2026-08-10 16:00:00.000000',
     %s, %s);

COMMIT;
```

Después se vuelven a ejecutar las auditorías de solapamiento, brechas y correspondencia de observaciones.

### 8.3 Corregir sin borrar procedencia

La versión anterior no debe eliminarse sin registro si ya sustentó resultados. El núcleo conserva fuente y motivo en la nueva versión; una solución de producción podría requerir historial de correcciones o bitemporalidad. `registrado_en` permite saber cuándo se incorporó la versión, pero no registra por sí solo todo el período durante el cual la versión anterior estuvo en la base.

### 8.4 Reproceso dependiente

Una corrección histórica puede cambiar:

- zona calculada de observaciones anteriores;
- clasificación de calidad;
- agregados del futuro almacén;
- conjuntos preparados para minería.

Por eso la trazabilidad OLTP → ETL → almacén debe conservar qué versión y carga sustentaron cada resultado.

## 9. Integridad temporal alcanzable en MySQL

### 9.1 Restricciones por fila

`CHECK`, tipos, nulabilidad y claves controlan:

- orden de extremos dentro de una fila;
- presencia de inicio y geometría;
- SRID y tipo;
- referencia a estación;
- unicidad de inicio;
- una sola fila abierta mediante columna generada.

### 9.2 Reglas entre filas

Solapamiento y continuidad dependen de otras filas. Las alternativas incluyen:

- transacción de aplicación con bloqueo y consulta previa;
- procedimiento almacenado;
- disparador;
- auditoría posterior programada;
- combinación de prevención y detección.

Ninguna alternativa elimina la necesidad de pruebas bajo concurrencia. El núcleo implementa transacción desde Python y auditorías SQL; los disparadores quedan como profundización.

### 9.3 Secuencia segura desde Python

```text
iniciar transacción
    → bloquear/leer versiones de la estación
    → comprobar solapamiento con la candidata
    → cerrar o dividir versión si corresponde
    → insertar nueva versión
    → ejecutar controles
    → confirmar o revertir
```

Una consulta previa sin transacción no es suficiente: otra sesión podría insertar una versión entre comprobación e inserción.

## 10. Consultas parametrizadas y pruebas

### 10.1 Recuperación desde Python

```python
def ubicacion_en(conexion, codigo, instante_utc):
    consulta = """
        SELECT ST_AsText(h.ubicacion) AS wkt,
               h.valido_desde, h.valido_hasta
        FROM historial_ubicacion_estacion AS h
        JOIN estacion_espacial AS e
          ON e.id_estacion = h.id_estacion
        WHERE e.codigo = %s
          AND h.valido_desde <= %s
          AND (h.valido_hasta IS NULL OR %s < h.valido_hasta)
    """
    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute(consulta, (codigo, instante_utc, instante_utc))
        filas = cursor.fetchall()
    if len(filas) != 1:
        raise ValueError(f"Se esperó una versión y se obtuvieron {len(filas)}")
    return filas[0]
```

### 10.2 Oráculo de cambio

Para el cambio de `EST-N01` a las 16:00 del 10 de agosto:

| Consulta | WKT esperado |
|---|---|
| 10-08 15:59:59.999999 | `POINT(25 75)` |
| 10-08 16:00:00.000000 | `POINT(30 70)` |
| 10-08 16:00:00.000001 | `POINT(30 70)` |

### 10.3 Pruebas mínimas

- antes del primer intervalo: cero versiones;
- exactamente en `valido_desde`: una versión;
- dentro del intervalo: una versión;
- exactamente en `valido_hasta`: versión siguiente;
- estación desconocida: error distinguible;
- intervalos solapados de ensayo: auditoría los detecta;
- brecha de ensayo: auditoría la clasifica;
- observación sin ubicación: cardinalidad cero visible.

## 11. Síntesis del núcleo obligatorio

```text
geometría actual
    → responde por el presente almacenado

geometría versionada
    → responde por una vigencia

instante ∈ [desde,hasta)
    → desde <= instante AND instante < hasta

observación + historial
    → ubicación válida al observar

ubicación válida + zona
    → relación espacial contextualizada temporalmente

corrección tardía
    → dividir, registrar, auditar y reprocesar
```

Hasta aquí es obligatorio evitar `BETWEEN` para el intervalo semiabierto, comprobar que cada observación encuentre exactamente una versión y declarar si una consulta usa zonas actuales o históricas.

## 12. Ejercicios y casos prácticos

### Ejercicio 1. Nivel básico: pertenencia a intervalos

Determine qué versión es válida a las 12:00 si A es `[08:00,12:00)` y B es `[12:00,18:00)`.

#### Resolución paso a paso

**Paso 1. Evaluar A.** `12:00 < 12:00` es falso; A no está vigente.

**Paso 2. Evaluar B.** `12:00 >= 12:00` y `12:00 < 18:00`; B está vigente.

**Paso 3. Concluir.** Solo B. La semántica semiabierta evita doble pertenencia.

### Ejercicio 2. Nivel básico–intermedio: detectar solapamiento

Clasifique las parejas A=`[1,5)`, B=`[5,8)`, C=`[4,7)` y D=`[9,∞)`.

#### Resolución paso a paso

**A–B.** Contiguos: el final de A coincide con el inicio de B; no se solapan.

**A–C.** Se solapan en `[4,5)` porque `1<7` y `4<5`.

**B–C.** Se solapan en `[5,7)` porque `5<7` y `4<8`.

**B–D.** Existe brecha `[8,9)`.

**C–D.** Existe brecha `[7,9)`.

### Ejercicio 3. Nivel intermedio: ubicar una observación

Escriba una consulta que devuelva observaciones junto con la ubicación válida y conserve aquellas sin historial.

#### Resolución paso a paso

**Paso 1. Partir de observación.** Es la entidad que no debe desaparecer.

**Paso 2. Usar `LEFT JOIN`.**

```sql
SELECT o.id_observacion,
       o.instante_observado_utc,
       ST_AsText(h.ubicacion) AS ubicacion_valida
FROM observacion_temporal AS o
LEFT JOIN historial_ubicacion_estacion AS h
  ON h.id_estacion = o.id_estacion
 AND h.valido_desde <= o.instante_observado_utc
 AND (h.valido_hasta IS NULL
      OR o.instante_observado_utc < h.valido_hasta)
ORDER BY o.id_observacion;
```

**Paso 3. Interpretar nulos.** `ubicacion_valida IS NULL` identifica ausencia histórica; no significa que la observación carezca necesariamente de estación.

**Paso 4. Auditar duplicados.** Se agrupa por observación y se exige una versión; un `LEFT JOIN` también puede producir varias filas si existen solapamientos.

### Ejercicio 4. Nivel avanzado: procesar un cambio tardío

El 20 de agosto llega una ubicación válida desde el 5 de agosto a las 12:00, dentro de una versión existente `[1 agosto,10 agosto 16:00)`. Diseñe la operación y sus controles.

#### Resolución paso a paso

**Paso 1. Iniciar transacción y recuperar la versión afectada.** Debe bloquearse para evitar cambios concurrentes.

**Paso 2. Conservar extremos.** Se registra el final original `10 agosto 16:00`.

**Paso 3. Acortar la versión previa.** Su nuevo final es `5 agosto 12:00`.

**Paso 4. Insertar la tardía.** Su intervalo es `[5 agosto 12:00,10 agosto 16:00)` con fuente y motivo.

**Paso 5. Auditar.** Se ejecutan controles de solapamiento, brecha, una sola versión abierta y cardinalidad por observación.

**Paso 6. Confirmar o revertir.** Solo se confirma si todos los controles esperados se cumplen.

**Paso 7. Registrar impacto.** Se identifican observaciones y derivados analíticos entre ambos extremos que necesitan reproceso.

## 13. Temas de profundización

### 13.1 Bitemporalidad

La bitemporalidad conserva simultáneamente cuándo un hecho fue válido en el dominio y cuándo estuvo registrado en la base. Permite reconstruir conocimiento retrospectivo, pero requiere versionar correcciones y no solo agregar `registrado_en`.

### 13.2 Coalescencia

Dos intervalos contiguos con igual valor pueden combinarse lógicamente en uno. Esta operación, denominada coalescencia, debe respetar procedencia y necesidades de auditoría; no siempre conviene borrar las versiones originales.

### 13.3 Trayectorias

Una trayectoria representa movimiento mediante posiciones ordenadas temporalmente y puede incluir interpolación. Las estaciones de ObservaSur cambian mediante versiones discretas; no se presume movimiento continuo entre puntos.

## 14. Referencia técnica

- Pertenencia: `desde <= t AND (hasta IS NULL OR t < hasta)`.
- Solapamiento: `a_desde < b_hasta AND b_desde < a_hasta`.
- Contigüidad: `a_hasta = b_desde`.
- `BETWEEN` incluye ambos extremos y no representa directamente `[desde,hasta)`.
- `LEAD()` y `LAG()` permiten comparar versiones adyacentes.
- `CHECK` no compara filas ni admite subconsultas.
- La columna generada más índice único limita versiones abiertas, no todo solapamiento.
- Recursos ejecutables: [`semana08_espacio_temporal.sql`](../observasur/sql/semana08_espacio_temporal.sql) y [`semana08_verificar_vigencias.py`](../observasur/python/semana08_verificar_vigencias.py).

El capítulo 9 iniciará la transición desde el sistema operacional hacia el análisis, comparando propósitos OLTP y OLAP y mostrando por qué las observaciones históricas requieren otra organización para agregaciones reproducibles.

## 15. Referencias bibliográficas

Jensen, C. S., Dyreson, C. E., Böhlen, M., Clifford, J., Elmasri, R., Gadia, S. K., Grandi, F., Hayes, P., Jajodia, S., Käfer, W., Kline, N., Lorentzos, N., Mitsopoulos, Y., Montanari, A., Nonen, D., Peressi, E., Pernici, B., Roddick, J. F., Sarda, N. L., ... Wiederhold, G. (1998). The consensus glossary of temporal database concepts—February 1998 version. En O. Etzion, S. Jajodia y S. Sripada (Eds.), *Temporal databases: Research and practice* (LNCS 1399, pp. 367–405). Springer. https://doi.org/10.1007/BFb0053710

MySQL. (2026). *MySQL 8.0 Reference Manual: CHECK constraints*. https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Comparison functions and operators*. https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Window function descriptions*. https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html

Snodgrass, R. T. (1999). *Developing time-oriented database applications in SQL*. Morgan Kaufmann.
