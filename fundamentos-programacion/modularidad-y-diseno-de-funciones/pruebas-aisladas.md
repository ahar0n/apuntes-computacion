---
title: "Prueba aislada de funciones"
bibliography:
  - ../referencias_capitulo_07.bib
---

## Diseño y ejecución de una prueba

La prueba de una función examina mediante ejecuciones concretas la correspondencia entre su  especificación y comportamiento, para lo cual utiliza argumentos previamente seleccionados y compara el valor retornado con el resultado esperado. Exige establecer previamente objeto de la comprobación, la justificación de cada caso y su resultado esperado.

Una **prueba aislada** ejecuta una función al margen de la coordinación del programa completo y compara su valor retornado con el resultado esperado. A diferencia de la prueba de integración, examina una unidad y no sus interacciones con otras [@iso29119_1_2022]. Los argumentos se suministran directamente, sin recurrir a las operaciones de entrada o presentación del programa.

La **especificación** delimita el dominio mediante la precondición y determina las propiedades del resultado mediante la postcondición. El **resultado esperado** se deduce de esas propiedades para unos argumentos determinados antes de ejecutar la implementación. De esta forma, distintas implementaciones pueden compartir los mismos casos mientras conserven la relación especificada entre argumentos y resultados [@iso29119_4_2021].

Un **caso de prueba** reúne tres elementos de diseño:

- Argumentos determinados
- Criterio que justifica su selección
- Resultado esperado

Después de ejecutar la función se registran el resultado obtenido y la conclusión. La conclusión indica si el resultado obtenido coincide con el esperado. Esta separación impide adaptar retrospectivamente la expectativa a la respuesta producida por el programa.

## Selección de casos

Un **conjunto de pruebas** combina casos con criterios complementarios. Su calidad depende de los comportamientos examinados, no solo de la cantidad de ejecuciones. Puede aplicarse el siguiente procedimiento, adaptado a partir de técnicas basadas en la especificación [@iso29119_4_2021]:

1. Examinar la precondición y delimitar el dominio.
2. Identificar los comportamientos diferentes establecidos por la postcondición.
3. Seleccionar representantes y límites relevantes.
4. Determinar los resultados esperados sin ejecutar la implementación.
5. Revisar el conjunto y eliminar repeticiones que no aporten un criterio nuevo.

Se denomina **caso representativo** a una entrada admitida elegida para examinar un comportamiento ordinario y **caso límite** a una entrada admitida situada en un extremo establecido por las restricciones. Esta terminología no constituye una taxonomía exhaustiva ni excluyente.

La [](#cap07-tab-pruebas-validacion) presenta el diseño y el registro de pruebas para la función `es_observacion_valida()`.

:::{table} Pruebas aisladas de `es_observacion_valida()`
:label: cap07-tab-pruebas-validacion
:align: center

| Argumento | Criterio de selección                       | Esperado  | Obtenido  |  Conclusión  |
|:---------:|:--------------------------------------------|:---------:|:---------:|:------------:|
|   `50`    | Entero representativo del interior          |  `True`   |  `True`   |   Coincide   |
|    `0`    | Límite inferior válido                      |  `True`   |  `True`   |   Coincide   |
|   `100`   | Límite superior válido                      |  `True`   |  `True`   |   Coincide   |
|   `-1`    | Entero inmediatamente inferior al intervalo |  `False`  |  `False`  |   Coincide   |
|   `101`   | Entero inmediatamente superior al intervalo |  `False`  |  `False`  |   Coincide   |
:::

Los argumentos `-1` y `101` pertenecen al [dominio de la función](#cap07-tab-especificacion-validacion), aunque correspondan a observaciones que el procesamiento global rechazará. La responsabilidad de la función es producir `False` para esos valores.

Para la función `calcular_promedio()` puede diseñarse el siguiente conjunto:

:::{table} Pruebas aisladas de `calcular_promedio()`
:label: cap07-tab-pruebas-promedio
:align: center

|  Argumento   | Criterio de selección                 | Esperado | Obtenido | Conclusión  |
|:------------:|:--------------------------------------|:--------:|:--------:|:-----------:|
|    `[80]`    | Cantidad mínima admitida de elementos |  `80.0`  |  `80.0`  |  Coincide   |
|  `[0,100]`   | Valores situados en ambos límites     |  `50.0`  |  `50.0`  |  Coincide   |
| `[20,40,60]` | Colección representativa              |  `40.0`  |  `40.0`  |  Coincide   |
:::

La lista vacía incumple la [precondición](#cap07-tab-especificacion-promedio) de `calcular_promedio()`. Si la especificación no declara un retorno, una excepción ni otro comportamiento para ella, no puede asignársele un resultado esperado. Su consideración permite revisar la obligación de la operación llamadora: evitar esa llamada. Un dato externo al dominio solo constituye un caso ejecutable cuando la especificación determina su tratamiento.

Que los resultados coincidan en estos casos aporta evidencia sobre las entradas seleccionadas, pero no demuestra por sí solo que las funciones sean correctas para todos los argumentos de sus dominios [@bijlsma2021students; @scatalon2019testing].

