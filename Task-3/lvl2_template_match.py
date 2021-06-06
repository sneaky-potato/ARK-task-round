import cv2
import numpy as np

img = cv2.imread("./Input/Level1.png", cv2.IMREAD_COLOR)
lvl2 = cv2.imread("./Input/zucky_elon.png", cv2.IMREAD_COLOR)
l,w, t = img.shape

initialpos = (6, 94)
template = np.zeros((200,150,3), np.uint8)

init_y = initialpos[0]
init_x = initialpos[1]
i = j = k = iter_y = iter_x = 0

# transforming image into 200 x 150
while i < 200:
    j = 0
    while j < 150:
        template[(i,j)] = img[init_y + iter_y, init_x + iter_x]
        iter_x+=1
        j+=1
        if(iter_x + init_x== 177): 
            iter_y += 1
            iter_x = 0
        if(iter_y != 0): init_x = 0
    i+=1
print('Image transformation complete', template.shape)
cv2.imshow('find it capn', template)
cv2.imwrite('./Output/lvl2_transformed.png', template)
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Initiating template search in ./Input/zucky_elon.png")
i = j = k = 0

while (i < lvl2.shape[0] - 200):
    j = 0
    while (j < lvl2.shape[1] - 150):
        iter_x = iter_y = 0
        if(lvl2[(i,j)] == template[(0,0)]).all():

            while iter_y < 200:
                iter_x = 0
                while iter_x < 150:
                    if(lvl2[(i + iter_y, j + iter_x)] != template[(iter_y, iter_x)]).all(): break
                    iter_x+=1
                iter_y += 1
            if(iter_y == 200 and iter_x == 150):
                print("Search complete")
                print("Coordinates = ({} {})".format(i, j))
                cv2.rectangle(lvl2, (j, i), (j + 150, i + 200), (0, 255, 0), thickness=1)
                cv2.imshow("Search result", lvl2)
                cv2.imwrite("./Output/lvl2_zucky_elon_search.png", lvl2)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break
        j+=1
    i+=1