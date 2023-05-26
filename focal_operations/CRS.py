import rasterio
import glob

# Путь к папке, содержащей спутниковые снимки формата TIFF
directory = 'path/to/images/'

# Получение списка путей ко всем файлам формата TIFF в папке
file_paths = glob.glob(directory + '*.tif')

# Изменение системы координат и пересэмплирование для каждого снимка
for file_path in file_paths:
    with rasterio.open(file_path) as src:
        # Изменение системы координат (CRS)
        dst_crs = 'EPSG:4326'  # Целевая система координат (например, WGS84)
        transformed = src.read(1, out_shape=src.shape, resampling=rasterio.enums.Resampling.nearest)
        profile = src.profile
        profile.update(crs=dst_crs)
        
        # Пересэмплирование
        scale_factor = 0.5  # Масштабный коэффициент (уменьшение разрешения в два раза)
        new_width = int(src.width * scale_factor)
        new_height = int(src.height * scale_factor)
        resampled = transformed.astype(rasterio.float32)
        resampled = resampled.reshape((1, src.height, src.width))
        resampled = rasterio.warp.reproject(
            resampled, src.profile,
            dst_transform=src.transform, dst_crs=src.crs,
            resampling=rasterio.enums.Resampling.bilinear,
            height=new_height, width=new_width
        )
        resampled = resampled.reshape((new_height, new_width))
        
        # Сохранение результата
        output_path = 'path/to/resampled_image.tif'
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(resampled, 1)
