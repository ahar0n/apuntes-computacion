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

::::{dropdown} Solución
:open:

:::{code-block} python
:linenos:

while True:
    try:
        nivel = int(input("Nivel de carga (1 a 8): "))
    except ValueError:
        print("El nivel de carga debe ser un número entero.")
        continue

    if not 1 <= nivel <= 8:
        print("El nivel de carga debe estar entre 1 y 8.")
        continue

    energia = nivel ** 2
    print("Energía liberada:", energia)

    if energia < 25:
        print("Energía insuficiente. El portal permanece cerrado.")
    elif energia == 25:
        print("¡El portal se abre!")
    else:
        print("Sobrecarga. El portal queda bloqueado.")

    break
:::

::::



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


::::{dropdown} Solución
:open:

:::{code-block} python
:linenos:

def leer_clave_y_digito():
    digito = int(input("Dígito original (0 a 9): "))
    clave = int(input("Clave (0 a 9): "))
    return digito, clave


def codificar(digito, clave):
    return (digito + clave) % 10


def decodificar(cifrado, clave):
    return (cifrado - clave) % 10


while True:
    try:
        digito, clave = leer_clave_y_digito()
    except ValueError:
        print("El dígito y la clave deben ser números enteros.")
        continue

    if not (0 <= digito <= 9 and 0 <= clave <= 9):
        print("El dígito y la clave deben estar entre 0 y 9.")
        continue

    cifrado = codificar(digito, clave)
    recuperado = decodificar(cifrado, clave)

    print("Valor codificado:", cifrado)
    print("Dígito recuperado:", recuperado)
    break
:::

::::



**VTE-003.** La secuencia de ADN se representa mediante una cadena de entre 6 y 60 caracteres. Solo se admiten las letras mayúsculas `A`, `C`, `G` y `T`, sin espacios.

Se requiere localizar todas las apariciones de un motivo, es decir, una cadena de exactamente tres letras del mismo alfabeto.

Por ejemplo, en la secuencia `"AAAAAA"`, el motivo `"AAA"` aparece en los índices `0`, `1`, `2` y `3`. Estas coincidencias se superponen porque comparten caracteres.

Implemente dos funciones:

- `validar_datos(secuencia, motivo)`: recibe dos cadenas y devuelve un mensaje que explica la primera restricción incumplida de los datos. Si ambas cadenas cumplen todas las restricciones, devuelve una cadena vacía.
- `buscar_motivo(secuencia, motivo)`: recibe cadenas previamente validadas y devuelve una lista con los índices iniciales de todas las coincidencias. Los índices comienzan en cero.

Para realizar la búsqueda, utilice un recorrido por índices y segmentación de la cadena. Puede implementar las funciones auxiliares que considere necesarias, siempre que cada una resuelva una tarea específica y claramente delimitada. No use el método `index()`.

El programa principal debe solicitar ambas cadenas, validarlas y, si alguna incumple las restricciones, mostrar un mensaje que explique el problema. Cuando los datos sean válidos, debe mostrar la lista de posiciones y terminar. Si no existen coincidencias, debe mostrar una lista vacía.

::::{dropdown} Solución
:open:

:::{code-block} python
:linenos:

def validar_datos(secuencia, motivo):
    if not 6 <= len(secuencia) <= 60:
        return "La secuencia debe tener entre 6 y 60 caracteres."

    if len(motivo) != 3:
        return "El motivo debe tener exactamente tres caracteres."

    for letra in secuencia:
        if letra not in "ACGT":
            return "La secuencia solo admite las letras A, C, G y T."

    for letra in motivo:
        if letra not in "ACGT":
            return "El motivo solo admite las letras A, C, G y T."

    return ""


def buscar_motivo(secuencia, motivo):
    posiciones = []

    for i in range(len(secuencia) - len(motivo) + 1):
        if secuencia[i:i + len(motivo)] == motivo:
            posiciones.append(i)

    return posiciones


while True:
    secuencia = input("Secuencia de ADN: ")
    motivo = input("Motivo de tres letras: ")

    rechazo = validar_datos(secuencia, motivo)

    if rechazo != "":
        print(rechazo)
        continue

    posiciones = buscar_motivo(secuencia, motivo)
    print("Índices de las coincidencias:", posiciones)
    break
:::


Pruebas:

|  Secuencia  |  Motivo  | Esperado                              |
|:-----------:|:--------:|:--------------------------------------|
| `"AAAAAA"`  | `"AAA"`  | `[0, 1, 2, 3]`                        |
| `"ACGTAC"`  | `"TAC"`  | `[3]`                                 |
| `"ACGTAC"`  | `"GGG"`  | `[]`                                  |
| `"ACGTNC"`  | `"ACG"`  | Rechazo por el carácter `N`           |
| `"acgtac"`  | `"ACG"`  | Rechazo por minúsculas                |
| `"ACGTAC"`  |  `"AC"`  | Rechazo por longitud del motivo       |
|  `"ACGT"`   | `"ACG"`  | Rechazo por longitud de la secuencia  |

::::



**VTE-004.** Un sensor de observatorio registra entre 4 y 12 lecturas enteras de brillo, cada una entre 0 y 100. Las lecturas se ingresan en una cadena separada por comas. Se permiten espacios alrededor de los números, pero no lecturas vacías.

Un destello es una lectura mayor que sus dos vecinas inmediatas (la anterior y la posterior). La primera y la última lectura no se consideran destellos. Los valores consecutivos iguales, como por ejemplo, `20,80,80,20`, tampoco constituyen destellos.

Desarrolle un programa que interprete la entrada y muestre una lista de tuplas `(indice, brillo)` con los destellos encontrados. Los índices comienzan en cero. Utilice índices para comparar las lecturas y organice la solución en funciones que resuelvan tareas específicas y claramente delimitadas.

Trate los errores de conversión y compruebe las restricciones de los datos. Si alguna lectura o el conjunto ingresado incumple los requisitos, informe el problema y solicite nuevamente la cadena completa.

Cuando la entrada sea válida, muestre el resultado y termine. Si no hay destellos, muestre una lista vacía.


::::{dropdown} Solución
:open:

:::{code-block} python
:linenos:

def interpretar_lecturas(texto):
    campos = texto.split(",")

    if not 4 <= len(campos) <= 12:
        return None, "Debe ingresar entre 4 y 12 lecturas."

    lecturas = []

    for i in range(len(campos)):
        try:
            brillo = int(campos[i])
        except ValueError:
            return None, f"La lectura del índice {i} debe ser un entero no vacío."

        if not 0 <= brillo <= 100:
            return None, f"La lectura del índice {i} debe estar entre 0 y 100."

        lecturas.append(brillo)

    return lecturas, ""


def detectar_destellos(lecturas):
    destellos = []

    for i in range(1, len(lecturas) - 1):
        if lecturas[i] > lecturas[i - 1] and lecturas[i] > lecturas[i + 1]:
            destellos.append((i, lecturas[i]))

    return destellos


while True:
    texto = input("Lecturas de brillo separadas por comas: ")
    lecturas, mensaje = interpretar_lecturas(texto)

    if mensaje != "":
        print(mensaje)
        continue

    print("Destellos:", detectar_destellos(lecturas))
    break
:::

- `interpretar_lecturas` devuelve la lista y una cadena vacía cuando la entrada es válida. Si detecta un problema, devuelve `None` y un mensaje explicativo. La lista parcial de un intento rechazado no se devuelve.

- `int()` admite espacios alrededor de los números y produce `ValueError` ante textos no convertibles, incluidos los campos vacíos. Las demás restricciones se comprueban mediante condiciones.

- La búsqueda recorre desde el índice 1 hasta el penúltimo índice, de modo que cada lectura evaluada tenga dos vecinas.

Casos de prueba:

| Entrada            | Esperado                              |
|:-------------------|:--------------------------------------|
| `"10,80,20,90,10"` | `[(1, 80), (3, 90)]`                  |
| `"20,80,80,20"`    | `[]`                                  |
| `"0,100,0,100"`    | `[(1, 100)]`                          |
| `"10, 20, 30, 40"` | `[]`                                  |
| `"10,20,30"`       | Rechazo por cantidad de lecturas      |
| `"10,,20,30"`      | Rechazo por campo vacío               |
| `"10,alto,20,30"`  | Rechazo por conversión                |
| `"10,101,20,30"`   | Rechazo por valor fuera del intervalo |

::::



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


::::{dropdown} Solución
:open:

:::{code-block} python
:linenos:

def validar_panel(panel):
    if not 2 <= len(panel) <= 8:
        return "El panel debe tener entre 2 y 8 filas."

    columnas = len(panel[0])

    if not 2 <= columnas <= 8:
        return "El panel debe tener entre 2 y 8 columnas."

    for fila in panel:
        if len(fila) != columnas:
            return "Todas las filas deben tener la misma cantidad de elementos."

        for luz in fila:
            if luz not in (0, 1):
                return "Cada elemento debe valer 0 o 1."

    return ""


def contar_vecinas(panel, fila, columna):
    encendidas = 0

    if fila > 0:
        encendidas += panel[fila - 1][columna]

    if fila < len(panel) - 1:
        encendidas += panel[fila + 1][columna]

    if columna > 0:
        encendidas += panel[fila][columna - 1]

    if columna < len(panel[0]) - 1:
        encendidas += panel[fila][columna + 1]

    return encendidas


def actualizar_panel(panel):
    mensaje = validar_panel(panel)

    if mensaje != "":
        return None, mensaje

    nuevo = []

    for fila in range(len(panel)):
        nueva_fila = []

        for columna in range(len(panel[0])):
            vecinas = contar_vecinas(panel, fila, columna)

            if vecinas == 2:
                nueva_fila.append(1)
            else:
                nueva_fila.append(0)

        nuevo.append(nueva_fila)

    return nuevo, ""


def mostrar_panel(panel):
    for fila in panel:
        print(fila)


paneles = [
    [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1], [0, 0]],
    [[0, 0], [0, 0]],
    [[0, 1], [1]],
    [[0, 2], [1, 0]],
    [],
]

for numero, panel in enumerate(paneles, start=1):
    print(f"\nCaso {numero}")

    nuevo, mensaje = actualizar_panel(panel)

    if mensaje != "":
        print("Panel rechazado:", mensaje)
        continue

    print("Panel original:")
    mostrar_panel(panel)

    print("Siguiente estado:")
    mostrar_panel(nuevo)
:::

- `validar_panel` comprueba primero la cantidad de filas, antes de acceder a `panel[0]`. Luego comprueba el ancho, la longitud de todas las filas y los valores de las luces.

- `contar_vecinas` comprueba los límites antes de consultar cada posición. No se necesita capturar `IndexError`: los accesos se realizan únicamente cuando la vecina existe.

- `actualizar_panel` devuelve `(None, mensaje)` cuando el panel es inadmisible y `(nuevo, "")` cuando puede calcular el siguiente estado. Cada fila del resultado se construye por separado y todas las consultas se realizan sobre el panel original.

**Comprobación de actualización simultánea e independencia**

:::{code-block} python
:linenos:

panel = [[1, 1], [0, 0]]
esperado = [[0, 0], [0, 0]]

nuevo, mensaje = actualizar_panel(panel)

if mensaje == "":
    print("Actualización correcta:", nuevo == esperado)
    print("Original conservado:", panel == [[1, 1], [0, 0]])

    # Cambiar el resultado no debe modificar el original ni otra fila.
    nuevo[0][0] = 1

    print("Original independiente:", panel == [[1, 1], [0, 0]])
    print("Filas independientes:", nuevo[1] == [0, 0])
:::

- Las cuatro comprobaciones deben mostrar `True`. El primer caso permite detectar una actualización sobre el mismo panel: si se modificaran las luces mientras se recorren, las siguientes podrían consultar valores ya alterados.

- No se utiliza `try–except` porque, bajo el supuesto de recibir listas de listas de enteros, las restricciones se comprueban mediante condiciones y no requieren provocar ni tratar excepciones.

::::


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


::::{dropdown} Solución
:open:

:::{code-block} python
:linenos:

def agregar_reaccion(mensajes, usuarios, identificador, usuario):
    autor, texto, reacciones = mensajes[identificador]

    if usuario not in usuarios:
        return None, "El usuario no está registrado."

    if usuario == autor:
        return None, "No puede dar «Me gusta» a su propio mensaje."

    if usuario in reacciones:
        return None, "El usuario ya dio «Me gusta» a este mensaje."

    nuevas_reacciones = reacciones + [usuario]
    mensajes[identificador] = (autor, texto, nuevas_reacciones)

    return len(nuevas_reacciones), ""


def gestionar_reacciones(mensajes, usuarios):
    while True:
        entrada = input("Identificador del mensaje o FIN: ")

        if entrada == "FIN":
            return

        try:
            identificador = int(entrada)
        except ValueError:
            print("El identificador debe ser un número entero.")
            continue

        usuario = input("Nombre de usuario: ")

        try:
            cantidad, mensaje = agregar_reaccion(
                mensajes, usuarios, identificador, usuario
            )
        except KeyError:
            print("El mensaje no existe.")
            continue

        if mensaje != "":
            print(mensaje)
            continue

        print("Cantidad de reacciones del mensaje:", cantidad)


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

gestionar_reacciones(mensajes, usuarios)

print("Mensajes al finalizar:")
for identificador, datos in mensajes.items():
    print(identificador, datos)
:::

`agregar_reaccion` consulta el mensaje y comprueba las restricciones antes de modificarlo. Si una condición impide realizar la operación, devuelve `None` y un mensaje explicativo. Si la acepta, actualiza las reacciones y devuelve su cantidad junto con una cadena vacía.

Si el identificador no existe, la consulta `mensajes[identificador]` produce `KeyError`. La excepción se propaga hasta `gestionar_reacciones`, donde se informa del problema y se inicia otra operación.

**Pruebas**

Ejecute esta secuencia desde el estado inicial:

| Identificador | Usuario | Resultado esperado |
|---|---|---|
| `"hola"` | No se solicita | Error de conversión |
| `999` | `"yei_lo"` | El mensaje no existe |
| `101` | `"desconocido"` | Usuario no registrado |
| `101` | `"la_mon"` | No puede reaccionar a su propio mensaje |
| `205` | `"la_mon"` | Ya reaccionó al mensaje |
| `101` | `"yei_lo"` | Operación aceptada; cantidad: 1 |
| `101` | `"yei_lo"` | Reacción repetida; cantidad conservada en 1 |
| `101` | `"nino_maravilla"` | Operación aceptada; cantidad: 2 |
| `FIN` | No se solicita | Finaliza |

Al terminar, las reacciones del mensaje `101` deben ser `["yei_lo", "nino_maravilla"]` y las del mensaje `205` deben seguir siendo `["la_mon"]`.

::::



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

Desarrolle un programa que valide una imagen definida en el código. Debe comprobar que:

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

::::{dropdown} Solución
:open:

:::{code-block} python
:linenos:

def validar_imagen(imagen):
    if not 1 <= len(imagen) <= 6:
        return "La imagen debe tener entre 1 y 6 filas."

    columnas = len(imagen[0])

    if not 1 <= columnas <= 6:
        return "La imagen debe tener entre 1 y 6 columnas."

    for fila in imagen:
        if len(fila) != columnas:
            return "Todas las filas deben tener la misma cantidad de píxeles."

        for pixel in fila:
            if len(pixel) != 3:
                return "Cada píxel debe tener exactamente tres componentes."

            for componente in pixel:
                if not 0 <= componente <= 255:
                    return "Todas las componentes deben estar entre 0 y 255."

    return ""


def transformar_imagen(imagen, operacion):
    # Recibe una imagen y una operación previamente validadas.
    resultado = []

    for fila in imagen:
        nueva_fila = []

        if operacion == "ESPEJO":
            for c in range(len(fila) - 1, -1, -1):
                nueva_fila.append(fila[c])
        else:
            for rojo, verde, azul in fila:
                nueva_fila.append(
                    (255 - rojo, 255 - verde, 255 - azul)
                )

        resultado.append(nueva_fila)

    return resultado


def mostrar_imagen(imagen):
    for fila in imagen:
        print(fila)


def ejecutar_editor(imagen):
    mensaje = validar_imagen(imagen)

    if mensaje != "":
        print(mensaje)
        return

    while True:
        operacion = input("Operación (ESPEJO o NEGATIVO): ")

        if operacion in ("ESPEJO", "NEGATIVO"):
            break

        print("Operación desconocida.")

    resultado = transformar_imagen(imagen, operacion)

    print("Imagen original:")
    mostrar_imagen(imagen)

    print("Imagen transformada:")
    mostrar_imagen(resultado)


imagen = [
    [(255, 255, 255), (255, 0, 0),     (255, 255, 255), (255, 0, 0),     (255, 255, 255)],
    [(255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 0, 0)],
    [(255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 0, 0)],
    [(255, 255, 255), (255, 0, 0),     (255, 0, 0),     (255, 0, 0),     (255, 255, 255)],
    [(255, 255, 255), (255, 255, 255), (255, 0, 0),     (255, 255, 255), (255, 255, 255)],
]

ejecutar_editor(imagen)
:::

La validación comprueba las dimensiones antes de acceder a los píxeles. Solo después de validar la imagen se solicita la operación.

Cada transformación construye nuevas listas para el resultado y sus filas. En `ESPEJO` se reutilizan las tuplas de los píxeles, que son inmutables; reemplazar un píxel del resultado no modifica el original.

**Pruebas de validación**

Este fragmento puede ejecutarse después de definir las funciones:

```python
casos = [
    [[(0, 128, 255)]],                     # Válida: un píxel.
    [[(255, 0, 0), (0, 255, 0)]],          # Válida: rectangular.
    [],                                    # Sin filas.
    [[]],                                  # Sin columnas.
    [[(0, 0, 0)], [(0, 0, 0), (1, 1, 1)]], # Filas desiguales.
    [[(0, 0)]],                            # Faltan componentes.
    [[(0, 0, 256)]],                       # Componente fuera de rango.
]

for numero, caso in enumerate(casos, start=1):
    mensaje = validar_imagen(caso)

    if mensaje == "":
        print("Caso", numero, ": imagen válida.")
    else:
        print("Caso", numero, ":", mensaje)
```

**Prueba del espejo y de la independencia del resultado**

```python
original = [
    [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
]

resultado = transformar_imagen(original, "ESPEJO")

print(
    "Espejo correcto:",
    resultado == [[(0, 0, 255), (0, 255, 0), (255, 0, 0)]],
)

resultado[0][0] = (0, 0, 0)

print(
    "Original conservado:",
    original == [[(255, 0, 0), (0, 255, 0), (0, 0, 255)]],
)
```

Ambas comprobaciones deben mostrar `True`. No se necesita manejo de excepciones, debido a que los tipos están garantizados por el enunciado y las restricciones se comprueban mediante condiciones.

::::