import rasterio
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
import glob
from scipy.stats import pearsonr
import tensorflow as tf

# Путь к папке, содержащей спутниковые снимки формата TIFF
directory = 'path/to/images/'

# Получение списка путей ко всем файлам формата TIFF в папке
file_paths = glob.glob(directory + '*.tif')

# Открытие всех снимков и получение их преобразования
datasets = []
transforms = []
for file_path in file_paths:
    dataset = rasterio.open(file_path)
    datasets.append(dataset)
    transform, width, height = calculate_default_transform(dataset.crs, dataset.crs, dataset.width, dataset.height, *dataset.bounds)
    transforms.append(transform)

# Проверка координат снимков
reference_bounds = datasets[0].bounds
for dataset, file_path in zip(datasets[1:], file_paths[1:]):
    if dataset.bounds != reference_bounds:
        raise ValueError(f"Координаты снимка {file_path} не совпадают с координатами других снимков!")

# Чтение пикселей каждого снимка и сохранение их в массив
image_arrays = []
for dataset in datasets:
    image_array = dataset.read(1)  # Чтение первого канала снимка
    image_array = tf.convert_to_tensor(image_array, dtype=tf.float32)
    image_arrays.append(image_array)

# Рассчет коэффициента корреляции Пирсона между парами снимков
correlation_matrix = np.zeros((len(file_paths), len(file_paths)))
for i in range(len(file_paths)):
    for j in range(len(file_paths)):
        correlation, _ = pearsonr(tf.reshape(image_arrays[i], [-1]).numpy(), tf.reshape(image_arrays[j], [-1]).numpy())
        correlation_matrix[i, j] = correlation

print(correlation_matrix)
