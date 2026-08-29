suma = 0
cantidad = 0
while True:
    numero = int(input('Número: '))
    if numero == 0:
        break

    suma += numero
    cantidad += 1

print("Cantidad:", cantidad)
print("Suma:", suma)