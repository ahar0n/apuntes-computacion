# Capítulo 3. Modelado e implementación de geometrías en MySQL

## Objetivos de aprendizaje

Al finalizar el capítulo, el estudiante será capaz de:

1. traducir una decisión conceptual sobre posición, trazado o extensión a una columna geométrica apropiada;
2. distinguir el tipo general `GEOMETRY` de los tipos específicos `POINT`, `LINESTRING` y `POLYGON`;
3. declarar columnas geométricas con nulabilidad y SRID explícitos en MySQL 8.0;
4. construir valores geométricos desde WKT mediante funciones constructoras;
5. insertar y recuperar geometrías sin confundir su codificación de intercambio con su representación interna;
6. integrar consultas parametrizadas de Python con funciones espaciales ejecutadas por MySQL;
7. diseñar controles iniciales de tipo, SRID, recuento y correspondencia entre valores esperados y obtenidos;
8. documentar el significado y las restricciones de una columna espacial en un diccionario de datos;
9. ejecutar una migración controlada desde coordenadas escalares hacia geometrías, conservando trazabilidad.

Estos objetivos desarrollan principalmente R1, R2 y R4 y preparan las consultas espaciales correspondientes a R3.

## Introducción

Los capítulos anteriores establecieron dos conclusiones. Primero, una propiedad espacial no queda adecuadamente modelada solo porque una tabla contenga números que parecen coordenadas. Segundo, una geometría debe interpretarse junto con su tipo y su sistema de referencia. Este capítulo convierte esas conclusiones en decisiones de esquema y operaciones reproducibles.

La pregunta guía es: **¿cómo puede la base de datos conservar la posición de una estación y la extensión de una zona de manera que su significado sea explícito y comprobable?** La respuesta exige coordinar tres niveles:

```text
decisión del modelo → declaración de columna → valor geométrico
```

Python participará como cliente: leerá valores, construirá parámetros, ejecutará sentencias y comparará resultados. MySQL será responsable de construir el valor espacial, comprobar la compatibilidad con la columna, persistirlo y exponer sus propiedades. Esta distribución evita convertir Python en una segunda base de datos espacial.

El alcance es deliberado. Aquí se implementan geometrías y controles estructurales iniciales. Las relaciones topológicas se desarrollarán en el capítulo 4; las medidas, la validez y la calidad espacial, en el capítulo 5; y los índices espaciales, en el capítulo 6.

---

## 1. Del modelo conceptual al esquema físico

### 1.1 Propiedad espacial y atributo geométrico

Una columna geométrica debe corresponder a una propiedad definida del dominio. Para ObservaSur se adoptan inicialmente estas decisiones:

| Entidad | Propiedad espacial | Geometría | Justificación |
|---|---|---|---|
| estación | posición operativa | `POINT` | interesa una ubicación puntual, no el perímetro del recinto |
| zona | extensión operativa | `POLYGON` | interesa representar una superficie delimitada |
| recorrido de inspección | trazado planificado | `LINESTRING` | interesa una secuencia ordenada de posiciones |

La decisión precede a la sintaxis. Declarar `POINT` no demuestra por sí solo que una entidad deba modelarse como punto; únicamente hace cumplir una decisión ya justificada.

### 1.2 Tipo específico o tipo general

MySQL ofrece `GEOMETRY` como supertipo capaz de almacenar distintas clases geométricas, y tipos específicos que restringen la columna. Entre ellos se encuentran `POINT`, `LINESTRING` y `POLYGON` [@mysqlSpatialTypes2026]. Por ejemplo:

```sql
ubicacion GEOMETRY SRID 0
```

admite distintos tipos de geometría con SRID 0. En cambio:

```sql
ubicacion POINT SRID 0
```

declara que cada valor no nulo debe ser puntual. Cuando el dominio conoce la clase esperada, el tipo específico expresa mejor la semántica y permite que el SGBD rechace incompatibilidades. `GEOMETRY` resulta apropiado solo cuando la heterogeneidad geométrica forma parte real del atributo, no como sustituto de una decisión de modelado.

Este criterio prolonga una regla conocida de Base de Datos I: se elige el dominio más específico que represente los valores válidos. Así como una fecha no debería almacenarse como texto arbitrario, la posición puntual de una estación no debería declararse como una geometría de cualquier clase sin necesidad.

### 1.3 Una geometría es un valor de una columna

El modelo relacional no desaparece. Una fila continúa representando una proposición sobre una entidad y una columna continúa tomando valores de un dominio. La diferencia es que el dominio geométrico posee estructura y operaciones especializadas, una característica central de los sistemas de bases de datos espaciales [@guting1994, pp. 357–364; @rigaux2002, caps. 1–2]. La clave primaria sigue identificando la estación; la geometría no reemplaza esa identidad.

Por tanto, estas expresiones responden preguntas diferentes:

```text
id_estacion = 3        → ¿qué registro es?
ubicacion = POINT(...) → ¿qué posición se registró?
```

Dos estaciones podrían compartir temporalmente una posición sin convertirse en la misma estación. A la inversa, una estación puede cambiar de ubicación conservando su identidad. El historial de ese cambio se abordará en los capítulos temporales.

## 2. Contrato de una columna geométrica

### 2.1 Componentes del contrato

Una declaración espacial mínima debe decidir:

1. **tipo geométrico:** qué estructura se admite;
2. **SRID:** bajo qué sistema se interpretan las coordenadas;
3. **nulabilidad:** si la propiedad es obligatoria en el estado operativo;
4. **significado:** qué propiedad del dominio representa;
5. **procedencia:** de dónde proviene el valor;
6. **reglas complementarias:** qué condiciones no expresa el tipo por sí solo.

En MySQL 8.0, una columna espacial puede incluir un atributo `SRID`. Una columna restringida por SRID acepta solo valores asociados a ese identificador; una incompatibilidad produce error [@mysqlSpatialTypes2026; @mysqlCreateSpatialColumns2026].

### 2.2 SRID 0 en el plano didáctico

ObservaSur utiliza inicialmente un plano cartesiano abstracto de 100 por 100 unidades. En MySQL, el SRID 0 representa un plano cartesiano abstracto sin unidad asignada y es el SRID espacial predeterminado [@mysqlSRS2026]. Por ello se declara:

```sql
ubicacion POINT SRID 0
```

Esta elección no autoriza a interpretar las coordenadas como longitud y latitud ni las distancias como metros. Su valor pedagógico consiste en separar el aprendizaje del tipo espacial de una formación cartográfica que el estudiantado aún no posee.

### 2.3 Nulabilidad y estados transitorios

`NOT NULL` expresa que toda fila debe poseer una geometría. Es una buena meta para estaciones operativas, pero una migración desde un esquema previo puede requerir un estado transitorio:

1. agregar la columna permitiendo `NULL`;
2. construir las geometrías a partir de datos existentes;
3. comprobar que ninguna fila permanezca sin valor;
4. convertir la columna a `NOT NULL`.

La secuencia distingue el **estado final válido** del **procedimiento necesario para alcanzarlo**. Intentar agregar directamente una columna obligatoria a una tabla poblada puede fracasar o forzar valores artificiales.

### 2.4 Restricciones expresadas y no expresadas

La declaración:

```sql
ubicacion POINT NOT NULL SRID 0
```

controla tipo, presencia y SRID. No demuestra, por sí sola, que:

- el punto corresponda a la estación correcta;
- las coordenadas provengan de una fuente confiable;
- el punto esté dentro de una zona determinada;
- la geometría posea la exactitud requerida;
- el valor no haya sido intercambiado en sus ejes.

La integridad espacial se construye por capas. Este capítulo cubre integridad estructural; los siguientes incorporarán relaciones, métricas, validez y controles de carga.

## 3. Creación y migración del esquema ObservaSur

### 3.1 Esquema espacial de destino

Una implementación nueva puede declarar las geometrías desde el comienzo:

```sql
CREATE TABLE zona_espacial (
    id_zona SMALLINT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL UNIQUE,
    extension POLYGON NOT NULL SRID 0
) ENGINE = InnoDB;

CREATE TABLE estacion_espacial (
    id_estacion INT PRIMARY KEY,
    codigo VARCHAR(12) NOT NULL UNIQUE,
    nombre VARCHAR(80) NOT NULL,
    ubicacion POINT NOT NULL SRID 0,
    id_zona_declarada SMALLINT NOT NULL,
    CONSTRAINT fk_estacion_espacial_zona
        FOREIGN KEY (id_zona_declarada)
        REFERENCES zona_espacial (id_zona)
) ENGINE = InnoDB;
```

La clave foránea conserva la asignación administrativa declarada. La geometría permitirá calcular posteriormente una relación espacial. Ambas pueden discrepar, y esa discrepancia constituye información que debe investigarse, no ocultarse.

### 3.2 Migración desde coordenadas escalares

El esquema inicial ya contiene `coordenada_x` y `coordenada_y`. Una migración controlada agrega y completa la nueva columna:

```sql
ALTER TABLE estacion
    ADD COLUMN ubicacion POINT SRID 0 NULL;

UPDATE estacion
SET ubicacion = ST_PointFromText(
    CONCAT('POINT(', coordenada_x, ' ', coordenada_y, ')'),
    0
);

SELECT COUNT(*) AS filas_sin_ubicacion
FROM estacion
WHERE ubicacion IS NULL;

ALTER TABLE estacion
    MODIFY COLUMN ubicacion POINT NOT NULL SRID 0;
```

`ST_PointFromText()` interpreta WKT puntual y construye una geometría con el SRID indicado. El segundo argumento es crucial: no transforma coordenadas; especifica el SRS en el que se construye el valor.

Las columnas antiguas no deben eliminarse inmediatamente. Durante la transición permiten comprobar correspondencia y recuperar el estado previo si se detecta un error. La eliminación, si se decide, debe ocurrir después de validar la migración y conservar un respaldo o procedimiento reproducible.

### 3.3 Incorporación de zonas

Las zonas Norte y Sur del plano didáctico pueden definirse mediante dos polígonos:

```sql
ALTER TABLE zona
    ADD COLUMN extension POLYGON SRID 0 NULL;

UPDATE zona
SET extension = CASE id_zona
    WHEN 1 THEN ST_PolygonFromText(
        'POLYGON((0 50,100 50,100 100,0 100,0 50))', 0)
    WHEN 2 THEN ST_PolygonFromText(
        'POLYGON((0 0,100 0,100 50,0 50,0 0))', 0)
END;

SELECT COUNT(*) AS zonas_sin_extension
FROM zona
WHERE extension IS NULL;

ALTER TABLE zona
    MODIFY COLUMN extension POLYGON NOT NULL SRID 0;
```

El anillo exterior repite su primer punto al final. En esta etapa se comprueba la construcción y el almacenamiento; la pertenencia de estaciones a zonas se reservará para el capítulo 4.

## 4. Construcción de valores geométricos

### 4.1 Constructor, argumento y resultado

Una función constructora recibe una codificación y devuelve un valor geométrico. La arquitectura de geometrías simples y sus representaciones normalizadas se apoyan en el estándar OGC Simple Feature Access [@ogcSFA2011, secs. 6–7]. El patrón es:

```sql
ST_GeomFromText(wkt, srid)
```

Por ejemplo:

```sql
SELECT ST_GeomFromText('POINT(25 75)', 0);
```

La cadena WKT es entrada textual; el resultado es un valor geométrico. MySQL almacena internamente geometrías mediante un encabezado de cuatro bytes para el SRID seguido de WKB, por lo que no debe suponerse que guarda literalmente la cadena WKT [@mysqlStorage2026].

### 4.2 Constructores generales y específicos

El constructor general acepta varias clases geométricas:

```sql
ST_GeomFromText('LINESTRING(0 0,50 50,100 50)', 0)
```

Los constructores específicos comunican una expectativa más precisa:

```sql
ST_PointFromText('POINT(25 75)', 0)
ST_LineStringFromText('LINESTRING(0 0,50 50)', 0)
ST_PolygonFromText('POLYGON((0 0,10 0,10 10,0 10,0 0))', 0)
```

Cuando la columna y el caso esperan una clase determinada, el constructor específico mejora la legibilidad. El tipo de la columna continúa siendo la defensa definitiva frente a un valor incompatible.

### 4.3 Errores como evidencia del contrato

Considérese:

```sql
INSERT INTO estacion_espacial
    (id_estacion, codigo, nombre, ubicacion, id_zona_declarada)
VALUES
    (10, 'EST-X10', 'Ensayo',
     ST_GeomFromText('LINESTRING(0 0,10 10)', 0), 1);
```

El valor construido es una línea, pero la columna exige un punto. El rechazo no es un obstáculo accidental: demuestra que el esquema está haciendo cumplir parte del modelo. Un laboratorio riguroso registra tanto casos aceptados como rechazados y explica qué regla observó.

## 5. Recuperación e inspección de geometrías

### 5.1 Volver a una representación legible

Un cliente no debe interpretar directamente la representación binaria interna. Para presentar o intercambiar una geometría se utiliza una función de salida:

```sql
SELECT
    codigo,
    ST_AsText(ubicacion) AS ubicacion_wkt
FROM estacion
ORDER BY codigo;
```

`ST_AsText()` produce WKT. El resultado sirve para inspección, comparación didáctica e intercambio simple, pero no modifica el valor almacenado.

### 5.2 Inspección de tipo y SRID

Las propiedades estructurales pueden consultarse explícitamente:

```sql
SELECT
    codigo,
    ST_GeometryType(ubicacion) AS tipo,
    ST_SRID(ubicacion) AS srid,
    ST_AsText(ubicacion) AS wkt
FROM estacion
ORDER BY id_estacion;
```

`ST_GeometryType()` devuelve el nombre del tipo geométrico y `ST_SRID()` devuelve el identificador asociado [@mysqlGeometryProperties2026]. El resultado esperado para las estaciones es `POINT`, SRID 0 y una representación WKT consistente con las coordenadas originales.

### 5.3 Consulta del catálogo

El esquema también puede inspeccionarse mediante metadatos:

```sql
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    SRS_ID,
    GEOMETRY_TYPE_NAME
FROM INFORMATION_SCHEMA.ST_GEOMETRY_COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME, COLUMN_NAME;
```

Esta consulta responde qué declaró la base, no solo qué parece contener una fila. La vista incluye, entre otros metadatos, nombre de tabla, nombre de columna, tipo geométrico y SRID [@mysqlGeometryColumns2026]. La distinción es análoga a consultar metadatos de columnas escalares en `INFORMATION_SCHEMA`.

## 6. Integración segura con Python

### 6.1 Distribución de responsabilidades

En el flujo adoptado:

| Python | MySQL |
|---|---|
| leer una fila de archivo o interfaz | ejecutar el constructor espacial |
| convertir valores escalares | comprobar compatibilidad con tipo y SRID |
| preparar parámetros | persistir dentro de una transacción |
| capturar y registrar errores | recuperar propiedades espaciales |
| comparar esperado y obtenido | mantener restricciones del esquema |

Python no necesita una biblioteca SIG para esta práctica. El objetivo es aprender a usar correctamente las capacidades espaciales de MySQL sin hacer del ecosistema Python una barrera de entrada.

### 6.2 Consulta parametrizada

Una inserción segura mantiene la sintaxis SQL fija y transmite los datos como parámetros:

```python
def insertar_estacion(conexion, registro):
    sentencia = """
        INSERT INTO estacion_espacial
            (id_estacion, codigo, nombre, ubicacion, id_zona_declarada)
        VALUES
            (%s, %s, %s, ST_PointFromText(%s, 0), %s)
    """

    wkt = f"POINT({registro['x']} {registro['y']})"
    parametros = (
        registro["id_estacion"],
        registro["codigo"],
        registro["nombre"],
        wkt,
        registro["id_zona_declarada"],
    )

    with conexion.cursor() as cursor:
        cursor.execute(sentencia, parametros)
```

Los marcadores `%s` no deben reemplazarse mediante interpolación manual. El conector transmite los parámetros según su protocolo; el WKT sigue siendo un dato entregado a `ST_PointFromText()`. La documentación de Connector/Python define `execute()` y `executemany()` para operaciones parametrizadas [@mysqlConnectorExecute2026; @mysqlConnectorExecutemany2026].

La construcción del pequeño WKT con una cadena formateada ocurre después de convertir y comprobar que `x` e `y` son números. No se inserta esa cadena concatenándola dentro de la sentencia SQL.

### 6.3 Carga de varias filas

Para un conjunto pequeño puede utilizarse `executemany()`:

```python
def cargar_estaciones(conexion, registros):
    sentencia = """
        INSERT INTO estacion_espacial
            (id_estacion, codigo, nombre, ubicacion, id_zona_declarada)
        VALUES (%s, %s, %s, ST_PointFromText(%s, 0), %s)
    """

    parametros = []
    for r in registros:
        x = float(r["x"])
        y = float(r["y"])
        parametros.append((
            int(r["id_estacion"]),
            r["codigo"],
            r["nombre"],
            f"POINT({x} {y})",
            int(r["id_zona_declarada"]),
        ))

    try:
        with conexion.cursor() as cursor:
            cursor.executemany(sentencia, parametros)
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
```

La transacción define una política: o se confirma el lote completo o se deshace ante un error. Otros procesos podrían aceptar parcialmente y registrar rechazos, pero esa política requiere una tabla de preparación y se desarrollará con calidad espacial y ETL.

### 6.4 Recuperación y comparación

Python puede pedir a MySQL una forma legible y propiedades calculadas por el SGBD:

```python
def recuperar_estaciones(conexion):
    consulta = """
        SELECT codigo,
               ST_AsText(ubicacion) AS wkt,
               ST_GeometryType(ubicacion) AS tipo,
               ST_SRID(ubicacion) AS srid
        FROM estacion_espacial
        ORDER BY codigo
    """

    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute(consulta)
        return cursor.fetchall()
```

El programa no deduce el tipo examinando el comienzo del texto. Solicita `ST_GeometryType()` a MySQL. Esta práctica evita replicar reglas del SGBD en el cliente.

## 7. Verificación de la implementación

### 7.1 Verificar más que la ejecución

Que un script termine sin excepciones es una evidencia insuficiente. Debe compararse el estado obtenido con un oráculo explícito. Para cuatro estaciones, el contrato inicial puede establecer:

| Código | WKT esperado | Tipo | SRID |
|---|---|---|---:|
| EST-N01 | `POINT(25 75)` | `POINT` | 0 |
| EST-N02 | `POINT(75 75)` | `POINT` | 0 |
| EST-S01 | `POINT(25 25)` | `POINT` | 0 |
| EST-S02 | `POINT(50 50)` | `POINT` | 0 |

La textualización puede normalizar ceros decimales; por eso una prueba no debería exigir que `POINT(25.00 75.00)` conserve exactamente ese formato. Debe comparar valores o una forma canónica producida por MySQL.

### 7.2 Controles SQL iniciales

```sql
SELECT COUNT(*) AS total_estaciones
FROM estacion;

SELECT COUNT(*) AS ubicaciones_nulas
FROM estacion
WHERE ubicacion IS NULL;

SELECT
    ST_GeometryType(ubicacion) AS tipo,
    ST_SRID(ubicacion) AS srid,
    COUNT(*) AS cantidad
FROM estacion
GROUP BY tipo, srid;

SELECT
    codigo,
    coordenada_x,
    coordenada_y,
    ST_X(ubicacion) AS x_obtenida,
    ST_Y(ubicacion) AS y_obtenida
FROM estacion
ORDER BY codigo;
```

El último control comprueba la migración componente por componente. Todavía no verifica exactitud respecto del mundo real; verifica que la transformación del esquema conservó los valores de origen.

### 7.3 Casos positivos y negativos

Una batería mínima incluye:

- punto bien formado con SRID correcto: debe aceptarse;
- WKT mal formado: debe rechazarse;
- línea dirigida a una columna `POINT`: debe rechazarse;
- geometría con SRID incompatible: debe rechazarse;
- parámetro nulo en columna `NOT NULL`: debe rechazarse.

Los mensajes exactos pueden variar entre versiones menores. La evidencia estable es la regla observada y si la operación confirmó o revirtió la transacción.

## 8. Diccionario de datos espacial

### 8.1 Documentar significado y no solo sintaxis

Una entrada mínima para `estacion.ubicacion` debe registrar:

| Elemento | Definición |
|---|---|
| significado | posición operativa asignada a la estación |
| tipo MySQL | `POINT` |
| SRID | 0 |
| ejes | x, y del plano didáctico ObservaSur |
| unidad | unidad abstracta, no metros |
| nulabilidad final | no admite nulos |
| fuente inicial | columnas escalares del esquema de semana 1 |
| constructor | `ST_PointFromText(wkt, 0)` |
| controles | tipo, SRID, no nulidad y correspondencia x/y |
| limitación | no representa el recinto ni acredita exactitud de terreno |

El diccionario evita que el conocimiento quede implícito en el código. También anticipa la procedencia requerida más adelante por las cargas y el almacén de datos.

### 8.2 Predicado de la tabla

Después de la migración, una formulación aproximada del predicado es:

> Cada fila de `estacion` afirma que la estación identificada por `id_estacion`, con código y nombre dados, posee la posición operativa `ubicacion`, expresada como punto en el SRID 0, y mantiene una asignación administrativa a `id_zona_declarada`.

Este predicado hace visible que asignación y ubicación son hechos distintos. El capítulo 4 permitirá compararlos mediante relaciones espaciales.

## 9. Síntesis del núcleo obligatorio

Al completar el núcleo, el estudiante debe poder justificar y ejecutar la siguiente cadena:

```text
pregunta del dominio
    ↓
propiedad espacial elegida
    ↓
tipo específico + SRID + nulabilidad
    ↓
WKT como entrada
    ↓
constructor de MySQL
    ↓
valor geométrico almacenado
    ↓
inspección de tipo, SRID y representación
    ↓
comparación esperado–obtenido desde SQL y Python
```

Hasta aquí es obligatorio comprender que WKT no es la columna, que el SRID no transforma coordenadas y que Python no reemplaza las restricciones de MySQL.

## 10. Ejercicios y casos prácticos

### Ejercicio 1. Nivel básico: seleccionar tipos geométricos

Para cada propiedad de ObservaSur, seleccione `POINT`, `LINESTRING`, `POLYGON` o `GEOMETRY`: posición de una estación, recorrido ordenado de inspección, extensión de una zona y una columna que deliberadamente admite cualquiera de esas geometrías para un inventario heterogéneo. Justifique cada decisión.

#### Resolución paso a paso

**Paso 1. Identificar la propiedad.** La estación requiere posición; el recorrido, trazado; la zona, extensión; el inventario declara heterogeneidad.

**Paso 2. Asociar estructura.** Posición corresponde a `POINT`; secuencia conectada a `LINESTRING`; superficie delimitada a `POLYGON`.

**Paso 3. Tratar la heterogeneidad.** Solo el inventario requiere `GEOMETRY`, porque admitir varias clases forma parte de su contrato.

**Paso 4. Comprobar especificidad.** Usar `GEOMETRY` para las tres primeras propiedades debilitaría restricciones conocidas.

**Resultado:** `POINT`, `LINESTRING`, `POLYGON` y `GEOMETRY`, respectivamente.

### Ejercicio 2. Nivel básico–intermedio: construir e inspeccionar

Escriba una consulta que construya el punto `POINT(25 75)` en SRID 0 y devuelva su WKT, tipo y SRID.

#### Resolución paso a paso

**Paso 1. Elegir constructor.** Como se conoce la clase, se utiliza `ST_PointFromText()`.

**Paso 2. Entregar codificación y SRID.** Los argumentos son la cadena WKT y 0.

**Paso 3. Aplicar funciones de inspección.** Se reutiliza el valor mediante una expresión común:

```sql
WITH geometria AS (
    SELECT ST_PointFromText('POINT(25 75)', 0) AS g
)
SELECT
    ST_AsText(g) AS wkt,
    ST_GeometryType(g) AS tipo,
    ST_SRID(g) AS srid
FROM geometria;
```

**Paso 4. Definir el oráculo.** Se espera `POINT(25 75)`, `POINT` y `0`.

### Ejercicio 3. Nivel intermedio: migrar sin perder evidencia

La tabla `sitio(id, x, y)` contiene filas existentes. Diseñe una migración hacia `ubicacion POINT NOT NULL SRID 0` que permita comprobar los datos antes de imponer la obligatoriedad.

#### Resolución paso a paso

**Paso 1. Agregar una columna transitoria nullable.**

```sql
ALTER TABLE sitio ADD COLUMN ubicacion POINT SRID 0 NULL;
```

**Paso 2. Construir los puntos.**

```sql
UPDATE sitio
SET ubicacion = ST_PointFromText(CONCAT('POINT(', x, ' ', y, ')'), 0);
```

**Paso 3. Comprobar completitud y correspondencia.**

```sql
SELECT COUNT(*) FROM sitio WHERE ubicacion IS NULL;

SELECT id, x, y, ST_X(ubicacion), ST_Y(ubicacion)
FROM sitio
WHERE x <> ST_X(ubicacion) OR y <> ST_Y(ubicacion);
```

Ambas consultas deben devolver cero incumplimientos.

**Paso 4. Imponer el estado final.**

```sql
ALTER TABLE sitio
    MODIFY COLUMN ubicacion POINT NOT NULL SRID 0;
```

**Paso 5. Conservar recuperación.** Las columnas `x` e `y` se mantienen hasta aprobar formalmente la migración; su eventual eliminación es una decisión posterior y respaldada.

### Ejercicio 4. Nivel avanzado: carga transaccional y diagnóstico

Diseñe una función Python que reciba estaciones, inserte el lote de forma parametrizada y compruebe que todas fueron almacenadas como `POINT` con SRID 0. Si falla una inserción, el lote completo debe revertirse.

#### Resolución paso a paso

**Paso 1. Preparar parámetros y no SQL dinámico.**

```python
def cargar_y_verificar(conexion, registros):
    insercion = """
        INSERT INTO estacion_espacial
            (id_estacion, codigo, nombre, ubicacion, id_zona_declarada)
        VALUES (%s, %s, %s, ST_PointFromText(%s, 0), %s)
    """

    filas = []
    codigos = []
    for r in registros:
        x = float(r["x"])
        y = float(r["y"])
        codigos.append(r["codigo"])
        filas.append((
            int(r["id_estacion"]), r["codigo"], r["nombre"],
            f"POINT({x} {y})", int(r["id_zona_declarada"])
        ))
```

**Paso 2. Ejecutar dentro de una transacción.**

```python
    try:
        with conexion.cursor() as cursor:
            cursor.executemany(insercion, filas)

            marcadores = ", ".join(["%s"] * len(codigos))
            consulta = f"""
                SELECT codigo, ST_GeometryType(ubicacion), ST_SRID(ubicacion)
                FROM estacion_espacial
                WHERE codigo IN ({marcadores})
            """
            cursor.execute(consulta, tuple(codigos))
            obtenidas = cursor.fetchall()

        if len(obtenidas) != len(codigos):
            raise ValueError("El número recuperado no coincide con el enviado")
        if any(tipo != "POINT" or srid != 0
               for _, tipo, srid in obtenidas):
            raise ValueError("Tipo o SRID inesperado")

        conexion.commit()
        return obtenidas
    except Exception:
        conexion.rollback()
        raise
```

**Paso 3. Interpretar la seguridad.** Los valores continúan parametrizados. La única parte dinámica es la cantidad de marcadores, derivada del tamaño de la lista y no del contenido de los datos.

**Paso 4. Probar un caso negativo.** Una fila con WKT imposible o un valor no convertible provoca excepción y `rollback()`. La prueba debe confirmar que ninguna fila del lote quedó persistida.

## 11. Temas de profundización

### 11.1 Representación interna y WKB

WKT favorece legibilidad; WKB favorece una codificación binaria normalizada. MySQL utiliza una representación interna relacionada con WKB y antepone el SRID [@mysqlStorage2026]. Las aplicaciones no deben depender de esos bytes internos cuando existen funciones oficiales de entrada y salida.

### 11.2 Columnas geométricas heterogéneas

`GEOMETRY` permite heterogeneidad, pero desplaza controles hacia reglas adicionales y consultas. Su uso debe responder a un requerimiento explícito. En esquemas operacionales estables suelen preferirse columnas específicas o relaciones separadas cuando cada clase posee significado distinto.

### 11.3 Evolución del esquema

Una migración espacial real puede requerir copia de seguridad, ventana de mantenimiento, control de concurrencia, versión del esquema y estrategia de reversión. El patrón nullable–población–verificación–`NOT NULL` ilustra una migración verificable, aunque no agota la administración de producción.

## 12. Referencia técnica

- Tipos individuales: `GEOMETRY`, `POINT`, `LINESTRING`, `POLYGON`.
- Declaración recomendada cuando el contrato lo permite: `tipo NOT NULL SRID n`.
- Entrada WKT: `ST_GeomFromText()`, `ST_PointFromText()`, `ST_LineStringFromText()` y `ST_PolygonFromText()`.
- Salida legible: `ST_AsText()`.
- Inspección: `ST_GeometryType()`, `ST_SRID()`, `ST_X()` y `ST_Y()`.
- Catálogo: `INFORMATION_SCHEMA.ST_GEOMETRY_COLUMNS` y `INFORMATION_SCHEMA.ST_SPATIAL_REFERENCE_SYSTEMS`.
- Cliente Python: `execute()` para una operación y `executemany()` para una secuencia de parámetros.
- Toda carga debe definir confirmación, reversión y resultados esperados.
- Recursos ejecutables: [`semana03_esquema_espacial.sql`](../observasur/sql/semana03_esquema_espacial.sql) y [`semana03_cargar_geometrias.py`](../observasur/python/semana03_cargar_geometrias.py).

El capítulo siguiente empleará las geometrías implementadas para estudiar pertenencia, contención, intersección y frontera. Esa transición equivale a pasar de las reuniones por claves conocidas en Base de Datos I a relaciones derivadas de la geometría.

## 13. Referencias bibliográficas

Güting, R. H. (1994). An introduction to spatial database systems. *The VLDB Journal, 3*, 357–399. https://doi.org/10.1007/BF01231602

MySQL. (2026). *MySQL 8.0 Reference Manual: Creating spatial columns*. https://dev.mysql.com/doc/refman/8.0/en/creating-spatial-columns.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Data type storage requirements*. https://dev.mysql.com/doc/refman/8.0/en/storage-requirements.html

MySQL. (2026). *MySQL 8.0 Reference Manual: General geometry property functions*. https://dev.mysql.com/doc/refman/8.0/en/gis-general-property-functions.html

MySQL. (2026). *MySQL 8.0 Reference Manual: The INFORMATION_SCHEMA ST_GEOMETRY_COLUMNS table*. https://dev.mysql.com/doc/refman/8.0/en/information-schema-st-geometry-columns-table.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Spatial data types*. https://dev.mysql.com/doc/refman/8.0/en/spatial-type-overview.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Spatial reference system support*. https://dev.mysql.com/doc/refman/8.0/en/spatial-reference-systems.html

MySQL. (2026). *MySQL Connector/Python Developer Guide: MySQLCursor.execute() method*. https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

MySQL. (2026). *MySQL Connector/Python Developer Guide: MySQLCursor.executemany() method*. https://dev.mysql.com/doc/connectors/en/connector-python-api-mysqlcursor-executemany.html

Open Geospatial Consortium. (2011). *OpenGIS implementation standard for geographic information—Simple feature access—Part 1: Common architecture* (Version 1.2.1, OGC 06-103r4). https://www.ogc.org/standards/sfa/

Rigaux, P., Scholl, M. y Voisard, A. (2002). *Spatial databases: With application to GIS*. Morgan Kaufmann.
