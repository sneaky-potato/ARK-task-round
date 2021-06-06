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

img = cv2.imread("./Input/maze_lv3.png", cv2.IMREAD_COLOR)
out = img.copy()

l,w,t = img.shape
print(l, w, t)

# Denoising
for i in range(l):
    for j in range(w):
        if(out[(i, j)][0] == 230):
            out[(i, j)] = [0,0,0]
        else:
            out[(i,j)] = [255,255,255]

clicks = 0
start = (0, 0)
end = (0, 0)
print("Maze denoisation completed . . .")
cv2.imshow("Denoization result", out)
print("Press Enter key")
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Click to select start point")
cv2.imwrite("./output/lvl2_denoised.png", out)

# Callback function
def setStartEnd(event, x, y, flag, params):
    # checking for left mouse clicks
    global clicks, start, end, out
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicks += 1
        if clicks == 1: 
            start = (x, y)
            print("captured start =", start)
            cv2.circle(out,(x,y),2,(0, 255,0),-1)
            print("Again click to capture end location")
            cv2.imshow("output", out)
            
        elif clicks == 2:
            end = (x, y)
            print("captured end =", end)
            cv2.circle(out,(x,y),2,(0, 0, 255),-1)
            cv2.imshow("output", out)
            cv2.destroyAllWindows()

cv2.namedWindow("output",1)
cv2.imshow("output", out)
cv2.setMouseCallback("output", setStartEnd, 0)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(start,end)

path = lvl3_mazeAlgo.dijkstra(out, Point(start[0], start[1]), Point(end[0], end[1]))
lvl3_mazeAlgo.showPath(out, path)                
cv2.imwrite("./output/lvl3_dijkstra.png", out)
cv2.imshow('Result', out)
cv2.waitKey(0)
cv2.destroyAllWindows()