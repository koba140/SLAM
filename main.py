from PIL import Image, ImageTk
import os
import tkinter
from GUI.IProc import IProc

window = tkinter.Tk()

iproc = IProc(window)

while window:
    iproc.update()
    try:
        window.update_idletasks()
        window.update()
    except Exception as exception:
        print(exception)
        break


