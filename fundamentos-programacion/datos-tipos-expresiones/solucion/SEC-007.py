texto = "Python permite resolver problemas computacionales"

# 1. separar palabras
palabras = []
palabra = ''
for caracter in texto:
    if caracter == ' ':
        palabras.append(palabra)
        palabra = ''
    else:
        palabra += caracter

# última palabra
palabras.append(palabra)
print(palabras)

# contar cantidad de palabras
print(len(palabras))

# 2. mas extensa
mas_extensa = ''
for palabra in palabras:
    if len(palabra) > len(mas_extensa):
        mas_extensa = palabra
print(mas_extensa)