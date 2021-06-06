import cv2
import numpy as np
import random
import math

class Point():
    def __init__(self, x_coor = 0, y_coor = 0):
        self.horizontal = x_coor
        self.vertical = y_coor
        self.distance = float('inf')
        self.prev_x = None
        self.prev_y = None
        self.visited = False
        self.obstacle = False

img = cv2.imread("maze_lv3.png", cv2.IMREAD_COLOR)
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
step = 100
"""
def setStartEnd(event, x, y, flag, params):
    # checking for left mouse clicks
    global clicks, start, end, out
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicks += 1
        if clicks == 1: 
            start = (x, y)
            print("captured start =", start)
            cv2.circle(out,(x,y),2,(0, 255,0),-1)
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
"""


outpush_element_image = np.zeros((400,600,3), np.uint8)
for i in range(400):
    for j in range(600):
        outpush_element_image[(i, j)] = [255, 255, 255]


cv2.rectangle(outpush_element_image, (100, 50), (120, 350), [0,0,0], thickness= -1)
cv2.rectangle(outpush_element_image, (200, 200), (300, 300), [0,0,0], thickness= -1)
cv2.rectangle(outpush_element_image, (180, 150), (550, 160), [0,0,0], thickness= -1)

img2 = cv2.imread("./output/lvl2_denoised.png", cv2.IMREAD_COLOR)
print(img.shape)
img = np.zeros((img2.shape[0]*2,img2.shape[1]*2,3), np.uint8)
for i in range(l):
    for j in range(w):
        color = img2[(i,j)]
        for n in range(2):
            for m in range(2):
                img[i*2 + n][j*2 + m] = color
def setStartEnd(event, x, y, flag, params):
    # checking for left mouse clicks
    global clicks, start, end, img
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicks += 1
        print("Click on the maze to capture point location")
        if clicks == 1: 
            start = Point(x, y)
            print("captured start =", x, y)
            cv2.circle(img,(x, y),2,(0, 255,0),-1)
            cv2.imshow("output", img)
            print("Again click to capture end location")
            
        elif clicks == 2:
            end = Point(x, y)
            print("captured end =", x, y)
            cv2.circle(img,(x, y),2,(0, 0, 255),-1)
            cv2.imshow("output", img)
            cv2.destroyAllWindows()

cv2.namedWindow("output",1)
cv2.imshow("output", img)
cv2.setMouseCallback("output", setStartEnd, 0)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(start.horizontal, start.vertical, "\n",end.horizontal, end.vertical)

def is_ok(img, matrix, x, y):
    h, w = matrix.shape
    return (x < w and x >= 0 and y < h and y >= 0 and img[int(y)][int(x)][0] != 0 and img[int(y)][int(x)][1] != 0 and img[int(y)][int(x)][2] != 0)

# Returning neighbours of current point
def point_generate(img, point):
    ran_x = random.randint(0, img.shape[1])
    ran_y = random.randint(0, img.shape[0])
    return Point(ran_x, ran_y)

def obstacle_free(img, matrix, Point1, Point2):
    
    # cv2.line(img, (10, int(Point1.x)),(10, int(Point2.x)), [0,0,0])

    start = Point1
    end = Point2
    for i in range(301):
        u = i/300
        temp_x = int(start.horizontal*u + end.horizontal*(1-u))
        temp_y = int(start.vertical*u + end.vertical*(1-u))
        img[(int(temp_y), int(temp_x))] = [193,182,255]
        if matrix[int(temp_y), int(temp_x)].obstacle == True:
            img[(int(temp_y), int(temp_x))] = [100,100,255] 
            return False
    return True

def step(img, startPoint, endPoint):
    newNode = Point(0, 0)
    theta = math.atan2(endPoint.vertical - startPoint.vertical, endPoint.horizontal - startPoint.horizontal)
    newNode.horizontal = startPoint.horizontal + 10*math.cos(theta)
    newNode.vertical = startPoint.vertical + 10*math.sin(theta)
    return newNode

def next_nearest(listNodes, point):
    nearestNode = listNodes[0]
    smallest_dist = math.sqrt((listNodes[0].horizontal - point.horizontal)**2+(listNodes[0].vertical - point.vertical)**2)
    for samplePoint in listNodes:
        if(math.sqrt((samplePoint.horizontal - point.horizontal)**2 + (samplePoint.vertical - point.vertical)**2) < smallest_dist):
            nearestNode = samplePoint
            smallest_dist = math.sqrt((samplePoint.horizontal - point.horizontal)**2 + (samplePoint.vertical - point.vertical)**2)

    return nearestNode

# Main algorithm
def rrt(img, start, end):
    l,w,t = img.shape
    found = False
    matrix = np.full((l, w), None)
    # Making a matrix full of points
    for r in range(l):
        for c in range(w):
            matrix[r][c] = Point(c,r)
            if(img[(r,c)][0] == 0 and img[r][c][1] == 0 and img[r][c][2] == 0): 
                matrix[r][c].obstacle = True
                #print(img[(r,c)], r, c)
    
    print("matrix done")
    pointList = []
    pointList.append(start)
    currentPoint = start
    currentPoint.start = 0
    cv2.circle(img, (start.horizontal, start.vertical), 4, [0, 255, 0], thickness= -1)
    print("Processing . . .")

    while len(pointList):
        randomPoint = point_generate(img, currentPoint)

        currentPoint = next_nearest(pointList, randomPoint)

        nextNode = step(img, currentPoint, randomPoint)
        
        if not is_ok(img, matrix, nextNode.horizontal, nextNode.vertical):
            continue
        if not obstacle_free(img, matrix, currentPoint, nextNode):
            continue

        # Setting parents
        matrix[int(nextNode.vertical)][int(nextNode.horizontal)].prev_x = int(currentPoint.horizontal)
        matrix[int(nextNode.vertical)][int(nextNode.horizontal)].prev_y = int(currentPoint.vertical)
        pointList.append(nextNode)
        cv2.line(img, (int(currentPoint.horizontal), int(currentPoint.vertical)), (int(nextNode.horizontal), int(nextNode.vertical)), (200, 200 , 0), thickness= 2)
        cv2.circle(img, (int(nextNode.horizontal), int(nextNode.vertical)), 1, (0,100,200), thickness=-1)

        currentPoint.visited = True

        if nextNode.horizontal > end.horizontal - 20 and nextNode.horizontal < end.horizontal + 20 and nextNode.vertical < end.vertical + 20 and nextNode.vertical > end.vertical - 20:
            found = True
            matrix[end.vertical][end.horizontal].prev_x = int(nextNode.horizontal)
            matrix[end.vertical][end.horizontal].prev_y = int(nextNode.vertical)
            cv2.line(img, (int(end.horizontal), int(end.vertical)), (int(nextNode.horizontal), int(nextNode.vertical)), (155, 155 , 0), thickness= 1)
            print("Path finding complete")
            cv2.destroyAllWindows()
            break
        #cv2.imshow("Processing sheee", img)
        #cv2.waitKey(1)
    
    img[(start.vertical, start.horizontal)] = [0,0 ,255]
    pathFound = []
    if found:
        # Backtracking to find the path
        Pointer = end
        while (Pointer.horizontal != start.horizontal or Pointer.vertical != start.vertical):
            Pointer = matrix[matrix[Pointer.vertical][Pointer.horizontal].prev_y][matrix[Pointer.vertical][Pointer.horizontal].prev_x]
            pathFound.append((Pointer.horizontal, Pointer.vertical))
        # print("Cost of Path = ", matrix[end.vertical][end.vertical].distance)
    else:
        print("Path could not be found")
    return pathFound
    

def showPath(img, path):
    # color coding path
    for i in path:
        cv2.circle(img, i, 3, (0,0,255), thickness=-1)


cv2.rectangle(img, (end.horizontal - 20, end.vertical - 20), (end.horizontal + 20, end.vertical + 20), (50,205,154), thickness=-1)
cv2.circle(img, (end.horizontal, end.vertical), 3, (0,0,255), thickness=-1)
path = rrt(img, start, end)
showPath(img, path)                
cv2.imwrite("./output/rrt_circle.png", img)
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
