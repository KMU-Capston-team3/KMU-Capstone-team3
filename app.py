from flask import Flask, request
from routes.test import test_bp
from routes.snap import snap_bp

app = Flask(__name__)

app.register_blueprint(test_bp)
app.register_blueprint(snap_bp)

@app.route('/')
def hello():
    return 'Hello, World'

if __name__ == "__main__":
    app.run(port=8000,host='0.0.0.0')
