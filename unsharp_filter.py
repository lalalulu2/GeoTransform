import tensorflow as tf
import tensorflow_io as tfio
import imageio
import glob

# Путь к папке, содержащей спутниковые снимки формата TIFF
directory = 'path/to/images/'

# Получение списка путей ко всем файлам формата TIFF в папке
file_paths = glob.glob(directory + '*.tif')

# Загрузка спутниковых снимков с использованием TensorFlow-IO
images = []
for file_path in file_paths:
    image = tfio.experimental.image.decode_tiff(tf.io.read_file(file_path))
    images.append(image)

# Преобразование списка изображений в тензоры TensorFlow
images = tf.convert_to_tensor(images, dtype=tf.float32)

# Применение фильтра Unsharp Masking к пикселям снимков
blurred_images = tf.image.filter2d(images, [-1, -1, -1, -1, 9, -1, -1, -1, -1], padding='SAME')
unsharp_masked_images = tf.clip_by_value(2 * images - blurred_images, 0.0, 1.0)

# Сохранение результатов фильтрации в формате TIFF
for i, file_path in enumerate(file_paths):
    imageio.imsave('path/to/unsharp_masked_image_{}.tif'.format(i), tf.cast(unsharp_masked_images[i], tf.uint8))
