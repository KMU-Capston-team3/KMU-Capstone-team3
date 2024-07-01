from picamera2 import Picamera2
import threading
from datetime import datetime
from flask import current_app
import os
import boto3

# AWS S3 설정
s3 = boto3.client(
    's3',
    aws_access_key_id='AKIAU6GDVRHB7HEDP37G',
    aws_secret_access_key='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',
    region_name='ap-northeast-2'
)
BUCKET_NAME = 'park-awss3-bucket'

# 카메라 객체
camera = Picamera2()
# 카메라 기본 설정
camera.configure(camera.create_video_configuration())
# 카메라 프로세스 시작
camera.start()

# 공유 자원(카메라) 사용을 위한 lock
lock = threading.Lock()

def capture_and_save():
    with lock:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_path = os.path.join(current_app.config['IMAGE_FOLDER'], f'image_{timestamp}.jpg') 
        
        # 이미지 파일을 위한 파일 경로에 저장
        camera.capture_file(image_path)
    
    filename = f'image_{timestamp}.jpg'

    # S3에 이미지 업로드
    s3.upload_file(image_path, BUCKET_NAME, filename)

    # S3에 업로드된 이밎  URL 생성
    s3_url = f"https://{BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{filename}"
    
    print(f"Image uploaded to: {s3_url}")  # 업로드 된 URL생성.
    
    return s3_url
