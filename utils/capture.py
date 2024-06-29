from utils.camera_manager import lock, camera
from datetime import datetime
from flask import current_app
import os

def capture_and_save():
    with lock:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_path = os.path.join(current_app.config['IMAGE_FOLDER'], f'image_{timestamp}.jpg') 
        
        # 이미지 파일 위에 정의한 파일 경로에 저장
        camera.capture_file(image_path)
    filename = f'image_{timestamp}.jpg'
 
    return filename
