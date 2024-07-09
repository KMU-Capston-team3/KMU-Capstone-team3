from flask import Flask
from flask_apscheduler import APScheduler
from routes.intro import intro_bp
from routes.capture import capture_bp
from routes.stream import stream_bp
from routes.empty_space import empty_space_bp, get_empty_space_number
from config import Config
from pymongo import MongoClient
from datetime import datetime
from db import mongo
# 서버 객체 초기화
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())


    # route 정의
    app.register_blueprint(intro_bp, url_prefix='/intro')
    app.register_blueprint(capture_bp, url_prefix='/capture')
    app.register_blueprint(stream_bp, url_prefix='/stream')
    app.register_blueprint(empty_space_bp, url_prefix='/empty_space')

    
    
    return app


app = create_app()

# 크론잡을 위한 스케쥴러
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='job_get_empty_space_number', minutes=30)
def scheduled_task():
    with app.app_context():
        empty_space_number = get_empty_space_number()
        result = mongo.collection.insert_one({
            "empty_space": empty_space_number,
            "created_at": datetime.now()
        })
        return str(result.inserted_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)

