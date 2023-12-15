# Sunscan
<div id='insignias' />
<a target="_blank" href="https://colab.research.google.com/github/EL-BID/Sunscan/blob/main/notebook/SunScan.ipynb">
  
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

***

SunScan es un proyecto que usa código abierto para ayudar a estimar la energía solar potencial sobre tejados usando imágenes satelitales y el modelo SAM (Segment anything by Meta)

<div id='índice' />

## Índice

* [Descripción del proyecto](#descripción-del-proyecto)

* [Guía de instalación](#configuracion-ambiente)

* [Guía de usuario](#demostracion-del-proyecto)

* [Licencia](#licencia)

* [Limitación de responsabilidades](#limitación-de-responsabilidades)

***
<div id='descripción-del-proyecto' />

## Descripción del Proyecto

SunScan es una herramienta diseñada para utilizar el modelo SAM (Segment Anything by Meta) con el propósito de detectar y segmentar tejados en imágenes satelitales. El enfoque principal es proporcionar una solución eficiente para la identificación automática de áreas de tejados, permitiendo así la estimación de la energía potencial disponible para la instalación de sistemas solares. Este proyecto aborda los desafíos asociados con la detección precisa de tejados en datos satelitales, mejorando la planificación y la implementación de proyectos de energía renovable.

### ***1 : Identificación y segmentación de los tejados***

Este paso implica el uso del modelo SAM (Segment Anything by Meta) para identificar y segmentar las áreas que corresponden a los tejados en una imagen satelital. El modelo se entrena para reconocer patrones y características que representan tejados, y luego aplica este conocimiento para segmentar las áreas relevantes en la imagen.

### ***2 : Área disponible***

Una vez que se han identificado y segmentado los tejados, se calcula el área disponible para la instalación de paneles solares. Este cálculo implica medir el área total de cada tejado segmentado. Dependiendo de la geometría del tejado, este proceso puede variar, pero comúnmente se utiliza la superficie plana proyectada del tejado.

### ***3 : Horas de sol***

Para estimar la energía potencial de cada tejado, es crucial conocer las horas de sol anuales en la ubicación específica de los tejados. Este dato se obtiene utilizando información climática y geográfica de la ubicación. Puedes integrar servicios o bases de datos de información climática para obtener este dato.

### ***4 : Enérgia solar por tejado***

Con el área disponible para paneles solares y las horas de sol anuales, se puede calcular la energía potencial de cada tejado. La fórmula general es:

Energía Potencial=Area Disponible×Horas de Sol Anuales×Rendimiento del Panel Solar×Eficiencia del Sistema

Esta fórmula tiene en cuenta factores como la eficiencia del panel solar y del sistema de conversión de energía.

### ***5 : Exportar los Resultados***

Para facilitar la visualización y análisis geoespacial, los resultados pueden ser exportados como un Shapefile. Un Shapefile es un formato de archivo comúnmente utilizado en SIG (Sistemas de Información Geográfica) que almacena información geoespacial. Puedes exportar los límites de los tejados y su información asociada a un Shapefile utilizando herramientas y bibliotecas como Geopandas.


## Guía de instalación

Instalación
Clonar el Repositorio
```bat
git clone https://github.com/tuusuario/SolarSatelliteAnalyzer.git
cd SolarSatelliteAnalyzer
```

Instalación de Dependencias:
```bat
pip install -r requirements.txt
```
