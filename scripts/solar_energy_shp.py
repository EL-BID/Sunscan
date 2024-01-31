import pandas as pd
import numpy as np
import datetime
import time
from astral import LocationInfo
from astral import sun
import pytz
import geopandas as gpd
import pyproj


def sunlight_hours(lat, lon, start, end, excel_out):
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
            
            data['sunrise'].append(s["sunrise"].time().strftime('%H:%M:%S'))
            data['sunset'].append(s["sunset"].time().strftime('%H:%M:%S'))
            data['noon'].append(s["noon"].time().strftime('%H:%M:%S'))
        except ValueError as e:
            print(f"No se pudo calcular el atardecer para {this_date}: {e}")
            continue  # Continuar con la próxima fecha si ocurre un error

    df = pd.DataFrame(data)
    df['noon'] = pd.to_datetime(df['noon'], format='%H:%M:%S').dt.time
    df['sunrise'] = pd.to_datetime(df['sunrise'], format='%H:%M:%S').dt.time
    df['sunset'] = pd.to_datetime(df['sunset'], format='%H:%M:%S').dt.time

    df['dif_sec'] = (pd.to_timedelta(df['noon'].astype(str)) -
                                  pd.to_timedelta(df['sunrise'].astype(str))).dt.total_seconds()
    df['sunlight_hours'] = (df['dif_sec'] / 60) / 60
    sunlight_hours_sum = np.sum((df['dif_sec'] / 60) / 60)
    df.to_excel(excel_out, index=False)
    return sunlight_hours_sum


def solar_energy_shp(shp_in,shp_out,start,end,panel_size,area_disp,factor_dim,panel_pot,excel_out):
  gdf = gpd.read_file(shp_in)
  # Get the CRS (coordinate reference system) of the shapefile
  crs = gdf.crs
  # Convert the CRS to a Proj4 string
  crs_proj4 = pyproj.CRS(crs).to_proj4()

  # Create a Transformer to convert the shapefile's CRS to WGS 84 (EPSG:4326)
  transformer = pyproj.Transformer.from_crs(crs_proj4, "+proj=longlat +datum=WGS84")
  gdf['centroid'] = gdf['geometry'].centroid

  # Transform centroids to standard coordinates (longitude, latitude)
  gdf['longitude'], gdf['latitude'] = zip(*gdf['centroid'].apply(lambda geom: transformer.transform(geom.x, geom.y)))

  # Drop the 'centroid' column if you don't need it
  gdf.drop(columns=['centroid'], inplace=True)

  #Area
  gdf['area'] = gdf['geometry'].area

  gdf['n_paneles'] = (gdf['area']*area_disp)/panel_size#Asumiendo paneles de 2x2

  gdf['horas_acum'] = gdf.apply(lambda row: sunlight_hours(row['latitude'], row['longitude'],start,end), axis=1)

  delta=end-start
  
  gdf['Energia_acum'] = panel_pot*gdf['horas_acum']*factor_dim*gdf['n_paneles']
  gdf['Energia_diaria'] = gdf['Energia_acum']/(delta.days+1)
  gdf['Energia_anual']= gdf['Energia_diaria']*365

  gdf.to_file(shp_out)
  gdf.to_excel(excel_out)
