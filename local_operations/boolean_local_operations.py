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

# Применение булевских операций к пикселям
logical_and_result = tf.math.logical_and(images[0], images[1])
logical_or_result = tf.math.logical_or(images[0], images[1])
logical_not_result = tf.math.logical_not(images[0])
logical_xor_result = tf.math.logical_xor(images[0], images[1])

# Сохранение результатов булевских операций в формате TIFF
imageio.imsave('path/to/logical_and_result.tif', tf.cast(logical_and_result, tf.uint8))
imageio.imsave('path/to/logical_or_result.tif', tf.cast(logical_or_result, tf.uint8))
imageio.imsave('path/to/logical_not_result.tif', tf.cast(logical_not_result, tf.uint8))
imageio.imsave('path/to/logical_xor_result.tif', tf.cast(logical_xor_result, tf.uint8))
