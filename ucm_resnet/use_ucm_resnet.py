import os
from PIL import Image
import tensorflow as tf

tiff_folder = 'путь_к_папке_tiff'

jpg_folder = 'путь_к_папке_jpg'

model = tf.keras.models.load_model('путь_к_обученной_модели')

for filename in os.listdir(tiff_folder):
    if filename.endswith('.tiff'):
       
        tiff_path = os.path.join(tiff_folder, filename)
        
        image = Image.open(tiff_path)
        
        jpg_image = image.convert('RGB')
        
        jpg_path = os.path.join(jpg_folder, f'{os.path.splitext(filename)[0]}.jpg')
        
        jpg_image.save(jpg_path)

        predictions = model.predict(preprocessed_image)
        

