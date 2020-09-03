#################################################################################
#This block allows to run main.py by running this file
import sys 
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#################################################################################
from PIL import Image
import numpy as np
import cv2 as cv
import math
import json


"""
In this module, functions take and return opencv compatible images 

Use convert_PIL() function to get PIL compatible images
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

def assign_color(image):
    """This function takes opencv image and returns its average color in RGB"""
    x,y = image.shape[1], image.shape[0]
    return cv.cvtColor(cv.resize(image, (1,1)), cv.COLOR_BGR2RGB)[0,0]

def find_color(color, dataset):
    index = json.loads(open(dataset+"index.json").read())
    best_match = [450, ""]
    for img in index:
        color2 = (img[1][0], img[1][1], img[1][2])
        dist = compare_color(color, color2)
        if  dist < best_match[0]:
            best_match[0] = dist
            best_match[1] = img[0]
    
    return best_match[1]
        
def compare_color(color1, color2):
    """
    This function shows distance between colors in a 3D RGB allignment
    """
    return math.sqrt((color1[0]-color2[0])**2+(color1[1]-color2[1])**2+(color1[2]-color2[2])**2)

def Build_from_images(image, scale, dataset):
    x,y = math.floor(image.shape[1]/scale), math.floor(image.shape[0]/scale)

    result = None
    row= None
    for i in range(y):
        for j in range(x):
            img = image[i*scale:(i+1)*scale, j*scale:(j+1)*scale]
            if type(row) == type(None):
                row = cv.resize(cv.imread(dataset+find_color(assign_color(img), dataset)), (scale,scale))
            else:
                row2 = cv.hconcat([row, cv.resize(cv.imread(dataset+find_color(assign_color(img), dataset)), (scale,scale))])
                row = row2
        if not type(row) == type(None):
            if type(result)==type(None):
                result = row
                row=None
            else:
                result2 = cv.vconcat([result, row])
                result= result2
                row = None

            
    return result


def convert_PIL(image):
    img = None
    img = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    return Image.fromarray(img)


def nothing(x):
    pass

#find_color((123,43,200), "BWI/image_datasets/flower_images/")