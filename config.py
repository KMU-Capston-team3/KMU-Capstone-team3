import os

class Config:
    SCHEDULER_API_ENABLED = True
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    IMAGE_FOLDER = os.path.join(ROOT_DIR, 'images')

