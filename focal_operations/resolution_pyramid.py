"""

В этом коде мы используем цикл while, чтобы 
создать пирамиду разрешений для каждого снимка. 
Мы начинаем с исходного изображения и на каждой итерации уменьшаем его размер в 
два раза, используя функцию tf.image.resize. Мы сохраняем все уровни пирамиды разрешений 
для каждого снимка в формате TIFF, добавляя уровень в название файла.

"""

import tensorflow as tf
import tensorflow_io as tfio
import imageio
import glob

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

# Создание пирамиды разрешений для каждого снимка
pyramid_images = []
current_image = images
pyramid_images.append(current_image)

while current_image.shape[0] >= 2 and current_image.shape[1] >= 2:
    new_height = current_image.shape[0] // 2
    new_width = current_image.shape[1] // 2
    current_image = tf.image.resize(current_image, [new_height, new_width], method=tf.image.ResizeMethod.BILINEAR)
    pyramid_images.append(current_image)

# Сохранение результатов пирамиды разрешений в формате TIFF
for i, file_path in enumerate(file_paths):
    for j, image in enumerate(pyramid_images):
        image = tf.cast(image[i] * 255.0, tf.uint8)
        imageio.imsave('path/to/pyramid_image_{}_level{}.tif'.format(i, j), image)
