from flask import Blueprint
from utils.get_empty_space import get_empty_space
from db.mongo import collection
from db.pipeline import pipeline
import numpy as np
from datetime import datetime
from utils.holiday import is_holiday
from utils.format import format_empty_space, format_predicted_space
import pickle


empty_space_bp = Blueprint('empty_space', __name__)

with open('parking_model.pkl', 'rb') as file:
    model, scaler = pickle.load(file)

# 빈자리 요청 route
@empty_space_bp.route("/", methods=["POST"])
def get_empty_space_handler():
    empty_space = get_empty_space()
    template = format_empty_space(empty_space)
    
    return {
        "version": "2.0",
        "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": template
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
    predicted_val = []
    current_date = datetime.now()
    day_of_week = current_date.weekday()
    is_holiday_param = is_holiday(current_date)
    for hour in range(0,24):
        prediction = predict_empty_space(hour, day_of_week, is_holiday_param)
        predicted_val.append({
            "hour": hour,
            "empty_space": prediction
        })
    template = format_predicted_space(predicted_val)

    return {
            "version": "2.0",
            "template": {
            "outputs": [
                        {
                    "simpleText": {
                        "text": template 
                    }
                        }
                    ]
                }
            }
def predict_empty_space(hour, day_of_week, is_holiday):

    is_weekend_value = 1 if day_of_week >= 5 else 0

    X_new = [[hour, day_of_week, is_weekend_value, is_holiday]]
    X_new_scaled = scaler.transform(X_new)
    prediction = model.predict(X_new_scaled)

    return round(prediction[0])

def get_empty_space_number():
    empty_space = get_empty_space()
    print("cronjob: 주차장 데이터 삽입 run")
    print(empty_space)
    return len(empty_space)