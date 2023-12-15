import os,fnmatch

def ultimo_archivo(path, palabra_clave):
    archivos = []

    # Recorre el directorio y subdirectorios
    for root, dirs, files in os.walk(path):
        for file in files:
            if fnmatch.fnmatch(file, '*' + palabra_clave + '*'):
                archivos.append({
                    'nombre': file,
                    'ruta': os.path.join(root, file),
                    'tiempo_modificacion': os.path.getmtime(os.path.join(root, file))
                })

    if archivos:
        # Encuentra el archivo más reciente basado en el tiempo de modificación
        archivo_reciente = max(archivos, key=lambda x: x['tiempo_modificacion'])
        return archivo_reciente['ruta']
    else:
        return None  # No se encontraron archivos que coincidan con la palabra clave
