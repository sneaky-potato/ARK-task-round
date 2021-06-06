import cv2
import numpy as np
import lvl3_mazeAlgo

class Point():
    def __init__(self, x_coor = 0, y_coor = 0):
        self.x = x_coor
        self.y = y_coor
        self.distance = float('inf')
        self.prev_x = None
        self.prev_y = None
        self.visited = False

img = cv2.imread("./output/lvl2_denoised.png", cv2.IMREAD_COLOR)
out = img.copy()

l,w,t = img.shape
print(l, w, t)

clicks = 0
start = Point(61, 145)
end = Point(409, 142)

path = lvl3_mazeAlgo.greedybfs(out, start, end)
lvl3_mazeAlgo.showPath(out, path)                
cv2.imwrite("./output/lvl3_comparisions/greedybfs.png", out)
cv2.imshow('Result', out)
cv2.waitKey(0)
cv2.destroyAllWindows()