
# Sunscan
<div id='insignias' />
<a target="_blank" href="https://colab.research.google.com/github/EL-BID/Sunscan/blob/main/notebook/SunScan_new.ipynb">
  
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

***

SunScan es un proyecto que usa código abierto para ayudar a estimar la energía solar potencial sobre tejados usando imágenes satelitales y el modelo SAM (Segment anything by Meta)

<div id='índice' />

## Índice

* [Descripción del proyecto](#descripción-del-proyecto)

* [Modelo](#Modelo)

* [Guía de instalación](#configuracion-ambiente)

* [Guía de usuario](#demostracion-del-proyecto)

* [Licencia](#licencia)

***
<div id='descripción-del-proyecto' />

## Descripción del proyecto

El repositorio de GitHub SunScan se basa en el uso de notebooks de Google Colab. Este enfoque simplifica notablemente el proceso de interactuar con el modelo, ya que elimina la necesidad de un entorno de desarrollo local, ofrece una metodología única para el uso de sus modelos. 

Una característica de SunScan es su uso de la herramienta tms2geotif para acceder a imágenes de Google Satellite. Esto permite a los usuarios seleccionar áreas específicas para análisis mediante la utilización de map tiles de Google Satellite. Estos tiles proporcionan datos detallados y actualizados, lo que es crucial para un análisis preciso y relevante.

El proceso comienza con el usuario eligiendo un área de interés en Google Satellite usando leafmap. A través de Google Colab, SunScan utiliza tms2geotif para convertir estas selecciones en imágenes GeoTIFF. Estas imágenes son luego accesibles para el análisis, proporcionando una base sólida para correr el modelo.

Este método no solo hace que el análisis sea más accesible y también más personalizable. Los usuarios pueden enfocarse en regiones específicas que sean de su interés, lo que permite una gran flexibilidad en la investigación y el análisis de datos. Esta característica es particularmente útil para proyectos que requieren un enfoque geográfico específico

<div id='Modelo' />

## Modelo

SunScan es una herramienta diseñada para utilizar el modelo SAM (Segment Anything by Meta) con el propósito de detectar y segmentar tejados en imágenes satelitales. El enfoque principal es proporcionar una solución eficiente para la identificación automática de áreas de tejados, permitiendo así la estimación de la energía potencial disponible para la instalación de sistemas solares. Este proyecto aborda los desafíos asociados con la detección precisa de tejados en datos satelitales, mejorando la planificación y la implementación de proyectos de energía renovable.

### ***1 : Identificación y segmentación de los tejados***

Este paso implica el uso del modelo SAM (Segment Anything by Meta) para identificar y segmentar las áreas que corresponden a los tejados en una imagen satelital. El modelo se entrena para reconocer patrones y características que representan tejados, y luego aplica este conocimiento para segmentar las áreas relevantes en la imagen. A continuación se dar una corta descripción de cómo funciona SAM:

***Arquitectura y Aprendizaje Profundo:*** SAM incorpora una arquitectura de red neuronal profunda, generalmente basada en modelos convolucionales (CNNs) que son efectivos para el análisis de imágenes. Estas redes se entrenan para reconocer y segmentar patrones complejos en los datos visuales. La arquitectura de SAM está diseñada para ser adaptable, permitiendo que se ajuste a diferentes tipos de datos y tareas de segmentación. Utiliza capas convolucionales para extraer características de bajo nivel (como bordes y texturas) y capas más profundas para entender características de alto nivel (como formas y objetos específicos). Este enfoque jerárquico permite al modelo aprender una representación rica y detallada de los datos de entrada.

***Proceso de Segmentación y Meta-Aprendizaje:*** Lo que distingue a SAM es su capacidad para realizar meta-aprendizaje, es decir, aprender a aprender. En lugar de simplemente entrenarse en un conjunto fijo de imágenes, SAM utiliza técnicas de meta-aprendizaje para adaptarse rápidamente a nuevos tipos de datos o tareas de segmentación con una mínima cantidad de ejemplos de entrenamiento. Esto se logra a través de un proceso iterativo donde el modelo ajusta sus parámetros internos no solo para realizar bien en un conjunto de datos específico, sino también para ser capaz de transferir ese aprendizaje a nuevas tareas de manera eficiente. En la práctica, esto significa que SAM puede ser entrenado en un conjunto de imágenes y luego rápidamente ajustado para segmentar con precisión en un conjunto de datos completamente diferente.

***Aplicaciones y Optimización:*** En la segmentación de imágenes, como en el caso de los tejados en imágenes satelitales, SAM puede distinguir con precisión estas estructuras de otros elementos en la imagen. Esto se logra a través de la segmentación semántica, donde cada píxel de la imagen se clasifica en categorías relevantes (por ejemplo, tejado, suelo, vegetación). Para optimizar su rendimiento, SAM puede ser equipado con técnicas adicionales como la ampliación de datos (data augmentation), el aprendizaje de transferencia y la regularización, lo que mejora su capacidad de generalización y reduce el sobreajuste. Esta flexibilidad y adaptabilidad hacen de SAM una herramienta poderosa para aplicaciones que requieren una segmentación precisa y detallada en diversos dominios, desde el análisis de imágenes médicas hasta la vigilancia por satélite.



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

El proyecto contiene la siguiente estructura de carpetas:
~~~
Sunscan:
    |--- notebook
    |--- scripts
~~~

- notebook : contiene el notebook de ejecución en google colab
- scripts : contiene las funciones de python que dan soporte al proyecto.

Para ejecutar el notebook se pueden seguir los pasos que están ahí mismo descritas.

## Licencia 

Este proyecto utiliza el modelo "Segment Anything" de Meta para la segmentación de tejados. Este modelo se distribuye bajo la licencia Apache-2.0. Se debe dar crédito apropiado a Meta por el desarrollo del modelo, y cualquier distribución del software modificado debe mantener la misma licencia. Más información sobre la licencia se puede encontrar en el repositorio oficial de Segment Anything.

Este proyecto ha sido financiado por el BID. Ver la siguiente licencia [LICENCIA](https://github.com/EL-BID/Sunscan/blob/main/LICENSE.md)





## Acknowledgments / Reconocimientos

**Copyright © [2025]. Inter-American Development Bank ("IDB"). Authorized Use.**  
The procedures and results obtained based on the execution of this software are those programmed by the developers and do not necessarily reflect the views of the IDB, its Board of Executive Directors or the countries it represents.

**Copyright © [2025]. Banco Interamericano de Desarrollo ("BID"). Uso Autorizado.**  
Los procedimientos y resultados obtenidos con la ejecución de este software son los programados por los desarrolladores y no reflejan necesariamente las opiniones del BID, su Directorio Ejecutivo ni los países que representa.

### Support and Usage Documentation / Documentación de Soporte y Uso

**Copyright © [2025]. Inter-American Development Bank ("IDB").** The Support and Usage Documentation is licensed under the Creative Commons License CC-BY 4.0 license. The opinions expressed in the Support and Usage Documentation are those of its authors and do not necessarily reflect the opinions of the IDB, its Board of Executive Directors, or the countries it represents.

**Copyright © [2025]. Banco Interamericano de Desarrollo (BID).** La Documentación de Soporte y Uso está licenciada bajo la licencia Creative Commons CC-BY 4.0. Las opiniones expresadas en la Documentación de Soporte y Uso son las de sus autores y no reflejan necesariamente las opiniones del BID, su Directorio Ejecutivo ni los países que representa.

### AI-Powered Services Disclaimer / Exención de responsabilidad por Servicios Impulsados por IA

The Software may include features which use, are powered by, or are an artificial intelligence system (“AI-Powered Services”), and as a result, the services provided via the Software may not be completely error-free or up to date. Additionally, the User acknowledges that due to the incorporation of AI-Powered Services in the Software, the Software may not dynamically (in “real time”) retrieve information and that, consequently, the output provided to the User may not account for events, updates, or other facts that have occurred or become available after the Software was trained. Accordingly, the User acknowledges that the use of the Software, and that any actions taken or reliance on such products, are at the User’s own risk, and the User acknowledges that the User must independently verify any information provided by the Software.

El Software puede incluir funciones que utilizan, están impulsadas por o son un sistema de inteligencia artificial (“Servicios Impulsados por IA”) y, como resultado, los servicios proporcionados a través del Software pueden no estar completamente libres de errores ni actualizados. Además, el Usuario reconoce que, debido a la incorporación de Servicios Impulsados por IA en el Software, este puede no recuperar información dinámicamente (en “tiempo real”) y que, en consecuencia, la información proporcionada al Usuario puede no reflejar eventos, actualizaciones u otros hechos que hayan ocurrido o estén disponibles después del entrenamiento del Software. En consecuencia, el Usuario reconoce que el uso del Software, y que cualquier acción realizada o la confianza depositada en dichos productos, se realiza bajo su propio riesgo, y reconoce que debe verificar de forma independiente cualquier información proporcionada por el Software.
