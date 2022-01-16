layerFields = QgsFields()
layerFields.append(QgsField('ID', QVariant.Int))
layerFields.append(QgsField('Value', QVariant.Double))
layerFields.append(QgsField('Name', QVariant.String))

fn = r'C:\programacion\trabajofinal\cuadrado\cuadrado2.shp'
writer = QgsVectorFileWriter(fn, 'UTF-8', layerFields,\
QgsWkbTypes.Polygon,\
QgsCoordinateReferenceSystem('EPSG:26912'),\
'ESRI Shapefile')

#------------------
point1 = QgsPointXY(50,50)
point2 = QgsPointXY(100,150)
point3 = QgsPointXY(50,150)
point4 = QgsPointXY(100, 50)
points = [point1,point3,point2,point4]
# or points = [QgsPoint(50,50),QgsPoint(50,150),QgsPoint(100,150),QgsPoint(100,50)] 


#-----------------
feat = QgsFeature()
feat.setGeometry(QgsGeometry.fromPolygonXY([points]))
feat.setAttributes([1, 1.1, 'cuadrado'])
writer.addFeature(feat)

layer = iface.addVectorLayer(fn, '', 'ogr')

del(writer)