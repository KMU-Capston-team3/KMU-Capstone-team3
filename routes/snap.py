from flask import Blueprint, send_file, url_for, current_app
from camera_manager import camera, lock
from time import sleep
from datetime import datetime
import io
import os


snap_bp = Blueprint('snap', __name__)


@snap_bp.route("/", methods=["POST"])
def snap_function():

    with lock:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_path = os.path.join(current_app.config['IMAGE_FOLDER'], f'image_{timestamp}.jpg') 
        
        # 이미지 파일 위에 정의한 파일 경로에 저장
        camera.capture_file(image_path)
        
        # 파일 경로로 image url 만들기. 응답에 담음
    image_url = url_for('snap.get_image', filename=f'image_{timestamp}.jpg', _external=True)

    # 응답 형식, 카카오에서 강제하는 방식
    return {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleImage": {
                    "imageUrl": image_url,
                    "altText": "image"
                }
            }
        ]
    }
}    


# 이미지가 담긴 image url
@snap_bp.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    image_path = os.path.join(current_app.config['IMAGE_FOLDER'], filename)
    if os.path.exists(image_path):
        # image 경로를 바탕으로 응답으로 이미지 파일 전송
        return send_file(image_path, mimetype='image/jpeg')
    else:
        return {
                "error": "Image not found"
                }

