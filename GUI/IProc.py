import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import GUI.Filter as Filter
class IProc:

    def __init__(self, root):
        root.title("IProc")
        
        self.size = (800, 800)
        self.update_flag = False
        self.subeditor = None
        self.image= None #Image.new("RGB", size)
        self.update_flag = False
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

        self.Open_but = tk.Button(self.Editor_frame, text="Open", command=self.get_pic)
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
        

        
        
    
    def update(self):
        ########################################################################################################################
        #This block of code updates the display
        if self.update_flag and self.image:
            #where to put image
            x,y= self.size[0]/2, self.size[1]/2

            if self.filter.get() == "No filter":
                self.apply()
                self.canvas.img = ImageTk.PhotoImage(image=self.image)
                self.canvas.create_image((x,y), image=self.canvas.img)
                
                self.update_flag = False

            elif self.filter.get() == "Brightness filter":
                if not type(self.subeditor) == BrightnessEditor:
                    self.apply()
                    self.subeditor = BrightnessEditor(self.Editor_frame, self)
                
                self.canvas.img = ImageTk.PhotoImage(image=Filter.brightness_filter(self.image, self.subeditor.threshold.get(), self.subeditor.compression.get()))
                self.canvas.create_image((x,y), image=self.canvas.img)
                
            
            elif self.filter.get() == "Edges filter":
                if not type(self.subeditor) == EdgesEditor:
                    self.apply()
                    self.subeditor = EdgesEditor(self.Editor_frame, self)

                self.canvas.img = ImageTk.PhotoImage(image=Filter.edges_filter(self.image, self.subeditor.threshold1.get(), self.subeditor.threshold2.get(), 1))
                self.canvas.create_image((x,y), image=self.canvas.img)
                
            else:
                #print()
                pass

    def get_pic(self):
        self.canvas.delete("all")
        try:
            path=filedialog.askopenfilename(filetypes=[("Image File",'.jpg'), ("Image File",'.png')])
            self.image = Image.open(path)
            if self.image.width > self.size[0]:
                self.image = self.image.resize((self.size[0], int(self.image.height*self.size[0]/self.image.width)))
            if self.image.height > self.size[1]:
                self.image = self.image.resize((int(self.image.width*self.size[1]/self.image.height), self.size[1]))    
            self.update_flag = True
        except Exception as exception:
            print("Couldn't load a file")
            print(exception)

    def apply(self):
        if self.subeditor:
            self.subeditor.Frame.destroy()
        if self.image:
            self.canvas.delete("all")
            self.update_flag = True
        
        else:
            print("No image to apply filter!")
            

    def start_updating_display(self, filler = None):
        self.update_flag = True

    def end_updating_diplay(self, filler = None):
        self.update_flag = False



################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################






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