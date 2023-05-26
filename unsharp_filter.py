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

# Применение фильтра Unsharp Masking к пикселям снимков
blurred_images = tf.image.conv2d(images, tf.expand_dims(tf.constant([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=tf.float32)), strides=1, padding='SAME')
unsharp_masked_images = tf.clip_by_value(2 * images - blurred_images, 0.0, 1.0)

# Сохранение результатов фильтрации в формате TIFF
for i, file_path in enumerate(file_paths):
    image = tf.cast(unsharp_masked_images[i] * 255.0, tf.uint8)
    imageio.imsave('path/to/unsharp_masked_image_{}.tif'.format(i), image)
