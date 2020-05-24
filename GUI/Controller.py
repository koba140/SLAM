import tkinter as tk
class Controller:
    def __init__(self, root, grid=(4,4)):
        self.Frame = tk.Frame(root)
        self.Frame.grid(row=grid[0], columnspan=grid[1])

    def __del__(self):
        print(self.Frame.winfo_children())
        for widget in self.Frame.winfo_children():
            widget.destroy()
        self.Frame.destroy()

        



class BrightnessController(Controller):

    def __init__(self, root, grid=(4,4)):
        super().__init__(root, grid)

        self.threshold = tk.Scale(self.Frame, from_=0, to=255, orient="horizontal", label="Threshold", length=300)
        self.threshold.grid(row=0, column=0)

        self.compression = tk.Scale(self.Frame, from_=1, to=5, orient="horizontal", label="Compression", resolution=0.1)
        self.compression.grid(row=0, column=1)

    
class EdgesController(Controller):
    def __init__(self, root, grid=(4,4)):
        super().__init__(root, grid)
        self.threshold1 = tk.Scale(self.Frame, from_=0, to=255, orient="horizontal", label="Threshold1", length=300)
        self.threshold1.grid(row=0, column=0)

        self.threshold2 = tk.Scale(self.Frame, from_=0, to=255, orient="horizontal", label="threshold2", length=300)
        self.threshold2.grid(row=0, column=1)

class CornerController(Controller):
    def __init__(self, root, grid=(4,4)):
        super().__init__(root, grid)

        self.blocksize = tk.Scale(self.Frame, from_=1, to=5, orient="horizontal", label="Block size", length=100)
        self.blocksize.grid(row=0, column=0)

        self.ksize = tk.Scale(self.Frame, from_=1, to=30, orient="horizontal", label="ksize", length=100, resolution=2)
        self.ksize.grid(row=0, column=1)

        self.k = tk.Scale(self.Frame, from_=0.00001, to=0.5, orient="horizontal", label="k", length=200, resolution=0.00001)
        self.k.grid(row=0, column=2)