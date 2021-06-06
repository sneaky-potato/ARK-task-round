import numpy as np
import math

class Point():
    def __init__(self, x_coor = 0, y_coor = 0):
        self.x = x_coor
        self.y = y_coor
        self.distance = float('inf')
        self.prev_x = None
        self.prev_y = None
        self.visited = False


def is_ok(img, matrix, x, y):
    h, w = matrix.shape
    return (x < w and x >= 0 and y < h and y >= 0 and matrix[y][x].visited == False and (img[(y,x)] != [0,0,0]).any())

# Returning neighbours of current point
def pop_element_adj(img, matrix, Point):
    adj = []
    x = Point.x
    y = Point.y
    if(is_ok(img, matrix, x - 1, y)): adj.append((matrix[y][x-1]))
    if(is_ok(img, matrix, x + 1, y)): adj.append((matrix[y][x+1]))
    if(is_ok(img, matrix, x, y-1)): adj.append((matrix[y-1][x]))
    if(is_ok(img, matrix, x, y+1)): adj.append((matrix[y+1][x]))
    return adj
def hue(Point1, Point2):
    return math.sqrt((Point1.x - Point2.x)**2 + (Point1.y - Point2.y)**2)
# Main algorithm
def dijkstra(img, start, end):
    l,w,t = img.shape
    found = False
    open_queue = []
    open_queue.append(start)
    start.distance = 0
    matrix = np.full((l, w), None)

    # Making a matrix full of points
    for r in range(l):
        for c in range(w):
            matrix[r][c] = Point(c,r)
    
    while len(open_queue):
        # Getting point with lowest distance in queue
        currentPoint = open_queue[0]
        current_index = 0
        for index, item in enumerate(open_queue):
            if item.distance < currentPoint.distance:
                currentPoint = item
                current_index = index
        open_queue.pop(current_index)
        img[(currentPoint.y, currentPoint.x)] = [220, 32, 45]
        currentPoint.visited = True

        if (currentPoint.y == end.y and currentPoint.x == end.x):
            found = True
            print("Path finding complete")
            break

        for nextNode in pop_element_adj(img, matrix, currentPoint):
            dist = 1
            if(nextNode.y - currentPoint.y and nextNode.x - currentPoint.x): dist = 1.4
            if nextNode in open_queue:
                if currentPoint.distance + dist < nextNode.distance:
                    matrix[nextNode.y][nextNode.x].distance = currentPoint.distance + dist
                    nextNode.distance = currentPoint.distance + dist
                    open_queue.append(nextNode)
                    matrix[nextNode.y][nextNode.x].prev_x = currentPoint.x
                    matrix[nextNode.y][nextNode.x].prev_y = currentPoint.y
            else:
                matrix[nextNode.y][nextNode.x].distance = currentPoint.distance + dist
                nextNode.distance = currentPoint.distance + dist
                open_queue.append(nextNode)
                matrix[nextNode.y][nextNode.x].prev_x = currentPoint.x
                matrix[nextNode.y][nextNode.x].prev_y = currentPoint.y

    img[(start.y, start.x)] = [0, 255 ,0]
    pathFound = []
    if found:
        # Backtracking to find the path
        Pointer = end
        while (Pointer.x != start.x or Pointer.y != start.y):
            Pointer = matrix[matrix[Pointer.y][Pointer.x].prev_y][matrix[Pointer.y][Pointer.x].prev_x]
            pathFound.append((Pointer.x, Pointer.y))
        print("Cost of Path = ", matrix[end.y][end.x].distance)
    else:
        print("Path could not be found")
    return pathFound

def bfs(img, start, end):
    l,w,t = img.shape
    found = False
    open_queue = []
    open_queue.append(start)
    start.distance = 0
    matrix = np.full((l, w), None)

    # Making a matrix full of points
    for r in range(l):
        for c in range(w):
            matrix[r][c] = Point(c,r)
    
    while len(open_queue):
        # Getting point with lowest distance in queue
        currentPoint = open_queue[0]
        open_queue.pop(0)
        img[(currentPoint.y, currentPoint.x)] = [220, 32, 45]
        currentPoint.visited = True

        if (currentPoint.y == end.y and currentPoint.x == end.x):
            found = True
            print("Path finding complete")
            break

        for nextNode in pop_element_adj(img, matrix, currentPoint):
            dist = 1
            if nextNode in open_queue:
                if currentPoint.distance + dist < nextNode.distance:
                    matrix[nextNode.y][nextNode.x].distance = currentPoint.distance + dist
                    nextNode.distance = currentPoint.distance + dist
                    open_queue.append(nextNode)
                    matrix[nextNode.y][nextNode.x].prev_x = currentPoint.x
                    matrix[nextNode.y][nextNode.x].prev_y = currentPoint.y
            else:
                matrix[nextNode.y][nextNode.x].distance = currentPoint.distance + dist
                nextNode.distance = currentPoint.distance + dist
                open_queue.append(nextNode)
                matrix[nextNode.y][nextNode.x].prev_x = currentPoint.x
                matrix[nextNode.y][nextNode.x].prev_y = currentPoint.y

    img[(start.y, start.x)] = [0, 255 ,0]
    pathFound = []
    if found:
        # Backtracking to find the path
        Pointer = end
        while (Pointer.x != start.x or Pointer.y != start.y):
            Pointer = matrix[matrix[Pointer.y][Pointer.x].prev_y][matrix[Pointer.y][Pointer.x].prev_x]
            pathFound.append((Pointer.x, Pointer.y))
        print("Cost of Path = ", matrix[end.y][end.x].distance)
    else:
        print("Path could not be found")
    return pathFound

def astar(img, start, end):
    l,w,t = img.shape
    found = False
    open_queue = []
    open_queue.append(start)
    start.distance = 0
    matrix = np.full((l, w), None)

    # Making a matrix full of points
    for r in range(l):
        for c in range(w):
            matrix[r][c] = Point(c,r)

    while len(open_queue):
        currentPoint = open_queue[0]
        current_index = 0
        for index, item in enumerate(open_queue):
            if item.distance + hue(item, end) < currentPoint.distance + hue(currentPoint, end):
                currentPoint = item
                current_index = index
        open_queue.pop(current_index)
        img[(currentPoint.y, currentPoint.x)] = [220, 100, 45]
        currentPoint.visited = True
        #closed_queue.append(currentPoint)

        if (currentPoint.y == end.y and currentPoint.x == end.x):
            found = True
            print("Path finding complete")
            break

        for nextNode in pop_element_adj(img, matrix, currentPoint):
            dist = 1
            if nextNode in open_queue:
                if nextNode.distance > currentPoint.distance + dist:
                    nextNode.distance = currentPoint.distance + dist
                    nextNode.prev_x = currentPoint.x
                    nextNode.prev_y = currentPoint.y
                    matrix[nextNode.y][nextNode.x].prev_x = currentPoint.x
                    matrix[nextNode.y][nextNode.x].prev_y = currentPoint.y
            else:
                nextNode.distance = currentPoint.distance + dist
                open_queue.append(nextNode)
                img[(nextNode.y, nextNode.x)] = [220, 32, 45]
                nextNode.prev_x = currentPoint.x
                nextNode.prev_y = currentPoint.y
                matrix[nextNode.y][nextNode.x].prev_x = currentPoint.x
                matrix[nextNode.y][nextNode.x].prev_y = currentPoint.y

    img[(start.y, start.x)] = [0,255,0]

    anotherPath = []
    if found:
        anotherPath.append((end.x, end.y))
        Pointer = end
        while (Pointer.x != start.x or Pointer.y != start.y):
            Pointer = matrix[matrix[Pointer.y][Pointer.x].prev_y][matrix[Pointer.y][Pointer.x].prev_x]
            anotherPath.append((Pointer.x, Pointer.y))
        anotherPath.append((start.x, start.y))
        print("Cost of Path = ", matrix[end.y][end.x].distance)
    else:
        print("Path could not be found")
    return anotherPath

def showPath(img, path):
    # color coding path
    for i in path:
        img[(i[1], i[0])] = [0,255,0]


def greedybfs(img, start, end):
    l,w,t = img.shape
    found = False
    open_queue = []
    open_queue.append(start)
    start.distance = 0
    matrix = np.full((l, w), None)

    # Making a matrix full of points
    for r in range(l):
        for c in range(w):
            matrix[r][c] = Point(c,r)

    while len(open_queue):
        currentPoint = open_queue[0]
        current_index = 0
        for index, item in enumerate(open_queue):
            if hue(item, end) < hue(currentPoint, end):
                currentPoint = item
                current_index = index
        open_queue.pop(current_index)
        img[(currentPoint.y, currentPoint.x)] = [220, 100, 45]
        currentPoint.visited = True
        #closed_queue.append(currentPoint)

        if (currentPoint.y == end.y and currentPoint.x == end.x):
            found = True
            print("Path finding complete")
            break

        for nextNode in pop_element_adj(img, matrix, currentPoint):
            dist = 1
            if nextNode in open_queue:
                if nextNode.distance > currentPoint.distance + dist:
                    nextNode.distance = currentPoint.distance + dist
                    nextNode.prev_x = currentPoint.x
                    nextNode.prev_y = currentPoint.y
                    matrix[nextNode.y][nextNode.x].prev_x = currentPoint.x
                    matrix[nextNode.y][nextNode.x].prev_y = currentPoint.y
            else:
                nextNode.distance = currentPoint.distance + dist
                open_queue.append(nextNode)
                img[(nextNode.y, nextNode.x)] = [220, 32, 45]
                nextNode.prev_x = currentPoint.x
                nextNode.prev_y = currentPoint.y
                matrix[nextNode.y][nextNode.x].prev_x = currentPoint.x
                matrix[nextNode.y][nextNode.x].prev_y = currentPoint.y

    img[(start.y, start.x)] = [0,255,0]
    img[(start.y, start.x)] = [0, 255 ,0]
    pathFound = []
    if found:
        # Backtracking to find the path
        Pointer = end
        while (Pointer.x != start.x or Pointer.y != start.y):
            Pointer = matrix[matrix[Pointer.y][Pointer.x].prev_y][matrix[Pointer.y][Pointer.x].prev_x]
            pathFound.append((Pointer.x, Pointer.y))
        print("Cost of Path = ", matrix[end.y][end.x].distance)
    else:
        print("Path could not be found")
    return pathFound
