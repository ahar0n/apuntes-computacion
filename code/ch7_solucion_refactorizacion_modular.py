def mostrar_menu():
    """Presenta las opciones disponibles."""
    print("\nMENÚ PRINCIPAL")
    print("1. Sumar dos números")
    print("2. Mostrar números pares entre 1 y n")
    print("3. Salir")


def calcular_suma():
    """Solicita dos números, calcula su suma y presenta el resultado."""
    a = float(input("Primer número: "))
    b = float(input("Segundo número: "))
    resultado = a + b
    print("Resultado:", resultado)


def mostrar_pares(n):
    """Muestra los pares entre 1 y n, inclusive."""
    print("Números pares:", end="")

    for numero in range(2, n + 1, 2):
        print("", numero, end="")

    print()


def obtener_pares():
    """Solicita n y comprueba su validez antes de mostrar los pares."""
    n = int(input("Ingrese n: "))

    if n <= 0:
        print("Error: n debe ser positivo.")
    else:
        mostrar_pares(n)


def ejecutar_menu():
    """Coordina las operaciones hasta que se selecciona salir."""
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion not in ["1", "2", "3"]:
            print("Opción inválida.")
            continue

        if opcion == "3":
            break

        if opcion == "1":
            calcular_suma()

        else:
            obtener_pares()

    print("Programa finalizado.")


ejecutar_menu()