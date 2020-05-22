"""
Test
"""

from numba import vectorize, jit, njit
from PIL import Image
import numpy as np
import random
import time

start_time = time.time()
SIZE = 1000000

img = Image.open("images/bear.png")
#img2 = Image.new("RGB", (img.width, img.height), color=(4,3,3))
px_data = np.array(list(img.getdata()))
#px_data2 = np.array(list(img2.getdata()))
threshold = 100
#print(px_data + px_data2)

for i in range(20):
    np.clip(px_data, threshold, )


'''
for i in range(20):
    A = np.random.random(SIZE)
    B = np.random.random(SIZE)
    D = np.random.random(SIZE)
    E = np.random.random(SIZE)
    F = np.random.random(SIZE)

    C = np.empty_like(A)
    C = A+B+D+F+E
    print(C)
'''
