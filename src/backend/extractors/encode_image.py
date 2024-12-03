import base64
from pathlib import Path 
import os
import mimetypes

def encode_image(file_path):
    with Path(file_path).open("rb") as image_file:
        encoded_str = base64.b64encode(image_file.read()).decode('utf-8')
        mime_type, _ = mimetypes.guess_type(file_path)

        return f'data:{mime_type};base64,{encoded_str}'


