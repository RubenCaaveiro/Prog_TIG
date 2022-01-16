import os

input_raster = r"C:\programacion\trabajofinal\pruebas\b3.tif"
output_raster = r"C:\programacion\trabajofinal\pruebas\b3_clip2.tif"
input_vector = r"C:\programacion\trabajofinal\cuadrado\cuadrado2.shp"

feedback = qgis.core.QgsProcessingFeedback()
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

#----------------

result = processing.run(alg_name, params, feedback=feedback)
capacortada = QgsRasterLayer(r"C:\programacion\trabajofinal\pruebas\b3_clip2.tif")

QgsProject.instance().addMapLayer(capacortada)