from flask import Blueprint, send_file, url_for, current_app
from utils.capture import capture_and_save

capture_bp = Blueprint('capture', __name__)

@capture_bp.route("/", methods=["POST"])
def get_image_handler():
    image_url = capture_and_save()
        # 파일 경로로 image url 만들기. 응답에 담음
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

