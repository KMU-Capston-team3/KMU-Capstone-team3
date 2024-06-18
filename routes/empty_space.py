from flask import Blueprint, current_app
from utils.get_empty_space import get_empty_space

empty_space_bp = Blueprint('empty_space', __name__)


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

def get_empty_space_number():
    print("실행")
    empty_space = get_empty_space()
    print(len(empty_space.split(" ")))
    
    return empty_space.split(" ")
                    
