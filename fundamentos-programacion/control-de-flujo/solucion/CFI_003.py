
cuenta_negativos = 0
suma = 0
for i in range(10):
    numero = int(input("Numero: "))
    if numero < 0:
        cuenta_negativos += 1
        continue

    suma += numero

print('Suma:', suma)
print('Negativos ignorados:', cuenta_negativos)