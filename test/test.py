from PIL import Image
import numpy as np
import cv2 as cv
img = Image.open("images/bear.png")
img_array = np.array(img) 

cv.cvtColor(img_array, cv.COLOR_BGR2RGB, img_array)

cv.imshow("im", img_array)
cv.waitKey(100)
pass