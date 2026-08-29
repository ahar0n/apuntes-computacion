
# It. 1: mostrar menu
# It. 2: validar opciones
# It. 3: desarollar opcion 1
# It. 4: desarollar opcion 2


menu = [
    (1, 'Sumar dos números'),
    (2, 'Mostrar números pares entre 1 y N'),
    (3, 'Salir')
]

opciones_validas = []
while True:

    # mostrar menu
    print("\nMENÚ PRINCIPAL")
    for i, descripcion in menu:
        print(f"{i}. {descripcion}")
        opciones_validas.append(str(i))

    # ingresar opción
    opcion = input("\nSeleccione una opción: ")
    if opcion not in opciones_validas:
        print('Opción inválida.')
        continue

    if opcion == '1':
        # sumar dos numero
        primero = int(input('Primer número: '))
        segundo = int(input('Seguno número: '))
        print("Resultado:", primero + segundo)

    elif opcion == '2':
        # mostrar numero pareas entre 1 y N
        n = int(input('Ingrese N: '))
        pares = ''
        for numero in range(1,n,1):
            if numero % 2 == 0:
                pares += str(numero) + ' '
        if pares != '':
            print('Números pares: ' + pares)
        else:
            print('No hay números pares.')

    else:
        break

print('Programa finalizado.')