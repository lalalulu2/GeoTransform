import rasterio
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling
import glob

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

# Объединение снимков в мозаику
mosaic, mosaic_transform = merge(datasets, bounds=reference_bounds)

# Расчет размера мозаики
mosaic_width = mosaic_transform.width
mosaic_height = mosaic_transform.height

# Создание нового датасета для мозаики
mosaic_profile = datasets[0].profile
mosaic_profile.update(width=mosaic_width, height=mosaic_height, transform=mosaic_transform)

# Пересэмплирование мозаики при необходимости
scale_factor = 0.5  # Масштабный коэффициент (уменьшение разрешения в два раза)
if scale_factor != 1.0:
    new_width = int(mosaic_width * scale_factor)
    new_height = int(mosaic_height * scale_factor)
    mosaic, _ = reproject(mosaic, mosaic_profile, transform=mosaic_transform, resampling=Resampling.bilinear, width=new_width, height=new_height)

# Сохранение мозаики в файл
output_path = 'path/to/mosaic.tif'
with rasterio.open(output_path, 'w', **mosaic_profile) as dst:
    dst.write(mosaic, 1)
