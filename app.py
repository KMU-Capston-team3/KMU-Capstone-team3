from flask import Flask, request
import sys
import jsonify
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

@app.route("/led", methods=["GET"])
def led_function():
    GPIO.output(4, GPIO.HIGH)
    return "LED ON!"


if __name__ == "__main__":
    app.run(port=8000,host='0.0.0.0')
