from utils.camera_manager import lock, camera
from datetime import datetime
from flask import current_app
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name='ap-northeast-2'
)

def capture_and_save():
    with lock:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'image_{timestamp}.jpg'
        # 이미지 파일 위에 정의한 파일 경로에 저장
        image_path = os.path.join(current_app.config['IMAGE_FOLDER'], f'image_{timestamp}.jpg') 
        camera.capture_file(image_path)

    
    s3.upload_file(image_path, os.environ.get("BUCKET_NAME"), filename)
    image_url = f"https://{os.environ.get('BUCKET_NAME')}.s3.ap-northeast-2.amazonaws.com/{filename}"
    os.remove(image_path)
    return image_url
