# app/utils.py

import os
import requests

def download_image(image_url: str, save_path: str):
    response = requests.get(image_url)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    return save_path
