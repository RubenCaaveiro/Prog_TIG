layerFields = QgsFields()
layerFields.append(QgsField('ID', QVariant.Int))

fn = r'C:\programacion\trabajofinal\cuadrado\cuadrado2.shp'
writer = QgsVectorFileWriter(fn, 'UTF-8', layerFields,\
QgsWkbTypes.Polygon,\
QgsCoordinateReferenceSystem('EPSG:32631'),\
'ESRI Shapefile')

#------------------
point1 = QgsPointXY(425231,4676488)
point2 = QgsPointXY(509722,4676488)
point3 = QgsPointXY(425231,4598087)
point4 = QgsPointXY(509722,4598087)
points = [point3,point4,point2,point1]



#-----------------
feat = QgsFeature()
feat.setGeometry(QgsGeometry.fromPolygonXY([points]))
feat.setAttributes([1])
writer.addFeature(feat)

layer = iface.addVectorLayer(fn, '', 'ogr')

del(writer)
