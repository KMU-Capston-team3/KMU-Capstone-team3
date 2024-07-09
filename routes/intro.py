from flask import Blueprint

intro_bp = Blueprint('intro', __name__)

@intro_bp.route("/", methods=["POST"])
def intro():
    return {
    "version": "2.0",
    "template": {
    "outputs": [
        {
        "textCard": {
            "title": "반갑습니다! 여러분의 빠른 주차를 도와드릴 주차맨이에요!",
            "description": "제가 가진 기능들에 대해 알려드릴게요!",
            "buttons": [
            {
                "action": "message",
                "label": "시간대 별 빈자리 수 예측",
                "messageText": "저는 30분마다 주차장 사진을 촬영하고, 남아있는 빈 자리 수를 DB에 저장해요. 날짜, 시간, 요일, 공휴일 여부에 따라 오늘 0시~23시에 주차 공간이 얼마나 남아있을 지 예측해서 알려드릴게요."
            },
            {
                "action": "message",
                "label": "주차장 사진 촬영",
                "messageText": "요청하시는 즉시 주차장 전체 사진을 찍어서 보내드려요."
            },
            {
                "action": "message",
                "label": "빈 자리 찾기",
                "messageText": "주차장 사진을 찍고, 주차장 바닥의 자리 번호를 인식해 빈 공간의 번호들을 알려드릴게요."
            }
            ]
        }
        }
    ]
    }
    }