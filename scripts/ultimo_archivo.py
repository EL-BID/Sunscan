import os
import glob

def ultimo_archivo(directorio,palabra_clave):
    # Comprueba si el directorio proporcionado existe
    if not os.path.exists(directorio):
        print(f"El directorio {directorio} no existe.")
        return None

    ultimo_archivo = None
    ultima_modificacion = 0

    # Busca todos los archivos .tif en el directorio y subdirectorios
    archivos_tif = glob.glob(directorio + '/**/*'+ palabra_clave, recursive=True)

    # Encuentra el archivo .tif más recientemente modificado
    for archivo in archivos_tif:
        tiempo_modificacion = os.path.getmtime(archivo)
        if tiempo_modificacion > ultima_modificacion:
            ultima_modificacion = tiempo_modificacion
            ultimo_archivo = archivo

    return ultimo_archivo
