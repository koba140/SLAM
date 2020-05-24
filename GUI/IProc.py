import cv2 as cv
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import GUI.Editor as Editor
class IProc:

    def __init__(self, root):
        
        self.size = (700, 700) #(Width, Height)
        self.max_fps = 40

        #Supported filetypes
        self.filetypes = [("All Files",".jpg"), ("All Files",".png"), ("All Files",".mp4"),
                          ("Image File",".jpg"), ("Image File",".png"),
                          ("Video File", ".mp4")]


        self.frame_timer = time.time()
        self.file = None

        ########################################################################################################################
        self.app_frame = tk.Frame(root)
        self.app_frame.grid(row=5)

        self.fps_trackbar = tk.Scale(self.app_frame, from_=1, to=120, orient="horizontal", label="FPS", length=200)
        self.fps_trackbar.set(50)
        self.fps_trackbar.grid(row=0, column=0)

        self.Open_but = tk.Button(self.app_frame, text="Open", command=self.get_file)
        self.Open_but.grid(row=0, column=1)


        ########################################################################################################################
        self.editor_frame = tk.Frame(root, width=self.size[0], height=self.size[1])
        self.editor_frame.grid(row=0)

        self.editor = None
    ########################################################################################################################
    #This block of code updates the display
    def update(self):
        if time.time()-self.frame_timer >= 1/self.max_fps:
            if not self.editor is None:
                self.editor.update()

            self.max_fps = self.fps_trackbar.get()
            self.frame_timer = time.time()
    ########################################################################################################################
    def get_file(self):
        #self.canvas.delete("all")
        try:
            path = filedialog.askopenfilename(filetypes=self.filetypes)

            if path.endswith(".mp4"):
                if not self.editor is None:
                    self.editor.destroy()
                self.editor = Editor.VideoPlayer(self.editor_frame, self.size, cv.VideoCapture(path))
            elif path.endswith(".jpg") or path.endswith(".png"):   
                if not self.editor is None:
                    self.editor.destroy() 
                self.editor = Editor.ImageEditor(self.editor_frame, self.size, cv.imread(path))

        except Exception as exception:
            print("Couldn't load a file")
            print(exception)

    
            
    
    
    

