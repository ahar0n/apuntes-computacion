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