#from flask import Blueprint
import pytesseract
import cv2

#space_bp = Blueprint('space', __name__)

img_color = cv2.imread('/home/pi/workspace/cv/test.jpg')
img_blur = cv2.GaussianBlur(img_color, (15, 15), 0)
height, width = img_blur.shape[:2]
	
img_hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
lower_blue = (115-10, 30, 30)
upper_blue = (130+10, 255, 255)

img_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)
img_result = cv2.bitwise_and(img_blur, img_blur, mask = img_mask)
print(pytesseract.image_to_string(img_result, config = '--psm 6'))

# cv2.imshow('img_mask', img_mask) masking 된 이미지 표시
# cv2.imshow('img_color', img_result) bitwise 연산으로 이진화된 이미지 표시
	
cv2.waitKey(0)
cv2.destroyAllWindows()
