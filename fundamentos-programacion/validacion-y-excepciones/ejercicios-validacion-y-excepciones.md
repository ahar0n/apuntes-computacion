# Ejercicios: Validación y tratamiento de excepciones


**VTE-001.** En un juego de exploración, el personaje encuentra un portal que necesita exactamente 25 puntos de energía para abrirse.

El jugador elige un nivel de carga, representado mediante un entero entre 1 y 8. Según las reglas del juego, la energía liberada ($e_l$) es el cuadrado del nivel de carga elegido ($n_c$):

$$ e_l = n_c^2 $$

Por ejemplo, el nivel 3 libera 9 puntos de energía.

El resultado de la jugada depende de la energía liberada. Con menos de 25 puntos, el portal permanece cerrado, con 25 puntos exactos, se abre, y con más de 25 puntos, se sobrecarga y queda bloqueado.

Escriba un programa que solicite al usuario el nivel de carga, calcule y muestre la energía liberada, informe el resultado de la jugada y termine. El jugador realiza una sola jugada válida por ejecución, aunque el portal no se abra. 

Si el valor ingresado no puede convertirse a entero, informe que se requiere un número entero y vuelva a solicitarlo. Si se convierte exitosamente, pero queda fuera del intervalo permitido, informe el intervalo válido y vuelva a solicitarlo.

Puede considerar aplicar la siguiente estrategia:

1. Evalúe si el valor ingresado es convertible, entero fuera del intervalo y nivel permitido. Por ejemplo, `"-5"` se convierte correctamente, pero no es un nivel permitido. 
2. Calcule la energía solo después de comprobar el intervalo.
3. Repita la solicitud por entradas incorrectas.



**VTE-002.** Un sistema de codificación transforma un dígito decimal mediante una clave que indica la cantidad de posiciones que debe avanzar la secuencia circular de dígitos: 

```text
0 → 1 → 2 → ... → 8 → 9 → 0 → ...`
```

Tanto el dígito original como la clave deben ser números enteros entre 0 y 9. Para codificar, se suma la clave al dígito y se obtiene el resto de dividir el resultado por 10:

$$ \text{codificado} = (\text{dígito} + \text{clave}) \bmod 10 $$

Para recuperar el dígito original, se retrocede la misma cantidad de posiciones. Se resta la clave al valor codificado y se aplica nuevamente el resto de dividir por 10.

$$ \text{original} = (\text{codificado} - \text{clave}) \bmod 10 $$

Recordar que, en Python, el operador `%` permite obtener el resto.

Por ejemplo, si el dígito es 8 y la clave es 5, se avanza cinco posiciones. El valor codificado es `(8 + 5) % 10 = 3`. Para recuperarlo, se calcula `(3 - 5) % 10 = 8`.

Construya tres funciones:

- `leer_clave_y_digito()`: solicita el dígito y luego la clave, convierte ambas entradas a enteros y devuelve la tupla `(digito, clave)`. No comprueba los intervalos ni captura excepciones.
- `codificar(digito, clave)`: recibe dos enteros válidos entre 0 y 9 y retorna el valor codificado.
- `decodificar(cifrado, clave)`: recibe el valor codificado y la misma clave válida, y retorna el dígito original.

El programa principal debe:

1. Llamar a `leer_clave_y_digito()` dentro de un bloque `try–except` que trate `ValueError`. Si falla una conversión, informar que ambos datos deben ser enteros y reiniciar la solicitud.
2r. Verifica que las entradas estén dentro del rango válido. Si alguno incumple esta restricción, informar el intervalo permitido y reiniciar la solicitud.
3. Una vez aceptadas las entradas, llamar a las funciones de codificación y decodificación, mostrar ambos resultados y terminar.




**VTE-003.** La secuencia de ADN se representa mediante una cadena de entre 6 y 60 caracteres. Solo se admiten las letras mayúsculas `A`, `C`, `G` y `T`, sin espacios.

Se requiere localizar todas las apariciones de un motivo, es decir, una cadena de exactamente tres letras del mismo alfabeto.

Por ejemplo, en la secuencia `"AAAAAA"`, el motivo `"AAA"` aparece en los índices `0`, `1`, `2` y `3`. Estas coincidencias se superponen porque comparten caracteres.

Implemente dos funciones:

- `validar_datos(secuencia, motivo)`: recibe dos cadenas y devuelve un mensaje que explica la primera restricción incumplida de los datos. Si ambas cadenas cumplen todas las restricciones, devuelve una cadena vacía.
- `buscar_motivo(secuencia, motivo)`: recibe cadenas previamente validadas y devuelve una lista con los índices iniciales de todas las coincidencias. Los índices comienzan en cero.

Para realizar la búsqueda, utilice un recorrido por índices y segmentación de la cadena. Puede implementar las funciones auxiliares que considere necesarias, siempre que cada una resuelva una tarea específica y claramente delimitada. No use el método `index()`.

El programa principal debe solicitar ambas cadenas, validarlas y, si alguna incumple las restricciones, mostrar un mensaje que explique el problema. Cuando los datos sean válidos, debe mostrar la lista de posiciones y terminar. Si no existen coincidencias, debe mostrar una lista vacía.





**VTE-004.** Un sensor de observatorio registra entre 4 y 12 lecturas enteras de brillo, cada una entre 0 y 100. Las lecturas se ingresan en una cadena separada por comas. Se permiten espacios alrededor de los números, pero no lecturas vacías.

Un destello es una lectura mayor que sus dos vecinas inmediatas (la anterior y la posterior). La primera y la última lectura no se consideran destellos. Los valores consecutivos iguales, como por ejemplo, `20,80,80,20`, tampoco constituyen destellos.

Desarrolle un programa que interprete la entrada y muestre una lista de tuplas `(indice, brillo)` con los destellos encontrados. Los índices comienzan en cero. Utilice índices para comparar las lecturas y organice la solución en funciones que resuelvan tareas específicas y claramente delimitadas.

Trate los errores de conversión y compruebe las restricciones de los datos. Si alguna lectura o el conjunto ingresado incumple los requisitos, informe el problema y solicite nuevamente la cadena completa.

Cuando la entrada sea válida, muestre el resultado y termine. Si no hay destellos, muestre una lista vacía.






**VTE-005.** Un panel de luces se representa mediante una lista de listas de enteros: `1` indica una luz encendida y `0` una apagada. El panel debe tener entre 2 y 8 filas y entre 2 y 8 columnas. Todas las filas deben tener la misma cantidad de elementos y cada elemento debe valer `0` o `1`.

El panel cambia al **siguiente estado** de acuerdo con la siguiente regla. Una luz queda encendida si dos de sus vecinas estaban encendidas, en cualquier otro caso, queda apagada. Se consideran vecinas las luces situadas inmediatamente arriba, abajo, a la izquierda y a la derecha. En los bordes se consideran solo las vecinas existentes.

Todos los cambios se calculan a partir del estado original del panel. El estado anterior de la propia luz no interviene en la regla.

Por ejemplo, para el panel original:

```text
0 1 0
1 0 1
0 1 0
```

El siguiente estado es:

```text
1 0 1
0 0 0
1 0 1
```

Cada esquina tiene exactamente dos vecinas encendidas y queda encendida. La luz central tiene cuatro vecinas encendidas, por lo que queda apagada.

Desarrolle una solución que valide el panel y, si cumple las restricciones, construya y devuelva un panel nuevo con el siguiente estado. Si no las cumple, debe comunicar el problema mediante un mensaje. Organice la solución en funciones que resuelvan tareas específicas y claramente delimitadas.

Diseñe un programa de demostración con paneles definidos en el código. Para cada caso, muestre el siguiente estado o un mensaje que explique la restricción incumplida y continúe con el siguiente panel. El panel original debe conservarse sin modificaciones en todos los casos.

Incluya pruebas que permitan verificar que los cambios se calculan simultáneamente y que el resultado es independiente del panel original.





**VTE-006.** Una red social permite que sus usuarios den «Me gusta» a los mensajes publicados. Cada mensaje tiene asociado un identificador, un autor, un texto y una lista con los nombres de quienes ya dieron «Me gusta».

Los mensajes se almacenan en un diccionario en el que cada clave es un identificador entero y su valor es una tupla `(autor, texto, reacciones)`:

```python
mensajes = {
    101: (
        "la_mon",
        "Vecino, no estoy gritando: estoy ensayando el coro.",
        [],
    ),
    205: (
        "nino_maravilla",
        "Cabros, era pichanga, no final del mundo. ¡Devuelvan la pelota, po!",
        ["la_mon"],
    ),
}
usuarios = ("la_mon", "nino_maravilla", "yei_lo")
```

En el estado inicial, el mensaje `101` no tiene reacciones y el mensaje `205` tiene una reacción de `"la_mon"`.

Diseñe e implemente un programa que solicite el identificador de un mensaje y el nombre del usuario que desea darle «Me gusta». La operación se acepta únicamente si:

- El mensaje existe.
- El usuario pertenece a la tupla `usuarios`.
- El usuario no es el autor del mensaje.
- El usuario no ha dado «Me gusta» previamente a ese mensaje.

Si la operación se acepta, agregue el nombre del usuario a la lista de reacciones y muestre la cantidad actualizada de reacciones del mensaje. Por ejemplo, si `"yei_lo"` reacciona al mensaje `101`, su lista pasa de `[]` a `["yei_lo"]` y la cantidad de reacciones es 1.

Si la entrada o la operación no cumplen los requisitos, el programa debe mostrar un mensaje que explique el problema y solicitar una nueva operación. Una operación rechazada no debe modificar los mensajes. Los nombres de usuario deben coincidir exactamente con los registrados.

El programa termina cuando se ingresa el texto `FIN` en lugar del identificador, sin solicitar el nombre del usuario. Al finalizar, debe mostrar el diccionario de mensajes.

Organice la solución en funciones que resuelvan tareas específicas y claramente delimitadas. Aplique validación de datos y tratamiento de excepciones de acuerdo con los requisitos del problema.




**VTE-007.** Un editor permite aplicar efectos a imágenes pequeñas. Cada imagen está formada por filas y columnas de píxeles. El color de cada píxel se representa mediante una tupla `(R, G, B)`, cuyas componentes corresponden a rojo, verde y azul. Cada componente debe ser un entero entre 0 y 255.

Las imágenes se definen en una variable en el código como listas de filas con tuplas `(R, G, B)`. Por ejemplo, la siguiente imagen de cinco filas y cinco columnas representa un corazón rojo sobre fondo blanco:

```python
imagen = [
    [(255, 255, 255), (255, 0, 0),     (255, 255, 255), (255, 0, 0),     (255, 255, 255)],
    [(255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 0, 0)],
    [(255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 0, 0)],
    [(255, 255, 255), (255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 255, 255)],
    [(255, 255, 255), (255, 255, 255), (255, 0, 0),     (255, 255, 255), (255, 255, 255)],
]
```

Diseñe e implemente programa que valide una imagen definida en el código. Debe comprobar que:

- Tiene entre 1 y 6 filas y entre 1 y 6 columnas.
- Todas las filas contienen la misma cantidad de píxeles.
- Cada píxel tiene exactamente tres componentes.
- Todas las componentes están entre 0 y 255.

Si la imagen incumple alguna restricción, el programa debe mostrar un mensaje que explique el problema y terminar.

Si la imagen es válida, debe solicitar una de las siguientes operaciones:

- `ESPEJO`: invierte el orden de los píxeles de cada fila, conservando el orden de las filas.
- `NEGATIVO`: reemplaza cada componente por su diferencia respecto de 255. Por ejemplo, `(20, 100, 255)` se transforma en `(235, 155, 0)`.

Los nombres deben coincidir con los indicados. Si la operación es desconocida, informe el problema y vuelva a solicitarla.

Cuando la operación sea válida, construya una imagen nueva, muestre la original y el resultado como filas de tuplas, y termine. La imagen original debe conservarse sin modificaciones, y cambiar una fila del resultado no debe alterar las del original.

Organice la solución en funciones que resuelvan tareas específicas y claramente delimitadas.

Verifique la solución con imágenes de un solo píxel, imágenes rectangulares, estructuras vacías, filas de distinto tamaño, píxeles con una cantidad incorrecta de componentes y valores fuera del intervalo. Además, incluya una imagen asimétrica para comprobar el efecto `ESPEJO`, ya que el corazón del ejemplo es simétrico.
