import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import glob
import numpy as np
import tensorflow as tf

# Путь к папке, содержащей спутниковые снимки формата TIFF
directory = 'path/to/images/'

# Получение списка путей ко всем файлам формата TIFF в папке
file_paths = glob.glob(directory + '*.tif')

# Задание параметров аффинного преобразования
scale_x = 0.5  # Масштаб по оси X
scale_y = 0.5  # Масштаб по оси Y
translate_x = 100  # Смещение по оси X
translate_y = 100  # Смещение по оси Y
affine_matrix = np.array([[scale_x, 0, translate_x], [0, scale_y, translate_y], [0, 0, 1]])

# Применение аффинного преобразования к каждому снимку
for file_path in file_paths:
    # Открытие снимка
    dataset = rasterio.open(file_path)

    # Получение новой матрицы преобразования на основе текущей матрицы и аффинной матрицы
    new_affine_matrix = dataset.transform * affine_matrix

    # Вычисление размера нового снимка на основе измененной матрицы преобразования
    new_height = int(dataset.height * scale_y)
    new_width = int(dataset.width * scale_x)

    # Создание нового массива для нового снимка
    new_image_array = np.zeros((dataset.count, new_height, new_width), dtype=dataset.dtypes[0])

    # Применение аффинного преобразования к каждому каналу снимка
    for i in range(1, dataset.count + 1):
        reproject(
            dataset.read(i),
            new_image_array[i - 1],
            src_transform=dataset.transform,
            src_crs=dataset.crs,
            dst_transform=new_affine_matrix,
            dst_crs=dataset.crs,
            resampling=Resampling.bilinear
        )

    # Сохранение нового снимка в новом файле
    new_file_path = file_path.replace('.tif', '_transformed.tif')
    with rasterio.open(
        new_file_path,
        'w',
        driver='GTiff',
        height=new_height,
        width=new_width,
        count=dataset.count,
        dtype=dataset.dtypes[0],
        crs=dataset.crs,
        transform=new_affine_matrix
    ) as new_dataset:
        new_dataset.write(new_image_array)

    print(f"Снимок {file_path} преобразован и сохранен в файл {new_file_path}")
