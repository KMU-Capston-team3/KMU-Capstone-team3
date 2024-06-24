from flask import Blueprint, current_app, request
from utils.get_empty_space import get_empty_space
from db.mongo import collection
from db.pipeline import pipeline
import joblib
import numpy as np

empty_space_bp = Blueprint('empty_space', __name__)
model = joblib.load('parking_model.pkl')
# 빈자리 요청 route
@empty_space_bp.route("/", methods=["POST"])
def get_empty_space_handler():
    empty_space = get_empty_space()
    return {
        "version": "2.0",
        "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": f"빈자리 : {empty_space}" 
                }
            }
        ]
    }
            }
@empty_space_bp.route("/average", methods=["POST"])
def get_empty_space_average():
    result = list(collection.aggregate(pipeline))
    print(result)

    return result

@empty_space_bp.route("/predict", methods=["POST"])
def predict_empty_space_handler():
    hour = request.args.get('hour', default=None, type=int)
    day_of_week = request.args.get('day_of_week', default=None, type=int)
    is_holiday = request.args.get('is_holiday', default=0, type=int)

    if hour is None or hour < 0 or hour >= 24:
        return {
            "error": "invalid hour"
        }
    if day_of_week is None or day_of_week < 0 or day_of_week >= 7:
        return {
            "error": "invalid day"
        }
    
    prediction = predict_empty_space(hour, day_of_week, is_holiday)

    return {
        "hour": hour,
        "day_of_week": day_of_week,
        "is_holiday": is_holiday,
        "predicted_average_number": prediction
    }

def predict_empty_space(hour, day_of_week, is_holiday):
    is_weekend = 1 if day_of_week >= 5 else 0
    features = np.array([[hour, day_of_week, is_weekend, is_holiday]])
    prediction = model.predict(features)
    return prediction[0]

def get_empty_space_number():
    empty_space = get_empty_space()
    print("실행")
    print(empty_space)
    return len(empty_space.split(" "))
                    
