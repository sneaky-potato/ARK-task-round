import cv2
import numpy as np
import random
import math

class Point():
    def __init__(self, x_coor = 0, y_coor = 0):
        self.x = x_coor
        self.y = y_coor
        self.distance = float('inf')
        self.prev_x = None
        self.prev_y = None
        self.visited = False
        self.obstacle = False

img = cv2.imread("./output/lvl2_denoised.png", cv2.IMREAD_COLOR)
out = img.copy()

l,w,t = img.shape
print(l, w, t)

start = Point(61, 145)
end = Point(409, 142)

img = cv2.imread("./output/lvl2_denoised.png", cv2.IMREAD_COLOR)
print(img.shape)


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
        temp_x = int(start.x*u + end.x*(1-u))
        temp_y = int(start.y*u + end.y*(1-u))
        img[(int(temp_y), int(temp_x))] = [193,182,255]
        if matrix[int(temp_y), int(temp_x)].obstacle == True:
            img[(int(temp_y), int(temp_x))] = [100,100,255] 
            return False
    return True

def step(img, startPoint, endPoint):
    newNode = Point(0, 0)
    theta = math.atan2(endPoint.y - startPoint.y, endPoint.x - startPoint.x)
    newNode.x = startPoint.x + 10*math.cos(theta)
    newNode.y = startPoint.y + 10*math.sin(theta)
    return newNode

def next_nearest(listNodes, point):
    nearestNode = listNodes[0]
    smallest_dist = math.sqrt((listNodes[0].x - point.x)**2+(listNodes[0].y - point.y)**2)
    for samplePoint in listNodes:
        if(math.sqrt((samplePoint.x - point.x)**2 + (samplePoint.y - point.y)**2) < smallest_dist):
            nearestNode = samplePoint
            smallest_dist = math.sqrt((samplePoint.x - point.x)**2 + (samplePoint.y - point.y)**2)

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
    cv2.circle(img, (start.x, start.y), 4, [0, 255, 0], thickness= -1)
    print("Processing . . .")

    while len(pointList):
        randomPoint = point_generate(img, currentPoint)

        currentPoint = next_nearest(pointList, randomPoint)

        nextNode = step(img, currentPoint, randomPoint)
        
        if not is_ok(img, matrix, nextNode.x, nextNode.y):
            continue
        if not obstacle_free(img, matrix, currentPoint, nextNode):
            continue

        # Setting parents
        matrix[int(nextNode.y)][int(nextNode.x)].prev_x = int(currentPoint.x)
        matrix[int(nextNode.y)][int(nextNode.x)].prev_y = int(currentPoint.y)
        pointList.append(nextNode)
        cv2.line(img, (int(currentPoint.x), int(currentPoint.y)), (int(nextNode.x), int(nextNode.y)), (200, 200 , 0), thickness= 2)
        cv2.circle(img, (int(nextNode.x), int(nextNode.y)), 1, (0,100,200), thickness=-1)

        currentPoint.visited = True

        if nextNode.x > end.x - 20 and nextNode.x < end.x + 20 and nextNode.y < end.y + 20 and nextNode.y > end.y - 20:
            found = True
            matrix[end.y][end.x].prev_x = int(nextNode.x)
            matrix[end.y][end.x].prev_y = int(nextNode.y)
            cv2.line(img, (int(end.x), int(end.y)), (int(nextNode.x), int(nextNode.y)), (155, 155 , 0), thickness= 1)
            print("Path finding complete")
            cv2.destroyAllWindows()
            break
        #cv2.imshow("Processing sheee", img)
        #cv2.waitKey(1)
    
    img[(start.y, start.x)] = [0,0 ,255]
    pathFound = []
    if found:
        # Backtracking to find the path
        Pointer = end
        while (Pointer.x != start.x or Pointer.y != start.y):
            Pointer = matrix[matrix[Pointer.y][Pointer.x].prev_y][matrix[Pointer.y][Pointer.x].prev_x]
            pathFound.append((Pointer.x, Pointer.y))
        # print("Cost of Path = ", matrix[end.y][end.y].distance)
    else:
        print("Path could not be found")
    return pathFound
    

def showPath(img, path):
    # color coding path
    for i in path:
        cv2.circle(img, i, 3, (0,0,255), thickness=-1)


cv2.rectangle(img, (end.x - 20, end.y - 20), (end.x + 20, end.y + 20), (50,205,154), thickness=-1)
cv2.circle(img, (end.x, end.y), 3, (0,0,255), thickness=-1)
path = rrt(img, start, end)
showPath(img, path)                
cv2.imwrite("./output/lvl3_comparisions/rrt.png", img)
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
