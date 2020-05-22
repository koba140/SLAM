from PIL import Image
import numpy as np
import cv2 as cv


def brightness_filter(image, threshold, compression):
    #
    #image is what needs to be filtered
    img = image.resize((int(image.width/compression), int(image.height/compression)))

    img = np.array(img)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY, img)
    cv.threshold(img, threshold, 255, cv.THRESH_BINARY, img)
    
    #cv.cvtColor(img, cv.rgb, img)

    img = Image.fromarray(img)
    img = img.resize((image.width, image.height))
    return img
    
def edges_filter(image, threshold1, threshold2, compression):
    #
    #image is what needs to be filtered
    img = image.resize((int(image.width/compression), int(image.height/compression)))

    img = np.array(img)
    cv.cvtColor(img, cv.COLOR_RGB2BGR, img)
    img = cv.Canny(img, threshold1, threshold2)
    cv.cvtColor(img, cv.COLOR_BGR2RGB, img)

    img = Image.fromarray(img)
    img = img.resize((image.width, image.height))
    return img

def nothing(x):
    pass