import logging
import datetime

import numpy as np
import pandas as pd
import geopandas as gpd
from astral import sun, LocationInfo
import pyproj

logger = logging.getLogger()

TIME_FORMAT = '%H:%M:%S'


def sunlight_hours(lat, lon, start, end):
    data = {}
    data['sunrise'] = []
    data['sunset'] = []
    data['noon'] = []
    delta = end - start

    for day in range(delta.days + 1):
        this_date = start + datetime.timedelta(days=day)
        try:
            l = LocationInfo()
            l.name = 'name'
            l.region = 'region'
            l.latitude = lat
            l.longitude = lon

            s = sun.sun(l.observer, date=this_date)
            
            data['sunrise'].append(s['sunrise'].time().strftime(TIME_FORMAT))
            data['sunset'].append(s['sunset'].time().strftime(TIME_FORMAT))
            data['noon'].append(s['noon'].time().strftime(TIME_FORMAT))

        except ValueError as e:
            logger.warning(f'No se pudo calcular el atardecer para {this_date}: {e}')
            continue  # Continuar con la próxima fecha si ocurre un error

    df = pd.DataFrame(data)
    df['noon'] = pd.to_datetime(df['noon'], format=TIME_FORMAT).dt.time
    df['sunrise'] = pd.to_datetime(df['sunrise'], format=TIME_FORMAT).dt.time
    df['sunset'] = pd.to_datetime(df['sunset'], format=TIME_FORMAT).dt.time

    df['dif_sec'] = (
        pd.to_timedelta(df['noon'].astype(str))
        - pd.to_timedelta(df['sunrise'].astype(str))
    ).dt.total_seconds()
    df['sunlight_hours'] = (df['dif_sec'] / 60) / 60
    sunlight_hours_sum = np.sum((df['dif_sec'] / 60) / 60)
    return sunlight_hours_sum


def calculate_solar_energy(shp_in, start, end, panel_size, area_disp, panel_pot, factor_dim) -> gpd.GeoDataFrame:
    gdf: gpd.GeoDataFrame = gpd.read_file(shp_in)
    # Get the CRS (coordinate reference system) of the shapefile
    crs = gdf.crs
    # Convert the CRS to a Proj4 string
    crs_proj4 = pyproj.CRS(crs).to_proj4()

    # Create a Transformer to convert the shapefile's CRS to WGS 84 (EPSG:4326)
    transformer = pyproj.Transformer.from_crs(crs_proj4, '+proj=longlat +datum=WGS84')
    gdf['centroid'] = gdf['geometry'].centroid

    # Transform centroids to standard coordinates (longitude, latitude)
    gdf['longitude'], gdf['latitude'] = zip(*gdf['centroid'].apply(lambda geom: transformer.transform(geom.x, geom.y)))

    # Drop the 'centroid' column if you don't need it
    gdf.drop(columns=['centroid'], inplace=True)

    #Area
    gdf['area'] = gdf['geometry'].area

    gdf['n_paneles'] = (gdf['area'] * area_disp) / panel_size #Asumiendo paneles de 2x2

    gdf['horas_acum'] = gdf.apply(lambda row: sunlight_hours(row['latitude'], row['longitude'], start, end), axis=1)

    delta = end - start

    gdf['ener_anual'] = panel_pot * gdf['horas_acum'] * factor_dim * gdf['n_paneles']
    gdf['ener_dia'] = gdf['ener_anual'] / (delta.days + 1)

    return gdf
