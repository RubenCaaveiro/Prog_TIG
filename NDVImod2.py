lyr1 = QgsRasterLayer('C:/programacion/trabajofinal/pruebas/b3.tif')
lyr2 = QgsRasterLayer('C:/programacion/trabajofinal/pruebas/b4.tif')
output = 'C:/programacion/trabajofinal/pruebas/LT05_L1TP_197031_19880801_20180216_01_T1_B1.tif)'
entries = []

ras = QgsRasterCalculatorEntry()
ras.ref = 'ras@1'
ras.raster = lyr1
ras.bandNumber = 1
entries.append(ras)

ras = QgsRasterCalculatorEntry()
ras.ref = 'ras@2'
ras.raster = lyr2
ras.bandNumber = 1
entries.append(ras)

calc = QgsRasterCalculator('(ras@2 + ras@1)/(ras@2 - ras@1)', output, 'GTiff',\
lyr1.extent(),lyr1.width(), lyr1.height(), entries)
calc.processCalculation()

lyr3 = QgsRasterLayer(output)

QgsProject.instance().addMapLayer(lyr3)
