#Nombre archivo: __main__.py
#Autores: Waldemar Taras Tresniowski Ujaldón y Rubén Caaveiro Barro
#Fecha: 18-1-2022
#Descripción: Se ejecuta la funcion 'main' que ejecuta todas las funciones definidas. Tras ejecutar las 4 funciones, se limpia el directorio de salida
#para obtener las nuevas ccapas creadas y eliminar archivos anteriores. Tras esto obtenemos una imagen NDVI recortada al area de estudio mediante un poligono
#que se crea en una capa vectorial. Por último se introduce la simbología definida para NDVI en la capa final. En la consola de QGIS se añaden las cuatro capas 
#creadas or orden. Y en la consola de resultdos de PyQGIS se imprimen los mensajes de ejecución y resultados del proceso.


import os
import glob

from qgis.core import *
from qgis.analysis import *
from qgis.PyQt.QtCore import *

def main():
    print ("Main started!")
    
    parent_path = 'C:/trabajofinal_final_2022_01_18/trabajofinal_final/' #ruta a la carpeta de proyecto
    
    clear(parent_path) #limpia la ejecucion anterior para que no haya problemas durante la ejecucion actual
    
    #ejecutamos los scripts secuencialmente
    if NDVIexecute(parent_path): #comprueba que NDVImod2 se ejecuto correctamente antes de continuar
        if crearpoligonoexecute(parent_path): #comprueba que crearpoligono se ejecuto correctamente antes de continuar
            if clipexecute(parent_path): #comprueba que clipsinfuncion se ejecuto correctamente antes de continuar
                if simbolizarNDVIexecute(parent_path): #comprueba que simbolizarRasterbien se ejecuto correctamente antes de continuar
                    print ("Main executed succesfully!")
                else:
                    print ("Error executing simbolizarRasterbien!")
            else:
                print ("Error executing clipsinfuncion!")
        else:
            print ("Error executing crearpoligono!")
    else:
        print ("Error executing NDVImod2!")
    


# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _




def NDVIexecute(parent_path):
    print ('NDVImod2 started!')
    
    #cargar las capas de entrada y salida
    red = QgsRasterLayer(os.path.join(parent_path, './input/b3.tif'))
    nir = QgsRasterLayer(os.path.join(parent_path, './input/b4.tif'))
    output = os.path.join(parent_path, './output/ndvi.tif')
    entries = []

    #referenciar las capa
    ras = QgsRasterCalculatorEntry()
    ras.ref = 'ras@1'
    ras.raster = red
    ras.bandNumber = 1
    entries.append(ras)

    ras = QgsRasterCalculatorEntry()
    ras.ref = 'ras@2'
    ras.raster = nir
    ras.bandNumber = 1
    entries.append(ras)

    #realizar el cálculo mediante el comando QgsRasterCalculator
    calc = QgsRasterCalculator('(ras@2 - ras@1)/(ras@2 + ras@1)', output, 'GTiff',\
    red.extent(), red.width(), red.height(), entries)
    calc.processCalculation()

    #mostrar la capa en la interfaz de QGIS
    ndvi = QgsRasterLayer(output)

    QgsProject.instance().addMapLayer(ndvi)

    print ('NDVI executed succesfully!')
        
    return True #devuelve true si todo esta correcto
    

# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


def crearpoligonoexecute(parent_path):
    print ('crearpoligono started!')
    
    dircuadr = os.path.join(parent_path,'./output/cuadrado.shp')

    #crear la capa en memoria
    mem_layer = QgsVectorLayer("Polygon?crs=EPSG:32631&index=yes", "cuadrado", "memory")
    provider = mem_layer.dataProvider()
    
    #definir atributos de la capa
    provider.addAttributes([QgsField('ID', QVariant.Int)])
    mem_layer.updateFields() 

    #introducir los vértices del polígono
    point1 = QgsPointXY(425231,4598087)
    point2 = QgsPointXY(509722,4598087)
    point3 = QgsPointXY(509722,4676488)
    point4 = QgsPointXY(425231,4676488)
    points = [point1,point2,point3,point4]

    #añadir a la capa el atributo y la geometría
    feature = QgsFeature()
    feature.setGeometry(QgsGeometry.fromPolygonXY([points]))
    feature.setAttributes([1])
    provider.addFeatures([feature])

    #escribir la capa en el disco
    QgsVectorFileWriter.writeAsVectorFormat(mem_layer, dircuadr, 'utf-8', 
                                            QgsCoordinateReferenceSystem('EPSG:32631'), "ESRI Shapefile")
    
    #Añadir la capa del polígono a la interfaz
    layer = iface.addVectorLayer(dircuadr, '', 'ogr')
        
    print ('crearpoligono executed succesfully!')
    
    return True #devuelve true si todo esta correcto

# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


def clipexecute(parent_path):
    print ('clip started!')
    
    #difinimos los directorios con las capas
    input_raster = os.path.join(parent_path, './output/ndvi.tif')
    output_raster = os.path.join(parent_path, './output/ndvi_clip.tif')
    input_vector = os.path.join(parent_path, './output/cuadrado.shp')

    #introducimos los parámetros, el feedback y el nombre del algoritmo
    feedback = QgsProcessingFeedback()
    alg_name = 'gdal:cliprasterbymasklayer'

    params = {'INPUT': input_raster,
                    'MASK': input_vector,
                    'NODATA': 255.0,
                    'ALPHA_BAND': False,
                    'CROP_TO_CUTLINE': True,
                    'KEEP_RESOLUTION': True,
                    'OPTIONS': 'COMPRESS=LZW',
                    'DATA_TYPE': 0,  # Byte
                    'OUTPUT': output_raster,
                    }

    #parametros extraidos de https://gis.stackexchange.com/questions/291301/
    #how-to-call-clip-raster-by-mask-layer-tool-using-qgis-console-gdalclipraste

    result = processing.run(alg_name, params, feedback=feedback)
    capacortada = QgsRasterLayer(os.path.join(parent_path, './output/ndvi_clip.tif'))

    #se añade la capa a la interfaz de QGIS
    QgsProject.instance().addMapLayer(capacortada)
    
    print ('clip executed succesfully!')
    
    return True #devuelve true si todo esta correcto

    
# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _



def simbolizarNDVIexecute(parent_path):
    print ('simbolizarNDVI started!')
    
    #directorio
    fn = (os.path.join(parent_path, './output/ndvi_clip.tif'))
        
    fi = QFileInfo(fn)
    fname = fi.baseName()

    rlayer = iface.addRasterLayer(fn, fname)

    stats = rlayer.dataProvider().bandStatistics(1, QgsRasterBandStats.All)

    fnc = QgsColorRampShader()
    fnc.setColorRampType(QgsColorRampShader.Interpolated)

    #crear una lista e introducirle la rampa de colores
    i= []
    qri = QgsColorRampShader.ColorRampItem
    i.append(qri(0, QColor(0,0,0,0), 'NODATA'))
    i.append(qri(0.1, QColor(120,69,25,255),'Biomasa ínfima'))
    i.append(qri(0.2, QColor(255,178,74,255), 'Biomasa muy baja'))
    i.append(qri(0.3, QColor(255, 237, 166, 255), 'Baja biomsa'))
    i.append(qri(0.5, QColor(173, 232, 94, 255), 'Biomasa moderda'))
    i.append(qri(0.7, QColor(135,181,64,255), 'Biomasa alta'))
    i.append(qri(0.8, QColor(3,156,0,255), 'Biomasa muy alta'))
    i.append(qri(0.9, QColor(1,100,0,255), 'Máxima biomasa'))
    #lista de colores extraida de: https://www.youtube.com/watch?v=pGW0Lyo6PAY

    fnc.setColorRampItemList(i)

    shader = QgsRasterShader()

    shader.setRasterShaderFunction(fnc)

    renderer = QgsSingleBandPseudoColorRenderer(rlayer.dataProvider(), 1, shader)
    rlayer.setRenderer(renderer)
        
    print ('simbolizarNDVI executed succesfully!')
    
    return True #devuelve true si todo esta correcto

# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    

    
#limpia el entorno antes de la siguiente ejecucion
def clear(parent_path):
    print ("Cleaning environment...")
    
    QgsProject.instance().removeAllMapLayers() #borra todas las capas del proyecto actual
    
    outputDir = os.path.abspath(os.path.join(parent_path, '.\output')) #recupera la ruta a la carpeta output
    filelist = glob.glob(os.path.join(outputDir,'*')) #recupera la lista de ficheros dentro de la carpeta output
    for file in filelist: #lista los ficheros de la carpeta output
        os.remove(file) #borra el fichero listado
        

main()
