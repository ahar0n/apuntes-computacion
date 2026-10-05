# Capítulo 4. Relaciones espaciales y consultas topológicas

## Objetivos de aprendizaje

Al finalizar el capítulo, el estudiante será capaz de:

1. distinguir interior, frontera y exterior de una geometría en casos espaciales simples;
2. interpretar pertenencia, contención, intersección, contacto y separación como predicados espaciales;
3. explicar la asimetría entre `ST_Within()` y `ST_Contains()`;
4. anticipar el resultado de una consulta para casos interiores, exteriores y de frontera;
5. formular consultas espaciales que combinen claves relacionales y relaciones geométricas;
6. diferenciar una asignación administrativa almacenada de una pertenencia espacial calculada;
7. ejecutar consultas topológicas parametrizadas desde Python sin trasladar el cálculo espacial al cliente;
8. construir un oráculo de pruebas positivas, negativas y fronterizas;
9. comunicar resultados espaciales sin convertir un predicado geométrico en una conclusión administrativa injustificada.

Estos objetivos desarrollan principalmente R2, R3 y R4 del programa oficial.

## Introducción

El capítulo 3 implementó la posición de cada estación como `POINT` y la extensión de cada zona como `POLYGON`. Tener geometrías almacenadas no responde todavía la pregunta central de esta etapa: **¿la estación pertenece espacialmente a la zona que tiene asignada?**

Desde Base de Datos I, una reunión relaciona filas mediante valores comparables:

```sql
estacion.id_zona_declarada = zona.id_zona
```

La igualdad de claves recupera la zona declarada por la organización. Sin embargo, la geometría permite formular una condición distinta:

```sql
ST_Within(estacion.ubicacion, zona.extension)
```

La primera condición consulta un hecho almacenado; la segunda calcula una relación entre formas. Ninguna reemplaza automáticamente a la otra. Su comparación permite detectar concordancias, discrepancias y casos que requieren una política explícita.

El problema más revelador es la estación `EST-S02`, ubicada en `(50,50)`, precisamente sobre la frontera común de las zonas Norte y Sur. Una respuesta basada solo en intuición podría asignarla a ambas zonas, a una de ellas o a ninguna. La base necesita predicados definidos y el sistema necesita una regla administrativa separada.

---

## 1. Del *join* por claves a la relación espacial

### 1.1 Dos fuentes de relación

En un esquema relacional tradicional, una clave foránea representa una asociación declarada. En ObservaSur:

```text
EST-S02.id_zona_declarada = 2
```

afirma que la organización asignó la estación a la zona Sur. Este hecho puede provenir de una resolución administrativa, una responsabilidad operativa o una decisión anterior. No demuestra geométricamente que el punto esté en el interior del polígono Sur.

Una relación espacial, en cambio, se deriva de los valores geométricos en el momento de la consulta. Si cambia la geometría de una zona, el resultado puede cambiar aunque la clave foránea permanezca igual.

| Relación | Origen | Pregunta respondida |
|---|---|---|
| clave foránea | dato almacenado | ¿qué zona fue declarada? |
| predicado espacial | cálculo sobre geometrías | ¿qué relación geométrica existe ahora? |

Esta distinción enlaza integridad relacional e integridad espacial. La clave foránea garantiza que la zona declarada exista; no garantiza coherencia geométrica. El predicado espacial calcula coherencia geométrica; no decide por sí solo responsabilidad administrativa.

### 1.2 Reunión espacial

Una reunión espacial combina filas cuando sus geometrías satisfacen un predicado. Su forma lógica es:

```sql
SELECT ...
FROM estacion_espacial AS e
JOIN zona_espacial AS z
  ON predicado_espacial(e.ubicacion, z.extension);
```

El operador `JOIN` sigue siendo relacional. Lo nuevo es que la condición no compara claves escalares, sino valores geométricos mediante una función especializada. Las bases espaciales integran precisamente tipos, predicados e índices capaces de expresar estas relaciones [@guting1994, pp. 367–375; @rigaux2002, caps. 2–3].

### 1.3 Relación calculada no equivale a relación permanente

No conviene copiar automáticamente el resultado de `ST_Within()` a una clave foránea. Antes deben resolverse preguntas como:

- ¿qué ocurre en una frontera compartida?;
- ¿qué geometría y fecha respaldan el cálculo?;
- ¿la asignación administrativa debe coincidir siempre con la espacial?;
- ¿qué sucede cuando una zona cambia de forma?;
- ¿quién aprueba una corrección?

El capítulo se concentra en calcular y explicar relaciones. La actualización de datos maestros exige reglas de negocio adicionales.

## 2. Fundamentos topológicos mínimos

### 2.1 Qué significa topología en este capítulo

Aquí, **topología** se refiere a relaciones que dependen de cómo se conectan, incluyen o separan las geometrías, no de una medida numérica. Preguntar si un punto está dentro de un polígono es diferente de preguntar a qué distancia se encuentra de su borde.

El estándar OGC Simple Feature Access caracteriza relaciones espaciales mediante los interiores, fronteras y exteriores de las geometrías [@ogcSFA2011, secs. 6.1.14 y 6.1.15]. No se desarrollará toda la matriz formal de nueve intersecciones; se utilizarán sus distinciones indispensables para interpretar consultas.

### 2.2 Interior, frontera y exterior

Para una geometría (g), se distinguen tres conjuntos:

- (I(g)): interior;
- (B(g)): frontera;
- (E(g)): exterior.

En un polígono simple:

- el interior corresponde a la superficie excluyendo sus anillos;
- la frontera corresponde al anillo exterior y a los anillos de huecos;
- el exterior contiene los puntos que no pertenecen ni al interior ni a la frontera.

Para el polígono Norte de ObservaSur:

```text
POLYGON((0 50,100 50,100 100,0 100,0 50))
```

los puntos `(25,75)` y `(75,75)` están en el interior; `(50,50)` está en la frontera inferior; `(25,25)` está en el exterior.

### 2.3 La frontera no es un error numérico

Un caso fronterizo no debe tratarse como si fuera simplemente “casi interior”. Posee una relación topológica diferente. Cambiar arbitrariamente una coordenada o agregar una tolerancia para forzar una respuesta oculta el problema de modelado.

En ObservaSur, las dos zonas comparten el segmento entre `(0,50)` y `(100,50)`. Un punto sobre ese segmento toca ambas fronteras. Si una política exige asignación única, esa unicidad debe resolverse con una regla del dominio, no alterando la semántica de `ST_Within()`.

### 2.4 Dimensión y frontera

La frontera depende del tipo geométrico. En términos introductorios:

- un punto no tiene una frontera espacial separada en el modelo simple;
- una línea posee extremos como frontera, salvo casos cerrados;
- un polígono posee anillos como frontera.

Por eso `ST_Touches()` no tiene el mismo sentido para todas las combinaciones. MySQL devuelve `NULL` para `ST_Touches()` cuando ambos argumentos tienen dimensión cero, es decir, cuando ambos son puntos o multipuntos [@mysqlSpatialRelations2026].

## 3. Predicados espaciales fundamentales

### 3.1 `ST_Within()`: el primer argumento está dentro del segundo

La expresión:

```sql
ST_Within(g1, g2)
```

pregunta si `g1` está espacialmente dentro de `g2`. Para estación y zona, el orden natural es:

```sql
ST_Within(e.ubicacion, z.extension)
```

El punto interior produce 1; un punto exterior produce 0; un punto situado únicamente en la frontera del polígono no se considera *within* y produce 0 en este caso [@mysqlSpatialRelations2026].

### 3.2 `ST_Contains()`: el primer argumento contiene al segundo

La expresión:

```sql
ST_Contains(g1, g2)
```

invierte los papeles. Para el mismo caso:

```sql
ST_Contains(z.extension, e.ubicacion)
```

`ST_Contains(z.extension, e.ubicacion)` y `ST_Within(e.ubicacion, z.extension)` expresan relaciones inversas. Confundir el orden cambia la pregunta. Una técnica de lectura consiste en verbalizarla:

```text
ST_Within(punto, polígono)
→ “¿el punto está dentro del polígono?”

ST_Contains(polígono, punto)
→ “¿el polígono contiene al punto?”
```

### 3.3 `ST_Intersects()`: existe algún punto común

`ST_Intersects(g1,g2)` devuelve verdadero cuando las geometrías comparten al menos algún punto. Es un predicado más amplio que pertenencia interior. Un punto interior intersecta el polígono; un punto en la frontera también lo intersecta; un punto exterior no.

Esto produce una distinción esencial:

| Posición del punto | `Within(punto, polígono)` | `Intersects(punto, polígono)` |
|---|---:|---:|
| interior | 1 | 1 |
| frontera | 0 | 1 |
| exterior | 0 | 0 |

Por tanto, reemplazar `ST_Within()` por `ST_Intersects()` cambia la política de inclusión de la frontera.

### 3.4 `ST_Touches()`: contacto sin intersección de interiores

Dos geometrías se tocan cuando sus interiores no se intersectan, pero la frontera de al menos una encuentra la frontera o el interior de la otra. MySQL implementa esta relación mediante `ST_Touches()` [@mysqlSpatialRelations2026].

Para un punto y un polígono:

- punto en el interior: no toca la frontera;
- punto en la frontera: toca el polígono;
- punto en el exterior: no toca el polígono.

Así, `ST_Touches()` permite identificar explícitamente el caso que `ST_Within()` excluye pero `ST_Intersects()` incluye.

### 3.5 `ST_Disjoint()`: ausencia de puntos comunes

`ST_Disjoint(g1,g2)` es verdadero cuando las geometrías no se intersectan. Para geometrías válidas y comparables:

\[
ST\_Disjoint(g_1,g_2)=\neg ST\_Intersects(g_1,g_2).
\]

Expresar directamente `ST_Disjoint()` suele comunicar mejor la intención cuando se buscan estaciones completamente fuera de una zona.

## 4. Tabla de verdad para ObservaSur

### 4.1 Oráculo antes de consultar

Antes de ejecutar SQL se debe predecir el resultado. Para la zona Norte:

| Estación | Punto | Situación | Within | Contains inverso | Intersects | Touches | Disjoint |
|---|---|---|---:|---:|---:|---:|---:|
| EST-N01 | `(25,75)` | interior | 1 | 1 | 1 | 0 | 0 |
| EST-N02 | `(75,75)` | interior | 1 | 1 | 1 | 0 | 0 |
| EST-S01 | `(25,25)` | exterior | 0 | 0 | 0 | 0 | 1 |
| EST-S02 | `(50,50)` | frontera | 0 | 0 | 1 | 1 | 0 |

Este cuadro funciona como **oráculo**: una especificación previa del resultado esperado. Si la consulta produce algo distinto, se revisan datos, orden de argumentos, SRID y función elegida antes de modificar la expectativa.

### 4.2 Consulta de verificación

```sql
SELECT
    e.codigo,
    ST_Within(e.ubicacion, z.extension) AS esta_dentro,
    ST_Contains(z.extension, e.ubicacion) AS zona_contiene,
    ST_Intersects(e.ubicacion, z.extension) AS intersecta,
    ST_Touches(e.ubicacion, z.extension) AS toca,
    ST_Disjoint(e.ubicacion, z.extension) AS esta_separada
FROM estacion_espacial AS e
JOIN zona_espacial AS z
  ON z.id_zona = 1
ORDER BY e.codigo;
```

La reunión por `z.id_zona = 1` selecciona una zona conocida; los predicados calculan la relación de cada estación con ella. Todavía no se está realizando una reunión espacial entre todas las estaciones y todas las zonas.

## 5. Reuniones espaciales en SQL

### 5.1 Estaciones en el interior de cada zona

```sql
SELECT
    e.codigo AS estacion,
    z.nombre AS zona_calculada
FROM estacion_espacial AS e
JOIN zona_espacial AS z
  ON ST_Within(e.ubicacion, z.extension)
ORDER BY e.codigo, z.nombre;
```

Cada pareja candidata se conserva si el punto está en el interior del polígono. `EST-S02` no aparece, pues está sobre la frontera compartida.

### 5.2 Estaciones que intersectan cada zona

```sql
SELECT
    e.codigo AS estacion,
    z.nombre AS zona_intersectada,
    ST_Touches(e.ubicacion, z.extension) AS es_frontera
FROM estacion_espacial AS e
JOIN zona_espacial AS z
  ON ST_Intersects(e.ubicacion, z.extension)
ORDER BY e.codigo, z.nombre;
```

Ahora `EST-S02` aparece dos veces, una por cada zona. No es duplicación accidental: existen dos parejas que satisfacen la condición. La cardinalidad del resultado depende del predicado y de los datos.

### 5.3 La elección del predicado define el conjunto resultado

Estas condiciones no son sinónimas:

```sql
ON ST_Within(e.ubicacion, z.extension)
ON ST_Intersects(e.ubicacion, z.extension)
ON ST_Touches(e.ubicacion, z.extension)
```

La primera excluye frontera, la segunda incluye interior y frontera, y la tercera conserva solo contacto fronterizo para punto–polígono. Elegir una función por producir el número de filas deseado invierte el razonamiento. Primero se formula el significado; después se selecciona el predicado que lo representa.

### 5.4 Producto de candidatos y condición espacial

Conceptualmente, una reunión espacial considera pares de filas y evalúa un predicado. Con pocas geometrías puede imaginarse el producto cartesiano seguido de un filtro:

\[
E \bowtie_{Within(E.ubicacion,Z.extension)} Z.
\]

Esta notación es lógica, no una orden para implementar manualmente un producto. El optimizador y los índices espaciales podrán reducir candidatos; ese procesamiento se estudiará en el capítulo 6.

## 6. Comparación entre asignación declarada y relación calculada

### 6.1 Consulta de auditoría

Para comparar ambos hechos se parte de la asignación declarada y se evalúa su geometría:

```sql
SELECT
    e.codigo,
    z.nombre AS zona_declarada,
    ST_Within(e.ubicacion, z.extension) AS en_interior,
    ST_Touches(e.ubicacion, z.extension) AS en_frontera,
    CASE
        WHEN ST_Within(e.ubicacion, z.extension) = 1 THEN 'coincide-interior'
        WHEN ST_Touches(e.ubicacion, z.extension) = 1 THEN 'caso-frontera'
        ELSE 'no-coincide'
    END AS diagnostico
FROM estacion_espacial AS e
JOIN zona_espacial AS z
  ON z.id_zona = e.id_zona_declarada
ORDER BY e.codigo;
```

El `JOIN` usa la clave para recuperar la zona declarada. Las funciones espaciales evalúan la posición respecto de esa zona. El `CASE` traduce combinaciones técnicas a categorías de revisión.

### 6.2 Tres estados, no un booleano apresurado

Clasificar solo como correcto/incorrecto perdería el caso de frontera. Una clasificación mínima distingue:

1. **coincide-interior:** relación espacial clara con la zona declarada;
2. **caso-frontera:** requiere política o revisión;
3. **no-coincide:** no está en el interior ni en la frontera de la zona declarada.

Esta clasificación no modifica datos. Produce evidencia para una decisión posterior.

### 6.3 Buscar zonas alternativas

Para una estación que no coincide, puede consultarse qué zonas contienen su punto:

```sql
SELECT z.id_zona, z.nombre
FROM zona_espacial AS z
JOIN estacion_espacial AS e
  ON ST_Within(e.ubicacion, z.extension)
WHERE e.codigo = 'EST-S01';
```

Si no aparece ninguna zona, el punto puede estar fuera de cobertura o en una frontera. Si aparecen varias, las zonas pueden superponerse. La consulta detecta una condición; no explica su causa.

## 7. Consultas parametrizadas desde Python

### 7.1 Parámetro relacional, cálculo espacial en MySQL

Python puede recibir el identificador de una zona y solicitar el diagnóstico:

```python
def diagnosticar_zona(conexion, id_zona):
    consulta = """
        SELECT e.codigo,
               ST_AsText(e.ubicacion) AS ubicacion,
               ST_Within(e.ubicacion, z.extension) AS esta_dentro,
               ST_Touches(e.ubicacion, z.extension) AS toca_frontera,
               ST_Intersects(e.ubicacion, z.extension) AS intersecta
        FROM estacion_espacial AS e
        JOIN zona_espacial AS z ON z.id_zona = %s
        ORDER BY e.codigo
    """
    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute(consulta, (id_zona,))
        return cursor.fetchall()
```

El identificador se transmite como parámetro. Python no descarga polígonos para implementar un algoritmo punto-en-polígono; delega el predicado al SGBD, que conoce tipo y SRID. `execute()` admite la operación y sus parámetros como argumentos separados [@mysqlConnectorExecute2026].

### 7.2 Comparación con un oráculo

```python
ESPERADO_NORTE = {
    "EST-N01": (1, 0, 1),
    "EST-N02": (1, 0, 1),
    "EST-S01": (0, 0, 0),
    "EST-S02": (0, 1, 1),
}


def comprobar_resultados(filas, esperado):
    obtenidos = {
        f["codigo"]: (
            f["esta_dentro"],
            f["toca_frontera"],
            f["intersecta"],
        )
        for f in filas
    }
    if obtenidos != esperado:
        raise AssertionError(
            f"Resultado inesperado: {obtenidos}; esperado: {esperado}"
        )
```

El propósito no es demostrar que Python conoce topología, sino automatizar la comparación entre especificación y respuesta de MySQL.

### 7.3 Parámetros vacíos, nulos y desconocidos

La función cliente debe distinguir:

- identificador convertible a entero;
- zona inexistente, que produce cero filas o requiere una comprobación previa;
- valor `None`, que no debe convertirse silenciosamente en una zona;
- error de conexión o ejecución.

Una interfaz robusta informa “zona inexistente” en lugar de presentar una tabla vacía como si significara “ninguna estación pertenece”. La interpretación del conjunto vacío depende de si la entidad consultada existe.

## 8. Argumentos, SRID y resultados nulos

### 8.1 Compatibilidad de SRID

Las funciones espaciales que reciben varias geometrías requieren SRID compatibles. MySQL produce error si los argumentos pertenecen a SRID distintos [@mysqlSpatialRelations2026; @mysqlSRS2026]. Esto protege contra comparaciones carentes de un marco común, pero no detecta un SRID incorrectamente etiquetado.

Antes de diagnosticar relaciones debe verificarse:

```sql
SELECT ST_SRID(ubicacion), COUNT(*)
FROM estacion_espacial
GROUP BY ST_SRID(ubicacion);

SELECT ST_SRID(extension), COUNT(*)
FROM zona_espacial
GROUP BY ST_SRID(extension);
```

### 8.2 `NULL` no equivale a falso

En SQL, `NULL` representa un valor desconocido o no aplicable. Las funciones espaciales suelen devolver `NULL` si algún argumento es `NULL` [@mysqlSpatialRelations2026]. Por ello:

```text
0    → la relación evaluada es falsa
1    → la relación evaluada es verdadera
NULL → no se obtuvo un valor lógico verdadero/falso
```

Aunque el esquema operativo declara geometrías `NOT NULL`, esta distinción será importante en tablas de preparación y cargas incompletas.

### 8.3 Funciones `ST_` y relaciones sobre formas

El núcleo utiliza funciones `ST_` que evalúan las formas geométricas. MySQL también posee funciones basadas en rectángulos mínimos envolventes con prefijo `MBR`. No son intercambiables: un rectángulo envolvente puede intersectar otro aunque las geometrías reales no lo hagan. El capítulo 6 explicará su función en la generación de candidatos y el refinamiento exacto.

## 9. Diseño de pruebas topológicas

### 9.1 Particiones de casos

Para punto–polígono, una prueba mínima debe incluir:

1. punto claramente interior;
2. punto claramente exterior;
3. punto en un segmento de frontera;
4. punto en un vértice;
5. argumento con SRID incompatible;
6. argumento nulo si el contexto lo admite.

Los casos 3 y 4 impiden que una implementación parezca correcta solo porque se probó con posiciones fáciles.

### 9.2 Pruebas metamórficas simples

Además de resultados puntuales pueden comprobarse relaciones entre funciones:

- `Within(p,z)` debe coincidir con `Contains(z,p)`;
- `Disjoint(p,z)` debe ser la negación de `Intersects(p,z)` para entradas válidas no nulas;
- si `Touches(p,z)=1`, entonces `Intersects(p,z)=1` y `Within(p,z)=0` para punto–polígono;
- intercambiar argumentos de `Within` no conserva, en general, el resultado.

Estas propiedades aumentan la capacidad de detectar errores sin requerir muchos datos.

### 9.3 Evidencia esperada

La evidencia de aprendizaje de la semana incluye:

- consulta SQL con predicados topológicos;
- función Python parametrizada;
- tabla esperado–obtenido;
- casos interior, exterior y frontera;
- explicación de la diferencia entre zona declarada y zona calculada;
- conclusión que identifique qué decisiones no puede tomar la geometría por sí sola.

## 10. Síntesis del núcleo obligatorio

La progresión central puede resumirse así:

```text
join por clave
    → recupera una relación declarada

join espacial
    → calcula una relación entre geometrías

Within / Contains
    → interior, con orden de argumentos asimétrico

Intersects
    → cualquier punto común, incluida la frontera

Touches
    → contacto fronterizo sin intersección de interiores

comparación declarada–calculada
    → evidencia para revisar, no actualización automática
```

Hasta aquí es obligatorio poder predecir y explicar los resultados para interior, exterior y frontera, además de ejecutar la consulta desde SQL y Python.

## 11. Ejercicios y casos prácticos

### Ejercicio 1. Nivel básico: interpretar predicados

Considere el polígono `POLYGON((0 0,10 0,10 10,0 10,0 0))` y los puntos A `(5,5)`, B `(10,5)` y C `(12,5)`. Prediga `Within`, `Intersects`, `Touches` y `Disjoint` para cada punto.

#### Resolución paso a paso

**Paso 1. Clasificar posiciones.** A está en el interior; B, en la frontera; C, en el exterior.

**Paso 2. Aplicar `Within`.** Solo A está dentro: A=1, B=0, C=0.

**Paso 3. Aplicar `Intersects`.** Interior y frontera comparten puntos con el polígono: A=1, B=1, C=0.

**Paso 4. Aplicar `Touches`.** Solo B contacta la frontera sin estar en el interior: A=0, B=1, C=0.

**Paso 5. Aplicar `Disjoint`.** Solo C está separado: A=0, B=0, C=1.

### Ejercicio 2. Nivel básico–intermedio: corregir el orden

Un estudiante escribe `ST_Within(z.extension,e.ubicacion)` para buscar estaciones dentro de zonas. Explique el error y escriba dos formulaciones equivalentes correctas.

#### Resolución paso a paso

**Paso 1. Verbalizar la expresión.** La consulta pregunta si el polígono está dentro del punto.

**Paso 2. Reordenar `Within`.**

```sql
ST_Within(e.ubicacion, z.extension)
```

**Paso 3. Usar la relación inversa.**

```sql
ST_Contains(z.extension, e.ubicacion)
```

**Paso 4. Comprobar.** Para entradas válidas, ambas expresiones deben producir el mismo resultado. Esta equivalencia constituye una prueba adicional.

### Ejercicio 3. Nivel intermedio: diagnosticar asignación

Escriba una consulta que clasifique cada estación como `interior`, `frontera` o `fuera` respecto de su zona declarada.

#### Resolución paso a paso

**Paso 1. Reunir por la clave declarada.**

```sql
FROM estacion_espacial AS e
JOIN zona_espacial AS z
  ON z.id_zona = e.id_zona_declarada
```

**Paso 2. Evaluar primero interior y luego frontera.**

```sql
SELECT e.codigo, z.nombre,
       CASE
           WHEN ST_Within(e.ubicacion, z.extension) THEN 'interior'
           WHEN ST_Touches(e.ubicacion, z.extension) THEN 'frontera'
           ELSE 'fuera'
       END AS relacion
FROM estacion_espacial AS e
JOIN zona_espacial AS z
  ON z.id_zona = e.id_zona_declarada
ORDER BY e.codigo;
```

**Paso 3. Justificar el orden.** Un punto interior intersecta, pero no toca; un punto fronterizo toca. Usar primero `Intersects` clasificaría interior y frontera en una misma categoría.

**Paso 4. Interpretar.** `fuera` indica discrepancia geométrica, no necesariamente error administrativo.

### Ejercicio 4. Nivel avanzado: consulta parametrizada y oráculo

Construya una función Python que reciba un código de estación, devuelva su relación con todas las zonas y verifique que una estación fronteriza intersecte al menos una zona sin aparecer como interior.

#### Resolución paso a paso

**Paso 1. Formular la consulta.**

```python
def relaciones_de_estacion(conexion, codigo):
    consulta = """
        SELECT z.nombre,
               ST_Within(e.ubicacion, z.extension) AS dentro,
               ST_Touches(e.ubicacion, z.extension) AS toca,
               ST_Intersects(e.ubicacion, z.extension) AS intersecta
        FROM estacion_espacial AS e
        CROSS JOIN zona_espacial AS z
        WHERE e.codigo = %s
        ORDER BY z.nombre
    """
    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute(consulta, (codigo,))
        filas = cursor.fetchall()
```

**Paso 2. Distinguir estación inexistente.**

```python
    if not filas:
        raise LookupError(f"No existe la estación {codigo}")
```

**Paso 3. Verificar el caso fronterizo.**

```python
    if not any(f["toca"] == 1 and f["intersecta"] == 1 for f in filas):
        raise AssertionError("No se detectó el contacto fronterizo esperado")
    if any(f["dentro"] == 1 for f in filas):
        raise AssertionError("La estación fronteriza apareció como interior")
    return filas
```

**Paso 4. Interpretar la cardinalidad.** Para `EST-S02` se esperan dos filas, pues se compara con dos zonas. Ambas pueden indicar contacto. No debe exigirse una única zona sin una regla administrativa adicional.

## 12. Temas de profundización

### 12.1 Modelo de nueve intersecciones

El modelo DE-9IM describe una relación examinando las intersecciones entre interior, frontera y exterior de dos geometrías. Predicados como `Within`, `Touches` e `Intersects` corresponden a patrones sobre esa matriz [@ogcSFA2011, sec. 6.1.15]. Su formalización completa es útil como referencia, pero no constituye requisito para ejecutar e interpretar los predicados nucleares.

### 12.2 Superposición y cruce

`ST_Overlaps()` y `ST_Crosses()` expresan relaciones adicionales cuya aplicabilidad depende de las dimensiones de las geometrías. Se estudiarán solo cuando el caso incluya polígonos superpuestos o trazados que atraviesen zonas; no deben memorizarse como un catálogo desconectado.

### 12.3 Políticas de frontera

Un sistema puede adoptar reglas como asignar una frontera compartida a una zona prioritaria, conservar una categoría especial o permitir responsabilidad compartida. Tales reglas pertenecen al dominio. La base puede implementarlas después de que estén declaradas, pero el predicado topológico no las inventa.

## 13. Referencia técnica

- `ST_Within(g1,g2)`: `g1` está dentro de `g2`.
- `ST_Contains(g1,g2)`: `g1` contiene a `g2`.
- `ST_Intersects(g1,g2)`: existe algún punto común.
- `ST_Touches(g1,g2)`: contacto sin intersección de interiores.
- `ST_Disjoint(g1,g2)`: no existen puntos comunes.
- `Within(a,b)` es la relación inversa de `Contains(b,a)`.
- En punto–polígono, un punto fronterizo intersecta y toca, pero no está dentro.
- Las geometrías comparadas deben poseer SRID compatible.
- `NULL` no debe interpretarse como falso.
- Recursos ejecutables: [`semana04_consultas_topologicas.sql`](../observasur/sql/semana04_consultas_topologicas.sql) y [`semana04_verificar_relaciones.py`](../observasur/python/semana04_verificar_relaciones.py).

El capítulo 5 añadirá consultas métricas y controles de calidad. Entonces la pregunta dejará de ser únicamente “¿qué relación topológica existe?” y pasará a incluir “¿qué significa estar cerca, en qué unidad y con qué supuestos?”.

## 14. Referencias bibliográficas

Güting, R. H. (1994). An introduction to spatial database systems. *The VLDB Journal, 3*, 357–399. https://doi.org/10.1007/BF01231602

MySQL. (2026). *MySQL 8.0 Reference Manual: Spatial relation functions that use object shapes*. https://dev.mysql.com/doc/refman/8.0/en/spatial-relation-functions-object-shapes.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Spatial reference system support*. https://dev.mysql.com/doc/refman/8.0/en/spatial-reference-systems.html

MySQL. (2026). *MySQL Connector/Python Developer Guide: MySQLCursor.execute() method*. https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

Open Geospatial Consortium. (2011). *OpenGIS implementation standard for geographic information—Simple feature access—Part 1: Common architecture* (Version 1.2.1, OGC 06-103r4). https://www.ogc.org/standards/sfa/

Rigaux, P., Scholl, M. y Voisard, A. (2002). *Spatial databases: With application to GIS*. Morgan Kaufmann.
