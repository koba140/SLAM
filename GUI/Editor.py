import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
from GUI.Controller import *
import GUI.Filter as Filter

class Editor:
    """
    This is a basic template for editor.
    Editors of different media can inherit from this
    """
    def __init__(self, root, size):
        #Settings
        self.size = size #(WIDTH, HEIGHT)
        
        #Working variables
        self.file = None
        self.update_flag = True

        #Other objects
        self.editor = None

        self.main_frame = tk.Frame(root)
        self.main_frame.grid(row=0)
        ########################################################################################################################
        #This block of code is for image display
        self.display_frame = tk.Frame(self.main_frame, width=self.size[0], height=self.size[1])
        self.display_frame.grid(row=0, column=0)

        self.canvas = tk.Canvas(self.display_frame, width=self.size[0], height=self.size[1])
        self.canvas.img = None
        self.canvas.pack()

        ########################################################################################################################
        #This block of code is for editor
        self.Editor_frame = tk.Frame(self.main_frame)
        self.Editor_frame.grid(row=5, column=0)

        options = [
            "No filter",
            "Brightness filter",
            "Edges filter",
            "Corner detector"
        ]
        self.filter = tk.StringVar(self.display_frame)
        self.Filters = tk.OptionMenu(self.Editor_frame, self.filter, *options)
        self.filter.set("No filter")
        self.Filters.grid(row=5, column=5)
    ########################################################################################################################
    def update(self, image):
        #where to put image
        x,y= self.size[0]/2, self.size[1]/2

        self.canvas.img = self.process_image(image, self.filter.get())
        self.canvas.create_image((x,y), image=self.canvas.img)
    ########################################################################################################################
    def process_image(self, image, _filter):
        image = self.fit_screen(image)
        if _filter == "No filter":
            if not type(self.editor) == Controller:
                self.clear()
                self.editor = Controller(self.Editor_frame)
            processed_image = ImageTk.PhotoImage(image=Filter.convert_PIL(image))
            self.update_flag = False

        elif _filter == "Brightness filter":
            if not type(self.editor) == BrightnessController:
                self.clear()
                self.editor = BrightnessController(self.Editor_frame)
            
            processed_image = ImageTk.PhotoImage(image=Filter.convert_PIL(Filter.brightness_filter(image, self.editor.threshold.get(), self.editor.compression.get())))
            
        elif _filter == "Edges filter":
            if not type(self.editor) == EdgesController:
                self.clear()
                self.editor = EdgesController(self.Editor_frame)

            processed_image = ImageTk.PhotoImage(image=Filter.convert_PIL(Filter.edges_filter(image, self.editor.threshold1.get(), self.editor.threshold2.get(), 1)))
        elif _filter == "Corner detector":
            if not type(self.editor) == CornerController:
                self.clear()
                self.editor = CornerController(self.Editor_frame)

            processed_image = ImageTk.PhotoImage(image=Filter.convert_PIL(Filter.corner_detector(image, self.editor.blocksize.get(), self.editor.ksize.get()+1, self.editor.k.get())))
         
        return processed_image
    ########################################################################################################################
    def fit_screen(self, image):
        """
        Returns vc2 images that fit screen resolution
        image.shape[1] - WIDTH (columns)
        image.shape[0] - HEIGHT (rows)
        """
        if  type(image) == Image.Image:
            if image.width < self.size[0] and image.height < self.size[1]:
                if image.width / self.size[0] >= image.height / self.size[1]:
                    image = image.resize((self.size[0], image.height*self.size[0]//image.width))
                else:
                    image = image.resize((image.width*self.size[1]//image.height, self.size[1]))

            if image.width > self.size[0]:
                image = image.resize((self.size[0], int(image.height*self.size[0]/image.width)))
            if image.height > self.size[1]:
                image = image.resize((int(image.width*self.size[1]/image.height), self.size[1]))

        elif type(image) == ImageTk.PhotoImage:
            raise Exception("Can not resize PIL.Imagetk.Photoimage! Please use PIL.Image.Image instead")

        else:  
            if image.shape[1] < self.size[0] and image.shape[0] < self.size[1]:
                if image.shape[1] / self.size[0] >= image.shape[0] / self.size[1]:
                    image = cv.resize(image, (self.size[0], image.shape[0]*self.size[0]//image.shape[1]))
                else:
                    image =cv.resize(image, (image.shape[1]*self.size[1]//image.shape[0], self.size[1]))  

            if image.shape[1] > self.size[0]:
                image = cv.resize(image, (self.size[0], image.shape[0]*self.size[0]//image.shape[1])) 
            if image.shape[0] > self.size[1]:
                image =cv.resize(image, (image.shape[1]*self.size[1]//image.shape[0], self.size[1])) 
        
        return image
    ########################################################################################################################
    def clear(self):
        if self.editor:
            del self.editor

        self.canvas.delete("all")
        self.update_flag = True 
    ########################################################################################################################
    def destroy(self):
        self.main_frame.destroy()

############################################################################################################################
class VideoPlayer(Editor):
    """
    This class can be used to play video files
    """

    def __init__(self, root, size, video):
        super().__init__(root, size)
        
        #Settings
        self.framerate = video.get(cv.CAP_PROP_FPS)
        self.filetypes = [("Video File", ".mp4")]
        self.playback_speed = self.framerate

        #Working variables
        self.current_frame = 0
        self.rewind = False

        #Other objects
        self.video = video

        self.rewind_switch = tk.Button(self.Editor_frame, text="Rewind", command=self.rewind_vid)
        self.rewind_switch.grid(row=0, column=0)

        self.playback_speed_bar = tk.Scale(self.Editor_frame, from_=1, to=10, orient="horizontal", label="Playback Speed", length=300)
        self.playback_speed_bar.grid(row=0, column=1)

    ############################################################################################################################
    def next_frame(self):
        """
        This method returns a boolean that indicates whether or not a frame exists an the following frame in a video
        """
        #This sets previous frame as a current frame to play the video in reverse
        if self.rewind:
            self.current_frame = self.current_frame - self.playback_speed
            self.video.set(cv.CAP_PROP_POS_FRAMES, self.current_frame)
        else:
            self.current_frame = self.current_frame + self.playback_speed
            self.video.set(cv.CAP_PROP_POS_FRAMES, self.current_frame - 1)

        return self.video.read() 
    ############################################################################################################################
    def update(self):
        isFrame, frame = self.next_frame()
        if isFrame:
            super().update(frame)
        
        self.playback_speed = self.playback_speed_bar.get()

    ############################################################################################################################
    def rewind_vid(self):
        if self.rewind:
            self.rewind = False
        else:
            self.rewind = True
class ImageEditor(Editor):
    def __init__(self, root, size, image):
        self.image = image
        super().__init__(root, size)
    
    def update(self):
        super().update(self.image)
