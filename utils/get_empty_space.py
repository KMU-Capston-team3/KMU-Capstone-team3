from utils.capture import capture_and_save
import pytesseract
import cv2
import numpy as np
import requests
from google.cloud import vision
import re
import requests
def vision_api():
    credentials_path = './parkingman.json'
    client = vision.ImageAnnotatorClient.from_service_account_json(credentials_path)
    
    image_url = capture_and_save()
    response = requests.get(image_url)
    image_content = response.content
    
    nparr = np.frombuffer(image_content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blue_areas = cv2.bitwise_and(image, image, mask=mask)

    success, encoded_image = cv2.imencode('.jpg', blue_areas)
    image_content = encoded_image.tobytes()

    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    numbers = []
    for text in texts:
        extracted_text = text.description
        extracted_numbers = re.findall(r'\b\d+\b', extracted_text)
        numbers.extend(extracted_numbers)

    unique_numbers = sorted(set(numbers), key=int)
    return unique_numbers



def get_empty_space():
    image_url = capture_and_save() 

    # image url을 바탕으로 이미지 처리
    img_nparray = np.asarray(bytearray(requests.get(image_url).content), dtype = np.uint8)
    img_color = cv2.imdecode(img_nparray, cv2.IMREAD_COLOR)

    height, width = img_color.shape[0:2]
    center = (height / 2, width / 2)

    # 각도 지정 (변경)
    # angle = -30

    # M = cv2.getRotationMatrix2D(center, angle , 1.0)
    # img_rotated = cv2.warpAffine(img_color, M, (width, height))

    # 투시변환 기준점 4개 지정
    # 152,88,1092,92, 4,502,1236,506
    src_points = np.float32([[152, 88], [1092, 92], [4, 502], [1236, 506]])
    dst_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # 회전 행렬 구한 뒤 이미지 회전
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    img_warped = cv2.warpPerspective(img_color,M, (width, height))
    
    # 이미지 전처리
    img_hsv = cv2.cvtColor(img_warped, cv2.COLOR_BGR2HSV)
    lower_blue = (115-10, 100, 100)
    upper_blue = (125+10, 255, 255)

    img_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)
    img_result = cv2.bitwise_and(img_warped, img_warped, mask = img_mask)
    
    # 이미지 처리 후 이미지에서 텍스트 추출
    empty_space = pytesseract.image_to_string(img_result, config='--psm 6 -c tessedit_char_whitelist="0123456789 "')

    return empty_space

