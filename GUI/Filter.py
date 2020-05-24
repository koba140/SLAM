from PIL import Image
import numpy as np
import cv2 as cv


"""
In this module, functions take and return opencv compatible images 

Use convert_PIL() function to get PIL compatible functions
"""
######################################################
#image.shape[1]-width
#image.shape[0]-height
def brightness_filter(image, threshold, compression):

    img = cv.resize(image, (int(image.shape[1]//compression), int(image.shape[0]//compression)))

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.threshold(img, threshold, 255, cv.THRESH_BINARY, img)

    img = cv.resize(img, (image.shape[1], image.shape[0]))
    return img
    
def edges_filter(image, threshold1, threshold2, compression = 1):
    #
    #image is what needs to be filtered
    img = cv.resize(image, (int(image.shape[1]//compression), int(image.shape[0]//compression)))

    img = cv.Canny(img, threshold1, threshold2)

    img = cv.resize(img, (image.shape[1], image.shape[0]))
    return img

def corner_detector(image, blocksize, ksize, k, borderType=cv.BORDER_CONSTANT):
    img = image
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = np.float32(img)

    corners = cv.cornerHarris(img, blocksize, ksize, k, borderType=borderType)
    #corners = cv.dilate(corners, None)

    image[corners>0.005*corners.max()]=[0,0,255]
    image[corners<0]=[0,255,0]

   


    return image

def convert_PIL(image):
    img = None
    img = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    return Image.fromarray(img)


def nothing(x):
    pass