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

# Применение интерполяции к каждому снимку
interpolated_images = []
for image in images:
    interpolated_image = tf.image.resize(image, [new_height, new_width], method=tf.image.ResizeMethod.BILINEAR)
    interpolated_images.append(interpolated_image)

# Преобразование списка изображений с интерполяцией в тензоры TensorFlow
interpolated_images = tf.stack(interpolated_images)

# Сохранение результатов с интерполяцией в формате TIFF
for i, file_path in enumerate(file_paths):
    image = tf.cast(interpolated_images[i] * 255.0, tf.uint8)
    imageio.imsave('path/to/interpolated_image_{}.tif'.format(i), image)
