from flask import Flask, request
from picamera2 import Picamera2, preview
from time import sleep
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT, initial=False)

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World'

@app.route("/test", methods=["POST"])
def test_function():
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "A3 F4 G5 A11 자리 확인"
                        }
                    }
                ] 
            }
            }
    return response  
    
@app.route("/snap", methods=["POST"])
def snap_function():
    cam = Picamera2() 
    camera_config = cam.create_preview_configuration()
    cam.configure(camera_config)
    cam.start_preview(Preview.QTGL)
    cam.start()
    time.sleep(3)
    cam.capture_file("image.jpg")
    cam.stop_preview()
    return "Snapped!"

@app.route("/led", methods=["GET"])
def led_function():
    GPIO.output(4, GPIO.HIGH)
    return "LED ON!"


if __name__ == "__main__":
    app.run(port=8000,host='0.0.0.0')
