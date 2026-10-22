# Representación temporal en RDBMS

## 1. Intervalos semiabiertos y pertenencia temporal

Una vigencia establece el período durante el cual un estado se considera válido. Para representar sus límites se adopta la convención de **intervalos semiabiertos** `[desde, hasta)`. El corchete indica que el inicio se incluye y el paréntesis, que el término se excluye. Así, dos períodos consecutivos pueden compartir un límite sin atribuir a ambos el instante de transición.

Un instante $t$ pertenece a una vigencia finita cuando cumple simultáneamente ambas condiciones:

$$ desde \leq t \quad \land \quad t < hasta $$

Esta convención evita ajustar artificialmente el término al segundo anterior. Si un estado cambia a las `10:00:00`, la vigencia anterior termina exactamente a esa hora y la siguiente comienza en ese mismo instante. La regla sigue siendo válida si se utilizan fracciones de segundo.

Cuando todavía no se conoce el término, se almacena `NULL` en `hasta_utc`. En este modelo, ese valor significa **sin término conocido**. La condición de pertenencia se expresa en SQL como:

```sql
desde_utc <= @instante
AND (hasta_utc IS NULL OR @instante < hasta_utc)
```

La primera comparación comprueba que la vigencia ya comenzó. La expresión entre paréntesis comprueba que no existe un término conocido o que el instante consultado es anterior a él. Es necesario utilizar `IS NULL`, porque una comparación como `@instante < NULL` no resulta verdadera.

Consultar solo `hasta_utc IS NULL` recupera vigencias sin término conocido, pero no asegura que ya hayan comenzado. Asimismo, `BETWEEN` incluye ambos extremos y no representa directamente la convención semiabierta.

Por ejemplo, considere el siguiente historial:

| Tramo | Inicio (UTC) | Término (UTC)        | Estado    |
|:-----:|:-------------|:---------------------|:----------|
|   1   | `19/oct 08:00` | `19/oct 10:00`         | OPERATIVA |
|   2   | `19/oct 10:00` | `19/oct 12:00`         | INACTIVA  |
|   3   | `19/oct 12:00` | Sin término conocido | OPERATIVA |

La pertenencia se resuelve de la siguiente manera:

| Instante consultado (UTC) | Resultado                | Descripción                                                                 |
|:--------------------------|:-------------------------|:----------------------------------------------------------------------------|
| `19/oct 07:59:59`         | Sin vigencia registrada. | Ningún tramo ha comenzado.                                                  |
| `19/oct 08:00:00`         | Tramo 1: OPERATIVA.      | El inicio está incluido.                                                    |
| `19/oct 09:59:59`         | Tramo 1: OPERATIVA.      | El instante es anterior al término.                                         |
| `19/oct 10:00:00`         | Tramo 2: INACTIVA.       | El término del tramo 1 está excluido y el inicio del tramo 2 está incluido. |
| `19/oct 12:00:00`         | Tramo 3: OPERATIVA.      | Comienza la nueva vigencia, cuyo término aún no se conoce.                  |

- Una lectura obtenida a las `10:00:00` se relaciona solo con el tramo 2. 
- Una consulta anterior a las `08:00:00` no permite determinar el estado.

## 2. Integridad dentro de una fila

La integridad de un intervalo exige que sus límites representen un período válido. Si el término es conocido, debe ser posterior al inicio. Si todavía no se conoce, se admite un término nulo. La restricción expresa ambas posibilidades:

```sql
CONSTRAINT ck_estado_intervalo
CHECK (hasta_utc IS NULL OR desde_utc < hasta_utc)
```

La condición se cumple cuando `hasta_utc` es nulo o cuando `desde_utc` es anterior a `hasta_utc`. El inicio se declara además como `NOT NULL`, porque toda vigencia debe tener un comienzo conocido.

| Inicio | Término | Resultado                                  |
|-------:|--------:|:-------------------------------------------|
|  10:00 |   12:00 | Válido: el término es posterior al inicio. |
|  10:00 |  `NULL` | Válido: no hay término conocido.           |
|  12:00 |   10:00 | Inválido: el intervalo está invertido.     |
|  10:00 |   10:00 | Inválido: el intervalo está vacío.         |

En la convención semiabierta `[desde, hasta)`, el inicio se incluye y el término se excluye. Por eso, `[10:00, 10:00)` no contiene ningún instante y se rechaza mediante la comparación estricta `<`.

MySQL comprueba esta condición al insertar o actualizar una fila y rechaza la operación si la expresión resulta falsa. Un `CHECK` también admite un resultado desconocido debido a valores nulos. Por lo tanto, las restricciones `NOT NULL` deben declarar por separado qué atributos son obligatorios [@oracle_mysql80_check].

Este control solo evalúa los valores de la fila modificada. MySQL no admite subconsultas dentro de `CHECK` para inspeccionar otras vigencias, de modo que la restricción no detecta solapamientos ni huecos entre períodos [@oracle_mysql80_check].

Por ejemplo, las vigencias `[08:00, 10:00)` y `[09:00, 11:00)` cumplen individualmente la restricción, pero se superponen entre las `09:00` y las `10:00`. Detectar ese conflicto exige comparar ambas filas mediante un control adicional.

## 3. Solapamiento entre vigencias

Considere dos tramos de una misma estación: `[08:00, 10:00)` y `[09:30, 10:30)`. Ambos atribuyen un estado al período que comienza a las `09:30` y termina antes de las `10:00`. Bajo la regla de un único estado por instante, son incompatibles aunque sus identificadores e inicios sean diferentes.

Para dos períodos finitos $A$ y $B$, 

$$ A=[a_i,a_f), \qquad B=[b_i,b_f) $$

existe intersección no vacía cuando:

$$ a_i < b_f \quad \land \quad b_i < a_f $$

Esta condición puede entenderse descartando las dos formas de separación, que $A$ termine antes o justo al comenzar $B$, o que $B$ termine antes o justo al comenzar $A$. Cuando ninguna separación se cumple, los períodos comparten tiempo.

La siguiente consulta busca vigencias que se superponen para una misma estación. Revisa todas las estaciones de `estado_estacion` y devuelve una fila por cada par de vigencias en conflicto:

:::{code-block} sql
:linenos:

SELECT a.estacion_id,
       a.estado_id AS estado_a,
       b.estado_id AS estado_b
FROM estado_estacion AS a
JOIN estado_estacion AS b
  ON a.estacion_id = b.estacion_id
 AND a.estado_id < b.estado_id
WHERE (b.hasta_utc IS NULL OR a.desde_utc < b.hasta_utc)
  AND (a.hasta_utc IS NULL OR b.desde_utc < a.hasta_utc)
ORDER BY a.estacion_id, a.estado_id, b.estado_id;
:::

La tabla se consulta dos veces mediante los alias `a` y `b`, que permiten comparar dos de sus filas. La condición `a.estacion_id = b.estacion_id` limita la comparación a vigencias de la misma estación. La condición `a.estado_id < b.estado_id` evita comparar una fila consigo misma y presentar dos veces el mismo par. Los identificadores se utilizan para distinguir pares, sin suponer que expresan un orden temporal.

El `WHERE` comprueba las dos condiciones (líneas 8 y 9) necesarias para que exista solapamiento. Sus interpretaciones son respectivamente: 

- B no tiene término conocido o A comienza antes de que termine B.
- A no tiene término conocido o B comienza antes de que termine A.

Ambas deben cumplirse. Se utiliza `<` porque los intervalos son semiabiertos. Si uno termina exactamente cuando comienza el otro, no comparten ningún instante. Las comprobaciones `IS NULL` permiten comparar también vigencias sin término conocido.

El resultado identifica la estación y los dos tramos que presentan el conflicto. `ORDER BY` organiza esos pares por estación e identificadores.

Con los datos cargados, la consulta no devuelve filas. E01 tiene tres vigencias consecutivas y E02 tiene una sola:

| Estación | Tramo | Inicio UTC, 19/oct | Término UTC, 19/oct |
|---|:---:|---|---|
| E01 | 1 | `08:00` | `10:00` |
| E01 | 2 | `10:00` | `12:00` |
| E01 | 3 | `12:00` | Sin término conocido |
| E02 | 4 | `08:00` | Sin término conocido |

Para E01 se comparan los pares 1–2, 1–3 y 2–3. Todos quedan descartados porque al menos una condición de solapamiento es falsa:

| Par  | Comparación falsa           | Interpretación                                   |
|:----:|:----------------------------|:-------------------------------------------------|
| 1–2  | `10:00 < 10:00`             | El tramo 2 comienza cuando termina el 1.         |
| 1–3  | `12:00 < 10:00`             | El tramo 3 comienza después de que termina el 1. |
| 2–3  | `12:00 < 12:00`             | El tramo 3 comienza cuando termina el 2.         |

E02 no genera pares porque solo tiene una vigencia. Tampoco se comparan sus filas con las de E01, pues pertenecen a estaciones diferentes.

Un resultado vacío indica que no se detectaron solapamientos entre las vigencias almacenadas.

## 4. Niveles de integridad temporal

La integridad temporal debe comprobarse dentro de cada fila y entre las filas del historial. Un intervalo puede tener límites válidos y, aun así, superponerse con otro o dejar un período sin información. Cada mecanismo ofrece una garantía específica:

- `CHECK` del intervalo, comprueba si el término conocido es posterior al inicio, también admite un término nulo.
- `UNIQUE (estacion_id, desde_utc)`, comprueba que no se repite un mismo inicio para una estación.
- Clave foránea, comprueba que existe la estación asociada al registro.
- Consulta de solapamientos, detecta pares de vigencias que comparten tiempo para una estación.

Las restricciones actúan al insertar o actualizar datos. La consulta de solapamientos, en cambio, detecta conflictos existentes.

Por ejemplo, un historial con vigencias `[08:00, 10:00)` y `[11:00, 12:00)` contiene intervalos válidos y sin solapamientos. Las observaciones de las `09:00` y las `11:30` encuentran una vigencia, pero el historial no permite determinar el estado a las `10:30`. Cumple la cobertura de esas observaciones, aunque no la continuidad del período `[08:00, 12:00)`.