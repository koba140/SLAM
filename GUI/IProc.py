import tkinter as tk
from GUI.editor import Editor
class IProc:

    def __init__(self, root):
        root.title("IProc")
        
        self.MFrame = tk.Frame(root)
        self.MFrame.pack()

        
        self.editor = Editor(self.MFrame, grid=(1, 0), display_size=(800, 800))
    
    def update(self):
        self.editor.update()





