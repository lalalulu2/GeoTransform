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

# Применение функций к пикселям
sin_result = tf.math.sin(images)
cos_result = tf.math.cos(images)
log_result = tf.math.log(images + 1)  # Добавляем 1, чтобы избежать логарифма от нуля
exp_result = tf.math.exp(images)

# Сохранение результатов в формате TIFF
imageio.imsave('path/to/sin_result.tif', tf.cast(sin_result, tf.uint8))
imageio.imsave('path/to/cos_result.tif', tf.cast(cos_result, tf.uint8))
imageio.imsave('path/to/log_result.tif', tf.cast(log_result, tf.uint8))
imageio.imsave('path/to/exp_result.tif', tf.cast(exp_result, tf.uint8))
