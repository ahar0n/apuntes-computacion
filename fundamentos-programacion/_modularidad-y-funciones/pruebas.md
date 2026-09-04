# Pruebas

## Diseño de pruebas

La prueba de una función examina mediante ejecuciones concretas la correspondencia entre su  especificación y comportamiento, para lo cual utiliza argumentos previamente seleccionados y compara el valor retornado con el resultado esperado. Exige establecer previamente objeto de la comprobación, la justificación de cada caso y su resultado esperado.

Por tanto, el diseño de pruebas consiste en observar si la respuesta parece razonable. Exige establecer de antemano qué se comprobará, por qué se utilizará cada caso y cuál debe ser su resultado.

El diseño de pruebas forma parte del diseño de la función. Los casos pueden prepararse después de especificar su comportamiento y antes de su implementación.

## Pruebas aisladas

Una **prueba aislada** de una función (unidad o componente) ejecuta su implementación al margen de la coordinación del programa completo y compara el valor retornado con el resultado esperado según su especificación. A diferencia de la prueba de integración, examina la funcionalidad de una unidad y no sus interacciones con otras [@iso29119_1_2022].

La prueba suministra directamente los argumentos, sin recurrir a operaciones de entrada o salida, lo que permite atribuir a la función las diferencias observadas. Los casos y sus resultados esperados se derivan de la especificación antes de ejecutar la implementación, para evitar una selección condicionada únicamente por el código.

Los aspectos esenciales del aislamiento son los siguientes:

- La función se examina respecto de su propia especificación.
- Los argumentos se suministran sin recorrer la solución completa,
- El valor retornado se considera por separado de cualquier operación de salida.

Por ejemplo, considere la función `calcular_area_rectangulo(base, altura)` que tiene como parámetros la base y altura de un triángulo. Para probarla de forma aislada se utilizan directamente argumentos como $5$ y $3$, y se compara el valor retornado con $15$. No es necesario leer entradas desde el teclado ni mostrar el área en pantalla. Esas operaciones pertenecen a la coordinación de la solución, no al cálculo que se desea examinar.

La **especificación** de una función establece, mediante su propósito, parámetros, precondición y postcondición, el dominio de los argumentos y el resultado requerido, sin imponer un algoritmo particular. La precondición delimita las llamadas definidas y la postcondición determina la propiedad que debe cumplir el resultado.

El **resultado esperado** se deduce de la especificación para unos argumentos determinados antes de ejecutar la implementación. Así distintas implementaciones pueden compartir las mismas pruebas mientras conserven la relación especificada entre argumentos y resultado. Esta independencia respecto del código caracteriza las pruebas basadas en la especificación [@iso29119_4_2021].

## Caso de prueba

Un **caso de prueba** reúne argumentos determinados, un resultado esperado y un **criterio de selección** que justifica su relevancia. Estos elementos se derivan de la especificación de la función [@iso29119_4_2021].

Durante el diseño se definen tres elementos:

- Argumentos 
- Criterio de selección 
- Resultado esperado

Después de ejecutar la función se añaden otros dos:

- Resultado obtenido 
- Conclusión

La **conclusión de un caso** indica si el resultado obtenido coincide con el esperado. La tabla [](#tab-estructura-registro-prueba) conserva la separación entre diseño y ejecución.

Un **conjunto de pruebas** combina casos con criterios complementarios. Su calidad depende de los comportamientos examinados, no solo de la cantidad de casos, por esto, cada uno debe aportar una contribución identificable.

::::{hint} Ejemplo de caso de prueba de una función.
:label: ex-ch7-prueba-resultado_esperado

La función `calcular_precio_con_descuento()` aplica un descuento general al subtotal de una compra. Cuando el cliente es frecuente, añade 5% de descuento, sin superar el 100%.

:::{table} Especificación de `calcular_precio_con_descuento()`.
:align: center
:label: ch7-tab-especificacion_fx_calcular_valor

| Elemento            | Descripción                                                                                                                                                                                                                                                        |
|:--------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Propósito           | Calcular el importe de una compra después de aplicar el descuento correspondiente.                                                                                                                                                                                 |
| Datos requeridos    | Subtotal de la compra, el porcentaje general de descuento y la condición de cliente frecuente.                                                                                                                                                                     |
| Precondición        | Subtotal debe ser mayor o igual a 0, porcentaje pertenece al intervalo cerrado entre 0 y 100, y la condición de cliente frecuente es un valor booleano.                                                                                                            |
| Resultado           | Número real que representa el precio con descuento aplicado de la compra.                                                                                                                                                                                          |
| Postcondición       | Si el cliente es frecuente, el porcentaje efectivo es el menor valor entre porcentaje más 5 y 100, en caso contrario, coincide con el porcentaje general. El precio final es: $$precio\_con\_descuento = subtotal\left(1-\frac{porcentaje\_efectivo}{100}\right)$$ |
| Efectos observables | Ninguno.                                                                                                                                                                                                                                                           |
:::

Para determinar el resultado esperado, considere una llama a la función con los siguientes datos:

- subtotal de la compra de 200
- porcentaje general de descuento 10%
- cliente frecuente

La condición de cliente frecuente añade cinco puntos porcentuales:
$$porcentaje\_efectivo=\min(10+5,100)=15.$$

El resultado esperado se obtiene aplicando la postcondición:
$$precio\_con\_descuento = 200\left(1-\frac{15}{100}\right) = 170$$

Por lo tanto, el caso de prueba queda diseñado de la siguiente forma:

| Argumentos    | Criterio de selección                         | Resultado esperado |
|:--------------|:----------------------------------------------|:------------------:|
| `200,10,True` | subtotal y porcentaje con descuento adicional |       `170`        |

::::

## Conjunto de pruebas

El diseño comienza en la especificación y avanza desde la delimitación del dominio hasta la selección de argumentos concretos. Para funciones pequeñas se integran técnicas basadas en la especificación [@iso29119_4_2021]. 

La estrategía de diseño de un conjunto de pruebas puede adoptar las siguientes tareas: 

1. **Examinar la precondición.** Determinar las combinaciones de argumentos pertenecientes al dominio y expresar sus restricciones de forma comprobable.
2. **Identificar comportamientos diferentes.** Reconocer los grupos de argumentos para los que la postcondición establece tratamientos distintos.
3. **Seleccionar representantes y límites.** Elegir al menos un representante de cada grupo y añadir los extremos relevantes cuando los grupos sean ordenados.
4. **Determinar los resultados esperados.** Aplicar la postcondición sin ejecutar ni inspeccionar la implementación. La ausencia de un comportamiento requerido obliga a revisar la especificación en lugar de inventar una salida.
5. **Revisar el conjunto.** Comprobar su alcance y eliminar repeticiones que no aporten un criterio nuevo.


## Casos representativos y casos límites

Un **caso representativo** utiliza una entrada admitida para examinar un comportamiento definido por la especificación. Un **caso límite** emplea una entrada situada en un extremo o próxima a este, donde puede cambiar el resultado esperado Ambos criterios son complementarios.

Por ejemplo, de acuerdo con la [especificación](ex-ch7-prueba-resultado_esperado) el 10% representa un descuento interior. Los valores 0% y 100% son casos límite porque constituyen los extremos admitidos por la precondición, el primero conserva el subtotal y el segundo produce un precio de cero. Los valores -1% y 101% no se ejecutan como casos de esta función porque incumplen su precondición.

Los casos límites no son únicamente extremos numéricos. Los siguientes casos se justifican por la estructura del dominio y por las reglas de la función:
- una colección con la cantidad mínima admitida de elementos,
- la primera o la última posición de una secuencia,
- ninguna, una o varias iteraciones,
- ausencia o presencia de un elemento,
- empate entre valores cuando la especificación establece su criterio de resolución.

## Argumentos que inclumplen la precondición

Un argumento **incumple la precondición** cuando la llamada queda fuera del dominio especificado. Sin un comportamiento requerido, no puede asignársele un resultado esperado ni evaluarse su ejecución. Esta condición depende de la función. Un dato rechazado puede ser admisible para una función de validación, pero quedar fuera del dominio de una función de cálculo.

Los argumentos externos al dominio permiten revisar la precondición y las obligaciones de la llamada a la función. Solo constituyen casos evaluables cuando la especificación establece una respuesta, como validación, rechazo o excepción. Aunque las técnicas profesionales contemplan particiones inválidas, no debe inventarse un comportamiento para entradas no especificadas.

Por ejemplo, considere que `calcular_promedio(valores)` tiene como precondición que `valores` no sea vacía. La lista `[80]` pertenece al dominio y representa la cantidad mínima admitida de elementos. La lista vacía incumple la precondición. Si la especificación no declara un retorno, un mensaje ni otro comportamiento para ella, no debe registrarse como caso de prueba. Su consideración revela, en cambio, que la llamada a la función debe evitar esa invocación o que la especificación debe ampliarse si se desea incorporar la validación.

## Pruebas de integración de funciones

Una **prueba de integración** examina las interacciones entre funciones conectadas en una solución. A diferencia de la prueba aislada, comprueba que la composición transmita los datos adecuados, respete las precondiciones y utilice correctamente los valores retornados [@iso29119_1_2022].

Que varias funciones superen sus pruebas aisladas no garantiza la corrección de su composición. Los defectos de integración pueden consistir en:

- suministrar argumentos equivocados,
- incumplir la precondición de una función llamada,
- omitir una llamada necesaria,
- utilizar incorrectamente un valor retornado,
- ejecutar las funciones en un orden incompatible con sus dependencias.

El diseño de estas pruebas parte de la **especificación global** y del esquema de composición. La primera establece el resultado requerido, el segundo identifica las funciones y los datos transferidos. Las pruebas deben comprobar estas conexiones sin volver a examinar las operaciones internas de cada función.

Para composiciones pequeñas se adopta el procedimiento siguiente:

1. **Identificar la interacción.** Seleccionar una llamada o transferencia entre funciones.
2. **Determinar los datos transferidos.** Registrar los argumentos proporcionados y el retorno recibido.
3. **Revisar las precondiciones.** Comprobar que los argumentos pertenecen al dominio de la función llamada.
4. **Establecer el resultado esperado.** Derivarlo de la especificación global.
5. **Ejecutar la composición.** Registrar los datos intercambiados y el resultado obtenido.
6. **Localizar el defecto.** Distinguir los errores internos de los producidos en las conexiones.

Los casos deben seleccionarse según las interacciones examinadas. Son útiles los que activan conexiones diferentes, transmiten valores límite o impiden una llamada cuya precondición no se satisface. Repetir sin criterio todas las pruebas aisladas aumenta el trabajo sin aportar necesariamente información sobre la composición.



