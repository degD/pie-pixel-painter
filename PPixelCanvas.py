
from os import stat
from tkinter import *
from tkinter import ttk


class PPixelPaintingCanvas(Canvas):
    """A modified version of tkinter canvas widget.

    Parent:
        Canvas (tkinter canvas): Child of the tkinter canvas class.
    """
    def __init__(self, parent, **kwargs):
        """Create a PPixelPaintingCanvas instance.

        Args:
            parent (tkinter root): The window that canvas will reside in.
            **kwargs: Arguments from tkinter canvas.
        """
        super().__init__(parent, **kwargs)
        
        # Size of painting pixels in screen pixels.
        self.size = 20
        
        # That's how color is referred. It is in hex form. Actually, that is same as RGB values.
        # Each two digits are a byte, so 0-255 of RGB.
        self.paintcolor = '#000000'
        
        # Defines tool mode. Modes are 'painter', 'eraser', 'cpicker', 'filler'
        self.tool_mode = 'picker'
        
        # These two special functions are for painting the canvas. They are binded to left-button and
        # left-button-movement, respectively.
        self.bind("<Button-1>", self.paintsingleppixel)
        self.bind("<B1-Motion>", self.paintppixels)
        
        # Painting data on canvas are saved in a dictionary, seeded with ids' of squares.
        # When you paint something on canvas, an id will be assigned to it. Though you can control
        # the thing with that id, it's quite impossible to do things only with that id. So I use 
        # another dictionary that is seeded with ids that store also coordinates and colors of
        # painting pixels. That is how it is organized:
        # {id1: ((x1, y1), color1), id2: ((x2, y2), color2), ...}
        self.data = {}
    
    def change_mode(self, mode):
        """Changes the tool.

        Args:
            mode (str): Should be one of these: painter, eraser, cpicker, filler
        """
        if mode not in ('painter', 'eraser', 'cpicker', 'filler'):
            raise ValueError('Unknown mode!')
        self.tool_mode = mode
        
    def get_mode(self):
        return self.tool_mode
        
    def getcolor(self):
        """Returns the hex of current painting color.

        Returns:
            str: Hex of color as string.
        """
        return self.paintcolor
    
    def setcolor(self, color):
        """Set the painting color.

        Args:
            color (str): Use a color in hex format, as a string.
        """
        self.paintcolor = color
    
    def get_pp_size(self):
        """Return size of the painting pixels.

        Returns:
            int: Size of painting pixels.
        """
        return self.size

    # Rectangle coordinates
    def ppixelcalc(self, x, y):
        """Convert taken x and y coordinates, to coordinates that will
        represent a square relative to the canvas. Size of the square
        will change, correspond to the size attribute of the PPixelCanvas
        instance.

        Args:
            x (int): x coordinate, increases from left to right.
            y (int): y coordinate, increases from top to bottom.

        Returns:
            tuple: Return a tuple that consists of coordinates that make up
            the square. Respectively topx, topy, bottomx, bottomy.
        """
        size = self.size
        
        px = x // size
        py = y // size
        
        topx, topy = px*size, py*size
        bottomx, bottomy = (px+1)*size, (py+1)*size
        
        return (topx, topy, bottomx, bottomy)
    
    # Returned coordinates from this function will be referred as free coordinates.
    def convcoords(self, rect_coords):
        """Convert square coordinates to coordinates that are independent
        by the size attribute.

        Args:
            rect_coords (tuple): Square coordinates. topx, topy, bottomx, bottomy

        Returns:
            tuple: An x, y coordinate that are independent from the size attribute.
        """
        x1, y1, x2, y2 = rect_coords[0], rect_coords[1], rect_coords[2], rect_coords[3]
        
        x = (x1 + x2 // 2) // self.size
        y = (y1 + y2 // 2) // self.size
        
        return (x, y)
        
    # 2 -> same coords, same colors
    # 1 -> same coords, diff colors
    # 0 -> diff coords  
    def testnew(self, new_rect_coords, new_color):
        """Takes a set of coordinates and color, and compares it with canvas' stored data.
        Returns integers and ids. Integers can change by the results.

        Args:
            new_rect_coords (tuple): Square coordinates. topx, topy, bottomx, bottomy.
            new_color (str): String that represents color in hex.

        Returns:
            tuple: Returns a tuple like (stat, id). stat could be one of 0, 1 or 2.
            If the new coordinates do not exist in canvas, return 0. If it exists, but
            with a different color, return 1. If it exists and also the existing color is
            same, return 2. 
        """
        # Coordinates are stored as free coordinates in data. So converting new_rect_coords to
        # free coordinates is the first step. Then testing.
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
        """Save painting pixel data.

        Args:
            id (tkinter canvas item id): id of object on canvas.
            rect_coords (tuple): topx, topy, bottomx, bottomy coordinates.
            color (str): String that represents color in hex.
        """
        # Converting at first.
        coords = self.convcoords(rect_coords)
        self.data[id] = (coords, color)
    
    def paintsingleppixel(self, event):
        """Paint single painting pixel.

        Args:
            event (tkinter bind event): Stores event data.
        """
        # Takes x, y coordinates from the event, so pointer coordinates. Because canvas
        # is scrollable, it is also necessary to convert them to canvas coordinates.
        # Lastly, converting them to square coordinates.
        x, y = int(self.canvasx(event.x)), int(self.canvasy(event.y))
        rect_coords = self.ppixelcalc(x, y)
        
        # Checking, testing the coordinate.
        status, id = self.testnew(rect_coords, self.paintcolor)
        
        # For color picking, using taken id to get the color of choosen ppixel.
        if self.tool_mode == 'cpicker':
            if status != 0:
                self.paintcolor = self.data[id][1]
                self.event_generate('<<PickedColor>>')
            return
            
        # And proceeds accordingly. Creating something on canvas will return an id.
        # At 0, only creating a square. At 1, removing the existing one and re-adding
        # A new square with a new id. Nothing happens at status 2, because it means
        # the square already exists. And there is the eraser, a step above painting.
        # If erasing, paint as usual at first, but after getting the id, remove it.
        if status == 0:
            id = self.create_rectangle(rect_coords, fill=self.paintcolor, outline='')
            self.save_ppixel(id, rect_coords, self.paintcolor)
        elif status == 1:
            self.delete(id)
            self.data.pop(id)
            id = self.create_rectangle(rect_coords, fill=self.paintcolor, outline='')
            self.save_ppixel(id, rect_coords, self.paintcolor)
        
        if self.tool_mode == 'eraser':
            self.delete(id)
            self.data.pop(id)
    
    def paintppixels(self, event):
        """Paint multiple painting pixels.

        Args:
            event (tkinter bind event): Stores event data.
        """
        # Same with above function except the name and use.
        x, y = int(self.canvasx(event.x)), int(self.canvasy(event.y))
        rect_coords = self.ppixelcalc(x, y)
        
        status, id = self.testnew(rect_coords, self.paintcolor)
        
        if self.tool_mode == 'cpicker': return
        
        if status == 0:
            id = self.create_rectangle(rect_coords, fill=self.paintcolor, outline='')
            self.save_ppixel(id, rect_coords, self.paintcolor)
        elif status == 1:
            self.delete(id)
            self.data.pop(id)
            id = self.create_rectangle(rect_coords, fill=self.paintcolor, outline='')
            self.save_ppixel(id, rect_coords, self.paintcolor)
            
        if self.tool_mode == 'eraser':
            self.delete(id)
            self.data.pop(id)  
            
    def get_cv_data(self):
        """Return canvas data.

        Returns:
            tuple: Return canvas data as a tuple.
        """
        return self.data.values()
    
    def reset_data(self):
        """
        Reset stored canvas data.
        """
        self.data.clear()
        
