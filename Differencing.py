import tensorflow as tf
from osgeo import gdal
import numpy as np

def tiff_difference(input_path_1, input_path_2, output_path):
    # Открываем исходные файлы TIFF с помощью GDAL
    dataset_1 = gdal.Open(input_path_1)
    dataset_2 = gdal.Open(input_path_2)

    # Получаем информацию о размерах растра
    rows = dataset_1.RasterYSize
    cols = dataset_1.RasterXSize

    # Читаем данные из исходных файлов
    data_1 = dataset_1.ReadAsArray()
    data_2 = dataset_2.ReadAsArray()

    # Преобразуем данные в тензоры TensorFlow
    tensor_1 = tf.convert_to_tensor(data_1, dtype=tf.float32)
    tensor_2 = tf.convert_to_tensor(data_2, dtype=tf.float32)

    # Вычисляем разность между тензорами
    difference = tf.subtract(tensor_1, tensor_2)

    # Преобразуем результат обратно в массив NumPy
    difference_array = difference.numpy()

    # Создаем новый датасет TIFF с помощью GDAL
    driver = gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)

    # Копируем геотрансформ и проекцию из исходного датасета
    output_dataset.SetGeoTransform(dataset_1.GetGeoTransform())
    output_dataset.SetProjection(dataset_1.GetProjection())

    # Записываем данные разности в новый датасет
    output_band = output_dataset.GetRasterBand(1)
    output_band.WriteArray(difference_array)

    # Закрываем датасеты GDAL
    dataset_1 = None
    dataset_2 = None
    output_dataset = None

    print(f"Difference image saved to: {output_path}")

input_path_1 = "input_1.tif"
input_path_2 = "input_2.tif"
output_path = "difference.tif"

tiff_difference(input_path_1, input_path_2, output_path)
