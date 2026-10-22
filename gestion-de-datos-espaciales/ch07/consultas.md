# Consultas

## 1. Selección de observaciones por período

Para recuperar las lecturas observadas por la estación `E01` el día 19 se usa el instante de observación:

:::{code-block} sql
:linenos:

SELECT lectura_id, instante_observado_utc, nivel_cm
FROM lectura
WHERE estacion_id = 'E01'
  AND instante_observado_utc >= '2026-10-19 00:00:00'
  AND instante_observado_utc <  '2026-10-20 00:00:00'
ORDER BY instante_observado_utc;
:::

El resultado contiene las lecturas 1 a 6. Primero se identifica la serie mediante `estacion_id`, después se delimita el período con el tiempo observado. La lectura 6 pertenece al resultado aunque se haya registrado al día siguiente.

La selección temporal y la presentación ordenada cumplen funciones diferentes. `WHERE` determina las observaciones que pertenecen al período y `ORDER BY` establece la forma de representación. Ordenar por fecha no corrige el uso de un campo temporal equivocado en el filtro.

El límite superior exclusivo incluye todos los instantes del día 19 sin depender de escribir la última hora como `23:59:59`.

## 2. Recuperación del estado en un instante

El estado de la estación E01 a las 10:00 se obtiene comprobando pertenencia temporal:

:::{code-block} sql
:linenos:

SET @instante = '2026-10-19 10:00:00';
SELECT estado_id, estado
FROM estado_estacion
WHERE estacion_id = 'E01'
  AND desde_utc <= @instante
  AND (hasta_utc IS NULL OR @instante < hasta_utc);
:::

La consulta devuelve el estado 2, `INACTIVA`. El primer tramo queda excluido porque su término coincide con el instante consultado. El segundo se incluye porque su inicio coincide con ese instante. La combinación de desigualdad estricta en el término y no estricta en el inicio asigna el cambio a una sola vigencia.

| Instante consultado (UTC) | Estado de E01               |
|:------------------------|:----------------------------|
| `19/oct 07:59:59`         | No hay vigencia registrada. |
| `19/oct 09:59:59`         | `OPERATIVA`, vigencia `1`.      |
| `19/oct 10:00:00`         | `INACTIVA`, vigencia `2`.       |
| `19/oct 12:00:00`         | `OPERATIVA`, vigencia `3`.      |

Un resultado vacío indicaría falta de cobertura histórica para ese instante. Dos resultados indicarían ambigüedad temporal. El número de filas, por tanto, forma parte de la interpretación de la consulta.

## 3. Unión de observaciones con vigencias

Una unión relaciona filas mediante una condición. Para asociar una observación con su estado histórico, deben coincidir la estación y la vigencia que contiene el instante observado. La igualdad del identificador establece a qué entidad pertenecen los registros. Las comparaciones temporales determinan la versión [@silberschatz2020].

La siguiente consulta revisa todas las lecturas y busca el estado vigente cuando fueron observadas:

:::{code-block} sql
:linenos:

SELECT l.lectura_id, l.estacion_id,
       l.instante_observado_utc, l.nivel_cm,
       e.estado
FROM lectura AS l
LEFT JOIN estado_estacion AS e
  ON e.estacion_id = l.estacion_id
 AND e.desde_utc <= l.instante_observado_utc
 AND (e.hasta_utc IS NULL
      OR l.instante_observado_utc < e.hasta_utc)
ORDER BY l.lectura_id;
:::

Los alias `l` y `e` identifican las filas de `lectura` y `estado_estacion`. La condición `ON` exige que se cumplan tres criterios:

Se utiliza `LEFT JOIN` para conservar todas las lecturas, incluso aquellas que no encuentren vigencia. En estas últimas, `e.estado` aparece como `NULL`, lo que indica ausencia de correspondencia histórica. No equivale al estado `INACTIVA`.

Las comparaciones temporales se mantienen en `ON` para conservar las lecturas sin coincidencia. Agregar `WHERE e.estado = 'INACTIVA'` seleccionaría las asociadas a inactividad y excluiría las que no encontraron estado. Ese filtro permite estudiar inactividad, pero no revisar la cobertura de todas las observaciones.

En el resultado de la consulta: 

- Cada lectura encuentra exactamente una vigencia. Las lecturas 1 y 2 corresponden al primer tramo operativo de E01; las lecturas 3 y 4, al tramo inactivo; y las lecturas 5 a 10, al tramo operativo que comienza el 19 de octubre a las 12:00 y no tiene término conocido. Las lecturas 11 a 13 corresponden a la vigencia operativa de E02.

- La lectura 3 pertenece al tramo inactivo porque fue observada a las `10:00`, su inicio incluido. La lectura 5 pertenece al siguiente tramo operativo, que comienza a las `12:00`. Los niveles nulos de las lecturas 4 y 12 no impiden encontrar sus estados. La unión depende de la estación y del instante observado, no del nivel registrado.


## 4. Verificación del número de coincidencias

Si una estación debe tener un único estado en cada instante, cada lectura debe encontrar exactamente una vigencia. La siguiente consulta identifica las lecturas que no cumplen esta condición:

:::{code-block} sql
:linenos:

SELECT l.lectura_id,
       COUNT(e.estado_id) AS vigencias_coincidentes
FROM lectura AS l
LEFT JOIN estado_estacion AS e
  ON e.estacion_id = l.estacion_id
 AND e.desde_utc <= l.instante_observado_utc
 AND (e.hasta_utc IS NULL
      OR l.instante_observado_utc < e.hasta_utc)
GROUP BY l.lectura_id
HAVING COUNT(e.estado_id) <> 1;
:::

El `LEFT JOIN` busca las vigencias que corresponden a la estación y contienen el instante observado. Luego, `GROUP BY l.lectura_id` reúne las coincidencias de cada lectura y `COUNT(e.estado_id)` las cuenta. Finalmente, `HAVING` conserva únicamente los grupos cuyo recuento es diferente de uno.

Se cuenta `e.estado_id` porque `COUNT` omite los valores nulos. Cuando una lectura no encuentra vigencia, la unión externa conserva la lectura y completa las columnas de `e` con `NULL`, por tanto, el recuento es cero. Usar `COUNT(*)` contaría esa fila conservada y produciría uno, ocultando la falta de cobertura.

El resultado de la consulta no devuelve filas. Cada lectura encuentra una vigencia y ninguna cumple la condición `HAVING COUNT(e.estado_id) <> 1`.

El resultado vacío indica que no se detectaron problemas de correspondencia en los instantes observados. Para ver el recuento de las 13 lecturas, puede ejecutarse la consulta sin la cláusula `HAVING`.

Este control no demuestra continuidad durante períodos sin observaciones ni verifica que los estados sean correctos respecto de la realidad. La clave foránea tampoco comprueba cobertura temporal, solo exige que exista la estación referenciada.

Por ejemplo, una lectura de E01 anterior al inicio de su historia registrada obtendría cero coincidencias y aparecería en el resultado. Si se incorporara otra vigencia de E01 que también cubriera las `10:00` del 19 de octubre, la lectura 3 obtendría dos coincidencias y también aparecería.