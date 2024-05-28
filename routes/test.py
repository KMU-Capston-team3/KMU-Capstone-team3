from flask import Blueprint

test_bp = Blueprint('test', __name__)

@test_bp.route('/test')
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
