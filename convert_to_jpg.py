"""
Конвертация .tiff снимка в формат jpg
"""

from PIL import Image

def convert_tiff_to_jpg(tiff_path, jpg_path):
    try:
        # Открываем TIFF-изображение
        image = Image.open(tiff_path)

        # Преобразуем и сохраняем в формате JPEG
        image.convert('RGB').save(jpg_path, 'JPEG')

        print("Конвертация успешно завершена!")
    except Exception as e:
        print("Возникла ошибка при конвертации:", str(e))

# Путь к исходному TIFF-изображению
tiff_path = ""

# Путь для сохранения результирующего JPEG-изображения
jpg_path = ""

# Вызов функции конвертации
convert_tiff_to_jpg(tiff_path, jpg_path)
