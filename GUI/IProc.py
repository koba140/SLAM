import cv2 as cv
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import GUI.Filter as Filter
class IProc:

    def __init__(self, root):
        root.title("IProc")
        
        self.size = (800, 800) #(WIDTH, HEIGHT)
        self.max_fps = 200
        self.frame_timer = time.time()
        self.update_flag = False
        self.video_flag = False
        self.subeditor = None
        self.image = None #Image.new("RGB", size)
        self.videoplayer = None
        self.filetypes = [("All Files",".jpg"), ("All Files",".png"), ("All Files",".mp4"),
                          ("Image File",".jpg"), ("Image File",".png"),
                          ("Video File", ".mp4")]
        ########################################################################################################################
        #This block of code is for image display
        self.display_frame = tk.Frame(root, width=self.size[0], height=self.size[1])
        self.display_frame.grid(row=0, column=0)

        self.canvas = tk.Canvas(self.display_frame, width=self.size[0], height=self.size[1])
        self.canvas.img = None
        self.canvas.pack()
        ########################################################################################################################
        #This block of code is for editor
        self.Editor_frame = tk.Frame(root)
        self.Editor_frame.grid(row=1, column=0)


        self.fps_trackbar = tk.Scale(self.Editor_frame, from_=1, to=120, orient="horizontal", label="FPS", length=200)
        self.fps_trackbar.set(50)
        self.fps_trackbar.grid(row=5, column=0)

        self.Open_but = tk.Button(self.Editor_frame, text="Open", command=self.get_file)
        self.Open_but.grid(row=5, column=1)


        options = [
            "No filter",
            "Brightness filter",
            "Edges filter"
        ]
        self.filter = tk.StringVar(self.display_frame)
        self.Filters = tk.OptionMenu(self.Editor_frame, self.filter, *options)
        self.Filters.bind("<Enter>", self.start_updating_display)
        self.Filters.bind("<Leave>", self.end_updating_diplay)
        self.filter.set("No filter")
        self.Filters.grid(row=5, column=2)
        

        
        
    
    ########################################################################################################################
    #This block of code updates the display
    def update(self):
        if time.time()-self.frame_timer >= 1/self.max_fps:

            if self.video_flag and not self.videoplayer is None:
                isFrame, self.image = self.videoplayer.next_frame()
                self.image = self.fit_screen(self.image)

                if not isFrame:
                    self.video_flag = False
                    return 


            if (self.update_flag or self.video_flag) and not self.image is None:
                #where to put image
                x,y= self.size[0]/2, self.size[1]/2

                self.canvas.img = self.process_image(self.image, self.filter.get())
                self.canvas.create_image((x,y), image=self.canvas.img)
                
            self.max_fps = self.fps_trackbar.get()
            self.frame_timer = time.time()

    ########################################################################################################################
    def process_image(self, image, _filter):
        if _filter == "No filter":
            self.apply()
            processed_image = ImageTk.PhotoImage(image=Filter.convert_PIL(image))
            self.update_flag = False

        elif _filter == "Brightness filter":
            if not type(self.subeditor) == BrightnessEditor:
                self.apply()
                self.subeditor = BrightnessEditor(self.Editor_frame, self)
            
            processed_image = ImageTk.PhotoImage(image=Filter.convert_PIL(Filter.brightness_filter(image, self.subeditor.threshold.get(), self.subeditor.compression.get())))
            
        elif _filter == "Edges filter":
            if not type(self.subeditor) == EdgesEditor:
                self.apply()
                self.subeditor = EdgesEditor(self.Editor_frame, self)

            processed_image = ImageTk.PhotoImage(image=Filter.convert_PIL(Filter.edges_filter(image, self.subeditor.threshold1.get(), self.subeditor.threshold2.get(), 1)))
        
        print(_filter)
        return processed_image
    ########################################################################################################################

    def get_file(self):
        self.canvas.delete("all")
        try:
            path = filedialog.askopenfilename(filetypes=self.filetypes)

            if path.endswith(".mp4"):
                self.videoplayer = VideoPlayer(cv.VideoCapture(path))
                self.video_flag = True
            elif path.endswith(".jpg") or path.endswith(".png"):    
                self.image = cv.imread(path)
                self.image = self.fit_screen(self.image)

            self.update_flag = True
        except Exception as exception:
            print("Couldn't load a file")
            print(exception)

    ########################################################################################################################
    def fit_screen(self, image):
        """
        Returns vc2 images that fit screen resolution
        image.shape[1] - WIDTH (columns)
        image.shape[0] - HEIGHT (rows)
        """
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
    def apply(self):
        if self.subeditor:
            self.subeditor.Frame.destroy()

        self.canvas.delete("all")
        self.update_flag = True
    
    ########################################################################################################################
    def start_updating_display(self, filler = None):
        self.update_flag = True

    def end_updating_diplay(self, filler = None):
        self.update_flag = False



################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################




class VideoPlayer:
    """
    This class can be used to play video files
    """

    def __init__(self, video, screen):
        self.video = video
        self.isFrame = False
        self.current_frame = 0
        self.framerate = video.get(cv.CAP_PROP_FPS)

        


    def next_frame(self, reverse=False):
        """
        This method returns a boolean that indicates whether or not a frame exists an the following frame in a video
        """

        #This sets previous frame as a current frame to play the video in reverse
        if reverse:
            self.current_frame = self.current_frame - 1
            self.video.set(cv.CAP_PROP_POS_FRAMES, self.current_frame)

        #This keeps track of current frame 
        return self.video.read() 
        self.current_frame = self.current_frame + 1


class BrightnessEditor:

    def __init__(self, root, master):
        
        self.Frame = tk.Frame(root)
        self.Frame.grid(row=4, columnspan=4)

        self.threshold = tk.Scale(self.Frame, from_=0, to=255, orient="horizontal", label="Threshold", length=300)
        self.threshold.bind("<Enter>", master.start_updating_display)
        self.threshold.bind("<Leave>", master.end_updating_diplay)
        self.threshold.grid(row=0, column=0)

        self.compression = tk.Scale(self.Frame, from_=1, to=5, orient="horizontal", label="Compression", resolution=0.1)
        self.compression.bind("<Enter>", master.start_updating_display)
        self.compression.bind("<Leave>", master.end_updating_diplay)

        self.compression.grid(row=0, column=1)

    
class EdgesEditor:
    def __init__(self, root, master):
        
        self.Frame = tk.Frame(root)
        self.Frame.grid(row=4, columnspan=4)

        self.threshold1 = tk.Scale(self.Frame, from_=0, to=255, orient="horizontal", label="Threshold1", length=300)
        self.threshold1.bind("<Enter>", master.start_updating_display)
        self.threshold1.bind("<Leave>", master.end_updating_diplay)
        self.threshold1.grid(row=0, column=0)

        self.threshold2 = tk.Scale(self.Frame, from_=0, to=255, orient="horizontal", label="threshold2", length=300)
        self.threshold2.bind("<Enter>", master.start_updating_display)
        self.threshold2.bind("<Leave>", master.end_updating_diplay)
        self.threshold2.grid(row=0, column=1)