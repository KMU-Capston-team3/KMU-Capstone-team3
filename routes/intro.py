from flask import Blueprint

intro_bp = Blueprint('intro', __name__)

@intro_bp.route("/", methods=["POST"])
def intro():
    return {
    "version": "2.0",
    "template": {
    "outputs": [
        {
        "basicCard": {
            "title": "기능 시연은 채팅 창 위의 흰색 칸으로 된 메뉴로 진행해주세요!",
            "description": "반갑습니다! 여러분의 빠른 주차를 도와드릴 주차맨이에요!\n제가 가진 기능들에 대해 알려드릴게요.",
            "thumbnail": {
                "imageUrl": "https://park-awss3-bucket.s3.ap-northeast-2.amazonaws.com/parkingman.jpg"
            },
            "buttons": [
            {
                "action": "message",
                "label": "시간대 별 빈자리 수 예측",
                "messageText": "시간대 별 빈자리 수 예측"
            },
            {
                "action": "message",
                "label": "주차장 사진 촬영",
                "messageText": "주차장 사진 촬영"
            },
            {
                "action": "message",
                "label": "빈 자리 찾기",
                "messageText": "빈 자리 찾기"
            }
            ]
        }
        }
    ]
    }
    }

@intro_bp.route("/empty_space/predict", methods=["POST"])
def intro_empty_space_predict():
    return {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "날짜, 시간, 주말/공휴일 여부에 따라 오늘 0시~23시에 주차 공간이 얼마나 남아있을 지 예측해서 알려드릴게요."
                }
            }
        ]
    }
}


@intro_bp.route("/capture", methods=["POST"])
def intro_capture():
    return {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "요청하시는 즉시 주차장 전체 사진을 찍어서 보내드려요. 여러 사람이 동시에 요청 시 요청하신 순서에 따라 시간이 5~10초 정도 소요될 수 있어요."
                }
            }
        ]
    }
}

@intro_bp.route("/empty_space", methods=["POST"])
def intro_empty_space():
    return {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "주차장 사진을 촬영 후 글자를 인식한 뒤 빈 공간의 번호들을 알려드릴게요."
                }
            }
        ]
    }
}