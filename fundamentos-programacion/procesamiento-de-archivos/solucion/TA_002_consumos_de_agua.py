def leer_consumos(nombre_archivo):
    consumos = []

    try:
        archivo = open(nombre_archivo, "r")
    except OSError:
        print("No se pudo abrir el archivo.")
        return None

    linea = archivo.readline()

    while linea != "":
        consumos.append(float(linea))
        linea = archivo.readline()

    archivo.close()

    return consumos


def analizar_consumos(consumos, umbral):
    cantidad = len(consumos)
    total = 0
    sospechosos = 0
    mayor = consumos[0]
    intervalo_mayor = 1

    for i in range(cantidad):
        total = total + consumos[i]

        if consumos[i] > umbral:
            sospechosos = sospechosos + 1

        if consumos[i] > mayor:
            mayor = consumos[i]
            intervalo_mayor = i + 1

    promedio = total / cantidad

    return cantidad, total, promedio, sospechosos, mayor, intervalo_mayor


def mostrar_resultados(cantidad, total, promedio, sospechosos,
                       mayor, intervalo_mayor):
    print("Cantidad de intervalos:", cantidad)
    print("Consumo total:", total, "litros")
    print("Consumo promedio:", promedio, "litros por intervalo")
    print("Intervalos sospechosos:", sospechosos)
    print("Mayor consumo:", mayor, "litros")
    print("Intervalo del mayor consumo:", intervalo_mayor)


def procesar_consumos():
    valido = False

    while not valido:
        try:
            umbral = float(input("Ingrese el umbral en litros: "))

            if umbral >= 0:
                valido = True
            else:
                print("El umbral no puede ser negativo.")

        except ValueError:
            print("Debe ingresar un número.")

    consumos = leer_consumos("consumos.txt")

    if consumos != None:
        if len(consumos) == 0:
            print("No existen mediciones.")
        else:
            cantidad, total, promedio, sospechosos, mayor, intervalo = \
                analizar_consumos(consumos, umbral)

            mostrar_resultados(cantidad, total, promedio, sospechosos,
                               mayor, intervalo)


procesar_consumos()