import os
from PIL import ImageTk, Image
from tkinter import Tk, Canvas, PhotoImage, mainloop
import time


MOD = 1
WID = 1500
HEI = 900


images = []
for img in os.listdir("images"):    
    images.append(Image.open("images/" + img))

window = Tk()
threshhold = 0
def mouse(event):
    x, y = event.x, event.y
    threshhold = x

window.bind("<Motion>", mouse)
canvas = Canvas(window, width=WID, height=HEI, bg="#000000")
canvas.pack()
canvas.image = None



'''
for i in range(150):
    canvas.delete('all')
canvas.img = ImageTk.PhotoImage(image=images[0])
canvas.create_image((WID/2, HEI/2), image=canvas.img, state="normal")
'''

i=0

draw = Image.new("RGB", (WID, HEI))
while True:
    threshhold = window.winfo_pointerx()
    #Index
    idx = 0#i%len(images)-1
    px_data = images[idx].load()
    draw_px = draw.load()
    for y in range(images[idx].height):
        for x in range(images[idx].width):
            px = px_data[x,y]
            brightness = (px[0] + px[1] + px[2])/3
            #print(px , end=" ")
            if brightness>=threshhold:
                draw_px[x,y] = (255, 255, 255)
            else:
                draw_px[x,y] = (0, 0, 0)

            #print(px)
    print(i)
    print(threshhold)


    i = i+1
    #threshhold = threshhold + 8
    if threshhold > 255:
        threshhold = 0
    #time.sleep(0.01)
    try:
        canvas.img = 0
        canvas.img = ImageTk.PhotoImage(image=draw)
        canvas.create_image((WID/2, HEI/2), image=canvas.img, state="normal")
        window.update_idletasks()
        window.update()
       
        #time.sleep(0.01)
    except Exception as exception:
        print(exception)
        break
    
   