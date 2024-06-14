from flask import Blueprint, send_file, url_for, current_app
from utils.capture import capture_and_save
import io
import os


capture_bp = Blueprint('capture', __name__)


@capture_bp.route("/", methods=["POST"])
def get_image():
    filename = capture_and_save()
        # 파일 경로로 image url 만들기. 응답에 담음
    image_url = url_for('capture.send_image', filename=filename, _external=True)

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
@capture_bp.route('/images/<filename>', methods=['GET'])
def send_image(filename):
    image_path = os.path.join(current_app.config['IMAGE_FOLDER'], filename)
    if os.path.exists(image_path):
        # image 경로를 바탕으로 응답으로 이미지 파일 전송
        return send_file(image_path, mimetype='image/jpeg')
    else:
        return {
                "error": "Image not found"
                }

