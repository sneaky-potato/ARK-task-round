import cv2
import numpy as np

img = cv2.imread("./Input/Level1.png", cv2.IMREAD_COLOR)

l,w,t = img.shape
print(l, w, t)

f = open("./Output/lvl1_message.txt", "w")

colonfound = False
for i in range(l):
    for j in range(w):
        if(chr(img[(i,j)][0]) == ':'):
            colonfound = True
            break
        f.write(chr(img[(i, j)][0]))
    if(colonfound): break
    f.write("\n")
f.close()        
initialpos = (i, j + 1)
distance = w - 1 - j + (l - 1 - i) * w
print("initialpos: = {}, img[initialpos] = {}".format(initialpos, img[initialpos]))
