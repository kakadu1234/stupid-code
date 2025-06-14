from PIL import Image 
from pillow_heif import register_heif_opener 
import os 


register_heif_opener()

heic_files = [photo for photo in os.listdir() if '.HEIC' in photo]

for photo in heic_files:
	temp_image = Image.open(photo)
	png_photo = photo.replace('.HEIC', '.png')
	temp_image.save(png_photo)
