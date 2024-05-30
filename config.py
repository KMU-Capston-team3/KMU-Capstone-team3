import os

class Config:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    IMAGE_FOLDER = os.path.join(ROOT_DIR, 'images')

