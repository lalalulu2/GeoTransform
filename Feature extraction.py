import tensorflow as tf
from osgeo import gdal
import numpy as np

def extract_features_tiff(input_path):
    # Открываем файл TIFF с помощью GDAL
    dataset = gdal.Open(input_path)

    # Получаем информацию о размерах растра
    rows = dataset.RasterYSize
    cols = dataset.RasterXSize

    # Читаем данные из файла
    data = dataset.ReadAsArray()

    # Преобразуем данные в тензор TensorFlow
    tensor = tf.convert_to_tensor(data, dtype=tf.float32)

    # Выполняем операции извлечения признаков с использованием TensorFlow
    # Здесь приведено вычисление среднего значения по всем пикселям
    features = tf.reduce_mean(tensor)

    # Получаем значение признака
    feature_value = features.numpy()

    # Закрываем датасет GDAL
    dataset = None

    return feature_value

input_path = "input.tif"

feature_value = extract_features_tiff(input_path)
print(f"Extracted feature value: {feature_value}")
