from picamera2 import Picamera2
import threading

# 카메라 객체 
camera = Picamera2()
# 카메라 기본 설정
camera.configure(camera.create_video_configuration())
# 카메라 프로세스 시작
camera.start()
# 공유 자원(카메라) 사용을 위한 lock, 여러 부분에서 카메라 사용하는 데 필수
lock = threading.Lock()
