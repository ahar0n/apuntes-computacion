# Capítulo 1. Fundamentos de datos complejos y extensión del modelo relacional

## Objetivos de aprendizaje

Este capítulo inicia el tránsito desde una base relacional convencional hacia una base capaz de representar y consultar información espacial. No requiere conocimientos previos de cartografía o SIG. Utiliza el modelado, la integridad, SQL y Python ya estudiados para descubrir una limitación concreta.

Al terminar el núcleo obligatorio, el estudiante podrá:

1. interpretar el predicado de una tabla y reconocer la identidad de sus entidades;
2. recuperar información relacionada mediante claves y consultas parametrizadas;
3. distinguir una zona declarada administrativamente de una relación espacial todavía no calculada;
4. explicar por qué almacenar coordenadas no equivale por sí solo a modelar una ubicación;
5. describir qué responsabilidades corresponden a MySQL y cuáles al cliente Python;
6. formular requerimientos que justifican incorporar tipos y operaciones espaciales.

El capítulo contribuye principalmente a R1 y prepara R2 y R4 del programa oficial.

---

## Introducción

El problema que orienta el capítulo puede formularse mediante la siguiente pregunta: ¿por qué conocer **qué estación** produjo una observación no basta para determinar **dónde ocurrió**? La respuesta exige examinar los límites semánticos del esquema relacional inicial y establecer qué mecanismos adicionales requiere la representación de datos espaciales.

Antes de iniciar este capítulo, el recorrido introductorio del libro mostró una observación atravesando una base operacional, un proceso ETL, un almacén dimensional, una consulta OLAP y un ejercicio de descubrimiento de patrones. Ese panorama funciona como mapa del curso, pero no explica todavía por qué el resultado es válido. El desarrollo comienza deliberadamente en el origen: el significado de las filas, la identidad de los objetos, la integridad y las limitaciones de su representación. Las decisiones construidas aquí serán reutilizadas posteriormente por el almacén y el proceso de minería.

## 1. Caso de estudio y formulación del problema

La organización ficticia **ObservaSur** mantiene estaciones que producen observaciones. En la primera versión de su base, cada estación posee un código, un nombre, dos coordenadas numéricas y una zona operativa declarada.

```text
ZONA(
    id_zona,
    nombre
)

ESTACION(
    id_estacion,
    codigo,
    nombre,
    coordenada_x,
    coordenada_y,
    id_zona_declarada
)

OBSERVACION(
    id_observacion,
    id_estacion,
    instante_observacion,
    variable,
    valor,
    unidad
)
```

En esta versión se han simplificado deliberadamente las variables y unidades. Más adelante se normalizarán y se incorporarán fuente, tiempo de carga y calidad.

### 1.1 Predicados del esquema inicial

Una tabla no es solamente una cuadrícula. Cada fila debe poder interpretarse como una afirmación. El modelo relacional organiza datos mediante relaciones, atributos, dominios y restricciones; su significado no depende de la interfaz que los muestra [@codd1970, pp. 377–383; @elmasri2016, cap. 2].

Para el esquema inicial pueden proponerse estos predicados:

- `ZONA`: la zona identificada por `id_zona` tiene el nombre indicado.
- `ESTACION`: la estación identificada por `id_estacion` tiene el código, nombre, coordenadas y zona declarada indicados.
- `OBSERVACION`: la observación identificada por `id_observacion` fue producida por una estación, en un instante, para una variable, con un valor y una unidad.

Expresar el predicado permite detectar ambigüedades. `id_zona_declarada` podría significar:

- la zona responsable de administrar la estación;
- la zona que contiene espacialmente la estación;
- la zona a la que alguien la asignó al cargar los datos.

Estas afirmaciones no son equivalentes.

## 2. Modelo de datos, esquema y estado

El problema de ObservaSur no se resuelve eligiendo inmediatamente una función o un formato. Primero se necesita distinguir tres niveles de descripción: el modelo de datos, el esquema y el estado de la base. Esta distinción permite separar las reglas relativamente estables de una aplicación de los valores que cambian durante su funcionamiento.

### 2.1 Modelo de datos

Un **modelo de datos** proporciona conceptos para describir la estructura de los datos, sus asociaciones, las restricciones que deben satisfacer y las operaciones disponibles para manipularlos [@elmasri2016, cap. 2; @silberschatz2020, caps. 2–3]. Una representación abstracta útil es:

\[
M=(C,O,R),
\]

donde:

- \(C\) es el conjunto de constructores estructurales;
- \(O\) es el conjunto de operaciones;
- \(R\) es el conjunto de reglas o restricciones.

En el modelo relacional, \(C\) incluye relaciones, atributos, tuplas y dominios; \(O\) incluye selección, proyección, reunión y operaciones de conjuntos; y \(R\) incluye restricciones de dominio, claves y referencias. La propuesta original de Codd separa la descripción lógica de los datos de detalles de acceso y representación física [@codd1970, pp. 377–383]. Por ello, una consulta expresa principalmente **qué** filas cumplen una condición, mientras el SGBD decide **cómo** acceder a ellas.

El modelo no es una base concreta ni un diagrama particular. Es el lenguaje conceptual con el que pueden construirse muchos esquemas. Decir “modelo relacional” no informa todavía qué estaciones existen, ni siquiera qué tablas tendrá ObservaSur; informa qué clases de constructores, operaciones y reglas pueden emplearse.

### 2.2 Esquema

Un **esquema** es una especificación relativamente estable construida mediante un modelo de datos. Declara nombres de relaciones y atributos, dominios, claves y restricciones. Puede representarse de manera simplificada como:

\[
S=(D,K,F,C),
\]

donde \(D\) reúne las definiciones de datos, \(K\) las claves, \(F\) las referencias y \(C\) otras condiciones de integridad.

El esquema inicial de ObservaSur declara, por ejemplo, que:

- `id_estacion` identifica una estación;
- `codigo` no debe repetirse;
- `id_zona_declarada` debe referir a una zona existente;
- cada observación debe referir a una estación existente;
- `valor` pertenece a un dominio numérico definido por su tipo SQL.

El esquema todavía no declara una geometría para la zona ni una relación de contención. Esa ausencia no es un detalle de implementación: limita las afirmaciones que la base puede comprobar.

### 2.3 Estado o instancia

El **estado**, **instancia** o **extensión** de la base es el conjunto de valores almacenados en un momento. Si \(I_t\) representa el estado en el instante \(t\), un estado admisible debe satisfacer el esquema:

\[
I_t \models S.
\]

La expresión se lee: “el estado \(I_t\) satisface el esquema \(S\)”. Por ejemplo, una fila con `id_zona_declarada = 99` viola el esquema si no existe la zona 99. En cambio, una estación puede referir correctamente a la zona 2 y, al mismo tiempo, encontrarse fuera de sus límites reales. Ese estado satisface las restricciones **declaradas**, porque la coherencia espacial aún no forma parte de \(S\).

Esta deducción es central:

1. un SGBD solo puede preservar reglas expresadas mediante mecanismos disponibles;
2. el esquema inicial expresa integridad referencial;
3. no expresa geometrías ni relaciones espaciales;
4. por tanto, aceptar una fila no demuestra que su asignación sea espacialmente correcta.

### 2.4 Representación lógica y física

El esquema anterior es lógico: permite hablar de estaciones y observaciones sin indicar en qué página, archivo o estructura de acceso reside cada fila. La representación física describe cómo el SGBD organiza bytes, páginas e índices. Esta separación hace posible añadir un índice sin cambiar necesariamente la consulta formulada por una aplicación [@silberschatz2020, cap. 14].

Más adelante ocurrirá algo semejante con el índice espacial. Primero se definirá qué significa una consulta; después se estudiará una estructura física que reduzca candidatos. Confundir ambos niveles lleva a elegir tecnología antes de formular correctamente el problema.

## 3. Semántica de relaciones y predicados

### 3.1 Una fila como proposición

Para interpretar una relación se asocia un **predicado**: una proposición abierta cuyos parámetros corresponden a atributos. Sustituir esos parámetros por los valores de una tupla produce una afirmación que la base considera verdadera.

Para `ESTACION`, un predicado inicial podría ser:

> La estación identificada por `id_estacion` posee el código `codigo`, el nombre `nombre`, los componentes numéricos `coordenada_x` y `coordenada_y`, y tiene declarada la zona `id_zona_declarada`.

Esta formulación obliga a utilizar “tiene declarada”, no “está contenida”, porque el esquema almacena una referencia administrativa. Si el significado pretendido fuese contención, la tabla estaría afirmando más de lo que sus restricciones pueden verificar.

### 3.2 Dominio y significado

Un dominio no es solamente el tipo físico elegido. `DECIMAL(8,2)` define una clase de valores representables, pero no declara si el número corresponde a metros, grados, una cuadrícula local o un código. La semántica completa requiere al menos:

- significado del atributo;
- unidad cuando corresponda;
- valores o intervalos admisibles;
- convención para ausencias;
- procedencia y calidad cuando afecten su interpretación.

Dos columnas pueden compartir tipo SQL y tener dominios conceptuales incompatibles. No sería válido comparar directamente una coordenada expresada en grados con otra expresada en metros solo porque ambas usan `DECIMAL`.

### 3.3 Claves e identidad

Una **superclave** es un conjunto de atributos que distingue tuplas; una **clave candidata** es una superclave mínima; la **clave primaria** es la candidata elegida como identificador principal [@elmasri2016, caps. 3–5]. En ObservaSur, `id_estacion` actúa como clave primaria y `codigo` como clave candidata alternativa protegida por `UNIQUE`.

La clave distingue representaciones registradas, pero debe elegirse conforme a la identidad del dominio. Usar coordenadas como clave sería inadecuado:

- dos estaciones distintas pueden compartir una posición;
- una corrección de coordenadas no debería crear otra estación;
- la ubicación puede cambiar a lo largo del tiempo;
- valores medidos pueden tener redondeo o incertidumbre.

La identidad de la estación debe permanecer estable aunque algunos atributos cambien.

### 3.4 Integridad

Las restricciones pueden agruparse, para este caso, en cuatro capas:

1. **integridad de entidad:** cada estación u observación tiene identidad no nula y no repetida;
2. **integridad de dominio:** los atributos contienen valores de una clase admisible;
3. **integridad referencial:** una observación refiere a una estación existente y una zona declarada refiere a una zona existente;
4. **integridad del dominio de aplicación:** las combinaciones de valores respetan reglas de ObservaSur.

La futura integridad espacial pertenecerá principalmente a la cuarta capa y utilizará tipos y operaciones espaciales. Puede exigir que una ubicación tenga el tipo previsto, utilice un sistema de referencia acordado, sea geométricamente válida y satisfaga determinadas relaciones con otros objetos.

La integridad no debe confundirse con limpieza posterior. Una restricción preventiva impide ciertos estados; una consulta de auditoría detecta otros; un proceso de carga decide qué hacer con los datos rechazados. Las tres estrategias son necesarias cuando el SGBD no puede expresar toda la regla mediante una declaración sencilla.

## 4. Objeto del dominio, identidad y representación

### 4.1 Distinción entre objeto, entidad y representación geométrica

En el caso conductor deben separarse:

1. **objeto del dominio:** la estación que existe y opera para ObservaSur;
2. **entidad registrada:** la identidad y los atributos que el esquema conserva sobre ella;
3. **representación espacial:** la geometría seleccionada para describir alguna dimensión espacial del objeto.

La estación no es su fila y tampoco es su futuro `POINT`. Una fila es una proposición registrada; un punto representará una ubicación conforme a una convención.

### 4.2 Identidad frente a igualdad de valores

La **igualdad de valor** compara representaciones. Dos filas podrían tener el mismo nombre y las mismas coordenadas. La **identidad** responde si representan la misma entidad persistente. Estas nociones no coinciden [@atkinson1990, pp. 225–232].

Considere dos situaciones:

- se instalan dos dispositivos independientes en el mismo recinto: comparten coordenadas, pero pueden constituir estaciones distintas;
- se corrige la posición registrada de una estación: cambian coordenadas, pero la estación conserva identidad.

Por tanto:

\[
igualdad\ de\ coordenadas \nRightarrow misma\ estación,
\]

y

\[
cambio\ de\ coordenadas \nRightarrow nueva\ estación.
\]

Esta distinción prepara el modelado temporal: la identidad estable se mantendrá separada del historial de ubicaciones.

### 4.3 Abstracción según el propósito

Toda representación selecciona propiedades y omite otras. Una estación puede representarse como punto cuando interesan cercanía o pertenencia a una zona. Si el problema fuese administrar el recinto completo, quizá se requeriría un polígono. Si se estudiara una ruta recorrida por un equipo móvil, podría necesitarse una línea o secuencia de posiciones.

No existe una geometría correcta independientemente de las preguntas. La representación se evalúa por su capacidad para preservar los hechos y operaciones relevantes [@rigaux2002, caps. 1–2; @manolopoulos2005, caps. 1–2].

## 5. Valores escalares y datos complejos

### 5.1 Valor escalar

En este curso llamaremos **escalar** a un valor tratado como una unidad dentro del esquema y dotado de operadores convencionales de su dominio. Para enteros existen orden y aritmética; para cadenas, igualdad, orden lexicográfico y operaciones textuales; para fechas, orden y operaciones temporales básicas.

“Escalar” no significa “simple en el mundo”. Un código institucional puede encerrar estructura, pero si la aplicación solo necesita almacenarlo y compararlo como una unidad, puede modelarse como cadena. La decisión depende de las operaciones requeridas.

### 5.2 Valor estructurado

Un valor estructurado contiene componentes cuya organización forma parte de su significado. Una posición bidimensional puede expresarse inicialmente como un par ordenado:

\[
p=(x,y).
\]

El orden importa: \((x,y)\) no puede sustituirse por el conjunto \(\{x,y\}\). Tampoco toda pareja de números pertenece al dominio pretendido. Deben conocerse sistema de referencia, ejes, unidad y región admisible.

Una zona puede representarse mediante una secuencia de puntos que forma uno o más anillos. Sin embargo, no toda secuencia produce un polígono válido. El dato posee reglas que involucran varios componentes.

### 5.3 Tipo como valores, operaciones y restricciones

Para analizar un tipo especializado es útil representarlo como:

\[
T=(V_T,O_T,R_T),
\]

donde \(V_T\) contiene los valores admitidos, \(O_T\) las operaciones definidas y \(R_T\) las reglas que determinan representaciones válidas.

Para un tipo espacial `POINT`:

- \(V_T\) contiene posiciones representables;
- \(O_T\) puede incluir construcción, recuperación de componentes, distancia o relaciones con otras geometrías;
- \(R_T\) incluye estructura, dimensionalidad y coherencia con el sistema de referencia.

Guardar `x` e `y` por separado conserva componentes, pero no crea automáticamente este contrato.

### 5.4 Definición operacional de dato complejo

En este libro, un **dato complejo** es un valor cuya gestión correcta requiere una o más de estas capacidades:

- preservar estructura interna significativa;
- disponer de operaciones específicas del dominio;
- validar reglas que involucran varios componentes;
- conservar identidad o referencias;
- representar extensión espacial o vigencia temporal;
- utilizar métodos especializados de consulta o indexación;
- registrar procedencia, precisión o calidad necesarias para interpretarlo.

La complejidad no depende del tamaño. Un punto puede ocupar poco espacio y, aun así, necesitar semántica e indexación especializadas. Una cadena muy extensa puede ser físicamente grande, pero permanecer opaca para el SGBD.

### 5.5 Persistencia de bytes frente a gestión del significado

Todo valor digital termina codificado como bytes. Pero una base de datos no se evalúa solo por su capacidad de guardar bytes. Una representación adecuada debe permitir:

1. construir valores sin ambigüedad;
2. rechazar o detectar valores inválidos;
3. formular las operaciones del dominio;
4. comparar resultados mediante reglas conocidas;
5. elegir estructuras de acceso compatibles;
6. mantener significado al actualizar o intercambiar datos.

Guardar coordenadas como texto, por ejemplo, resuelve persistencia elemental. No garantiza orden de ejes, separador, número de componentes, SRID ni disponibilidad de predicados espaciales.

## 6. Requerimientos para gestionar datos complejos

Reconocer un dato complejo no basta. Deben derivarse requisitos verificables para el SGBD y para el esquema.

### 6.1 Representación

La representación debe conservar los componentes y convenciones que necesitan las preguntas. Para una ubicación se deben decidir, progresivamente:

- geometría apropiada;
- número y orden de coordenadas;
- sistema de referencia;
- dimensionalidad;
- tratamiento de valores ausentes o inciertos.

### 6.2 Operaciones

Las operaciones derivan de las preguntas, no de un catálogo de funciones. “Estaciones dentro de una zona” requiere un predicado espacial; “estaciones próximas” requiere una medida y un umbral; “ubicación en una fecha” requiere además una selección temporal.

Una consulta solo es correcta si el operador corresponde al significado. Igualdad de coordenadas no equivale a cercanía; intersección no equivale necesariamente a contención.

### 6.3 Integridad

La integridad debe abarcar la forma interna y las relaciones con otros datos. Para una ubicación pueden existir reglas como:

- el valor no es nulo para estaciones activas;
- la geometría es un punto;
- utiliza el SRID acordado;
- sus componentes se encuentran en el dominio esperado;
- no contradice una asignación que el negocio exige mantener coherente.

No todas estas reglas se implementarán en el primer capítulo. Aquí se identifican como requisitos; los mecanismos se incorporarán gradualmente.

### 6.4 Consulta declarativa

Una base espacial debe permitir expresar **qué relación** se busca sin programar manualmente el recorrido de coordenadas. Esta propiedad mantiene el puente con SQL: el estudiante formula una condición y el SGBD selecciona una estrategia de ejecución.

### 6.5 Indexación y procesamiento

Un operador correcto puede ser costoso sobre muchos objetos. Los datos espaciales requieren estructuras capaces de descartar candidatos usando más de una dimensión. El índice espacial se estudiará después de comprender tipos, relaciones e integridad; no tiene sentido optimizar una pregunta mal formulada.

### 6.6 Actualización e historia

Sobrescribir una ubicación elimina el valor anterior. Si el dominio necesita responder dónde estaba una estación cuando produjo una observación, la actualización debe convertirse en historial. El requerimiento espacial conduce así a un requerimiento temporal.

### 6.7 Intercambio y procedencia

Los datos pueden llegar desde archivos, dispositivos o procesos manuales. Para interpretarlos se necesita saber, según el caso, fuente, unidad, tiempo, sistema de referencia, calidad y transformaciones aplicadas. Python ayudará a leer y preparar entradas; MySQL conservará los valores y reglas compartidos.

## 7. Comparación de representaciones iniciales

Antes de elegir un tipo espacial conviene comparar alternativas respecto de las preguntas.

| Representación | Qué conserva | Qué permite fácilmente | Limitación principal |
|---|---|---|---|
| `id_zona_declarada` | asociación administrativa | reuniones por clave | no demuestra relación geométrica |
| `ubicacion_texto` | caracteres según una convención externa | mostrar o intercambiar texto | estructura, unidad y operaciones quedan implícitas |
| `coordenada_x`, `coordenada_y` | dos componentes numéricos | filtros y cálculos escalares | no forman un valor espacial gestionado |
| geometría especializada | estructura espacial y SRID, según definición | operadores espaciales y futura indexación | exige aprender semántica y soporte del SGBD |

### 7.1 Deducción desde los requerimientos

Considere la pregunta “¿qué estaciones están dentro de la zona Norte?”.

1. Se necesita representar la ubicación de cada estación.
2. Se necesita representar el límite de la zona.
3. Ambas representaciones deben ser comparables.
4. Se necesita definir qué significa “dentro”, incluidos los casos de frontera.
5. El SGBD debe ofrecer un predicado que implemente esa relación.
6. La carga debe preservar las convenciones usadas por ambas geometrías.

La conclusión no es simplemente “usar un mapa”. Es incorporar tipos, operaciones y restricciones al esquema relacional.

### 7.2 Extensión del repertorio de tipos y operaciones

La base seguirá utilizando relaciones, claves, referencias y SQL. La extensión espacial añade dominios geométricos y operadores especializados. La identidad de estación continúa en una relación; sus observaciones continúan referidas por clave; solo la ubicación adquiere una representación mejor adaptada a las preguntas.

Los sistemas extensibles muestran que un SGBD puede incorporar tipos y operaciones más ricos sin sustituir la organización relacional ni convertir cada valor en un objeto persistente [@atkinson1990, pp. 225–232]. Para este curso importa la consecuencia práctica: los conocimientos de Base de Datos I siguen vigentes y se amplían mediante dominios geométricos, operadores espaciales y estructuras de acceso especializadas.

## 8. Reutilización de operaciones relacionales

Para recuperar las estaciones y sus zonas declaradas puede utilizarse una reunión por claves:

```sql
SELECT
    e.codigo,
    e.nombre AS estacion,
    z.nombre AS zona_declarada
FROM estacion AS e
JOIN zona AS z
  ON z.id_zona = e.id_zona_declarada
ORDER BY e.codigo;
```

La consulta es correcta respecto del esquema: relaciona una clave foránea con la clave primaria referida. También puede consultarse una estación desde Python sin concatenar valores en el texto SQL:

```python
consulta = """
    SELECT codigo, nombre, coordenada_x, coordenada_y
    FROM estacion
    WHERE codigo = %s
"""

cursor.execute(consulta, (codigo_buscado,))
fila = cursor.fetchone()
```

Connector/Python establece conexiones mediante `connect()` y permite ejecutar una operación con parámetros a través de un cursor [@mysqlConnectorConnection2026; @mysqlConnectorExecute2026]. La separación entre el texto de la consulta y sus parámetros evita tratar el dato introducido como parte de la sintaxis SQL.

### 8.1 Alcance semántico de la consulta

La consulta demuestra que:

- la estación existe;
- la zona declarada existe, si la clave foránea está activa;
- existe una asociación explícita entre ambas filas;
- MySQL puede recuperar esa asociación de manera declarativa.

### 8.2 Limitaciones semánticas de la consulta

La consulta no demuestra que las coordenadas de la estación estén dentro de los límites de la zona. La clave foránea preserva **integridad referencial**, no **coherencia espacial**.

Este contraste será uno de los puentes centrales del curso:

> reunión por claves → asociación almacenada;

> relación espacial → asociación calculada a partir de geometrías.

Todavía no se dispone de la geometría de la zona ni de una operación espacial. Por eso la pregunta “¿la estación está realmente dentro?” no puede responderse correctamente con el esquema inicial.

## 9. Limitaciones de la representación escalar de ubicaciones

Las columnas `coordenada_x` y `coordenada_y` preservan dos números. Eso permite:

- mostrarlos;
- ordenarlos;
- compararlos individualmente;
- aplicar operaciones aritméticas.

Pero el esquema todavía no expresa:

- qué representa cada eje;
- en qué orden deben interpretarse;
- cuál es su unidad;
- cuál es el sistema de referencia;
- qué conjunto de valores forma una posición;
- qué operaciones espaciales son válidas;
- cómo comprobar la relación entre la estación y una zona.

Un valor se vuelve complejo para la gestión cuando su significado depende de estructura interna, operaciones específicas o reglas que no se preservan tratándolo como componentes escalares independientes [@atkinson1990, pp. 225–232]. Un punto contiene pocos números, pero necesita semántica espacial.

MySQL 8.0 dispone de tipos espaciales como `POINT`, `LINESTRING` y `POLYGON`, además de columnas restringidas a un SRID [@mysqlSpatialTypes2026, sec. 13.4.1]. No los utilizaremos aún en este capítulo. Primero debemos comprender qué problema resolverán.

## 10. Análisis de requerimientos espaciales en ObservaSur

Una **estación** es un objeto del dominio. Puede poseer identidad, nombre, responsable, estado y ubicación. Un **punto** es una representación geométrica seleccionada para determinadas preguntas. La estación no se convierte en punto: se representa su ubicación mediante un punto.

La diferencia es importante porque:

- dos estaciones distintas podrían compartir temporalmente una ubicación;
- una estación mantiene su identidad si se corrige su posición;
- una instalación extensa podría requerir otra geometría;
- una geometría no contiene por sí sola todos los atributos de la estación.

La selección de representación debe comenzar por las preguntas [@rigaux2002; @manolopoulos2005]. En ObservaSur se desea responder, progresivamente:

1. ¿qué observaciones produjo cada estación?;
2. ¿qué zona fue declarada para la estación?;
3. ¿qué zona contiene realmente la ubicación?;
4. ¿qué estaciones están cerca de un lugar?;
5. ¿dónde estaba una estación cuando produjo una observación histórica?

Las dos primeras preguntas se resuelven con el modelo inicial. Las tres últimas requieren mecanismos espaciales y, finalmente, temporales.

## 11. Arquitectura cliente-servidor con Python y MySQL

En este curso Python y MySQL se utilizan conjuntamente desde el inicio.

### 11.1 Responsabilidades del sistema gestor MySQL

MySQL debe encargarse de:

- definir tablas, tipos y restricciones;
- preservar claves e integridad;
- almacenar el estado compartido;
- ejecutar reuniones, filtros y, más adelante, relaciones espaciales;
- administrar índices y transacciones.

### 11.2 Responsabilidades de la aplicación cliente en Python

Python permite:

- abrir la conexión;
- suministrar parámetros;
- ejecutar consultas repetidamente;
- recuperar y presentar resultados;
- leer archivos y automatizar cargas;
- ejecutar casos de prueba.

En este capítulo Python no calcula si una estación está dentro de una zona. Hacerlo ocultaría precisamente la limitación que se está estudiando. Más adelante Python invocará una consulta espacial ejecutada por MySQL.

### 11.3 Flujo de una consulta

Una consulta parametrizada sigue este recorrido:

```text
entrada del usuario
        ↓
Python valida la forma elemental del parámetro
        ↓
Connector/Python envía instrucción y parámetros
        ↓
MySQL interpreta, optimiza y ejecuta SQL
        ↓
MySQL devuelve filas y metadatos
        ↓
Python recorre y presenta el resultado
```

La consulta no se ejecuta “en ambos lugares”. Python controla la interacción; MySQL evalúa la condición sobre el estado persistente.

### 11.4 Conexión y recursos

Una conexión representa una sesión con el servidor. A partir de ella se crea un cursor que ejecuta instrucciones y recupera filas. Ambos recursos deben cerrarse incluso si ocurre un error. La plantilla del curso usa `try`/`finally` para hacer explícita esta obligación.

Las credenciales no pertenecen al código fuente. El ejemplo las obtiene desde variables de entorno. Esta decisión no resuelve toda la seguridad de una aplicación, pero evita distribuir contraseñas junto con las soluciones.

### 11.5 Parámetros y separación entre datos y sintaxis

En una consulta parametrizada, el texto SQL permanece estable y los valores se suministran por separado. Connector/Python utiliza marcadores `%s` en `cursor.execute()` [@mysqlConnectorExecute2026]. El controlador se encarga de transmitir el valor conforme al protocolo; no se deben añadir manualmente comillas ni concatenar la entrada.

La parametrización aporta dos ventajas pedagógicas:

- permite distinguir con claridad la instrucción del dato;
- evita que un valor sea interpretado como fragmento de SQL.

No obstante, un parámetro representa valores, no nombres arbitrarios de tablas, columnas u operadores. La estructura de la consulta debe diseñarse explícitamente.

## 12. Actividad de integración conceptual y práctica

### Paso 1. Prediga

Antes de ejecutar, responda:

1. ¿Qué garantiza la clave foránea `id_zona_declarada`?
2. ¿Puede una estación quedar asignada a una zona existente pero espacialmente incorrecta?
3. ¿Qué información falta para comprobarlo?

### Paso 2. Consulte desde MySQL

Ejecute la consulta de estaciones y zonas declaradas. Compruebe que todas las referencias son válidas.

### Paso 3. Consulte desde Python

Ejecute la misma pregunta mediante el cliente suministrado. Cambie el código buscado sin modificar el texto de la consulta.

### Paso 4. Intente responder una pregunta espacial

Seleccione las estaciones de la zona Norte usando `id_zona_declarada`. Después explique si el resultado significa:

> estaciones administradas por Norte

o

> estaciones ubicadas geométricamente dentro de Norte.

El esquema solo permite afirmar lo primero.

### Paso 5. Registre la limitación

Complete:

| Pregunta | ¿Puede responderse? | Datos/operaciones disponibles | Qué falta |
|---|---|---|---|
| ¿Qué zona fue declarada? | Sí | FK y `JOIN` | — |
| ¿Qué observaciones produjo una estación? | Sí | FK, filtro y `JOIN` | — |
| ¿Qué zona contiene la estación? | No todavía | coordenadas separadas | geometría de zona y relación espacial |
| ¿Qué estaciones están cerca? | No todavía | coordenadas separadas | semántica, unidad y operación de distancia |

## 13. Criterios de logro

Una solución completa de este capítulo debe demostrar:

1. que Python se conecta sin contener la contraseña en el código;
2. que la consulta usa parámetros;
3. que el estudiante distingue consulta ejecutada por MySQL de presentación realizada por Python;
4. que la clave foránea no se interpreta como prueba de pertenencia espacial;
5. que se formulan al menos dos requerimientos que exigen una representación espacial.

## 14. Errores conceptuales y técnicos frecuentes

### 14.1 Equiparación de coordenadas y dato espacial

Guardar números no expresa automáticamente sistema de referencia, unidad, geometría ni operaciones.

### 14.2 Equiparación de referencia y pertenencia espacial

La clave solo demuestra que existe la zona referida y que la fila apunta a ella.

### 14.3 Interpretación incorrecta de la ejecución cliente-servidor

Si Python envía la misma consulta y parámetros, MySQL ejecuta la lógica. Python recibe otra representación del mismo resultado.

### 14.4 Concatenación de parámetros en instrucciones SQL

Construir SQL mediante concatenación mezcla datos y sintaxis, dificulta representar tipos y crea riesgos de seguridad. Se utilizarán parámetros desde el inicio.

### 14.5 Equiparación del objeto del dominio y su geometría

La estación es la entidad persistente. El punto será una representación de su ubicación.

## 15. Ejercicios y casos prácticos resueltos

### Ejercicio 1. Nivel básico: interpretar claves y afirmaciones

Considere esta fila:

```text
ESTACION(4, 'EST-S02', 'Cruce', 50.00, 50.00, 2)
```

Responda:

1. ¿Qué identifica la estación?
2. ¿Qué significa el valor `2`?
3. ¿Qué afirmación espacial puede garantizarse únicamente a partir de la fila y la FK?

#### Resolución paso a paso

**Paso 1. Identificar la clave.** `id_estacion = 4` es la clave primaria y distingue esta estación de las demás. `codigo = 'EST-S02'` también es único en el esquema, pero cumple la función de código operativo.

**Paso 2. Interpretar la referencia.** El valor `2` se encuentra en `id_zona_declarada`. La clave foránea exige que exista una fila de `ZONA` con `id_zona = 2`.

**Paso 3. Delimitar la afirmación.** Puede afirmarse que la estación tiene declarada o asignada la zona 2. No puede afirmarse que `(50, 50)` se encuentre dentro de sus límites, porque la zona aún no posee geometría y no se ejecutó ninguna relación espacial.

**Conclusión.** Las claves preservan identidad y referencia; la pertenencia espacial necesita otra representación y otra operación.

### Ejercicio 2. Nivel básico–intermedio: conservar estaciones sin observaciones

Construya una consulta que muestre todas las estaciones y la cantidad de observaciones de cada una, incluyendo las que no tienen observaciones.

#### Resolución paso a paso

**Paso 1. Determinar la tabla que debe conservarse.** Se requieren todas las estaciones, por lo que `estacion` debe ubicarse en el lado izquierdo de una reunión externa.

**Paso 2. Elegir la reunión.** `LEFT JOIN` conserva una estación aunque no encuentre una observación relacionada.

**Paso 3. Elegir qué contar.** Debe contarse una columna de `observacion` que sea no nula cuando la fila exista. `COUNT(*)` contaría también la fila extendida con nulos que produce la reunión.

```sql
SELECT
    e.codigo,
    e.nombre,
    COUNT(o.id_observacion) AS cantidad_observaciones
FROM estacion AS e
LEFT JOIN observacion AS o
  ON o.id_estacion = e.id_estacion
GROUP BY e.id_estacion, e.codigo, e.nombre
ORDER BY e.codigo;
```

**Paso 4. Comprobar.** Con los datos iniciales se esperan:

- `EST-N01`: 2;
- `EST-N02`: 1;
- `EST-S01`: 3;
- `EST-S02`: 0.

**Conclusión.** La consulta demuestra una relación por identidad. No utiliza todavía la ubicación.

### Ejercicio 3. Nivel intermedio: parametrizar una consulta desde Python

Se desea recuperar las estaciones de una zona declarada cuyo nombre se recibe como dato de entrada. Explique por qué la siguiente construcción es incorrecta y proponga una versión parametrizada:

```python
sql = "SELECT * FROM zona WHERE nombre = '" + nombre + "'"
cursor.execute(sql)
```

#### Resolución paso a paso

**Paso 1. Detectar la mezcla.** La variable `nombre` se incorpora al texto que MySQL interpretará como sintaxis. El programa debe distinguir la instrucción estable del dato variable.

**Paso 2. Formular SQL con marcador.** Connector/Python utiliza `%s` como marcador, independientemente del tipo del valor.

```python
sql = """
    SELECT
        e.codigo,
        e.nombre
    FROM estacion AS e
    JOIN zona AS z
      ON z.id_zona = e.id_zona_declarada
    WHERE z.nombre = %s
    ORDER BY e.codigo
"""
```

**Paso 3. Entregar una secuencia de parámetros.** Aunque exista un único valor, se proporciona una tupla de un elemento:

```python
cursor.execute(sql, (nombre,))
filas = cursor.fetchall()
```

**Paso 4. Interpretar la ejecución.** Python entrega consulta y datos mediante la interfaz del controlador. MySQL realiza la reunión y el filtro; Python recupera las filas.

**Paso 5. Delimitar el resultado.** Si `nombre = 'Norte'`, el resultado contiene estaciones cuya zona **declarada** es Norte. La parametrización mejora la interacción y la seguridad, pero no convierte la consulta en espacial.

### Ejercicio 4. Nivel avanzado: auditar un requerimiento ambiguo

Un usuario solicita: “Mostrar todas las estaciones de la zona Norte”. Proponga una desambiguación, determine qué versiones puede responder el esquema inicial y especifique qué necesitaría la futura solución espacial.

#### Resolución paso a paso

**Paso 1. Identificar interpretaciones.** La palabra “de” puede significar al menos:

1. estaciones administrativamente asignadas a Norte;
2. estaciones cuya ubicación actual está dentro de Norte;
3. estaciones que estuvieron dentro de Norte en una fecha pasada;
4. estaciones suficientemente cercanas a Norte según un umbral.

**Paso 2. Evaluar la primera interpretación.** Puede resolverse reuniendo `estacion.id_zona_declarada` con `zona.id_zona`. La respuesta refleja una declaración almacenada.

**Paso 3. Evaluar la segunda.** No puede resolverse correctamente: se necesita una representación de la ubicación de la estación, una geometría de la zona y un predicado de pertenencia o contención.

**Paso 4. Evaluar la tercera.** Además de geometrías, se necesita historial de ubicación y una convención temporal para elegir el estado válido en la fecha consultada.

**Paso 5. Evaluar la cuarta.** Se requieren geometrías, una operación de distancia, un umbral y unidades interpretables.

**Paso 6. Reformular el requerimiento inmediato.** Una versión verificable sería:

> Mostrar las estaciones cuya `id_zona_declarada` refiere a la zona denominada Norte.

La futura versión espacial podría formularse:

> Mostrar las estaciones cuya geometría puntual actual satisface la relación espacial acordada respecto del polígono vigente de la zona Norte.

**Conclusión.** Desambiguar el requerimiento revela los datos, operaciones y dimensiones temporales que debe soportar la base. Este análisis constituye una primera evidencia de R1.

## 16. Conclusiones

- El esquema inicial puede relacionar estaciones, observaciones y zonas declaradas.
- La integridad referencial no garantiza coherencia espacial.
- Dos coordenadas almacenan valores, pero no expresan toda la semántica de una ubicación.
- Las preguntas determinan qué representación y operaciones necesita la base.
- MySQL y Python se complementan, pero no cumplen la misma función.
- El capítulo siguiente, **Fundamentos de la representación de datos espaciales**, formalizará los niveles objeto–propiedad–geometría–codificación y desarrollará punto, línea, polígono, coordenadas, SRS, SRID y WKT. La implementación de columnas geométricas se reservará para el capítulo 3.

---

## 17. Temas de profundización

### 17.1 Extensibilidad de tipos

Un SGBD extensible no se limita a almacenar una codificación adicional: incorpora un dominio de valores, operaciones y reglas que pueden participar en consultas declarativas. Esta idea permite analizar JSON, texto, geometrías o intervalos mediante el mismo criterio general \(T=(V_T,O_T,R_T)\), aunque cada familia posea semántica y soporte técnico diferentes [@atkinson1990, pp. 225–232].

### 17.2 Descomposición relacional y valores estructurados

Un valor estructurado no debe mantenerse necesariamente dentro de una sola columna. Si sus componentes poseen identidad, atributos o ciclos de vida independientes, puede ser preferible representarlos mediante relaciones normalizadas. Si los componentes forman conjuntamente un valor sometido a operaciones propias —como una geometría—, un tipo especializado puede preservar mejor su contrato. La elección debe derivarse de predicados, dependencias, operaciones y reglas de actualización, no de una preferencia general por “más tablas” o “más objetos”.

### 17.3 Independencia física e índices especializados

La extensión lógica y la optimización física son decisiones distintas. Incorporar un tipo geométrico permite formular predicados espaciales; añadir posteriormente un índice espacial busca reducir el costo de acceso sin redefinir el significado de esos predicados. Esta separación retoma la independencia entre descripción lógica y estructuras físicas [@codd1970, pp. 377–383; @silberschatz2020, cap. 14].

---

## 18. Referencia técnica

- Archivo de esquema y datos: [`semana01_esquema_inicial.sql`](../observasur/sql/semana01_esquema_inicial.sql).
- Configuración del cliente: [`conexion.py`](../observasur/python/conexion.py).
- Consulta parametrizada: [`semana01_consultar.py`](../observasur/python/semana01_consultar.py).
- Variables de entorno requeridas: `OBSERVASUR_DB_HOST`, `OBSERVASUR_DB_PORT`, `OBSERVASUR_DB_USER`, `OBSERVASUR_DB_PASSWORD` y `OBSERVASUR_DB_NAME`.
- Controlador propuesto: `mysql-connector-python`; debe confirmarse su disponibilidad antes de publicar la guía.

## 19. Referencias bibliográficas

Atkinson, M., Bancilhon, F., DeWitt, D., Dittrich, K., Maier, D. y Zdonik, S. (1990). The object-oriented database system manifesto. *Proceedings of the First International Conference on Deductive and Object-Oriented Databases*, 223–240.

Codd, E. F. (1970). A relational model of data for large shared data banks. *Communications of the ACM, 13*(6), 377–387. https://doi.org/10.1145/362384.362685

Elmasri, R. y Navathe, S. B. (2016). *Fundamentals of database systems* (7.ª ed.). Pearson.

Manolopoulos, Y., Papadopoulos, A. N. y Vassilakopoulos, M. G. (2005). *Spatial databases: Technologies, techniques and trends*. Idea Group Publishing.

MySQL. (2026). *MySQL 8.0 Reference Manual: Spatial Data Types*. https://dev.mysql.com/doc/refman/8.0/en/spatial-type-overview.html

MySQL. (2026). *Connector/Python connection establishment*. https://dev.mysql.com/doc/connector-python/en/connector-python-connecting.html

MySQL. (2026). *MySQLCursor.execute() method*. https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

Rigaux, P., Scholl, M. y Voisard, A. (2002). *Spatial databases: With application to GIS*. Morgan Kaufmann.

Silberschatz, A., Korth, H. F. y Sudarshan, S. (2020). *Database system concepts* (7.ª ed.). McGraw Hill.
