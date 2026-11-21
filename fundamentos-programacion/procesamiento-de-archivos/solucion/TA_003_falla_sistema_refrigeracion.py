from helper import leer_observaciones


def crear_episodio(inicio, cantidad):
    return {
        "inicio": inicio,
        "final": inicio + cantidad - 1,
        "cantidad": cantidad
    }


def detectar_episodios(temperaturas, limite):
    episodios = []
    inicio = 0
    cantidad = 0

    for i in range(len(temperaturas)):
        if temperaturas[i] > limite:
            # Comienza un nuevo episodio.
            if cantidad == 0:
                inicio = i + 1

            cantidad = cantidad + 1

        else:
            # La lectura normal termina el episodio.
            if cantidad > 0:
                episodio = crear_episodio(inicio, cantidad)
                episodios.append(episodio)
                cantidad = 0

    # Guardar el episodio si llega hasta la ultima lectura.
    if cantidad > 0:
        episodio = crear_episodio(inicio, cantidad)
        episodios.append(episodio)

    return episodios


def contar_lecturas_fuera_rango(episodios):
    total = 0

    for episodio in episodios:
        total = total + episodio["cantidad"]

    return total


def buscar_episodio_mayor(episodios):
    if len(episodios) == 0:
        return None

    mayor = episodios[0]

    for episodio in episodios:
        if episodio["cantidad"] > mayor["cantidad"]:
            mayor = episodio

    return mayor


def crear_informe(nombre_archivo, episodios):

    try:
        archivo = open(nombre_archivo, "w")
    except FileNotFoundError:
        print("No se pudo crear el informe:", nombre_archivo)
        return False

    if len(episodios) == 0:
        archivo.write("No se detectaron episodios fuera de rango.\n")

    for i in range(len(episodios)):
        episodio = episodios[i]

        archivo.write("Episodio " + str(i + 1) + "\n")
        archivo.write("Inicio: " + str(episodio["inicio"]) + "\n")
        archivo.write("Final: " + str(episodio["final"]) + "\n")
        archivo.write(
            "Cantidad de lecturas: "
            + str(episodio["cantidad"]) + "\n"
        )
        archivo.write("\n")

    archivo.close()
    return True


def mostrar_resumen(temperaturas, episodios):
    print("Lecturas analizadas:", len(temperaturas))
    print("Lecturas fuera de rango:", contar_lecturas_fuera_rango(episodios))
    print("Episodios detectados:", len(episodios))

    mayor = buscar_episodio_mayor(episodios)

    if mayor is None:
        print("No hay episodios fuera de rango.")
    else:
        print("Episodio mas largo:")
        print("Inicio:", mayor["inicio"])
        print("Final:", mayor["final"])
        print("Cantidad de lecturas:", mayor["cantidad"])



if __name__ == '__main__':

    """
    main
    │
    ├── leer_temperaturas()
    │
    ├── detectar_episodios()
    │   └── crear_episodio()
    │
    ├── mostrar_resumen()
    │   ├── contar_lecturas_fuera_rango()
    │   └── buscar_episodio_mayor()
    │
    └── escribir_informe()
    """

    temperaturas = leer_observaciones("../datos/temperaturas.txt")

    if len(temperaturas) == 0:
        print("El archivo no contiene mediciones.")

    else:
        episodios = detectar_episodios(temperaturas, 8)

        mostrar_resumen(temperaturas, episodios)

        if crear_informe("../datos/alertas.txt", episodios):
            print("Informe generado: alertas.txt")