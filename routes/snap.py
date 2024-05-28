from flask import Blueprint
from picamera2 import Picamera2, Preview
from time import sleep
snap_bp = Blueprint('snap', __name__)


@snap_bp.route("/snap", methods=["POST"])
def snap_function():

    camera = Picamera2(0)
    camera_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    camera.configure(camera_config)
    camera.start()
    sleep(1)
    camera.capture_file("test.jpg")   
    camera.stop()
    camera.close()

    return "Snapped!"


