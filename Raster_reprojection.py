import tensorflow as tf
from osgeo import gdal
import numpy as np

def raster_reprojection(source_data_placeholder, target_data_placeholder, target_projection, target_geotransform):
    # Определяем размеры исходного и целевого растров
    source_rows = source_data_placeholder.shape[0]
    source_cols = source_data_placeholder.shape[1]
    target_rows = target_data_placeholder.shape[0]
    target_cols = target_data_placeholder.shape[1]

    # Создаем новый растр для репроецированных данных
    target_dataset = gdal.GetDriverByName('MEM').Create('', target_cols, target_rows, 1, gdal.GDT_Float32)
    target_dataset.SetProjection(target_projection)
    target_dataset.SetGeoTransform(target_geotransform)

    # Преобразуем тензоры TensorFlow в массивы NumPy
    source_data = source_data_placeholder.numpy()
    target_data = target_data_placeholder.numpy()

    # Записываем данные в исходный и целевой растр
    source_dataset.GetRasterBand(1).WriteArray(source_data)
    target_dataset.GetRasterBand(1).WriteArray(target_data)

    # Выполняем растровую репроекцию
    gdal.ReprojectImage(source_dataset, target_dataset, source_projection, target_projection, gdal.GRA_Bilinear)

    # Читаем репроецированные данные из целевого растра
    target_data = target_dataset.GetRasterBand(1).ReadAsArray()

    # Преобразуем репроецированные данные обратно в тензор TensorFlow
    target_data_tensor = tf.convert_to_tensor(target_data)

    return target_data_tensor

# Открываем исходный файл .TIFF с помощью GDAL
source_dataset = gdal.Open('input.tif', gdal.GA_ReadOnly)

# Получаем информацию об исходном растре
source_projection = source_dataset.GetProjection()
source_geotransform = source_dataset.GetGeoTransform()
source_data = source_dataset.ReadAsArray()

# Закрываем исходный датасет GDAL
source_dataset = None

# Определяем размеры исходного растра
source_rows, source_cols = source_data.shape
source_bands = 1

# Определяем размеры репроецированного растра
target_rows = 100
target_cols = 100

# Определяем новую геометрию и преобразование координат для репроецированного растра
target_geotransform = (30.0, 0.01, 0, -20.0, 0, -0.01)
target_projection = 'EPSG:4326'

# Создаем новый растровый массив для репроецированного растра
target_data = np.zeros((target_rows, target_cols, source_bands), dtype=np.float32)

# Создаем TensorFlow граф для растровой репроекции
tf.compat.v1.disable_eager_execution()

source_data_placeholder = tf.compat.v1.placeholder(tf.float32, shape=(source_rows, source_cols, source_bands))
target_data_placeholder = tf.compat.v1.placeholder(tf.float32, shape=(target_rows, target_cols, source_bands))
transformed_data = raster_reprojection(source_data_placeholder, target_data_placeholder, target_projection, target_geotransform)

with tf.compat.v1.Session() as sess:
    transformed_data = sess.run(transformed_data, feed_dict={
        source_data_placeholder: source_data,
        target_data_placeholder: target_data
    })

# Создаем новый файл .TIFF для сохранения репроецированного растра
driver = gdal.GetDriverByName('GTiff')
target_dataset = driver.Create('output.tif', target_cols, target_rows, source_bands, gdal.GDT_Float32)

# Устанавливаем проекцию и геометрию репроецированного растра
target_dataset.SetProjection(target_projection)
target_dataset.SetGeoTransform(target_geotransform)

# Записываем репроецированный растр в файл с использованием GDAL
for band_num in range(source_bands):
    band = target_dataset.GetRasterBand(band_num + 1)
    band.WriteArray(transformed_data[:, :, band_num])

# Закрываем датасет GDAL
target_dataset = None
