import os
from PIL import Image
import tensorflow as tf

tiff_folder = ''

jpg_folder = ''

model = tf.keras.models.load_model('resnet_model.hdf5')

for filename in os.listdir(tiff_folder):
    if filename.endswith('.tiff'):
       
        tiff_path = os.path.join(tiff_folder, filename)
        
        image = Image.open(tiff_path)
        
        jpg_image = image.convert('RGB')
        
        jpg_path = os.path.join(jpg_folder, f'{os.path.splitext(filename)[0]}.jpg')
        
        jpg_image.save(jpg_path)

        predictions = model.predict(preprocessed_image)
        

