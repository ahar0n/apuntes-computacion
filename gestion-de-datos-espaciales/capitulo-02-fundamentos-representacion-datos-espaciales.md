# Capítulo 2. Fundamentos de la representación de datos espaciales

## Objetivos de aprendizaje

Al finalizar el capítulo, el estudiante será capaz de:

1. distinguir fenómeno u objeto del dominio, entidad registrada, propiedad espacial, geometría y codificación;
2. explicar por qué una ubicación requiere estructura, sistema de referencia, operaciones y reglas de integridad;
3. diferenciar posición, forma y extensión mediante las geometrías conceptuales punto, línea y polígono;
4. interpretar coordenadas como valores dependientes de ejes, orden, unidad y sistema de referencia;
5. explicar la función de un sistema de referencia espacial y de su identificador SRID sin presuponer formación cartográfica;
6. comparar representaciones mediante columnas escalares, texto y tipos geométricos;
7. utilizar WKT como notación legible para comunicar geometrías simples;
8. justificar una representación inicial para estaciones y zonas del caso ObservaSur;
9. distribuir correctamente entre Python y MySQL las tareas de preparación, transmisión, construcción, almacenamiento y validación de geometrías.

Estos objetivos desarrollan principalmente R1 y R2 y preparan R3 y R4 del programa oficial.

## Introducción

El capítulo anterior estableció que una entidad, su identidad y su representación espacial no son equivalentes, y que dos columnas numéricas no constituyen por sí solas un dominio espacial gestionado. Este capítulo retoma esa conclusión y formaliza la cadena objeto–propiedad espacial–geometría–codificación. La discusión progresa desde la semántica del dato espacial hasta las geometrías simples, los sistemas de coordenadas, los sistemas de referencia y las codificaciones utilizadas para intercambiar geometrías. La creación efectiva de columnas y valores geométricos queda delimitada para el capítulo 3.

---

## 1. Semántica de los datos espaciales

En el capítulo anterior, ObservaSur almacenó una estación mediante dos columnas numéricas:

```text
coordenada_x = 25.00
coordenada_y = 75.00
```

La pareja parece describir una ubicación, pero los números aislados admiten muchas interpretaciones. Podrían representar metros en una cuadrícula ficticia, coordenadas de una imagen, grados angulares, índices de una matriz o desplazamientos respecto de un origen local. La base conserva la forma escrita del valor, pero no necesariamente su significado.

Una representación espacial adecuada debe responder al menos cuatro preguntas:

1. **¿Qué se representa?** Una posición, un recorrido, un límite o una extensión.
2. **¿Cómo se representa?** Como punto, línea, polígono u otra geometría.
3. **¿En qué espacio de coordenadas?** Con ejes, orden, origen y unidades definidos.
4. **¿Qué operaciones tienen sentido?** Pertenencia, intersección, distancia, longitud o área, entre otras.

Los sistemas de bases de datos espaciales amplían un SGBD para representar objetos con propiedades espaciales y ofrecer operaciones e índices adecuados [@guting1994, pp. 357–364; @rigaux2002, caps. 1–2]. La ampliación no convierte automáticamente cualquier par numérico en información geográfica: el esquema debe declarar el contrato que permite interpretarlo.

## 2. Niveles de abstracción de la representación espacial

Para modelar correctamente se deben separar cinco niveles. Los dos primeros amplían la distinción entre objeto y entidad introducida en el capítulo 1; los tres restantes precisan cómo una propiedad espacial se abstrae y se codifica.

### 2.1 Fenómeno u objeto del dominio

Es aquello sobre lo cual la organización necesita conservar información. Puede ser una estación, una zona operativa, una vía, un incidente o una observación. Su existencia y significado pertenecen al dominio, no al software.

Una estación posee más propiedades que su ubicación: identidad, nombre, fuentes, estado y observaciones. Una zona puede tener nombre, responsable, vigencia y reglas de administración, además de un límite.

### 2.2 Entidad registrada

Es la representación lógica del objeto dentro del esquema. La relación `ESTACION` conserva una identidad y atributos seleccionados. No pretende copiar el objeto real; registra hechos necesarios para los propósitos del sistema.

### 2.3 Propiedad espacial

Es el aspecto espacial que se decide representar. Para una estación puede ser su posición operativa. Para una zona puede ser su extensión. Un mismo objeto podría tener varias propiedades espaciales: punto de acceso, recinto completo o área de influencia.

### 2.4 Geometría

Es una abstracción matemática de la propiedad espacial. El estándar OGC Simple Feature Access organiza geometrías mediante una arquitectura que incluye `Point`, curvas, superficies y colecciones; cada objeto geométrico se asocia a un sistema de referencia espacial [@ogcSFA2011, secs. 6.1–6.2].

En el núcleo del curso utilizaremos tres geometrías simples:

- **punto:** representa una posición sin extensión interna relevante para la escala del problema;
- **línea:** representa un trazado construido por segmentos ordenados;
- **polígono:** representa una superficie delimitada por un anillo exterior y, opcionalmente, anillos interiores.

### 2.5 Codificación

Es la forma en que una geometría se comunica o almacena: texto, representación binaria o formato de intercambio. Una misma geometría puede expresarse mediante WKT, WKB o una codificación interna del SGBD. Cambiar la codificación no necesariamente cambia la geometría.

Esta cadena resume las dependencias:

```text
objeto del dominio
        ↓ selección
propiedad espacial relevante
        ↓ abstracción
geometría
        ↓ expresión
codificación
        ↓ persistencia
valor almacenado por el SGBD
```

El error “la estación es un punto” elimina niveles. Una formulación más precisa es: “para estas preguntas, la posición de la estación se representa mediante una geometría puntual”.

## 3. Geometrías simples y dimensionalidad

### 3.1 Punto

Un punto representa una posición individual en un espacio de coordenadas. En dos dimensiones puede escribirse:

\[
p=(x,y).
\]

Se considera de dimensión topológica cero: no posee longitud ni área en el modelo. Esto no afirma que el objeto real carezca de tamaño. Una estación ocupa espacio físico, pero su extensión puede ser irrelevante para preguntas a escala regional.

Usar un punto resulta razonable cuando se necesita:

- localizar una estación;
- comprobar en qué zona se encuentra;
- calcular cercanía respecto de otras posiciones;
- representar un sitio de observación a la escala del problema.

No resulta suficiente si se necesita administrar el perímetro del recinto o comprobar qué infraestructura atraviesa su interior.

### 3.2 Línea

Una `LineString` representa una secuencia ordenada de puntos conectados mediante interpolación lineal. Si:

\[
L=\langle p_1,p_2,\dots,p_n\rangle,
\]

cada par consecutivo \((p_i,p_{i+1})\) define un segmento. El orden forma parte del valor: invertir la secuencia puede preservar el trazado geométrico, pero cambia inicio y fin.

Una línea puede representar:

- un camino o eje vial;
- una tubería;
- el recorrido planificado entre estaciones;
- una sección lineal de una red.

No debe confundirse con una colección desordenada de puntos. La conectividad se conserva mediante la secuencia.

### 3.3 Polígono

Un polígono representa una superficie planar. Su límite exterior se describe mediante un anillo cerrado; puede incluir anillos interiores que representan huecos [@ogcSFA2011, sec. 6.1.11]. Conceptualmente:

\[
P=(R_0,R_1,\dots,R_k),
\]

donde \(R_0\) es el anillo exterior y los restantes, si existen, son interiores.

En ObservaSur, una zona operativa se representará inicialmente como polígono porque interesa determinar qué posiciones pertenecen a su extensión. El polígono no es la zona administrativa completa: es la representación de su componente espacial.

### 3.4 Dependencia respecto del propósito y la escala

Una carretera puede modelarse como línea en una base regional y como polígono en un inventario detallado de pavimentos. Un lago puede ser punto en una base mundial de nombres y polígono en un estudio territorial. La elección no se decide por la forma visual cotidiana, sino por las operaciones y la resolución requeridas.

Un procedimiento razonado es:

1. formular las preguntas;
2. identificar la propiedad espacial involucrada;
3. determinar si interesa posición, trazado o extensión;
4. escoger la geometría mínima que preserve esa propiedad;
5. comprobar casos límite;
6. verificar soporte del SGBD.

Elegir la geometría más detallada no siempre mejora el modelo. Aumenta carga, mantenimiento y costo de consulta sin aportar necesariamente respuestas nuevas.

## 4. Sistemas de coordenadas y propiedades métricas

### 4.1 Sistema de coordenadas

Un sistema de coordenadas establece cómo se asignan números a posiciones. En un plano cartesiano bidimensional se definen dos ejes, un origen y una unidad. La pareja \((x,y)\) expresa desplazamientos o posiciones respecto de ese marco.

La misma pareja numérica puede designar lugares diferentes bajo marcos distintos. Por ello:

\[
coordenadas + sistema\ de\ referencia \longrightarrow posición\ interpretable.
\]

Las coordenadas no contienen por sí solas el sistema que las hace significativas.

### 4.2 Orden de ejes

El orden es parte del contrato. En un plano cartesiano suele escribirse \((x,y)\), pero en sistemas geográficos existen prácticas y definiciones que pueden usar longitud–latitud o latitud–longitud. MySQL conserva definiciones de ejes para los SRS y determina su orden a partir de ellas [@mysqlSRS2026, sec. 13.4.5].

Intercambiar ejes puede producir una ubicación válida desde el punto de vista numérico pero incorrecta en el dominio. Por eso no basta comprobar que dos valores sean números.

### 4.3 Unidad

Una distancia calculada en el plano utiliza las unidades del sistema de coordenadas. Si los ejes están expresados en metros, una distancia cartesiana se expresa en metros; si el sistema carece de unidad declarada, el resultado no puede interpretarse automáticamente como metros.

En MySQL, el SRID 0 representa un plano cartesiano abstracto sin unidades asignadas. Es legal y útil para el plano ficticio de ObservaSur, pero no está georreferenciado ni representa automáticamente la Tierra [@mysqlSRS2026, sec. 13.4.5].

### 4.4 Precisión, exactitud y resolución

Aunque este curso no desarrolla teoría de medición, deben distinguirse tres ideas:

- **precisión de almacenamiento:** cantidad de dígitos que el tipo puede conservar;
- **resolución:** cambio mínimo distinguible en la representación o captura;
- **exactitud:** cercanía del valor respecto de la posición que pretende representar.

Agregar decimales a una columna aumenta capacidad de representación, pero no mejora la exactitud de la fuente. La base debe evitar sugerir una calidad inexistente.

## 5. Sistemas de referencia espaciales e identificadores SRID

### 5.1 Función de un SRS

Un **sistema de referencia espacial** o SRS describe el espacio de coordenadas en el que se define una geometría. Para los propósitos iniciales basta reconocer que establece elementos como:

- naturaleza cartesiana, geográfica o proyectada;
- ejes y orden;
- unidad;
- parámetros que vinculan coordenadas con posiciones.

Este capítulo no enseña proyecciones ni transformaciones. Introduce el SRS como un contrato obligatorio para interpretar y comparar geometrías.

### 5.2 SRID

Un **identificador de sistema de referencia espacial** o SRID es un número que refiere a una definición de SRS. No es el sistema completo ni modifica coordenadas por sí mismo. Su función puede expresarse así:

\[
SRID \xrightarrow{referencia} definición\ del\ SRS.
\]

Asignar un SRID incorrecto no transforma una posición; solo la etiqueta con una interpretación posiblemente falsa. Para transformar coordenadas se necesita una operación específica y soporte adecuado.

MySQL mantiene un catálogo consultable mediante `INFORMATION_SCHEMA.ST_SPATIAL_REFERENCE_SYSTEMS`. Para operaciones entre varias geometrías, los valores deben tener el mismo SRID; de lo contrario se produce un error [@mysqlSRS2026, sec. 13.4.5].

### 5.3 Columnas restringidas por SRID

MySQL 8.0 permite declarar una columna geométrica con un SRID específico. Una columna restringida acepta únicamente geometrías que utilicen ese identificador. Esta declaración fortalece el esquema y prepara el uso del índice espacial por el optimizador [@mysqlSpatialTypes2026, sec. 13.4.1].

Conceptualmente:

```sql
ubicacion POINT NOT NULL SRID 0
```

declara que cada valor es puntual, no nulo y asociado al plano cartesiano abstracto 0. La implementación completa se realizará en el capítulo siguiente.

### 5.4 Selección del SRS para el caso didáctico

ObservaSur comienza con un plano ficticio de 0 a 100. Esta decisión pedagógica permite aprender estructura, geometría, frontera e integridad sin exigir cartografía o geodesia. Utilizar SRID 0 hace explícito que:

- las coordenadas pertenecen a un plano abstracto;
- no deben interpretarse como latitud/longitud;
- las distancias carecen de una unidad terrestre automática;
- los resultados sirven para comprender las operaciones, no para decisiones territoriales reales.

Más adelante podrá mostrarse un ejemplo terrestre cuidadosamente preparado, pero no será prerrequisito para comprender el modelo espacial.

## 6. Representación textual de geometrías mediante WKT

### 6.1 Distinción entre geometría y codificación

**Well-Known Text** (WKT) es una representación textual de geometrías. Permite leer y escribir ejemplos, intercambiarlos en una guía y enviarlos como parámetros. No constituye el formato interno de almacenamiento del SGBD.

OGC Simple Feature Access especifica representaciones WKT y WKB para geometrías simples. MySQL admite ambas como formatos de entrada/salida y utiliza una representación interna que incorpora el SRID y una codificación binaria [@ogcSFA2011, sec. 7; @mysqlSpatialFormats2026, sec. 13.4.3; @mysqlStorage2026, sec. 13.7].

### 6.2 Punto

```text
POINT(25 75)
```

La palabra identifica el tipo. Dentro de paréntesis aparecen las coordenadas separadas por espacio. No se escribe una coma entre los componentes de un mismo punto.

### 6.3 Línea

```text
LINESTRING(10 10, 40 30, 80 20)
```

Cada pareja representa un punto; las comas separan puntos consecutivos. La secuencia contiene tres puntos y dos segmentos.

### 6.4 Polígono

```text
POLYGON((0 50, 100 50, 100 100, 0 100, 0 50))
```

El doble paréntesis distingue el polígono de la lista que define su anillo exterior. El primer y último punto coinciden para cerrar el anillo. Un polígono con hueco contendría listas adicionales.

### 6.5 Errores interpretativos frecuentes

- escribir `POINT(25, 75)` como si fuera una tupla de Python;
- olvidar cerrar el anillo de un polígono;
- intercambiar ejes;
- creer que WKT incluye siempre el SRID;
- tratar el texto WKT como geometría sin usar un constructor del SGBD;
- creer que dos cadenas visualmente distintas representan necesariamente geometrías distintas.

WKT es especialmente valioso para enseñar y depurar porque hace visible la estructura. En producción pueden usarse otras codificaciones sin cambiar el modelo conceptual.

## 7. Modelo de tipos geométricos

MySQL ofrece `GEOMETRY`, `POINT`, `LINESTRING`, `POLYGON` y tipos de colección compatibles con la familia de geometrías simples [@mysqlSpatialTypes2026, sec. 13.4.1].

Una jerarquía simplificada es:

```text
GEOMETRY
├── POINT
├── LINESTRING
├── POLYGON
└── colecciones
    ├── MULTIPOINT
    ├── MULTILINESTRING
    ├── MULTIPOLYGON
    └── GEOMETRYCOLLECTION
```

### 7.1 Tipo general o específico

Una columna `GEOMETRY` puede admitir valores de diferentes clases. Una columna `POINT` restringe la clase geométrica. Si todas las estaciones deben representarse puntualmente, `POINT` comunica mejor la intención y evita insertar una línea o un polígono por error.

El principio es análogo a elegir `DATE` en vez de una cadena genérica: un tipo específico expresa dominio y habilita operaciones coherentes.

### 7.2 Colecciones y multiplicidad

Los tipos `MULTI*` representan varias geometrías de una misma familia dentro de un valor. Una zona fragmentada podría requerir `MULTIPOLYGON`. Sin embargo, introducir colecciones antes de necesitarlas aumentaría complejidad. ObservaSur comenzará con zonas simples y trasladará multiplicidad a profundización.

### 7.3 Tipo geométrico y cardinalidad relacional

Una colección geométrica no sustituye automáticamente una relación uno-a-muchos. Si cada elemento necesita identidad, atributos o historia independiente, conviene modelarlo en filas relacionadas. Elegir entre una colección dentro de un valor y varias filas es una decisión semántica, no solo técnica.

## 8. Comparación sistemática de representaciones

Consideremos cuatro alternativas para la ubicación de una estación.

### 8.1 Texto libre

```text
'frente al edificio principal'
```

Es comprensible para una persona, pero difícil de validar y consultar geométricamente. Puede conservarse como descripción complementaria, no como única representación para preguntas espaciales.

### 8.2 WKT almacenado como texto

```text
'POINT(25 75)'
```

La estructura parece espacial, pero una columna `VARCHAR` continúa siendo texto para el SGBD. El motor puede comparar cadenas, no aplicar automáticamente relaciones geométricas ni validar el SRID.

### 8.3 Componentes escalares

```text
coordenada_x = 25
coordenada_y = 75
```

Facilita importación inicial y algunas comprobaciones por atributo. Sin embargo, cada consulta debe reconstruir el valor y repetir convenciones. El esquema no impide que un componente se interprete bajo otro sistema.

### 8.4 Tipo `POINT`

La ubicación se almacena como un valor espacial. El esquema puede restringir tipo y SRID, y las consultas pueden utilizar funciones espaciales. El tipo no resuelve por sí solo calidad, exactitud o corrección del origen, pero hace explícito un contrato antes implícito.

### 8.5 Matriz de decisión

| Criterio | Texto libre | WKT en `VARCHAR` | `x`,`y` escalares | `POINT` con SRID |
|---|---:|---:|---:|---:|
| lectura humana inmediata | alta | alta | media | requiere conversión de salida |
| estructura verificable por el SGBD | baja | baja | parcial | alta |
| relación espacial declarativa | no | no directa | reconstrucción repetida | sí |
| restricción de SRID | no | no | columnas auxiliares | declarable |
| índice espacial | no | no | no como geometría | disponible bajo condiciones |
| intercambio sencillo | narrativo | bueno | bueno | mediante WKT/WKB |

La elección para ObservaSur será conservar un `POINT` como ubicación gestionada y utilizar WKT solamente en la interfaz de entrada/salida didáctica.

## 9. Fundamentos de integridad espacial

El capítulo 1 mostró cuatro capas de integridad. Ahora podemos formular controles espaciales más concretos.

### 9.1 Tipo

La ubicación de una estación debe ser un punto; la extensión de una zona, un polígono. Usar columnas específicas expresa esta regla en el esquema.

### 9.2 Sistema de referencia

Las geometrías que participan en una operación deben compartir una interpretación compatible. Restringir columnas por SRID evita mezclar inadvertidamente valores etiquetados con sistemas diferentes.

### 9.3 Buena formación y validez

Una codificación puede estar mal formada y no producir geometría. Una geometría bien formada puede violar reglas de validez, por ejemplo, un polígono con configuración problemática. MySQL distingue aspectos de buena formación y validez; su comportamiento exacto debe comprobarse en la revisión utilizada [@mysqlValidity2026, sec. 13.4.4].

### 9.4 Reglas entre objetos

Una regla como “toda estación activa debe ubicarse dentro de alguna zona operativa” involucra varias filas y un predicado espacial. No se reduce a `NOT NULL` o FK. Puede requerir consultas de auditoría, lógica de carga o mecanismos adicionales.

### 9.5 Procedencia

Una geometría puede ser correcta sintácticamente y estar mal obtenida. Debe conservarse de dónde provino, cuándo se capturó, qué transformación recibió y qué calidad se le atribuye cuando esas preguntas sean relevantes.

## 10. Integración Python–MySQL para la preparación de geometrías

### 10.1 Preparación de datos en Python

Python puede leer componentes escalares, comprobar que son convertibles a número y construir una cadena WKT en un ejemplo didáctico controlado:

```python
def punto_wkt(x, y):
    return f"POINT({x} {y})"
```

Esta función solo produce texto conforme a una convención. No crea por sí misma un valor geométrico almacenado, no comprueba el dominio espacial de los componentes y no asigna un SRS. En una carga real debe complementarse con un contrato de entrada y con la construcción parametrizada ejecutada por MySQL.

### 10.2 Construcción de geometrías en MySQL

El texto y el SRID se entregarán a una función constructora de MySQL. En términos conceptuales:

```text
texto WKT + SRID
        ↓ constructor de MySQL
valor geométrico
        ↓ columna POINT restringida
estado persistente validado por el esquema
```

El capítulo siguiente desarrollará la sintaxis y los casos de error.

### 10.3 Comparación de representaciones desde Python

En la práctica asociada, Python recupera zona declarada, componentes escalares y una cadena WKT construida para presentación. Los estudiantes comparan qué significado puede garantizar cada representación. No calculan contención manualmente ni insertan todavía geometrías: ambas operaciones corresponden a capítulos posteriores.

### 10.4 Contrato de entrada

Antes de construir geometrías, el cliente debe conocer:

- nombres y orden de campos;
- tipo convertible de cada componente;
- convención de ejes;
- SRID esperado;
- tratamiento de valores faltantes;
- política de rechazo.

Una función Python que solo concatena valores sin comprobar este contrato automatiza errores más rápidamente.

## 11. Diseño espacial inicial de ObservaSur

### 11.1 Requerimientos de consulta

El sistema debe responder en etapas:

1. ¿qué zona fue declarada para la estación?;
2. ¿qué posición se registró?;
3. ¿qué zona contiene esa posición?;
4. ¿la zona declarada coincide con la calculada?;
5. ¿qué ocurre si la estación está en el límite?;
6. ¿qué ubicación era válida al producir una observación?

### 11.2 Decisiones iniciales

- `ESTACION` mantiene identidad estable y atributos propios.
- La posición actual se representará inicialmente como `POINT`.
- `ZONA` conserva identidad y atributos administrativos.
- La extensión se representará inicialmente como `POLYGON`.
- Ambas geometrías utilizarán SRID 0 en el caso ficticio.
- WKT se utilizará como notación didáctica e interfaz de carga.
- `id_zona_declarada` se conservará para comparar asignación administrativa con relación espacial calculada.

### 11.3 Decisiones diferidas

- relación exacta para tratar la frontera;
- validaciones disponibles en la revisión instalada;
- uso de índice espacial;
- historial de ubicación y de zonas;
- transformación entre SRS;
- incertidumbre o exactitud posicional.

Postergar estas decisiones es deliberado. Cada una se abordará cuando aparezca una pregunta que la necesite.

## 12. Errores conceptuales y técnicos frecuentes

### 12.1 Confundir coordenadas con geometría

Las coordenadas son componentes; la geometría añade estructura y tipo.

### 12.2 Confundir SRID con transformación

Cambiar o asignar el número no recalcula coordenadas. Etiquetar incorrectamente produce una interpretación falsa.

### 12.3 Suponer que `POINT` significa GPS

Un punto puede pertenecer a un plano local, una imagen o un SRS terrestre. El tipo no determina por sí solo el sistema.

### 12.4 Almacenar WKT en texto y creer que está indexado espacialmente

La apariencia del contenido no cambia el tipo SQL de la columna.

### 12.5 Elegir polígono porque “es más preciso”

Una geometría más compleja solo es mejor si preserva propiedades necesarias para las preguntas.

### 12.6 Calcular en Python lo que se desea aprender en SQL espacial

La práctica puede preparar valores en Python, pero las futuras relaciones espaciales deben quedar expresadas en MySQL.

## 13. Conclusiones

- Una ubicación es interpretable solo dentro de un contrato de coordenadas y referencia.
- Objeto, entidad, propiedad espacial, geometría y codificación son niveles diferentes.
- Punto, línea y polígono abstraen posición, trazado y extensión.
- El SRID refiere a la definición de un SRS; no transforma valores.
- WKT comunica geometrías de forma legible, pero no es el tipo interno del SGBD.
- Un tipo específico expresa mejor el dominio y habilita operaciones e integridad.
- Python prepara y transmite valores; MySQL construye, valida conforme al esquema, conserva y opera sobre geometrías.
- ObservaSur usará un plano cartesiano ficticio con SRID 0 para aprender sin presuponer cartografía.

## 14. Ejercicios y casos prácticos resueltos

### Ejercicio 1. Nivel básico: separar niveles de representación

Clasifique cada elemento:

1. estación Mirador;
2. fila `ESTACION(1, 'EST-N01', ...)`;
3. posición operativa de Mirador;
4. `POINT(25 75)`;
5. bytes usados internamente por MySQL.

#### Resolución paso a paso

**Paso 1. Identificar el dominio.** “Estación Mirador” es el objeto del dominio.

**Paso 2. Identificar el registro.** La fila es la representación lógica de hechos seleccionados sobre esa estación.

**Paso 3. Identificar la propiedad.** La posición operativa es la propiedad espacial elegida.

**Paso 4. Identificar geometría y notación.** `POINT` es la clase geométrica; `POINT(25 75)` es su expresión WKT concreta.

**Paso 5. Identificar persistencia.** Los bytes corresponden a la codificación interna, que no debe interpretarse manualmente desde la aplicación.

**Conclusión.** Los cinco elementos están relacionados, pero no son intercambiables.

### Ejercicio 2. Nivel básico–intermedio: elegir una geometría

Seleccione una geometría inicial y justifique:

1. posición de una estación a escala regional;
2. eje de un camino entre estaciones;
3. extensión de una zona operativa;
4. recinto detallado de una estación cuando interesa saber qué objetos atraviesan su límite.

#### Resolución paso a paso

**Caso 1.** `POINT`, porque interesa posición y no extensión interna.

**Caso 2.** `LINESTRING`, porque debe preservarse un trazado ordenado.

**Caso 3.** `POLYGON`, porque se necesita representar una superficie y consultar pertenencia.

**Caso 4.** `POLYGON`, porque la extensión y el límite del recinto participan en la pregunta.

**Comprobación.** Las elecciones dependen del propósito. La estación del caso 1 y la del caso 4 pueden ser el mismo tipo de objeto real representado de manera distinta para preguntas diferentes.

### Ejercicio 3. Nivel intermedio: interpretar WKT y detectar errores

Analice:

```text
A = POINT(25 75)
B = LINESTRING(10 10, 40 30, 80 20)
C = POLYGON((0 50, 100 50, 100 100, 0 100))
D = POINT(25, 75)
```

#### Resolución paso a paso

**A.** Representa un punto con dos componentes. La sintaxis básica es coherente, pero no informa por sí sola el SRID.

**B.** Representa una secuencia de tres puntos y dos segmentos.

**C.** Pretende representar un polígono, pero el anillo no está cerrado: falta repetir `0 50` al final.

**D.** Usa una coma entre los componentes del punto. En WKT, los componentes de un punto se separan mediante espacio; la coma separa puntos en geometrías que contienen secuencias.

Una corrección para C es:

```text
POLYGON((0 50, 100 50, 100 100, 0 100, 0 50))
```

Una corrección para D es:

```text
POINT(25 75)
```

### Ejercicio 4. Nivel avanzado: diseñar el contrato de ubicación

Un archivo contiene:

```text
codigo;x;y;sistema
EST-N01;25;75;local
EST-N02;-36.82;-73.05;WGS84
```

Diseñe las decisiones mínimas necesarias antes de cargar ambas filas como puntos.

#### Resolución paso a paso

**Paso 1. Reconocer heterogeneidad.** La primera fila parece pertenecer a una cuadrícula local; la segunda parece usar valores angulares terrestres. No deben cargarse automáticamente en una misma columna restringida por SRID.

**Paso 2. Definir el significado de campos.** Para cada sistema deben conocerse orden de ejes, unidad, dominio admisible y definición del SRS. “WGS84” como texto informal no basta para decidir automáticamente el orden usado por el archivo.

**Paso 3. Seleccionar SRID.** El plano pedagógico podría usar SRID 0. Para la fila terrestre debe verificarse la definición apropiada y la convención de ejes; no se asigna un código solo por apariencia.

**Paso 4. Elegir política de carga.** Alternativas válidas incluyen separar staging por fuente, normalizar ambas a un SRS acordado mediante un proceso verificado o rechazar la mezcla hasta disponer de metadatos.

**Paso 5. Asignar responsabilidades.** Python lee, convierte y clasifica las filas; MySQL construye valores con el SRID declarado y aplica restricciones. Una transformación, si se requiere, debe ser explícita, trazable y compatible con la versión instalada.

**Paso 6. Registrar procedencia.** Deben conservarse fuente, sistema declarado y resultado de validación para no ocultar supuestos.

**Conclusión.** La conversión sintáctica a `POINT` es la parte más sencilla; el trabajo central es preservar significado.

## 15. Temas de profundización

### 15.1 Geometría y topología

La geometría estudia propiedades métricas y formas; la topología se ocupa de propiedades preservadas bajo transformaciones continuas, como conexión, interior y frontera. Las relaciones espaciales de capítulos posteriores se apoyarán en estas nociones, pero se introducirán mediante casos antes de formalizarlas.

### 15.2 Geometrías múltiples

Una entidad puede ocupar varias partes separadas. `MULTIPOLYGON` permite representarlas como un único valor compuesto. Se debe decidir si las partes carecen de identidad propia o si corresponde modelarlas como filas relacionadas.

### 15.3 Sistemas geográficos y proyectados

Un SRS geográfico representa posiciones mediante coordenadas angulares sobre un elipsoide; uno proyectado representa posiciones en un plano mediante una proyección y suele usar unidades de longitud [@mysqlSRS2026, sec. 13.4.5]. Esta distinción será referencia técnica, no prerrequisito de las prácticas iniciales.

## 16. Referencia técnica

- OGC Simple Feature Access 1.2.1 define la arquitectura común de geometrías simples.
- MySQL 8.0 admite `POINT`, `LINESTRING`, `POLYGON`, tipos múltiples y `GEOMETRY`.
- Las columnas pueden restringirse por SRID.
- SRID 0 representa un plano cartesiano abstracto sin unidad asignada.
- WKT se utilizará para ejemplos y entrada/salida; MySQL almacena una representación interna.
- Las funciones constructoras y de inspección se desarrollarán en el capítulo 3.

Con este vocabulario ya es posible pasar de la representación conceptual a la implementación. El capítulo 3 desarrollará la construcción, el almacenamiento y la validación de geometrías en MySQL, mientras Python se utilizará para preparar entradas y comprobar resultados sin sustituir las responsabilidades del SGBD.

## 17. Referencias bibliográficas

Güting, R. H. (1994). An introduction to spatial database systems. *The VLDB Journal, 3*, 357–399. https://doi.org/10.1007/BF01231602

MySQL. (2026). *MySQL 8.0 Reference Manual: Geometry well-formedness and validity*. https://dev.mysql.com/doc/refman/8.0/en/geometry-well-formedness-validity.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Spatial data types*. https://dev.mysql.com/doc/refman/8.0/en/spatial-type-overview.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Spatial reference system support*. https://dev.mysql.com/doc/refman/8.0/en/spatial-reference-systems.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Supported spatial data formats*. https://dev.mysql.com/doc/refman/8.0/en/gis-data-formats.html

MySQL. (2026). *MySQL 8.0 Reference Manual: Data type storage requirements*. https://dev.mysql.com/doc/refman/8.0/en/storage-requirements.html

Open Geospatial Consortium. (2011). *OpenGIS implementation standard for geographic information—Simple feature access—Part 1: Common architecture* (Version 1.2.1, OGC 06-103r4). https://www.ogc.org/standards/sfa/

Rigaux, P., Scholl, M. y Voisard, A. (2002). *Spatial databases: With application to GIS*. Morgan Kaufmann.
