import json
import os
from PIL import Image
def assign_color(_path):
    try:
        return Image.open(_path).resize((1,1)).load()[0,0]
    except:
        return 0


path = os.getcwd()+"/BWI/image_datasets/flowers_google"
f=[]

for root, directories, files in os.walk(path):
    f=files

img_set = []

for imgfile in f:
   img_set.append((imgfile, assign_color("BWI/image_datasets/flowers_google/"+imgfile)))

print(json.dumps(img_set))


