# Escritura de archivos de texto

## Escritura con `write()` y modo `"w"`

El método `write()` escribe una cadena en un archivo de texto abierto 
para escritura y devuelve la cantidad de caracteres escritos. Es importante 
considerar que no agrega saltos de línea automáticamente, para insertarlos 
se utiliza `\n`.

El siguiente ejemplo crea `output.txt` o reemplaza su contenido si ya existe:

:::{code-block} python
:linenos:

# 1. Abrir
archivo = open("data/output.txt", "w", encoding="utf-8")

# 2. Procesar: escribir dos líneas.
archivo.write("Esta primera oración se escribe en una línea.\n")
archivo.write("Esta es otra, en una nueva línea.\n")

# 3. Cerrar
archivo.close()
:::

**Nota:** el modo `"w"` vacía un archivo existente al abrirlo, incluso 
si después no se llama a `write()`. La carpeta `data` debe existir.

Para escribir valores de otros tipos, primero deben convertirse a texto, 
por ejemplo, mediante la función `str()` o una cadena formateada.

## Adición de contenido con modo `"a"`

El modo `"a"` permite escribir al final del archivo, conservando 
su contenido previo. Si el archivo no existe, se crea.

El siguiente programa solicita notas y agrega cada una al archivo `notas.txt`:

:::{code-block} python
def agregar_nota(nombre_archivo, nueva_nota):
    # 1. Abrir
    archivo = open(nombre_archivo, "a", encoding="utf-8")

    # 2. Procesar
    archivo.write(nueva_nota + "\n")

    # 3. Cerrar
    archivo.close()


mis_notas = "data/notas.txt"
while True:
    nueva_nota = input("Ingrese una nota [Enter para salir]: ")
    if nueva_nota == "":
        break
    agregar_nota(mis_notas, nueva_nota)
:::

- Cada nota termina con un salto de línea. 
- Si el archivo ya contenía texto sin un salto de línea final, la primera nota añadida quedará unida a la última línea. 
- El modo `"a"` no introduce separadores por sí solo.