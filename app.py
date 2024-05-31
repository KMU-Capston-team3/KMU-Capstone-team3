from flask import Flask
from routes.snap import snap_bp
from routes.stream import stream_bp
from routes.space import space_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(snap_bp, url_prefix='/snap')
    app.register_blueprint(stream_bp, url_prefix='/stream')
    app.register_blueprint(space_bp, url_prefix='/space')
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)

