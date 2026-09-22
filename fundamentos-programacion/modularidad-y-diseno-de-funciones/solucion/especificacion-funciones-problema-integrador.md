
:::{table} Especificación de `leer_observacion()`
:label: tab-especificacion-leer-observacion
:align: center

| Elemento                     | Especificación                                                                 |
|:-----------------------------|:-------------------------------------------------------------------------------|
| Propósito                    | Solicitar y obtener la observación situada en una posición determinada.        |
| Datos requeridos (parámetro) | `posicion` de la observación dentro de la secuencia de entrada.                |
| Precondición                 | `posicion` es un entero positivo y la entrada puede interpretarse como entero. |
| Resultado (retorno)          | Entero introducido para la posición indicada.                                  |
| Poscondición                 | El resultado coincide con el entero ingresado.                                 |
| Efectos observables          | Muestra una solicitud de entrada y consume un dato de la entrada disponible.   |

:::

:::{table} Especificación de `mostrar_resumen()`
:label: tab-especificacion-mostrar-resumen
:align: center

| Elemento            | Especificación                                                                                                                                                                                     |
|:--------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Propósito           | Mostrar las cantidades de observaciones válidas y rechazadas, y promedio cuando está definido.                                                                                                     |
| Datos requeridos    | `validas`: cantidad de observaciones válidas, `rechazadas`: cantidad de observaciones rechazadas, `promedio`: promedio de las observaciones válidas o `None`.                                      |
| Precondición        | `validas` y `rechazadas` son enteros no negativos. Si `validas = 0`, `promedio` es `None`. Si `validas > 0`, `promedio` es el valor numérico previamente calculado para las observaciones válidas. |
| Resultado           | Ninguno                                                                                                                                                                                            |
| Poscondición        | Los tres argumentos conservan sus valores.                                                                                                                                                         |
| Efectos observables | Muestra las dos cantidades. Si `promedio == None`, muestra `Promedio no calculado: sin observaciones válidas`, en caso contrario, muestra `Promedio:` seguido del valor del valor `promedio`.      |
:::