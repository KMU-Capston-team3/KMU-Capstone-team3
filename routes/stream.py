from flask import Blueprint, Response, render_template_string
import cv2
from utils.camera_manager import camera, lock
import threading
import time

stream_bp = Blueprint('stream', __name__)

# streaming 을 위한 route
def gen_frames():
    
#    picam2 = Picamera2()
#    picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
#    picam2.start()


    while True:
        with lock:
            frame = camera.capture_array()   
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # 프레임 단위로 이미지 계속 뿌려줌
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@stream_bp.route('/')
def get_stream():
    # 만들어진 프레임으로 응답을 만듬
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

