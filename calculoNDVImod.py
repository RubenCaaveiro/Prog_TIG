from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qgis.analysis import *

#cargamos la imagen
rasterName = "farm"
raster = QgsRasterLayer('C:/programacion/trabajofinal/farm-field.tif', rasterName)

#creamos las entradas para la calculadora raster
ir = QgsRasterCalculatorEntry()
r = QgsRasterCalculatorEntry()

#asignamos las capas raster como los componentes raster de cada entrada de la calculadora
ir.raster = raster
r.raster = raster

#seleccionamos la banda apropiada para cada entrada
ir.bandNumber = 2
r.bandNumber = 1

#asignamos un numero de referencia para cada entrada mediante el convencionalismo de QGIS
ir.ref = rasterName + "@2"
r.ref = rasterName + "@1"

#añadimos la expresión del calculo
references = (ir.ref, r.ref, ir.ref, r.ref)
exp = "1.0 * (%s - %s)/1.0 + (%s + %s)" % references 
output = "C:/programacion/trabajofinal/NDVI.tif"

#variables para la calculadora
e = raster.extent()
w = raster.width()
h = raster.height()
entries=[ir,r]

#creamos el NDVI usando la expresion anterior
ndvi = QgsRasterCalculator(exp, output, "GTifff", e,w,h, entries)
ndvi.processCalculation()

#cargamos el raster ndvi calculado 
lyr = QgsRasterLayer(output, "NDVI")

#mejoramos la visión del raster medante un algoritmo de mejora del contraste
algorithm = QgsContrastEnhancement.StretchToMinimumMaximum
limits = QgsRaster.ContrastEnhancementMinMax
lyr.setContrastEnhancement(algorithm, limits)

#creamos una rampa de colores para colorear el NDVI
s = QgsRasterShader()
c = QgsRasterRampShader()
c.setColorRampType(Qgs.ColorRampShader.INTERPOLATED)

#añadimos la entrada para cada color 
i= []
qri = QgsColorRampShader.ColorRampItem
i.append(qri(0, QColor(0,0,0,0), 'NODATA'))
i.append(qri(214, QColor(120,69,25,255),'Lowest Biomass'))
i.append(qri(236, QColor(255,178,74,255), 'Lower Biomass'))
i.append(qri(258, QColor(255, 237, 166, 255), 'Low Biomass'))
i.append(qri(280, QColor(173, 232, 94, 255), 'Moderate Biomass'))
i.append(qri(303, QColor(135,181,64,255), 'High Biomass'))
i.append(qri(325, QColor(3,156,0,255), 'Higher Biomass'))
i.append(qri(400, QColor(1,100,0,255), 'Highest Biomass'))

#añadimos las entradas para el shader y los aplicamos
c.setColorRampItemList(i) #le añadimos la lista con los colores a QgsRasterRampshade
s.setRasterShaderFunction(c)
ps = QgsSingleBandPseudoColorRenderer(lyr.dataProvider(),1,s)
lyr.setRenderer(ps)

#cargamos la capa resultado en el directorio de QGIS
QgsMapLayerRegistry.instance().addMapLayer(lyr)

