"""

Здесь мы используем функцию tf.image.extract_patches 
для создания тайлов для каждого снимка. Мы указываем размеры тайлов tile_size, шаг 
перемещения stride и другие параметры функции. Затем мы сохраняем все тайлы для 
каждого снимка в формате TIFF, добавляя номер тайла в название файла.

"""


import tensorflow as tf
import tensorflow_io as tfio
import imageio
import glob

# Параметры тайлов
tile_size = (256, 256)  # Размер тайла
stride = (128, 128)  # Шаг перемещения тайла

# Путь к папке, содержащей спутниковые снимки формата TIFF
directory = 'path/to/images/'

# Получение списка путей ко всем файлам формата TIFF в папке
file_paths = glob.glob(directory + '*.tif')

# Загрузка спутниковых снимков без использования decode_tiff
images = []
for file_path in file_paths:
    image = imageio.imread(file_path)
    image = tf.convert_to_tensor(image, dtype=tf.float32) / 255.0  # Нормализация значений пикселей
    images.append(image)

# Преобразование списка изображений в тензоры TensorFlow
images = tf.stack(images)

# Создание тайлов для каждого снимка
tiled_images = []
for image in images:
    patches = tf.image.extract_patches(
        images=tf.expand_dims(image, axis=0),
        sizes=[1, tile_size[0], tile_size[1], 1],
        strides=[1, stride[0], stride[1], 1],
        rates=[1, 1, 1, 1],
        padding='VALID'
    )
    tiled_image = tf.reshape(patches, [-1, tile_size[0], tile_size[1], image.shape[-1]])
    tiled_images.append(tiled_image)

# Сохранение результатов тайлинга в формате TIFF
for i, file_path in enumerate(file_paths):
    for j, image in enumerate(tiled_images[i]):
        image = tf.cast(image * 255.0, tf.uint8)
        imageio.imsave('path/to/tiled_image_{}_tile{}.tif'.format(i, j), image)
