from flask import Blueprint

test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route('/')
def test_function():
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "A#EDDFSAFSADFA"
                        }
                    }
                ]
            }
        } 
    return "TEST"
