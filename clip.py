import os

def clip_raster_by_vector(input_raster, input_vector, output_raster, overwrite=False):
    if overwrite:
        if os.path.isfile(output_raster):
            os.remove(output_raster)

    if not os.path.isfile(input_raster):
        print ("File doesn't exists", input_raster)
        return None
    else:
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

        feedback = qgis.core.QgsProcessingFeedback()
        alg_name = 'gdal:cliprasterbymasklayer'
        print(processing.algorithmHelp(alg_name))
        result = processing.run(alg_name, params, feedback=feedback)
        return result


input_raster = r"C:\programacion\trabajofinal\pruebas\b3.tif"
output_raster = r"C:\programacion\trabajofinal\pruebas\b3_clip.tif"
input_vector = r"C:\programacion\trabajofinal\cuadrado\cuadrado2.shp"
result = clip_raster_by_vector(input_raster, input_vector, output_raster, overwrite=True)
print('result =', result)

capacortada = QgsRasterLayer(r"C:\programacion\trabajofinal\pruebas\b3_clip.tif")

QgsProject.instance().addMapLayer(capacortada)