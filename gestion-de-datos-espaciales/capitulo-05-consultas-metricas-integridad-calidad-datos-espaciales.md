# Capítulo 5. Consultas métricas, integridad y calidad de datos espaciales

## Objetivos de aprendizaje

Al finalizar el capítulo, el estudiante será capaz de:

1. distinguir relación topológica, medida espacial y regla de proximidad;
2. interpretar una distancia de acuerdo con el sistema de referencia y su unidad;
3. formular consultas de distancia y proximidad mediante `ST_Distance()`;
4. explicar por qué un umbral forma parte de una regla del dominio y no de la geometría por sí sola;
5. diferenciar geometría sintácticamente bien formada de geometría geométricamente válida;
6. aplicar controles de tipo, SRID, nulabilidad, validez, dominio y procedencia;
7. diseñar una tabla de preparación (*staging*) que preserve la entrada original;
8. clasificar filas aceptadas y rechazadas sin perder evidencia del error;
9. coordinar Python y MySQL para procesar una carga controlada y producir un reporte reproducible;
10. reconocer los límites de una respuesta métrica cuando no existe formación suficiente sobre sistemas de referencia o calidad de medición.

Estos objetivos desarrollan R1–R4, con énfasis en consulta, administración e integridad de datos espaciales.

## Introducción

El capítulo anterior respondió preguntas topológicas: una estación está en el interior de una zona, toca su frontera o permanece fuera. Ahora se incorporan preguntas métricas: **¿qué estación está más cerca?, ¿qué significa “cerca” y en qué unidad se expresa la respuesta?**

La consulta parece sencilla:

```sql
ST_Distance(g1, g2)
```

Sin embargo, un número solo resulta interpretable si se conoce el sistema de referencia, la unidad, la calidad de las geometrías y el propósito del umbral utilizado. En el plano didáctico de ObservaSur, SRID 0 describe un espacio cartesiano abstracto sin unidad asignada. Por ello una distancia de 10 significa diez unidades del plano, no diez metros.

El segundo problema del capítulo aparece durante la carga. Una cadena puede parecer WKT y aun así contener un anillo abierto, un polígono autointersectado, un tipo inesperado, un SRID equivocado o coordenadas incompatibles con el dominio. No todas estas anomalías se detectan en la misma capa. Se necesita un flujo que conserve la entrada, aplique controles identificables y registre por qué una fila fue aceptada o rechazada.

La secuencia de aprendizaje será:

```text
pregunta de proximidad
    → distancia y unidad
    → umbral del dominio
    → geometrías confiables
    → staging y controles
    → aceptación o rechazo explicable
```

---

## 1. De las relaciones topológicas a las medidas

### 1.1 Predicados y funciones métricas

Un predicado topológico devuelve una condición lógica:

```text
Within(p,z) → verdadero o falso
Touches(p,z) → verdadero o falso
```

Una función métrica devuelve una magnitud:

```text
Distance(g1,g2) → número
```

Ambas familias responden preguntas diferentes. Dos estaciones pueden pertenecer a la misma zona y estar muy separadas; dos puntos en zonas distintas pueden estar próximos a una frontera común. La topología describe relaciones de inclusión, contacto o separación, mientras la métrica cuantifica propiedades como distancia, longitud o área [@guting1994, pp. 367–375; @rigaux2002, caps. 2–3].

### 1.2 Distancia como función

En un plano cartesiano, la distancia euclidiana entre puntos

\[
p_1=(x_1,y_1), \qquad p_2=(x_2,y_2)
\]

es:

\[
d(p_1,p_2)=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}.
\]

Para `EST-N01 = (25,75)` y `EST-N02 = (75,75)`:

\[
d=\sqrt{(75-25)^2+(75-75)^2}=50.
\]

En SRID 0, el resultado se interpreta como 50 unidades abstractas. El cálculo manual sirve como oráculo sencillo; MySQL debe realizar la operación sobre las geometrías persistidas.

### 1.3 Propiedades mínimas

Para geometrías puntuales cartesianas, la distancia satisface propiedades útiles para comprobar resultados:

1. no negatividad: \(d(a,b)\geq 0\);
2. identidad: \(d(a,a)=0\);
3. simetría: \(d(a,b)=d(b,a)\);
4. desigualdad triangular: \(d(a,c)\leq d(a,b)+d(b,c)\).

Estas propiedades no sustituyen un oráculo numérico, pero permiten detectar errores de orden, carga o interpretación.

## 2. Distancia en MySQL

### 2.1 `ST_Distance()`

MySQL calcula la distancia mínima entre dos geometrías mediante:

```sql
ST_Distance(g1, g2)
```

El resultado utiliza la unidad del SRS, salvo que se proporcione una unidad lineal admitida para un SRS apropiado [@mysqlSpatialRelations2026]. Para las estaciones de ObservaSur:

```sql
SELECT
    a.codigo AS estacion_a,
    b.codigo AS estacion_b,
    ST_Distance(a.ubicacion, b.ubicacion) AS distancia
FROM estacion_espacial AS a
JOIN estacion_espacial AS b
  ON a.codigo = 'EST-N01'
 AND b.codigo = 'EST-N02';
```

El resultado esperado es 50 unidades del plano.

### 2.2 Tipo de geometría y significado de la distancia

La función no se limita a punto–punto. Para geometrías generales devuelve la distancia mínima entre sus conjuntos de puntos. Esto implica:

- punto dentro de polígono: distancia 0;
- punto en la frontera: distancia 0;
- punto exterior: distancia positiva hasta el punto más próximo del polígono;
- dos polígonos que se intersectan: distancia 0.

Por tanto, distancia cero no significa necesariamente igualdad geométrica. Puede indicar intersección. La consulta topológica sigue siendo necesaria para distinguir interior, frontera y superposición.

### 2.3 SRID y compatibilidad

Los argumentos de una operación binaria deben tener el mismo SRID. Si difieren, MySQL produce error [@mysqlSpatialRelations2026; @mysqlSRS2026]. Que ambos tengan SRID 0 permite el cálculo, pero solo acredita que comparten la etiqueta del plano abstracto; no demuestra que sus coordenadas provengan realmente del mismo marco.

Antes de calcular se debe responder:

1. ¿ambas geometrías tienen el mismo SRID?;
2. ¿ese SRID representa el espacio en que fueron capturadas?;
3. ¿la unidad está definida?;
4. ¿el tipo de distancia es adecuado para la pregunta?;
5. ¿la calidad de origen permite la precisión comunicada?

### 2.4 Unidades admitidas y SRID 0

MySQL expone unidades aceptadas para `ST_Distance()` en `INFORMATION_SCHEMA.ST_UNITS_OF_MEASURE` [@mysqlUnits2026]. Sin embargo, solicitar una unidad lineal para geometrías SRID 0 produce un error porque el SRS no posee unidad conocida [@mysqlSpatialRelations2026]. Esta consulta no es válida para el plano didáctico:

```sql
-- No usar con SRID 0:
SELECT ST_Distance(g1, g2, 'metre');
```

No debe corregirse el error suprimiendo información en el informe y llamando “metros” al resultado sin respaldo.

### 2.5 `ST_Distance_Sphere()` no resuelve el contrato

`ST_Distance_Sphere()` calcula una distancia mínima sobre una esfera para combinaciones admitidas de puntos o multipuntos y devuelve metros [@mysqlConvenience2026]. En SRID 0 interpreta X e Y como longitud y latitud en grados. Aplicarla a las coordenadas ficticias de ObservaSur sería semánticamente incorrecto, aunque la función pudiera ejecutarse.

La regla es simple: no se selecciona una función porque entregue la unidad deseada; se selecciona porque su modelo corresponde a los datos.

## 3. Proximidad y umbrales

### 3.1 “Cerca” es una regla, no un tipo espacial

Una distancia es un valor. **Proximidad** es una clasificación construida mediante un umbral:

\[
cerca(a,b;t) \iff d(a,b)\leq t.
\]

El umbral \(t\) debe provenir de una necesidad: cobertura operativa, tiempo de respuesta, resolución del análisis u otra regla. MySQL puede aplicar el umbral, pero no decidir qué valor es significativo para la organización.

### 3.2 Consulta parametrizada de proximidad

Para buscar estaciones a no más de 40 unidades de un punto de referencia:

```sql
SELECT
    codigo,
    ST_Distance(
        ubicacion,
        ST_PointFromText('POINT(50 50)', 0)
    ) AS distancia
FROM estacion_espacial
WHERE ST_Distance(
        ubicacion,
        ST_PointFromText('POINT(50 50)', 0)
      ) <= 40
ORDER BY distancia, codigo;
```

La consulta calcula la distancia en `SELECT` y filtra por el umbral en `WHERE`. La repetición se puede encapsular en una expresión común:

```sql
WITH distancias AS (
    SELECT codigo,
           ST_Distance(
               ubicacion,
               ST_PointFromText('POINT(50 50)', 0)
           ) AS distancia
    FROM estacion_espacial
)
SELECT codigo, distancia
FROM distancias
WHERE distancia <= 40
ORDER BY distancia, codigo;
```

### 3.3 Orden y empates

Varias estaciones pueden estar a la misma distancia. Para obtener resultados reproducibles se agrega un segundo criterio:

```sql
ORDER BY distancia, codigo
```

`LIMIT 1` sin una política de desempate puede seleccionar arbitrariamente entre candidatos equivalentes. Si se necesitan todas las estaciones más cercanas, primero se calcula la distancia mínima y luego se recuperan todas las filas que la igualan dentro de una tolerancia numérica justificada.

### 3.4 Precisión comunicada

MySQL puede devolver muchos decimales, pero esos dígitos no acreditan exactitud. En un informe pueden redondearse para presentación, conservando el valor sin redondear para comparación:

```sql
SELECT codigo,
       ST_Distance(ubicacion, ST_PointFromText(?, 0)) AS distancia_calculo,
       ROUND(ST_Distance(ubicacion, ST_PointFromText(?, 0)), 2)
           AS distancia_presentada
FROM estacion_espacial;
```

Los marcadores concretos dependen del cliente; en Connector/Python se usa `%s`, no `?`.

## 4. Integridad y calidad espacial

### 4.1 Integridad como conjunto de capas

La integridad espacial no es una sola prueba. Conviene separar:

| Capa | Pregunta | Ejemplo de control |
|---|---|---|
| sintáctica | ¿puede construirse la geometría? | WKT y anillos cerrados |
| estructural | ¿tipo, SRID y nulabilidad son correctos? | `POINT NOT NULL SRID 0` |
| geométrica | ¿la forma es válida? | `ST_IsValid()` |
| dominio | ¿los valores son plausibles para ObservaSur? | x e y entre 0 y 100 |
| relacional | ¿las referencias existen? | clave foránea de estación |
| coherencia espacial | ¿las relaciones esperadas se cumplen? | estación y zona declarada |
| procedencia | ¿se conoce fuente y transformación? | archivo, fila y fecha de carga |

Una fila puede superar una capa y fallar en otra. Un punto `POINT(500 500)` es sintácticamente correcto y geométricamente válido, pero está fuera del dominio acordado del plano ObservaSur.

### 4.2 Bien formada y válida no significan lo mismo

MySQL distingue geometrías sintácticamente bien formadas de geometrías geométricamente válidas. Un polígono bien formado posee anillos cerrados con el mínimo estructural requerido; aun así puede ser inválido si se autointersecta. Las funciones de importación rechazan geometrías mal formadas, pero MySQL puede almacenar geometrías bien formadas que sean geométricamente inválidas [@mysqlValidity2026].

Ejemplos:

```text
POLYGON((0 0,10 0,10 10,0 10))
→ mal formado: el anillo no cierra

POLYGON((0 0,10 10,10 0,0 10,0 0))
→ bien formado sintácticamente, pero inválido por autointersección
```

### 4.3 `ST_IsValid()`

La validez debe comprobarse explícitamente:

```sql
SELECT
    id_zona,
    nombre,
    ST_IsValid(extension) AS es_valida
FROM zona_espacial;
```

Operar con geometrías inválidas puede producir error o resultados indefinidos. La validación debe preceder a consultas cuyas conclusiones dependan de esas formas [@mysqlValidity2026; @mysqlConvenience2026].

Para puntos simples, la validez geométrica rara vez constituye el principal problema; predominan SRID, orden de ejes, dominio y procedencia. Para polígonos, anillos y autointersecciones requieren mayor atención.

### 4.4 Restricciones declarativas y controles de carga

Tipo, SRID y nulabilidad pertenecen al esquema. Rangos escalares de entrada pueden protegerse con `CHECK` en tablas de preparación. MySQL aplica restricciones `CHECK` desde la versión 8.0.16 [@mysqlCheckConstraints2026]. Sin embargo, no toda función o regla espacial resulta adecuada para una restricción declarativa. Las reglas costosas, dependientes de otras filas o que necesitan explicar rechazos pueden gestionarse mejor en un proceso de carga verificable.

El principio no es mover toda validación a Python, sino ubicar cada regla donde pueda aplicarse de manera confiable y auditable.

## 5. Preparación de datos mediante *staging*

### 5.1 Por qué no cargar directamente

Una inserción directa mezcla lectura, conversión, validación y persistencia. Cuando una fila falla, puede ser difícil reconstruir qué se recibió. Una tabla de *staging* conserva la entrada en una forma cercana a la fuente antes de promoverla al esquema espacial.

```text
archivo o formulario
       ↓
staging textual y trazable
       ↓ controles
aceptada ─────────────→ tabla espacial candidata
       └─ rechazada ─→ estado y motivo
```

### 5.2 Esquema de preparación

```sql
CREATE TABLE IF NOT EXISTS staging_ubicacion (
    id_staging BIGINT AUTO_INCREMENT PRIMARY KEY,
    codigo_estacion VARCHAR(12) NOT NULL,
    wkt_original VARCHAR(500) NULL,
    srid_declarado BIGINT NULL,
    fuente VARCHAR(120) NOT NULL,
    numero_fila INT NOT NULL,
    instante_carga DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente','aceptada','rechazada') NOT NULL
        DEFAULT 'pendiente',
    motivo_rechazo VARCHAR(500) NULL,
    UNIQUE (fuente, numero_fila)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS ubicacion_candidata (
    codigo_estacion VARCHAR(12) PRIMARY KEY,
    ubicacion POINT NOT NULL SRID 0,
    id_staging BIGINT NOT NULL UNIQUE,
    CONSTRAINT fk_candidata_estacion
        FOREIGN KEY (codigo_estacion)
        REFERENCES estacion_espacial (codigo),
    CONSTRAINT fk_candidata_staging
        FOREIGN KEY (id_staging)
        REFERENCES staging_ubicacion (id_staging)
) ENGINE = InnoDB;
```

`wkt_original` admite `NULL` y texto incorrecto porque su propósito es conservar lo recibido, no fingir que ya es geometría válida.

### 5.3 Reglas de aceptación

Para la práctica se acuerdan reglas mínimas:

1. la estación debe existir;
2. WKT no puede estar vacío;
3. SRID declarado debe ser 0;
4. la cadena debe construir una geometría bien formada;
5. el tipo debe ser `POINT`;
6. `ST_IsValid()` debe devolver 1;
7. X e Y deben pertenecer al intervalo `[0,100]`;
8. toda aceptación conserva `id_staging`.

Estas reglas son explícitas y comprobables. El rango `[0,100]` pertenece al caso didáctico, no es una regla universal para puntos espaciales.

### 5.4 Rechazo explicable

Un reporte útil no se limita a “error de datos”. Debe registrar categorías como:

- `ESTACION_INEXISTENTE`;
- `WKT_AUSENTE`;
- `WKT_MAL_FORMADO`;
- `SRID_INCORRECTO`;
- `TIPO_INESPERADO`;
- `GEOMETRIA_INVALIDA`;
- `FUERA_DE_DOMINIO`;
- `ERROR_BASE_DATOS`.

El mensaje técnico original puede conservarse en una bitácora controlada, pero el estudiante debe producir una categoría estable que pueda contarse y explicarse.

## 6. Procesamiento coordinado con Python y MySQL

### 6.1 Python orquesta; MySQL valida lo espacial

Python leerá filas pendientes y gestionará el flujo. Para cada fila:

1. comprueba presencia y tipos escalares básicos;
2. solicita a MySQL construir e inspeccionar la geometría;
3. clasifica el resultado;
4. inserta la candidata aceptada o registra rechazo;
5. confirma una decisión reproducible.

No se requiere una biblioteca espacial de Python. La función `ST_GeomFromText()` y los controles espaciales se ejecutan en MySQL.

### 6.2 Inspección parametrizada

```python
INSPECCION = """
    WITH valor AS (
        SELECT ST_GeomFromText(%s, %s) AS g
    )
    SELECT ST_GeometryType(g) AS tipo,
           ST_SRID(g) AS srid,
           ST_IsValid(g) AS es_valida,
           ST_X(g) AS x,
           ST_Y(g) AS y
    FROM valor
"""
```

Esta consulta supone que el valor debe ser puntual; si el tipo no es `POINT`, aplicar `ST_X()` o `ST_Y()` puede generar un error de tipo. Una implementación robusta usa dos etapas: primero obtiene tipo, SRID y validez; solo después consulta X e Y para puntos.

```python
INSPECCION_1 = """
    WITH valor AS (SELECT ST_GeomFromText(%s, %s) AS g)
    SELECT ST_GeometryType(g) AS tipo,
           ST_SRID(g) AS srid,
           ST_IsValid(g) AS es_valida
    FROM valor
"""

INSPECCION_PUNTO = """
    WITH valor AS (SELECT ST_PointFromText(%s, %s) AS g)
    SELECT ST_X(g) AS x, ST_Y(g) AS y
    FROM valor
"""
```

### 6.3 Transacción por fila y trazabilidad

Una estrategia introductoria procesa cada fila como unidad de trabajo. Si falla la construcción, se revierte la promoción, pero se registra el rechazo en una operación controlada. Para lotes grandes se usarían políticas más eficientes; aquí importa que ningún dato desaparezca silenciosamente.

```python
def marcar_rechazo(conexion, id_staging, motivo):
    sentencia = """
        UPDATE staging_ubicacion
        SET estado = 'rechazada', motivo_rechazo = %s
        WHERE id_staging = %s
    """
    with conexion.cursor() as cursor:
        cursor.execute(sentencia, (motivo, id_staging))
    conexion.commit()
```

Las consultas parametrizadas mantienen datos y sintaxis separados, siguiendo la interfaz de Connector/Python [@mysqlConnectorExecute2026].

### 6.4 No ocultar excepciones

Este patrón es inadecuado:

```python
try:
    procesar(fila)
except Exception:
    pass
```

Elimina evidencia. El flujo correcto captura la excepción, revierte el cambio incompleto, clasifica el motivo, registra la decisión y permite resumir los resultados.

## 7. Consultas métricas parametrizadas desde Python

### 7.1 Punto y umbral como parámetros

```python
def buscar_cercanas(conexion, x, y, umbral):
    x = float(x)
    y = float(y)
    umbral = float(umbral)
    if umbral < 0:
        raise ValueError("El umbral no puede ser negativo")

    wkt = f"POINT({x} {y})"
    consulta = """
        WITH distancias AS (
            SELECT codigo,
                   ST_Distance(
                       ubicacion,
                       ST_PointFromText(%s, 0)
                   ) AS distancia
            FROM estacion_espacial
        )
        SELECT codigo, distancia
        FROM distancias
        WHERE distancia <= %s
        ORDER BY distancia, codigo
    """
    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute(consulta, (wkt, umbral))
        return cursor.fetchall()
```

Python valida que el umbral sea numérico y no negativo; MySQL construye el punto y calcula distancias. La salida debe etiquetarse “unidades del plano ObservaSur”.

### 7.2 Pruebas de umbral

Para el punto `(50,50)`:

| Estación | Distancia esperada aproximada |
|---|---:|
| EST-S02 | 0.000 |
| EST-N01 | 35.355 |
| EST-N02 | 35.355 |
| EST-S01 | 35.355 |

Con umbral 35, solo aparece `EST-S02`. Con umbral 36 aparecen las cuatro. El cambio muestra que la clasificación depende del umbral y que los valores cercanos a él requieren atención a precisión y redondeo.

### 7.3 Comparar con tolerancia

Los cálculos de punto flotante no siempre deben compararse mediante igualdad textual. Para verificar una distancia esperada \(e\) y una obtenida \(o\) puede utilizarse:

\[
|o-e|\leq \varepsilon,
\]

donde \(\varepsilon\) se declara según el problema. Elegir una tolerancia enorme para hacer pasar una prueba invalida la comprobación.

## 8. Procedencia y reporte de calidad

### 8.1 Procedencia mínima

Una geometría aceptada debe poder relacionarse con:

- archivo o fuente;
- número de fila o identificador original;
- instante de carga;
- WKT recibido;
- SRID declarado;
- reglas aplicadas;
- estado final;
- versión del proceso si corresponde.

Esta información permitirá reconstruir cómo un dato operacional llegó después al almacén y al conjunto analítico.

### 8.2 Reconciliación de recuentos

Todo lote debe satisfacer:

\[
filas\ recibidas = filas\ aceptadas + filas\ rechazadas + filas\ pendientes.
\]

Una consulta de control es:

```sql
SELECT estado, COUNT(*) AS cantidad
FROM staging_ubicacion
GROUP BY estado
ORDER BY estado;
```

También se deben contar motivos:

```sql
SELECT motivo_rechazo, COUNT(*) AS cantidad
FROM staging_ubicacion
WHERE estado = 'rechazada'
GROUP BY motivo_rechazo
ORDER BY cantidad DESC, motivo_rechazo;
```

### 8.3 Calidad no equivale a ausencia de errores

Una tasa baja de rechazo no demuestra alta calidad si las reglas son débiles. Una tasa alta tampoco demuestra necesariamente una fuente inútil: puede revelar que cambió el contrato, que los metadatos son insuficientes o que el proceso de captura necesita corrección.

El reporte debe responder:

1. qué se recibió;
2. qué reglas se aplicaron;
3. cuántas filas superaron cada etapa;
4. qué motivos explican los rechazos;
5. qué limitaciones permanecen;
6. qué acciones se recomiendan sin alterar silenciosamente los datos.

## 9. Síntesis del núcleo obligatorio

```text
distancia
    → magnitud dependiente del SRS

proximidad
    → distancia comparada con umbral del dominio

bien formada
    → estructura sintáctica aceptable

válida
    → geometría coherente según reglas geométricas

staging
    → conserva entrada y procedencia

aceptación/rechazo
    → decisión basada en reglas y evidencia
```

Hasta aquí es obligatorio no llamar metros a unidades abstractas, no confundir ejecución con validez y no eliminar filas incorrectas sin registrar su procedencia y motivo.

## 10. Ejercicios y casos prácticos

### Ejercicio 1. Nivel básico: calcular e interpretar distancia

Calcule manualmente la distancia entre `POINT(25 75)` y `POINT(50 50)`. Escriba la consulta MySQL y declare correctamente la unidad.

#### Resolución paso a paso

**Paso 1. Aplicar la fórmula.**

\[
d=\sqrt{(50-25)^2+(50-75)^2}
=\sqrt{625+625}=\sqrt{1250}\approx35.355.
\]

**Paso 2. Escribir SQL.**

```sql
SELECT ST_Distance(
    ST_PointFromText('POINT(25 75)', 0),
    ST_PointFromText('POINT(50 50)', 0)
) AS distancia;
```

**Paso 3. Interpretar.** El resultado es aproximadamente 35,355 unidades abstractas del plano SRID 0. No se informa en metros.

### Ejercicio 2. Nivel básico–intermedio: analizar un umbral

Explique por qué las consultas `distancia < 35.355` y `distancia <= 35.355` pueden clasificar de manera distinta una estación cuyo valor real aproximado es `35.355339...`.

#### Resolución paso a paso

**Paso 1. Reconocer el redondeo.** `35.355` es una presentación truncada o redondeada, no el valor completo.

**Paso 2. Comparar.** El valor real es mayor que `35.355`; por ello ambas condiciones lo excluyen.

**Paso 3. Evitar comparar la presentación.** El filtro debe usar la distancia sin redondear y un umbral definido por el dominio.

**Paso 4. Documentar inclusión.** Si el límite debe incluir exactamente 36 unidades, se usa `<= 36`; el operador forma parte de la regla.

### Ejercicio 3. Nivel intermedio: clasificar anomalías

Clasifique los siguientes registros: A, WKT nulo; B, `POLYGON((0 0,10 0,10 10,0 10))`; C, `LINESTRING(0 0,10 10)` para una ubicación puntual; D, `POINT(500 500)` con SRID 0; E, `POINT(25 75)` con SRID 4326.

#### Resolución paso a paso

**A.** `WKT_AUSENTE`: falla presencia antes de construir.

**B.** `WKT_MAL_FORMADO`: el anillo no está cerrado; el constructor debe rechazarlo.

**C.** `TIPO_INESPERADO`: la geometría puede estar bien formada, pero no es `POINT`.

**D.** `FUERA_DE_DOMINIO`: es punto válido y SRID correcto, pero excede `[0,100]`.

**E.** `SRID_INCORRECTO`: el contrato de la columna y del caso exige 0. Cambiar la etiqueta a 0 sin conocer el origen no constituye una transformación válida.

### Ejercicio 4. Nivel avanzado: diseñar un flujo de carga verificable

Diseñe el procesamiento de un lote de seis filas de ubicación, de las cuales cuatro son válidas, una tiene WKT mal formado y otra está fuera de dominio. Indique estados, transacciones y reconciliación.

#### Resolución paso a paso

**Paso 1. Registrar las seis filas.** Todas ingresan a `staging_ubicacion` como `pendiente`, preservando fuente y número de fila.

**Paso 2. Procesar cada fila.** La construcción y promoción de cada candidata se realiza en una unidad transaccional controlada.

**Paso 3. Aceptar cuatro.** Se insertan en `ubicacion_candidata` con referencia a `id_staging`; luego su estado cambia a `aceptada`.

**Paso 4. Rechazar WKT incorrecto.** Se revierte cualquier promoción parcial y se registra `WKT_MAL_FORMADO`.

**Paso 5. Rechazar el punto plausible sintácticamente.** La comprobación de X/Y detecta el incumplimiento y registra `FUERA_DE_DOMINIO`.

**Paso 6. Reconciliar.**

```text
recibidas = 6
aceptadas = 4
rechazadas = 2
pendientes = 0
6 = 4 + 2 + 0
```

**Paso 7. Informar límites.** La aceptación acredita las reglas implementadas, no exactitud de terreno ni corrección de la fuente original.

## 11. Temas de profundización

### 11.1 Distancias geodésicas y proyectadas

Los SRS geográficos y proyectados requieren conocimientos de referencia, unidades y propiedades métricas que exceden este núcleo. MySQL admite cálculos geográficos en funciones determinadas, pero seleccionar SRS y método exige una justificación geomática. No se aplicarán códigos reales por apariencia.

### 11.2 Restricciones espaciales avanzadas

Disparadores, procedimientos y procesos externos pueden reforzar reglas que no caben en una declaración de columna. Su conveniencia depende de costo, concurrencia, claridad del error y posibilidad de pruebas. Una regla central debe evitar duplicarse de manera divergente entre múltiples clientes.

### 11.3 Reparación de geometrías

Corregir automáticamente una geometría puede cambiar su forma y significado. Toda reparación requiere conservar el original, registrar el algoritmo, comparar antes/después y definir quién autoriza el resultado. Rechazar de forma explicable suele ser más seguro que “arreglar” silenciosamente.

## 12. Referencia técnica

- `ST_Distance(g1,g2)`: distancia mínima en la unidad del SRS.
- `ST_Distance(g1,g2,unidad)`: conversión a una unidad admitida cuando el SRS posee unidad conocida.
- `ST_Distance_Sphere()`: caso esférico específico; no es sustituto universal.
- `ST_IsValid(g)`: control explícito de validez geométrica.
- `ST_GeometryType(g)`, `ST_SRID(g)`, `ST_X(g)` y `ST_Y(g)`: inspección estructural.
- `INFORMATION_SCHEMA.ST_UNITS_OF_MEASURE`: catálogo de unidades aceptables.
- El SRID 0 no asigna metros ni otra unidad a sus ejes.
- Una carga explicable conserva entrada, procedencia, estado y motivo.
- Recursos ejecutables: [`semana05_calidad_espacial.sql`](../observasur/sql/semana05_calidad_espacial.sql) y [`semana05_procesar_staging.py`](../observasur/python/semana05_procesar_staging.py).

El capítulo 6 estudiará cómo ejecutar consultas espaciales sobre conjuntos mayores sin revisar innecesariamente todas las parejas, mediante rectángulos envolventes, índices espaciales y lectura básica de planes.

## 13. Referencias bibliográficas

Güting, R. H. (1994). An introduction to spatial database systems. *The VLDB Journal, 3*, 357–399. https://doi.org/10.1007/BF01231602

MySQL. (2026). *MySQL 8.0 Reference Manual: CHECK constraint metadata*. https://dev.mysql.com/doc/refman/8.0/en/information-schema-check-constraints-table.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Geometry well-formedness and validity*. https://dev.mysql.com/doc/refman/8.0/en/geometry-well-formedness-validity.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Spatial convenience functions*. https://dev.mysql.com/doc/refman/8.0/en/spatial-convenience-functions.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Spatial relation functions that use object shapes*. https://dev.mysql.com/doc/refman/8.0/en/spatial-relation-functions-object-shapes.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Spatial reference system support*. https://dev.mysql.com/doc/refman/8.0/en/spatial-reference-systems.html

MySQL. (2026). *MySQL 8.0 Reference Manual: The INFORMATION_SCHEMA ST_UNITS_OF_MEASURE table*. https://dev.mysql.com/doc/refman/8.0/en/information-schema-st-units-of-measure-table.html

MySQL. (2026). *MySQL Connector/Python Developer Guide: MySQLCursor.execute() method*. https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

Rigaux, P., Scholl, M. y Voisard, A. (2002). *Spatial databases: With application to GIS*. Morgan Kaufmann.
