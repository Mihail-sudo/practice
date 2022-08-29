import secrets
import os
from PIL import Image
from flask import current_app



def safe_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_file_name = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img', picture_file_name)
    
    output_size = 125, 125
    img = Image.open(picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    
    return picture_file_name