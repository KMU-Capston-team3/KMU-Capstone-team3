from flask import Blueprint, current_app
from utils.capture import capture_and_save
import os
import pytesseract
import cv2

empty_space_bp = Blueprint('empty_space', __name__)

# 빈자리 요청 route
@empty_space_bp.route("/", methods=["POST"])
def get_empty_space():
   
    filename = capture_and_save() 
    # 저장된 image 를 바탕으로 이미지 처리
    image_path = os.path.join(current_app.config['IMAGE_FOLDER'], filename)

    img_color = cv2.imread(image_path)
    img_blur = cv2.GaussianBlur(img_color, (15, 15), 0)
    height, width = img_blur.shape[:2]
        
    img_hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
    lower_blue = (115-10, 30, 30)
    upper_blue = (130+10, 255, 255)

    img_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)
    img_result = cv2.bitwise_and(img_blur, img_blur, mask = img_mask)
 
    # cv2.imshow('img_mask', img_mask) masking 된 이미지 표시
    # cv2.imshow('img_color', img_result) bitwise 연산으로 이진화된 이미지 표시
	  
    # 이미지 처리 후 이미지에서 텍스트 추출함
    empty_space = pytesseract.image_to_string(img_result, config='--psm 6')

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
