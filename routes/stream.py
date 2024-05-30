from flask import Blueprint, Response, render_template_string
import cv2
from camera_manager import camera, lock
import threading
import time

stream_bp = Blueprint('stream', __name__)
def gen_frames():
    
#    picam2 = Picamera2()
#    picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
#    picam2.start()


    while True:
        with lock:
            frame = camera.capture_array()   
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@stream_bp.route('/')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

