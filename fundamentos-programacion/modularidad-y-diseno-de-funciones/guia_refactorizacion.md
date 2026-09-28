---
title: "Ejercicio guiado de refactorización"
bibliography:
  - ../referencias_capitulo_07.bib
---

## Contexto y description del ejercicio

El siguiente programa es funcional (basado en la solución del ejercicio [CFI-008](#ch7-ejercicio-CFI-008)), pero reúne en un único bloque la lectura de
datos, la selección de opciones, los cálculos y la presentación de resultados.

:::{code-block} python
:label: cap07-code-refactorizacion
:linenos:

while True:
    print("\nMENÚ PRINCIPAL")
    print("1. Sumar dos números")
    print("2. Mostrar números pares entre 1 y n")
    print("3. Salir\n")

    opcion = input("Seleccione una opción: ")

    if opcion not in ["1", "2", "3"]:
        print("Opción inválida.")
        continue

    if opcion == "3":
        break

    if opcion == "1":
        a = float(input("Primer número: "))
        b = float(input("Segundo número: "))
        resultado = a + b
        print("Resultado:", resultado)

    else:
        n = int(input("Ingrese n: "))

        if n <= 0:
            print("Error: n debe ser positivo.")
        else:
            numeros_pares = ""
            for numero in range(2, n, 2):
                numeros_pares += str(numero) + " "
            print("Números pares:", numeros_pares)

print("Programa finalizado.")
:::

Reorganice el programa mediante funciones, conservando su comportamiento. El
propósito consiste en distribuir las responsabilidades y componer las partes.

Suponga que los operandos ingresados pueden convertirse a números y que `n` 
puede convertirse a entero.

## Paso 1. Análisis del problema

Realice una descripción breve de la especificación del problema (global) y su 
descomposición en tareas específicas. Para esto,

1. Identifique los resultados que debe producir y los datos necesarios para obtenerlos. 
2. Distinga las tareas que componen la solución. 
3. Describa las decisiones que determinan la ejecución, repetición o término de cada tarea. 
4. Establezca las condiciones necesarias para ejecutar correctamente cada operación.

**Resultados:** Descripción de la especificación global y descomposición en tareas específicas.

## Paso 2. Propuesta de organización

1. Proponga una organización con una función principal que coordine el programa y las funciones auxiliares que sean necesarias. Complete la tabla de descripciones breves:

| Función propuesta | Responsabilidad | Parámetros | Retorno o efecto observable |
|:------|:---|:---|:---|
|...|...|...|...|

2. Dibuje un diagrama de dependencias indicando los parámetros y registrando los 
retornos cuando corresponda.

3. Opcionalmente, especifique cada función.

4. Redacte una secuencia en lenguaje natural que explique las repeticiones y decisiones de la coordinación. Esta secuencia deben ser coherentes con el diagrama de dependencias.

**Resultados:** tabla de responsabilidades, diagrama de dependencias y secuencia de coordinación.

## Paso 3. Refactorización del programa

Transforme el programa inicial de acuerdo con la organización propuesta. Para 
esto, implemente y pruebe cada función de forma aislada. A continuación, 
integre las funciones.

Esta nueva versión debe:

- Conservar las opciones, los mensajes, los resultados y el regreso al menú. 
- Tener una función principal que coordine la ejecución y delegue tareas. 
- Comunicar los datos necesarios mediante argumentos y retornos, sin utilizar variables globales. 
- Respetar las condiciones de uso de las funciones que definieron. 
- Si durante la implementación necesitan modificar su diseño, actualice la tabla y el diagrama. Registren brevemente los cambios y su justificación.

**Resultados:** Programa modular y diseño actualizado.

## Paso 4. Pruebas de integración

En esta etapa debe comprobar que las funciones colaboran correctamente y que la 
organización o composición conserva el comportamiento inicial.

Genere los casos de prueba identificando las entradas y las salidas esperadas. A 
continuación, ejecute las pruebas (de escritorio y de ejecución) para observar 
y contrastar los resultados esperados y los obtenidos de la ejecución.

**Resultados:** Registro de pruebas.

## Actividad

Intercambie su solución con su compañero y aborde las siguientes tareas.

1. Contraste las llamadas implementadas con las dependencias representadas en el diagrama y señalen las diferencias. 
2. Examine la responsabilidad de cada función e identifiquen aquellas cuya tarea no se comprende con claridad. 
3. Siga el recorrido de los datos entre funciones, indicando los argumentos transmitidos y el uso de los retornos. 
4. Verifique que las condiciones necesarias se comprueben antes de ejecutar las operaciones correspondientes. 
5. Compruebe que la función coordinadora delegue las tareas previstas en el diseño. 
6. Relacione cada prueba de integración con la conexión o decisión que permite comprobar.

**Tarea:** Prepare una presentación de los resultados de la revisión y expóngala ante el curso.