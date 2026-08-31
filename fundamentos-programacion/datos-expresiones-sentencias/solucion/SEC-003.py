# Ordenamiento por selección
# Identifica el menor valor menor de una lista y lo intercambia de lugar con el primer valor.
# Repite este paso con el resto de la lista hasta que todos los números quedan ordenados.

tareas = [
    "Revisar el uso de la sintaxis",
    "Formular una solución",
    "Resolver el ejercicios",
]

lista = tareas
for i in range(len(lista)):
    menor = i
    for j in range(i+1,len(lista)):
        if lista[j] < lista[menor]:
            menor = j
    aux = lista[i]
    lista[i] = lista[menor]
    lista[menor] = aux

lista