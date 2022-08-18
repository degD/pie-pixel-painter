
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

        # Size of a pixel on canvas, in amount of pixels.
        self.pp_pixel_size = 20
        
        # Indicates the current selected tool.
        # 0 -> painter, 1 -> eraser, 2 -> color picker, 3 -> fill 
        self.tool_mode = 0
        
        # Painting color in hex.
        self.color_hex = '#000000'
        
        # Binding left-button and left-button-movement to some functions.
        # clicktools is a function for single click paint, color pick and fill.
        self.bind('<Button-1>', self.clicktools)
        self.bind('<B1-Motion>', self.motion_paint)
        
        # Coordinates are stored in a 2-dimensional list, which is x and y axis.
        # In each index, a tuple of color and id are stored. As an example:
        # [[('#000000', 1), ('#000000', 2)], [('#111111', 8)]]
        self.data = [[]]
        self.w = self.h =0

    def refresh_canvas_data(self, w, h):
        """Refresh canvas, and reset data.

        Args:
            w (int): width
            h (int): height
        """
        self.delete('all')
        
        x_l = [0 for _ in range(w)]
        data_list = [list(x_l) for _ in range(h)]
        
        self.data = data_list
        self.w, self.h = w, h
    
    def to_square_coords(self, x, y):
        """Use mouse coordinates relative to canvas, to calculate 
        four coordinates that form a square.

        Args:
            x (int): x coordinate
            y (int): y coordinate

        Returns:
            tuple: coordinates that form up a square.
            topx, topy, bottomx, bottom respectively.
        """
        size = self.pp_pixel_size
        
        px = x // size
        py = y // size
        
        topx, topy = px*size, py*size
        bottomx, bottomy = (px+1)*size, (py+1)*size
        
        return (topx, topy, bottomx, bottomy)
    
    def independent_coords(self, square_coords):
        """Calculates a coordinate that is independent from the canvas
        using square coordinates. In other words, real coordinates.

        Args:
            square_coords (tuple): Square coordinates

        Returns:
            tuple: independent coordinates.
        """
        x1, y1, x2, y2 = square_coords[0], square_coords[1], square_coords[2], square_coords[3]
        
        size = self.pp_pixel_size
        x = (x1 + x2 // 2) // size
        y = (y1 + y2 // 2) // size
        
        return (x, y)
    
    def iscoord(self, x, y):
        """Checks if coordinate is painted.

        Args:
            x (int): coordinate
            y (int): coordinate

        Returns:
            bool: True if yes and False if no.
        """
        if self.data[y][x] == 0: 
            return False
        return True

    def clicktools(self, event):
        """Tools when clicked on canvas. Controlled using the self.tool_mode.
        Tool modes are 0, 1, 2, 3 or paint, erase, color pick, fill.

        Args:
            event (tkinter input event): Used for getting coordinates.
        """
        # x and y are coordinates when clicked on the canvas.
        # sqrc is a tuple of four coordinates that represent a square,
        # which will be a painting pixel square.
        # Second x, y coordinates are independent from canvas, 
        # in other words, real coordinates.
        rawx, rawy = int(self.canvasx(event.x)), int(self.canvasy(event.y))
        sqrc = self.to_square_coords(rawx, rawy)
        x, y = self.independent_coords(sqrc)
        
        # If painting...
        if self.tool_mode == 0:
            
            # The procedure is simple: If the coordinate is not occupied, just create a new square there.
            # But if it does, with different color, delete the old one and create a new with right color.
            # Just skip if colors are also same.
            if self.iscoord(x, y) == True:
                p_color, p_id = self.data[y][x]

                if p_color != self.color_hex:
                    self.delete(p_id)
                    new_id = self.create_rectangle(sqrc, fill=self.color_hex, outline='')
                    self.data[y][x] = (self.color_hex, new_id)
            
            else:
                new_id = self.create_rectangle(sqrc, fill=self.color_hex, outline='')
                self.data[y][x] = (self.color_hex, new_id)
        
        # Erase tool.
        elif self.tool_mode == 1:
            
            # Like the former, but deletes instead of painting.
            if self.iscoord(x, y) == True:
                p_color, p_id = self.data[y][x]
                
                self.delete(p_id)
                self.data[y][x] = 0
        
        # Color picker.
        elif self.tool_mode == 2:
            
            if self.iscoord(x, y) == True:
                p_color, p_id = self.data[y][x]
                
                self.color_hex = p_color
                self.event_generate('<<PickedColorChangeIndicator>>')
                # Event is for informing the program for updating the indicator of paint tool.
        
        # And lastly fill tool.
        # Using an recursive flood fill algorithm.
        # Because of Python's internal design, recursion might fail oftenly.
        elif self.tool_mode == 3:
            
            def flood_fill_func(rawx, rawy, color):
                
                sqrc = self.to_square_coords(rawx, rawy)
                x, y = self.independent_coords(sqrc)
                
                if self.iscoord(x, y) == True:
                    p_color, p_id = self.data[y][x]
                    
                    if p_color == color:
                        self.delete(p_id)
                        new_id = self.create_rectangle(sqrc, fill=self.color_hex, outline='')
                        self.data[y][x] = (self.color_hex, new_id)
                    else:
                        return
                        
                else:
                    new_id = self.create_rectangle(sqrc, fill=self.color_hex, outline='')
                    self.data[y][x] = (self.color_hex, new_id)
                    
                s = self.pp_pixel_size
                if (not 0 < rawx < self.w) or (not 0 < rawy < self.h): return
                
                try:
                    flood_fill_func(rawx+s, rawy, color)
                    flood_fill_func(rawx-s, rawy, color)
                    flood_fill_func(rawx, rawy+s, color)
                    flood_fill_func(rawx, rawy-s, color)
                except RecursionError:
                    return
            
            if self.iscoord(x, y) == True:   
                p_color, p_id = self.data[y][x]
                
                if p_color != self.color_hex:
                    flood_fill_func(rawx, rawy, p_color)
            
            else:
                flood_fill_func(rawx, rawy, 0)
        
    def motion_paint(self, event):
        """Tools when clicking while moving the mouse. Painter and eraser

        Args:
            event (tkinter input event): Used for getting coordinates.
        """
        rawx, rawy = int(self.canvasx(event.x)), int(self.canvasy(event.y))
        sqrc = self.to_square_coords(rawx, rawy)
        x, y = self.independent_coords(sqrc)
        
        if self.tool_mode == 0:
            
            if self.iscoord(x, y) == True:
                p_color, p_id = self.data[y][x]

                if p_color != self.color_hex:
                    self.delete(p_id)
                    new_id = self.create_rectangle(sqrc, fill=self.color_hex, outline='')
                    self.data[y][x] = (self.color_hex, new_id)
            
            else:
                new_id = self.create_rectangle(sqrc, fill=self.color_hex, outline='')
                self.data[y][x] = (self.color_hex, new_id)     

        elif self.tool_mode == 1:
            
            if self.iscoord(x, y) == True:
                p_color, p_id = self.data[y][x]
                
                self.delete(p_id)
                self.data[y][x] = 0   
    
    def change_mode(self, mode):
        """Change tool mode.

        Args:
            mode (int): Might be 0, 1, 2, 3

        Raises:
            ValueError: If mode is unknown.
        """
        if mode not in (0, 1, 2, 3):
            raise ValueError('Unknown mode!')
        self.tool_mode = mode
        
    def get_mode(self):
        """Returns the current tool mode.

        Returns:
            int: Tool mode, so one of the following: 0, 1, 2, 3
        """
        return self.tool_mode
        
    def getcolor(self):
        """Returns the hex of current painting color.

        Returns:
            str: Hex of color as string.
        """
        return self.color_hex

    def setcolor(self, color):
        """Set the painting color.

        Args:
            color (str): Use a color in hex format, as a string.
        """
        self.color_hex = color
    
    def get_pp_size(self):
        """Return size of the painting pixels.

        Returns:
            int: Size of painting pixels.
        """
        return self.pp_pixel_size
        
