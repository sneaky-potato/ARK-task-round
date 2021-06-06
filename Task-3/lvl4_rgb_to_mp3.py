import cv2
import numpy as np

img = cv2.imread("./output/treasure_mp3.png", cv2.IMREAD_COLOR)

l,w,t = img.shape
print(l, w, t)
matr = np.full((l, w), None)

f = open("./output/lvl4_binary_file.dat", "wb")

colonfound = False
for i in range(l):
    for j in range(w):
        f.write(img[(i, j)][0])
f.close()
print("Done writing")