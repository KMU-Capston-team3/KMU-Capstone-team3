from flask import Flask
from flask_apscheduler import APScheduler
from routes.capture import capture_bp
from routes.stream import stream_bp
from routes.empty_space import empty_space_bp, get_empty_space_number
from config import Config

# 서버 객체 초기화
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())


    # route 정의
    app.register_blueprint(capture_bp, url_prefix='/capture')
    app.register_blueprint(stream_bp, url_prefix='/stream')
    app.register_blueprint(empty_space_bp, url_prefix='/empty_space')

    
    
    return app


app = create_app()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='job_get_empty_space_number', seconds=10)
def scheduled_task():
    with app.app_context():
        get_empty_space_number()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)

