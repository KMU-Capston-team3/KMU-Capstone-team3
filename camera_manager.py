from picamera2 import Picamera2
import threading

camera = Picamera2()
camera.configure(camera.create_video_configuration())
camera.start()
lock = threading.Lock()
