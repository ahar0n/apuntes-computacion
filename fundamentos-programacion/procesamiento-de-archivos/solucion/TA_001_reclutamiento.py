

def lista_de_puntajes(archivo_de_puntajes):

    # 1 apertura
    fid = open(archivo_de_puntajes)

    puntajes = []
    # 2 procesamiento: leer puntajes y llevarlos a una lista
    while True:
        puntaje_str = fid.readline()

        if puntaje_str == "":
            break

        if puntaje_str[-1] == "\n":
            puntaje_str = puntaje_str[:-1]

        puntaje = int(puntaje_str)
        puntajes.append(puntaje)

    # 3 cierre
    fid.close()

    return puntajes


def mejores_puntajes(puntajes, cantidad):

    mejores = []

    while len(mejores) < cantidad:
        el_mayor = maximo(puntajes)
        puntajes.remove(el_mayor)
        mejores.append(el_mayor)

    return mejores


def maximo(lista):
    el_maximo = lista[0]
    for valor in lista[1:]:
        if valor > el_maximo:
            el_maximo = valor

    return el_maximo


def escribe_puntaje(nombre_de_archivo, lista):

    fid = open(nombre_de_archivo, "w")
    for valor in lista:
        fid.write(str(valor) + "\n")
    fid.close()


def seleccionar_postulantes(archivo_de_puntajes):

    puntajes = lista_de_puntajes(archivo_de_puntajes)
    mejores_30 = mejores_puntajes(puntajes, 30)

    mejores_25 = mejores_30[:25]
    lista_de_espera = mejores_30[25:]

    escribe_puntaje('../datos/mejores_puntajes.txt', mejores_25)
    escribe_puntaje('../datos/lista_de_espera.txt', lista_de_espera)



archivo = "../datos/puntajes_2018.txt"
print(lista_de_puntajes(archivo))
























