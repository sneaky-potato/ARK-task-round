import cv2
import os
import numpy as np
import random
import math

class Controller():
    def __init__(self, x, y, rad):
        self.x = x
        self.y = y
        self.radius = rad
    def __add__(self, other):
        return Controller(self.x + other.x, self.y + other.y, self.radius)
    
cascPath = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"

faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)

max_height = int(video_capture.get(4))
max_width = int(video_capture.get(3)) 
width = 1280
height = 720
# video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
# video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
l_img = np.zeros((height, width, 3), np.uint8)

masked_data = np.zeros(l_img.shape[:2], dtype=np.uint8)

ball_pos = Controller(width / 2, 100, 25)
pos = Controller(0, 0, 0)

angle = random.randint(20, 340)
if 160 <= angle <= 200:
    angle = 90

def prepare_arena(window, frame):
    line_thickness = 2
    cv2.line(window, (frame.shape[1]//2, 1), (frame.shape[1]//2, window.shape[0]), (0, 255, 0), thickness=line_thickness)
    cv2.line(window, (window.shape[1]-frame.shape[1]//2, 1), (window.shape[1] - frame.shape[1]//2, window.shape[0]), (0, 255, 0), thickness=line_thickness)

def move_ball(l_img):
    global ball_pos
    global angle
    global pos
    global score
    l_img = cv2.circle(l_img, (int(ball_pos.x), int(ball_pos.y)), 25, [0,0,0], -1)
    ball_pos += Controller(10 * math.cos(angle * math.pi / 180), 10* math.sin(angle * math.pi / 180), 25)
    l_img = cv2.circle(l_img, (int(ball_pos.x), int(ball_pos.y)), 25, [200,100,200], -1)
    distance = math.sqrt((ball_pos.x - pos.x)**2 + (ball_pos.y - pos.y)**2)
    if(ball_pos.y <= 50):
        angle = -angle
    if(ball_pos.y >= height - 50):
        print("Game Over senor")
        return True
    if(ball_pos.x >= width - 50 - max_width // 2 or ball_pos.x <= 50 + max_width // 2):
        angle = 180 - angle
    if(distance <= pos.radius + ball_pos.radius):
        theta = math.atan((ball_pos.y - y) /  (ball_pos.x - x))
        theta *= 180 / math.pi
        angle = math.fabs(2 * theta - angle - 180) % 360
        if 2 * theta - angle - 180 > 0:
            angle *= -1
        l_img = cv2.circle(l_img, (int(ball_pos.x), int(ball_pos.y)), 25, [0,0,0], -1)
        ball_pos += Controller(15 * math.cos(angle * math.pi / 180), 15* math.sin(angle * math.pi / 180), 25)
    
        score += 1
    return False

key = '0'
gameOver = False
print("press q to exit:")
score = 0

while key != ord('q') and gameOver == False:

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    frame_width = 720//2
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60), flags=cv2.CASCADE_SCALE_IMAGE)
    
    prepare_arena(l_img, frame)

    for (x,y,w,h) in faces:
        cv2.circle(frame, (x + w//2, y + h//2), w//4 + h//4, (0,0,255), 2)
        roi = frame[y-25:y+h+25, x-25:x+w+25]
        circularmask = np.zeros((w + 50, h + 50, 3), np.uint8)
        cv2.circle(circularmask,(w//2 + 25, h//2 + 25),w//4 + h//4,[255,255,255],thickness=-1)
        
        y_excess = x - frame_width//2
        x_offset = width // 2 - w//2
        y_offset = height - 300
        roi = cv2.bitwise_and(roi, circularmask)
        l_img[y_offset:y_offset+roi.shape[0], x_offset - y_excess:x_offset - y_excess+roi.shape[1]] = roi
        pos.x = x_offset - y_excess + roi.shape[1]//2
        pos.y = height - 300 + roi.shape[0]//2
        pos.radius = w//4 + h//4
        
    cv2.imshow("masked", l_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    gameOver = move_ball(l_img)
    key = cv2.waitKey(1)
else:
    cv2.destroyAllWindows()
    l_img = cv2.putText(l_img,"So soon? Aww (>w<)", (10, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, [255, 255, 255])
    l_img = cv2.putText(l_img,"Score = {0}".format(score), (10, 3*height//5 ), cv2.FONT_HERSHEY_SIMPLEX, 2, [0, 255, 255])
    cv2.imshow("Game over :-(", l_img)
    cv2.waitKey(0)
video_capture.release()
cv2.destroyAllWindows()