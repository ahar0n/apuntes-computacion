from helper import leer_mensajes, juntar_segmentos


def ejecutar_analisis(archivo, carpeta_salida):
    """Coordinadora

    :param archivo:
    :return:
    """

    # cargar mensajes
    lista_mensajes = leer_mensajes(archivo)

    palabras_positivas = ["bueno", "buena", "excelente", "genial", "encanta", "feliz"]
    palabras_negativas = ["malo", "mala", "terrible", "pesimo", "odio", "triste"]

    #clasificar mensajes
    clasificacion, mayor_puntaje, menor_puntaje = clasificar_mensajes(
        lista_mensajes, palabras_positivas, palabras_negativas
    )

    # exportar mensajes clasificados
    for clase, mensajes in clasificacion.items():
        escribir_mensaje(f"{carpeta_salida}/{clase}.txt", mensajes)

    mostrar_reporte(clasificacion, mayor_puntaje, menor_puntaje)


def mostrar_reporte(mensajes_clasificados, mayor_puntaje, menor_puntaje):

    positivos = len(mensajes_clasificados['positivos'])
    negativos = len(mensajes_clasificados['negativos'])
    neutrales = len(mensajes_clasificados['neutrales'])
    total = positivos + negativos + neutrales

    print(f'Mensajes analizados: {total}')
    print(f'Positivos: {positivos} ({positivos/total*100:.1f}%)')
    print(f'Negativos: {negativos} ({negativos/total*100:.1f}%)')
    neutros = total-(positivos+negativos)
    print(f'Neutros: {neutros} ({neutros/total*100:.1f}%)')
    print(f'Mensaje mas positivo: {mayor_puntaje[0]}, puntaje: {mayor_puntaje[1]}')
    print(f'Mensaje mas negativo: {menor_puntaje[0]}, puntaje: {menor_puntaje[1]}')


def clasificar_mensajes(mensajes, palabras_positivas, palabras_negativas):

    mayor = (0, 0) # indice, valor
    menor = (0, 0) # indice, valor

    clasificados = {
        'positivos': [],
        'negativos': [],
        'neutrales': []
    }

    i = 1
    for mensaje in mensajes:

        puntaje = calcular_puntaje(mensaje, palabras_positivas, palabras_negativas)

        if puntaje > 0:
            clasificados['positivos'].append(mensaje)
            if puntaje > mayor[-1]:
                mayor = (i, puntaje)

        elif puntaje < 0:
            clasificados['negativos'].append(mensaje)
            if puntaje < menor[-1]:
                menor = (i, puntaje)

        else:
            clasificados['neutrales'].append(mensaje)

        i += 1

    return clasificados, mayor, menor


def escribir_mensaje(archivo, mensajes):

    fid = open(archivo, 'w')
    for mensaje in mensajes:
        mensaje_compuesto = juntar_segmentos(mensaje, ' ')
        fid.write(mensaje_compuesto + "\n")
    fid.close()


def calcular_puntaje(mensaje, positivas, negativas):

    puntaje = 0
    for palabra in mensaje:

        if palabra in positivas:
            puntaje += 1

        if palabra in negativas:
            puntaje -= 1

    return puntaje


if __name__ == '__main__':

    ejecutar_analisis(
        archivo="../datos/mensajes.txt",
        carpeta_salida="../datos"
    )