from flask import current_app
from utils.capture import capture_and_save
import os
import pytesseract
import cv2
import numpy as np

def get_empty_space():
    filename = capture_and_save() 
    # 저장된 image 를 바탕으로 이미지 처리
    image_path = os.path.join(current_app.config['IMAGE_FOLDER'], filename)

    img_color = cv2.imread(image_path)
    height, width = img_color.shape[0:2]
    center = (height / 2, width / 2)

    # 각도 지정 (변경)
    angle = -45

    M = cv2.getRotationMatrix2D(center, angle , 1.0)
    img_rotated = cv2.warpAffine(img_color, M, (width, height))

    # 투시변환 기준점 4개 지정
    src_points = np.float32([[304, 388], [2456, 960], [120, 1796], [2776, 2024]])
    dst_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # 회전 행렬 구한 뒤 이미지 회전
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    img_warped = cv2.warpPerspective(img_rotated, M, (width, height))
    
    # 이미지 전처리
    img_hsv = cv2.cvtColor(img_warped, cv2.COLOR_BGR2HSV)
    lower_blue = (115-10, 100, 100)
    upper_blue = (125+10, 255, 255)

    img_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)
    img_result = cv2.bitwise_and(img_warped, img_warped, mask = img_mask)
    
    # 이미지 처리 후 이미지에서 텍스트 추출
    empty_space = pytesseract.image_to_string(img_result, config='--psm 6 -c tessedit_char_whitelist="0123456789 "')

    return empty_space

    """ cv2 window로 이미지 처리과정 확인
    cv2.namedWindow('img_rotated', cv2.WINDOW_NORMAL)
    cv2.namedWindow('img_warped', cv2.WINDOW_NORMAL)
    cv2.namedWindow('img_mask', cv2.WINDOW_NORMAL)

    cv2.imshow('img_rotated', img_rotated)
    cv2.imshow('img_warped', img_warped)
    cv2.imshow('img_mask', img_mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """