
suma = 0
cuenta = 0
while True:
    temperatura = float(input("Temperatura: "))
    if temperatura == 999:
        break

    if temperatura < -50 or temperatura > 60:
        continue

    suma += temperatura
    cuenta += 1

if cuenta > 0:
    promedio = suma / cuenta
    print(promedio)
