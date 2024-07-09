from utils.capture import capture_and_save
import pytesseract
import cv2
import numpy as np
import requests
from google.cloud import vision
import re
import requests

def get_empty_space():
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

