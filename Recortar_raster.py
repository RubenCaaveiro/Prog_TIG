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
                  'OPTIONS': '-of GTiff -co COMPRESS=LZW',
                  'DATA_TYPE': 0,  # Byte6
                  'OUTPUT': output_raster,
                  }

        feedback = qgis.core.QgsProcessingFeedback()
        alg_name = 'gdal:cliprasterbymasklayer'
        print(processing.algorithmHelp(alg_name))
        result = processing.run(alg_name, params, feedback=feedback)
        return result


input_raster = r"C:/SIG_EXPERIMENTS/Imagen_SAT_SIngapour/sing_B4.TIF"
output_raster = r"C:\SIG_EXPERIMENTS\PRUEBAS_PROG_ndvi\B_7.tif"
input_vector = r"C:\SIG_EXPERIMENTS\PRUEBAS_PROG_ndvi\ndvi_shp.shp"
result = clip_raster_by_vector(input_raster, input_vector, output_raster, overwrite=True)
print('result =', result)

result = QgsRasterLayer(output)
QgsProject.instance().addMapLayer(result)