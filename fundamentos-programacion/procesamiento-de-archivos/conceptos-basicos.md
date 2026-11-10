# Conceptos básicos

## Almacenamiento persistente y concepto de archivo

Mantener los datos únicamente en la memoria principal (RAM) presenta dos 
limitaciones:

- Su capacidad de almacenamiento es limitada.
- Es volátil: su contenido se pierde al interrumpirse el suministro eléctrico.

El almacenamiento de datos en archivos permite conservarlos y procesar 
volúmenes mayores que la RAM disponible, trabajando por partes. Los archivos
se almacenan en dispositivos de almacenamiento secundario 
(_e.g._, discos duros o unidades SSD), y habitualmente 
se organizan jerárquicamente mediante directorios.

Un archivo:

- Es una **secuencia de bytes** que el sistema operativo trata como una unidad lógica.
- Tiene un **tamaño** expresado como un número entero de bytes, limitado por el sistema de archivos.
- **Contiene datos** cuya interpretación depende de su formato y del software que los procesa.

Estas características corresponden a la abstracción habitual de archivo 
regular.[@silberschatz2018operating]

## Archivos de texto y archivos binarios

Todos los archivos almacenan bytes. Al tratarlos como **texto**, estos 
se interpretan mediante una codificación de caracteres, por ejemplo, UTF-8. 
Al tratarlos como **binarios**, se accede directamente a los bytes y 
el programa los interpreta según el formato correspondiente.

Un carácter no equivale necesariamente a un byte, por ejemplo, en UTF-8 
algunos caracteres ocupan varios bytes.

## Operaciones y etapas del procesamiento

Entre las operaciones habituales sobre archivos se encuentran las siguientes [@silberschatz2018operating]:

- **Create (crear):** crear un archivo con un nombre y determinados atributos.
- **Open (abrir):** habilitar el acceso al archivo e indicar su modo de uso.
- **Read/Write (leer/escribir):** transferir datos entre el archivo y la memoria principal.
- **Append (añadir):** escribir al final del archivo, conservando el contenido existente. En Python se habilita mediante un modo de apertura.
- **Close (cerrar):** finalizar el acceso y liberar los recursos asociados.
- **Delete (eliminar):** quitar el archivo del sistema de archivos; esto no garantiza el borrado físico inmediato de sus datos.

El procesamiento de un archivo comprende tres etapas básicas:

1. **Abrir el archivo**, indicando su ruta (*path*) y modo de acceso: lectura, escritura o adición al final. El modo elegido puede implicar crear el archivo o sobrescribir su contenido.
2. **Leer o escribir datos**, según la tarea, ya sea en su totalidad o por partes —por ejemplo, líneas o bloques— para limitar el uso de memoria.
3. **Cerrar el archivo**, para vaciar los búferes de escritura y liberar los recursos asociados. El cierre debe realizarse también si ocurre un error durante el procesamiento.