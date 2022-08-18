
from tkinter import *
from tkinter import ttk
from PiePixelEditor import PiePixelEditor
import sys
# Importing the necessary modules

if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    
    root = Tk()
    PiePixelEditor(root)
    root.mainloop()
    # Main loop.
