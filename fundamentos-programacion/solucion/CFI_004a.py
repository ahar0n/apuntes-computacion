nombres = ["Ana", "Luis", "Camila", "Luis", "Pedro"]

nombre_ingresado = input('Nombre: ')
encontrado = False
for i in range(len(nombres)):

    if nombres[i] == nombre_ingresado:
        encontrado = True
        break

if encontrado:
    print(i)
else:
    print('Nombre no encontrado.')