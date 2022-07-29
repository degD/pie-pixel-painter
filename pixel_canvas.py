
from tkinter import *
from tkinter import ttk

class PixelPaintingCanvas(Canvas):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.paintcolor = '#000000' # 7 character  
        self.is_eraser = False
        
        self.bind("<Button-1>", self.paintsinglepixel)
        self.bind("<B1-Motion>", self.paintpixels)
        
        self.data = {}
        # Find a way to speed this up.
        
    def getcolor(self):
        return self.paintcolor
    
    def setcolor(self, color):
        self.paintcolor = color
    
    def eraser_mode(self):
        self.is_eraser = True
        
    def paint_mode(self):
        self.is_eraser = False
    
    # 2 -> same coords, same colors
    # 1 -> same coords, diff colors
    # 0 -> diff coords  
    def testnew(self, new_coords, new_color):
        for id in self.data.keys():
            coords = self.data[id][0]
            color = self.data[id][1]
            
            if coords == new_coords:
                if color == new_color:
                    return (2, id)
                else:
                    return (1, id)
        return (0, 0)
    
    def paintsinglepixel(self, event):
        x, y = self.canvasx(event.x), self.canvasy(event.y)
        rect_coords = self.pixelcalc(x, y)
        
        status, id = self.testnew(rect_coords, self.paintcolor)
        
        if status == 0:
            id = self.create_rectangle(rect_coords, fill=self.paintcolor, outline='')
            self.data[id] = (rect_coords, self.paintcolor)
        elif status == 1:
            self.delete(id)
            self.data.pop(id)
            id = self.create_rectangle(rect_coords, fill=self.paintcolor, outline='')
            self.data[id] = (rect_coords, self.paintcolor)
        
        if self.is_eraser:
            self.delete(id)
            self.data.pop(id)    
  
    def paintpixels(self, event):
        x, y = self.canvasx(event.x), self.canvasy(event.y)
        rect_coords = self.pixelcalc(x, y)
        
        status, id = self.testnew(rect_coords, self.paintcolor)
        
        if status == 0:
            id = self.create_rectangle(rect_coords, fill=self.paintcolor, outline='')
            self.data[id] = (rect_coords, self.paintcolor)
        elif status == 1:
            self.delete(id)
            self.data.pop(id)
            id = self.create_rectangle(rect_coords, fill=self.paintcolor, outline='')
            self.data[id] = (rect_coords, self.paintcolor)
            
        if self.is_eraser:
            self.delete(id)
            self.data.pop(id)  
        
    def pixelcalc(self, x, y):
        size = 20
        
        px = x // size
        py = y // size
        
        topx, topy = px*size, py*size
        bottomx, bottomy = (px+1)*size, (py+1)*size
        
        return (topx, topy, bottomx, bottomy)