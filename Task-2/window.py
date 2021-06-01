import cv2
import numpy as np
import random
import math
import winsound

class Controller():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Controller(self.x + other.x, self.y + other.y)

height = 720
width = 1280

score = 0

window = np.zeros((height, width, 3), np.uint8)

pos = Controller(width / 2, height - 100)
ball_pos = Controller(width / 2, height / 2)
angle = random.randint(20, 340)
if 160 <= angle <= 200:
    angle = 90

window = cv2.circle(window, (int(ball_pos.x), int(ball_pos.y)), 50, [200,100,200], -1)
window = cv2.circle(window, (int(pos.x), int(pos.y)), 50, [255,255,200], 2)
distance = 10

def tap_sound(filename):
    winsound.PlaySound("./sound/{}.wav".format(filename), winsound.SND_ASYNC | winsound.SND_ALIAS )

def control_char(window):
    global pos
    global key
    if key == ord('d') and pos.x <= width - 50:
        window = cv2.circle(window, (int(pos.x), int(pos.y)), 50, [0,0,0], 2)
        pos = pos + Controller(distance, 0)
        window = cv2.circle(window, (int(pos.x), int(pos.y)), 50, [255,255,200], 2)
    elif key == ord('a') and pos.x >= 50:
        window = cv2.circle(window, (int(pos.x), int(pos.y)), 50, [0,0,0], 2)
        pos = pos + Controller(-distance, 0)
        window = cv2.circle(window, (int(pos.x), int(pos.y)), 50, [255,255,200], 2)

def move_ball(window):
    global ball_pos
    global angle
    global pos
    global score
    window = cv2.circle(window, (int(ball_pos.x), int(ball_pos.y)), 50, [0,0,0], -1)
    ball_pos += Controller(1 * math.cos(angle * math.pi / 180), 1* math.sin(angle * math.pi / 180))
    window = cv2.circle(window, (int(ball_pos.x), int(ball_pos.y)), 50, [200,100,200], -1)
    distance = math.sqrt((ball_pos.x - pos.x)**2 + (ball_pos.y - pos.y)**2)
    if(ball_pos.y <= 50):
        tap_sound('pingpong')
        angle = -angle
    if(ball_pos.y >= height - 50):
        print("Game Over senor")
        return True
    if(ball_pos.x >= width - 50 or ball_pos.x <= 50):
        tap_sound('pingpong')
        angle = 180 - angle
    if(distance <= 100 and distance >= 20):
        tap_sound('score')
        theta = math.atan((ball_pos.y - pos.y) /  (ball_pos.x - pos.x))
        theta *= 180 / math.pi
        angle = (2 * theta - angle - 180) % 360
        score += 1
    return False

cv2.imshow("game", window)
key = cv2.waitKey(0)
gameOver = False
print("press q to exit:")
while key != ord('q') and gameOver == False:
    cv2.imshow("game", window)
    control_char(window)
    gameOver = move_ball(window)
    key = cv2.waitKey(1)
else:
    cv2.destroyAllWindows()
    window = cv2.putText(window,"So soon? Aww (>w<)", (10, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, [255, 255, 255])
    window = cv2.putText(window,"Score = {0}".format(score), (10, 3*height//5 ), cv2.FONT_HERSHEY_SIMPLEX, 2, [0, 255, 255])
    cv2.imshow("Game over :-(", window)
    cv2.waitKey(0)