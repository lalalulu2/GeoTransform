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

# Применение фильтра Собеля к пикселям снимков
sobel_images = []
for image in images:
    sobel_x = tf.image.sobel_edges(tf.expand_dims(image, axis=0))[0, :, :, :, 0]  # Градиент по оси x
    sobel_y = tf.image.sobel_edges(tf.expand_dims(image, axis=0))[0, :, :, :, 1]  # Градиент по оси y
    sobel_image = tf.sqrt(tf.square(sobel_x) + tf.square(sobel_y))  # Вычисление модуля градиента
    sobel_images.append(sobel_image)

# Преобразование списка изображений собеля в тензоры TensorFlow
sobel_images = tf.stack(sobel_images)

# Сохранение результатов фильтрации в формате TIFF
for i, file_path in enumerate(file_paths):
    image = tf.cast(sobel_images[i] * 255.0, tf.uint8)
    imageio.imsave('path/to/sobel_image_{}.tif'.format(i), image)
