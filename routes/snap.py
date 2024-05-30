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

        camera.capture_file(image_path)
    image_url = url_for('snap.get_image', filename=f'image_{timestamp}.jpg', _external=True)

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


@snap_bp.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    image_path = os.path.join(current_app.config['IMAGE_FOLDER'], filename)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/jpeg')
    else:
        return {
                "error": "Image not found"
                }

