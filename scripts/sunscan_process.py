import os,glob, sys
from samgeo.text_sam import LangSAM
import leafmap
import city_from_coord as cfc
import ultimo_archivo as ua
import datetime
import shutil

def sunscan_process(west,south,east,north,z,reults_fol):
    
    #[-73.2316, 9.587, -73.2309, 9.5875]
    #[west,south,east,north]

    bb=[west,south,east,north]
    lat,lon=((north+south)/2),((east+west)/2)#Centroid
    str_bb=str(north)+'_'+str(south)+'_'+str(east)+'_'+str(west)

    #Quitemos esta parte del nombre de las ciudades
    city=cfc.city_from_coord(latitude=lat, longitude=lon)
    city_name=str(city).replace("'",'').replace('(','').replace(')','').replace(', ','_').replace(' ','').replace('/','')
    city_name=city_name+'_'+str_bb

    if not os.path.exists(results_fol):
            os.makedirs(results_fol)

    image=os.path.join(results_fol,city_name+'_{}z.tif'.format(str(z)))
    leafmap.tms_to_geotiff(image, bb, zoom=z,
                       source='Satellite')
    
    palabra_clave='z.tif'
    img_in=ua.ultimo_archivo(results_fol, '.tif')
    
    sam = LangSAM()
    text_prompt='houses'
    sam.predict(img_in, text_prompt, box_threshold=0.24, text_threshold=0.24)

    #Crear el raster
    tif_out=img_in.replace('.tif','_{}.tif'.format(text_prompt))
    sam.show_anns(  cmap='Greys_r',  add_boxes=False,  alpha=1,
      title='Segmentación  de tejados usando SAM', blend=False,  output=tif_out)

    #Crear el shp
    shp_out=tif_out.replace('.tif','.shp')
    sam.raster_to_vector(tif_out,shp_out)
