import tensorflow as tf
import tensorflow_io as tfio
import imageio
import glob

# Путь к папке, содержащей спутниковые снимки формата TIFF
directory = 'path/to/images/'

# Получение списка путей ко всем файлам формата TIFF в папке
file_paths = glob.glob(directory + '*.tif')

# Загрузка спутниковых снимков с использованием imageio
images = []
for file_path in file_paths:
    image = imageio.imread(file_path)
    images.append(image)

# Преобразование списка изображений в тензоры TensorFlow
images = tf.convert_to_tensor(images, dtype=tf.float32)

# Сложение пикселей
summed_image = tf.reduce_sum(images, axis=0)

# Вычитание пикселей
subtracted_image = tf.subtract(images[0], tf.reduce_sum(images[1:], axis=0))

# Умножение пикселей
multiplied_image = tf.reduce_prod(images, axis=0)

# Деление пикселей
divided_image = tf.math.divide(images[0], tf.reduce_prod(images[1:], axis=0))

# Сохранение результатов операций в формате TIFF
imageio.imsave('path/to/summed_image.tif', tf.cast(summed_image, tf.uint8))
imageio.imsave('path/to/subtracted_image.tif', tf.cast(subtracted_image, tf.uint8))
imageio.imsave('path/to/multiplied_image.tif', tf.cast(multiplied_image, tf.uint8))
imageio.imsave('path/to/divided_image.tif', tf.cast(divided_image, tf.uint8))
