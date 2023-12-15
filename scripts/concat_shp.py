import geopandas as gpd
import os,glob
import pandas as pd

def concat_shp(folder,end,out_shp,out_excel):
    # Obtener la lista de archivos en la carpeta con la extensión .shp
    archivos_shape = glob.glob(folder+end)
    # Crear una lista para almacenar los GeoDataFrames individuales
    gdfs = []

    # CRS objetivo común (puedes cambiarlo según tus necesidades)
    crs_objetivo = 'EPSG:4326'  # Por ejemplo, WGS 84

    # Iterar a través de los archivos shapefiles y cargarlos en GeoDataFrames
    for archivo in archivos_shape:
        print(archivo)
        #ruta_completa = os.path.join(carpeta_shapefiles, archivo)
        gdf = gpd.read_file(archivo)

        # Transformar el CRS al CRS objetivo
        gdf = gdf.to_crs(crs_objetivo)
        gdf['image']=archivo
        gdfs.append(gdf)

    # Concatenar los GeoDataFrames en uno solo
    geodf_concatenado = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=crs_objetivo)


    # Guardar el GeoDataFrame concatenado en un nuevo shapefile si es necesario
    geodf_concatenado.to_file(out_shp)
    geodf_concatenado.to_excel(out_excel)

    # Imprimir información sobre el GeoDataFrame resultante
    display(geodf_concatenado.head())
    print(geodf_concatenado.shape)
    display(geodf_concatenado.describe())
