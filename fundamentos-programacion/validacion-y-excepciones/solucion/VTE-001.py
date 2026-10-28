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