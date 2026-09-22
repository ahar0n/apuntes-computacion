# Composición e integración

## Implementación de la composición

La **composición** conecta unidades previamente delimitadas para satisfacer la
especificación del problema completo. La operación coordinadora determina 
cuándo llamar a cada función, qué argumentos suministrar y cómo utilizar sus 
retornos. Las pruebas aisladas aportan evidencia sobre cada unidad, mientras 
que, las conexiones entre ellas aún deben comprobarse [@guttag2021introduction; @iso29119_1_2022].

Las [interfaces previstas](#cap07-tab-interfaces-problema) establece que:

- Toda observación solicitada debe leerse y clasificarse una vez.
- Solo los dentro de rango deben incorporarse a la lista de observaciones válidas.
- La cantidad de rechazos debe incrementarse únicamente cuando la validación produce `False`.
- La unidad que calcula el promedio debe recibir una lista no vacía de valores previamente validados.
- La presentación debe recibir valores coherentes.

Estas obligaciones derivan de las relaciones entre las unidades. Una prueba aislada 
de la unidad «Determinar validez» no puede comprobar, por ejemplo, que la 
coordinación utilice su retorno en la rama correcta.

:::{table} Correspondencia entre funciones y responsabilidades
:label: cap07-tab-funciones-responsabilidades
:align: center

| Función                  | Responsabilidad                         | Resultado o efecto principal                         |
|:-------------------------|:----------------------------------------|:-----------------------------------------------------|
| `leer_observacion`       | obtener una observación                 | retorna un entero y realiza una operación de entrada |
| `es_observacion_valida`  | determinar la validez                   | retorna un valor booleano                            |
| `calcular_promedio`      | calcular el promedio                    | retorna un número                                    |
| `mostrar_resumen`        | comunicar los resultados                | realiza operaciones de salida                        |
| `procesar_observaciones` | coordinar lectura, validación y cálculo | construye los datos requeridos por el resumen        |

:::

::::{dropdown} Especificación de funciones

:::{table} Especificación de `leer_observacion()`
:label: tab-especificacion-leer-observacion
:align: center

| Elemento            | Especificación                                                                 |
|:--------------------|:-------------------------------------------------------------------------------|
| Propósito           | Solicitar y obtener la observación situada en una posición determinada.        |
| Parámetro           | `posicion` de la observación dentro de la secuencia de entrada.                |
| Precondición        | `posicion` es un entero positivo y la entrada puede interpretarse como entero. |
| Retorno             | Entero introducido para la posición indicada.                                  |
| Poscondición        | El resultado coincide con el entero ingresado.                                 |
| Efectos observables | Muestra una solicitud de entrada y consume un dato de la entrada disponible.   |

:::

:::{table} Especificación de `mostrar_resumen()`
:label: tab-especificacion-mostrar-resumen
:align: center

| Elemento            | Especificación                                                                                                                                                                                     |
|:--------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Propósito           | Mostrar las cantidades de observaciones válidas y rechazadas, y promedio cuando está definido.                                                                                                     |
| Parámetro           | `validas`: cantidad de observaciones válidas, `rechazadas`: cantidad de observaciones rechazadas, `promedio`: promedio de las observaciones válidas o `None`.                                      |
| Precondición        | `validas` y `rechazadas` son enteros no negativos. Si `validas = 0`, `promedio` es `None`. Si `validas > 0`, `promedio` es el valor numérico previamente calculado para las observaciones válidas. |
| Retorno             | Ninguno                                                                                                                                                                                            |
| Poscondición        | Los tres argumentos conservan sus valores.                                                                                                                                                         |
| Efectos observables | Muestra las dos cantidades. Si `promedio == None`, muestra `Promedio no calculado: sin observaciones válidas`, en caso contrario, muestra `Promedio:` seguido del valor del valor `promedio`.      |
:::

- [Especificacificación de `es_observacion_valida()`](#cap07-tab-esp-es-observacion-valida)
- [Especificacificación de `calcular_promedio()`](#cap07-tab-esp-es-observacion-valida)

::::

Antes de su implementación, la coordinación puede describirse mediante sus 
estados y decisiones principales. Por ejemplo,

(ch7-ejemplo-composicion-lenguaje-natural)=
1. Crear una lista vacía para las observaciones válidas e inicializar en cero la cantidad de rechazos.
2. Repetir la lectura para cada observación.
3. Validar cada observación leída.
4. Si es válida, incorporar el valor leído a la lista de válidas, en caso contrario, incrementar los rechazos.
5. Obtener la cantidad de observaciones válidas a partir de la longitud de la lista.
6. Si la cantidad es mayor que cero, calcular el promedio, en caso contrario, representar su ausencia mediante `None`.
7. Mostrar las cantidades y el promedio.

La lista y el contador de rechazos resumen el procesamiento efectuado hasta 
cada punto del recorrido. Después de procesar una observación, la lista contiene 
los valores válidos hasta ese momento y el contador de rechazos contiene la 
cantidad de valores rechazados. Esta relación permite evaluar sobre la coherencia 
de la coordinación sin atribuir a la función de validación la responsabilidad 
de almacenar o contar resultados.

La [](#cap07-fig-flujo-composicion) muestra el flujo de control de la 
coordinación. Mientras que el [diagrama de dependencias](#cap07-fig-dependencias-problema) 
identifica las unidades que colaboran, el diagrama de flujo representa la 
repetición de llamadas, como las realizadas a `leer_observacion()`, y las 
condiciones que determinan otras llamadas, como la efectuada a `calcular_promedio()`.


:::{figure} ../../assets/images/fundamentos-programacion/flowchart_composicion.png
:alt: Diagrama de flujo que inicializa la lista y el contador, lee y valida cada observación, agrega o rechaza el valor, calcula el promedio solo si existen valores válidos y muestra el resumen.
:width: 350px
:align: center
:label: cap07-fig-flujo-composicion

Flujo de control del procesamiento.
:::

Una implementación en Python coherente con el algoritmo se presenta a 
continuación:

:::{code-block} python
:label: cap07-code-solucion-modular
:linenos:

def es_observacion_valida(valor):
    """Indica si valor pertenece al intervalo cerrado [0, 100]."""
    observacion_valida = 0 <= valor <= 100
    return observacion_valida


def calcular_promedio(observaciones_validas):
    """Devuelve el promedio de una lista no vacía de observaciones."""
    suma = 0
    cantidad = 0

    for valor in observaciones_validas:
        suma += valor
        cantidad += 1

    promedio = suma / cantidad
    return promedio


def leer_observacion(posicion):
    """Lee y devuelve la observación situada en posicion."""
    observacion = int(input(f"Observación {posicion}: "))
    return observacion


def mostrar_resumen(validas, rechazadas, promedio):
    """Muestra las cantidades y el promedio, cuando está definido."""
    print("Observaciones válidas:", validas)
    print("Observaciones rechazadas:", rechazadas)

    if promedio is None:
        print("Promedio no calculado: sin observaciones válidas")
    else:
        print("Promedio:", promedio)


def procesar_observaciones(cantidad):
    """Lee, clasifica y resume una cantidad positiva de observaciones."""
    observaciones_validas = []
    rechazadas = 0

    for posicion in range(1, cantidad + 1):
        valor = leer_observacion(posicion)

        if es_observacion_valida(valor):
            observaciones_validas.append(valor)
        else:
            rechazadas += 1

    validas = len(observaciones_validas)

    if validas > 0:
        promedio = calcular_promedio(observaciones_validas)
    else:
        promedio = None

    mostrar_resumen(validas, rechazadas, promedio)


cantidad = int(input("Cantidad de observaciones: "))
procesar_observaciones(cantidad)

:::


## Pruebas de integración

Una **prueba de integración** examina las interacciones entre unidades 
conectadas. Comprueba que la composición suministre los argumentos adecuados, 
respete las precondiciones, use correctamente los retornos y ejecute las 
unidades en un orden compatible con sus dependencias [@iso29119_1_2022].

Que varias funciones superen sus pruebas aisladas no garantiza que la composición 
sea correcta. Una conexión podría proporcionar argumentos equivocados, omitir 
una llamada, usar incorrectamente un retorno o invocar una función cuando su 
precondición no se satisface.

La selección de casos de integración se guía por **interacciones**, no por 
funciones consideradas separadamente. Por ejemplo, en [la implementación](cap07-code-solucion-modular) 
se debe examinar al menos tres situaciones:

:::{table} Ejemplo de pruebas de integración
:label: tab-cap07-pruebas-integracion
:align: center

|  Observaciones  | Interacción examinada                                                           | Resultado esperado                               |
|:---------------:|:--------------------------------------------------------------------------------|:-------------------------------------------------|
| `80,-1,100,140` | La validación produce ambos resultados y el promedio recibe una lista no vacía. | 2 válidas, 2 rechazadas y promedio `90.0`.       |
|    `-1,101`     | Ninguna observación es válida. Debe omitirse la llamada al promedio.            | 0 válidas, 2 rechazadas y promedio no calculado. |
|     `0,100`     | Los dos límites se transmiten al promedio.                                      | 2 válidas, 0 rechazadas y promedio `50.0`.       |

:::

El resultado esperado se determina a partir de la especificación global y de 
las conexiones previstas. Solo después se ejecuta el programa completo y se 
registra la salida obtenida.

El primer caso activa todas las conexiones. El segundo comprueba que la 
coordinación no infrinja la precondición del promedio. El tercero examina la 
transmisión de valores límite. No es necesario repetir todas las pruebas aisladas 
durante la integración si no aportan información nueva sobre las conexiones.
