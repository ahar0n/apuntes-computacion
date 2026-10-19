# Solución ejercicio Cap. 6

:::{note} Ejercicio C6-E1. Recorrido de una ventana.
:class: dropdown

Para una ventana,

$$Q = [85,100] \times [50,70]$$

- ¿Qué región ($A$ o $B$) se descarta y con qué desigualdad?
- ¿Qué punto coincide?
- ¿Por qué una ventana puede coincidir con dos ramas y no encontrar puntos?

:::

:::{dropdown} Solución de C6-E1

Se descarta $A$,

$$ x_{\max}(A)=60<85=x_{\min}(Q) \quad\Longrightarrow\quad A\cap Q=\varnothing. $$

Se conserva $B$, ya que $B\cap Q\neq\varnothing$, y el punto coincidente es $P_2=(90,60)\in Q$.

Una ventana puede intersecar dos envolventes internas sin contener ninguno de los objetos que estas agrupan. Si $S_A\subseteq A$ y $S_B\subseteq B$ son los conjuntos de puntos almacenados en cada rama, puede ocurrir que

$$ Q\cap A\neq\varnothing, \qquad Q\cap B\neq\varnothing, \qquad Q\cap(S_A\cup S_B)=\varnothing.$$

Las envolventes incluyen posiciones sin datos. 
:::




:::{note} Ejercicio C6-E2. Consulta con filtro.
:class: dropdown

Formule en SQL una solución progresiva que aplique una estrategia de filtro y refinamiento para encontrar los puntos situados a una distancia menor o igual que $~28$ unidades de la posición $(91,43)$.

1. Calcule las coordenadas mínima y máxima de la nueva caja conservadora.
2. Identifique los puntos que pasan el filtro `MBRIntersects`.
3. Calcule la distancia de cada candidato y determine el resultado exacto.
4. Identifique los falsos positivos.
5. Escriba la consulta SQL que combina filtro y refinamiento.
:::

::::{dropdown} Solución de C6-E2

La caja conservadora es, 

$$[63,119]\times[15,71]$$ 

Por lo tanto, los candidatos son `P2`, `P4` y `P6`. Sus distancias al centro ($C$) son, respectivamente,
\begin{align}
d_{P2-C} &= \sqrt{290}\approx 17.029 \\
d_{P4-C} &= \sqrt{905}\approx 30.083 \\
d_{P6-C} &= \sqrt{425}\approx 20.616
\end{align}

Por lo tanto, `P2` y `P6` se encuentran dentro del radio de búsqueda, mientras que, `P4` está sobre el borde inferior de la caja. Se conserva en el filtro inclusivo y se descarta por distancia.

:::{code-block} sql
:linenos:

SET @C = ST_GeomFromText('POINT(91 43)', 0);
SET @caja = ST_GeomFromText('POLYGON((63 15,119 15,119 71,63 71,63 15))', 0);

SELECT id_punto, ST_Distance(ubicacion, @centro) AS distancia
FROM ra3_punto
WHERE MBRIntersects(@caja, ubicacion)
  AND ST_Distance(ubicacion, @centro) <= 28
ORDER BY id_punto;
:::

::::



## 8. Ejercicios

**C6-E3.** Considere `LINESTRING(0 0,2 2)` y `LINESTRING(0 1,0.4 1.4)`. Determine sus MBR, evalúe antes de ejecutar las funciones `MBRIntersects` y `ST_Intersects` y justifique por qué ambos resultados pueden diferir.

:::{dropdown} Solución de C6-E3

Los MBR son $[0,2]\times[0,2]$ y $[0,0{,}4]\times[1,1{,}4]$. Intersecan, pero las líneas están en las rectas paralelas $y=x$ e $y=x+1$. Los valores esperados son 1 y 0. La coincidencia de envolventes es un falso positivo respecto de la intersección de las formas.
:::

**C6-E4.** Para el triángulo original (zona de inspección) y el punto auxiliar $(0,20)$, compare `MBRContains(@zona,@p)`, `MBRIntersects(@zona,@p)` y `ST_Intersects(@zona,@p)`. ¿Qué ocurre si se combina la primera función con el predicado exacto?

:::{dropdown} Solución de C6-E4

Los resultados esperados son 0, 1 y 1. El punto está sobre la frontera del MBR y del triángulo. `MBRContains` no conserva este punto; por tanto, combinado con `AND ST_Intersects` introduce un falso negativo para el requerimiento inclusivo. El refinamiento no recupera filas descartadas por el filtro. Para este caso debe usarse `MBRIntersects` [@oracle_mbr; @oracle_shapes].
:::

**C6-E5.** Una columna se declara `ubicacion POINT NULL`. Distinga el requisito que impide crear un índice espacial del que impide que el optimizador lo considere. Indique qué debe auditarse antes de cambiar la definición.

:::{dropdown} Solución de C6-E5

La columna debe ser `NOT NULL` para crear el índice; la restricción SRID explícita permite que el optimizador lo considere. Antes de modificarla deben comprobarse los nulos y los SRID existentes. Si el caso realmente utiliza SRID 0, la declaración es `POINT NOT NULL SRID 0`. Declarar un SRID no debe confundirse con transformar coordenadas. No se debe imponer SRID 0 a datos pertenecientes a otro sistema.
:::

**C6-E6.** Sobre 10.000 registros, la envolvente $ A$ conserva 100 candidatos y 50 coincidencias. La envolvente $ B$ conserva 2.000 candidatos y 1.900 coincidencias. Calcule la selectividad del filtro y la proporción de falsos positivos entre los candidatos. ¿Es posible determinar cuál consulta es más rápida?

:::{dropdown} Solución de C6-E6

A conserva el 1\% del total y presenta 50 % de falsos positivos entre candidatos. B conserva el 20 % y presenta 5 % de falsos positivos. A es más restrictivo, pero estos recuentos no determinan por sí solos el tiempo: faltan el plan, los costos de evaluación y las mediciones.
:::

**C6-E7.** Dos consultas devuelven los identificadores $\{1,3,4,5\}$ y $\{1,2,4,5\}$. Explique por qué no son equivalentes y adapte la comprobación de diferencia de conjuntos para detectarlo.

:::{dropdown} Solución de C6-E7

Ambas tienen cuatro filas, pero en la segunda falta 3 y aparece 2 como adicional. La diferencia simétrica contiene ambos identificadores. Un recuento no permite detectar este intercambio.
:::

**C6-E8.** Considere los siguientes planes,

| Plan  | `key`                    | `type`  | `rows` |
|:-----:|:-------------------------|:--------|---:|
|  `A`  | `idx_ra7_demo_ubicacion` | `range` | `120` |
|  `B`  | `NULL`                   | `ALL`   | `10.000` |

- ¿Qué plan utiliza el índice? 
- ¿`120` significa respuestas exactas? 
- ¿El Plan `A` es más rápido que `B`?

:::{dropdown} Solución de C6-E8

- `A` selecciona el índice y `B` recorre la tabla. 
- `120` es una estimación de filas examinadas, no el número exacto de respuestas. 
- Se necesitan resultados equivalentes y mediciones comparables para afirmar una mejora temporal.

:::