

fn = ('C:/programacion/trabajofinal/pruebas/NDVI4.tif')



#----------------



fi = QFileInfo(fn)
fname =fi.baseName()

rlayer = iface.addRasterLayer(fn, fname)

stats = rlayer.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
min = stats.minimumValue
max = stats.maximumValue

fnc = QgsColorRampShader()
fnc.setColorRampType(QgsColorRampShader.Interpolated)

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
#lista de colores extraida de: https://www.youtube.com/watch?v=pGW0Lyo6PAY

fnc.setColorRampItemList(i)

shader = QgsRasterShader()

shader.setRasterShaderFunction(fnc)

renderer = QgsSingleBandPseudoColorRenderer(rlayer.dataProvider(), 1, shader)
rlayer.setRenderer(renderer)



