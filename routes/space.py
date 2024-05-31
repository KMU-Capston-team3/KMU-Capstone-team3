from PIL import Image
from flask import Blueprint, url_for, current_app
from camera_manager import camera, lock
from datetime import datetime
import os
import pytesseract
import numpy as np
import cv2

space_bp = Blueprint('space', __name__)

def preprocess_image(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path)
    
    # 이미지를 회색조로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 가우시안 블러를 적용하여 노이즈 제거
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 적응적 이진화 처리
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 3)
    
    # 세로 주차선 제거: 수직 선 필터 사용
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    temp_img = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    vertical_lines = cv2.dilate(temp_img, vertical_kernel, iterations=2)
    
    # 세로 주차선을 이미지에서 제거
    cleaned_image = cv2.bitwise_and(binary, binary, mask=cv2.bitwise_not(vertical_lines))
    
    # 윤곽선 검출
    contours, _ = cv2.findContours(cleaned_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 숫자가 포함된 영역만 남기기 위해 마스크 생성
    mask = np.zeros_like(binary)
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        
        # 적절한 크기의 직사각형만 선택 (너무 큰 직사각형이나 너무 작은 직사각형 제외)
        if 0.2 < aspect_ratio < 1.0 and h > 10 and w > 10:  # 조건을 조절할 수 있음
            # 외곽선 그리기
            cv2.drawContours(mask, [cnt], -1, (255), thickness=cv2.FILLED)  # 외곽선 내부를 채우기
    
    # 마스크를 원본 이미지에 적용하여 숫자 부분만 흰색으로 남기고 배경을 검은색으로 설정
    result = cv2.bitwise_and(binary, mask)
    
    # 배경을 흰색으로, 숫자를 검은색으로 반전
    final_result = cv2.bitwise_not(result)
    
    return final_result

def extract_digits(image):
    # pytesseract 설정: 숫자만 추출
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    
    # pytesseract를 이용하여 이미지에서 텍스트 추출
    extracted_text = pytesseract.image_to_string(image, config=custom_config)
    return extracted_text



@space_bp.route("/", methods=["GET"])
def space_function():
    with lock:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(current_app.config['IMAGE_FOLDER'], f'image_{timestamp}.jpg')
        camera.capture_file(image_path)
    
    # 이미지 전처리
    processed_image = preprocess_image(image_path)

    # 숫자 추출
    digits = extract_digits(processed_image)


    # 결과 이미지 저장 (선택사항)
    cv2.imwrite('processed_parking_lot.jpg', processed_image)

    return digits
