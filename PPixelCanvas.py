
from tkinter import *
from tkinter import ttk


class PPixelPaintingCanvas(Canvas):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.size = 20
        
        self.paintcolor = '#000000' # 7 character  
        self.is_eraser = False
        
        self.bind("<Button-1>", self.paintsingleppixel)
        self.bind("<B1-Motion>", self.paintppixels)
        
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
    
    def get_pp_size(self):
        return self.size
    
    # Rectangle to x, y coordinates
    def convcoords(self, coords):
        x1, y1, x2, y2 = coords[0], coords[1], coords[2], coords[3]
        
        x = (x1 + x2 // 2) // self.size
        y = (y1 + y2 // 2) // self.size
        
        return (x, y)
        
    # 2 -> same coords, same colors
    # 1 -> same coords, diff colors
    # 0 -> diff coords  
    def testnew(self, new_rect_coords, new_color):
        for id in self.data.keys():
            coords = self.data[id][0]
            new_coords = self.convcoords(new_rect_coords)
            color = self.data[id][1]
            
            if coords == new_coords:
                if color == new_color:
                    return (2, id)
                else:
                    return (1, id)
        return (0, 0)
    
    def save_ppixel(self, id, rect_coords, color):
        coords = self.convcoords(rect_coords)
        self.data[id] = (coords, color)
    
    def paintsingleppixel(self, event):
        x, y = int(self.canvasx(event.x)), int(self.canvasy(event.y))
        rect_coords = self.ppixelcalc(x, y)
        
        status, id = self.testnew(rect_coords, self.paintcolor)
        
        if status == 0:
            id = self.create_rectangle(rect_coords, fill=self.paintcolor, outline='')
            self.save_ppixel(id, rect_coords, self.paintcolor)
        elif status == 1:
            self.delete(id)
            self.data.pop(id)
            id = self.create_rectangle(rect_coords, fill=self.paintcolor, outline='')
            self.save_ppixel(id, rect_coords, self.paintcolor)
        
        if self.is_eraser:
            self.delete(id)
            self.data.pop(id)    
  
    def paintppixels(self, event):
        x, y = int(self.canvasx(event.x)), int(self.canvasy(event.y))
        rect_coords = self.ppixelcalc(x, y)
        
        status, id = self.testnew(rect_coords, self.paintcolor)
        
        if status == 0:
            id = self.create_rectangle(rect_coords, fill=self.paintcolor, outline='')
            self.save_ppixel(id, rect_coords, self.paintcolor)
        elif status == 1:
            self.delete(id)
            self.data.pop(id)
            id = self.create_rectangle(rect_coords, fill=self.paintcolor, outline='')
            self.save_ppixel(id, rect_coords, self.paintcolor)
            
        if self.is_eraser:
            self.delete(id)
            self.data.pop(id)  
    
    # Rectangle coordinates
    def ppixelcalc(self, x, y):
        size = self.size
        
        px = x // size
        py = y // size
        
        topx, topy = px*size, py*size
        bottomx, bottomy = (px+1)*size, (py+1)*size
        
        return (topx, topy, bottomx, bottomy)

    def get_cv_data(self):
        return self.data.values()
    
    def reset_data(self):
        self.data.clear()