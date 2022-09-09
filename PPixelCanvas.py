
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
        self.pp_pixel_size = 0
        
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
        self.w = self.h = 0

        self.realw = self.realh = 0

    def refresh_canvas_data(self, w, h, s):
        """Refresh canvas, and reset data.

        Args:
            w (int): width
            h (int): height
            s (int): painting pixel size
        """
        self.delete('all')
        
        x_l = [(0, 0) for _ in range(w)]
        data_list = [list(x_l) for _ in range(h)]
        
        self.data = data_list
        self.w, self.h = w, h

        self.pp_pixel_size = s
        self.realw, self.realh = w*s, h*s

    def get_pp_size(self):
        """Return painting pixel size.

        Returns:
            int: width or height in real pixels
        """
        return self.pp_pixel_size

    def zoom_func(self, new_pp_size):
        """As the result, zooms in or out the canvas. To achieve this,
        deletes everything on the canvas first, and repaints it with the
        desired pixel size, using the canvas data.

        Args:
            new_pp_size (int): New size for the pixels.
        """
        self.delete('all')

        size = new_pp_size
        for y in range(self.h):
            for x in range(self.w):
                
                if self.iscoord(x, y):
                    
                    # Calculating square coords from x, y matrix data.
                    # Which will be used to paint the canvas again.
                    topx, topy = x*size, y*size
                    bottomx, bottomy = (x+1)*size, (y+1)*size
                    sqrc = (topx, topy, bottomx, bottomy)

                    # Painting the canvas.
                    pp_color = self.data[y][x][0]
                    new_id = self.create_rectangle(sqrc, fill=pp_color, outline='')
                    self.data[y][x] = (pp_color, new_id)                    

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
        tx, ty, bx, by = square_coords[0], square_coords[1], square_coords[2], square_coords[3]
        
        size = self.pp_pixel_size
        x = ((tx + bx) // 2) // size
        y = ((ty + by) // 2) // size
        
        return (x, y)
    
    def iscoord(self, x, y):
        """Checks if coordinate is painted.

        Args:
            x (int): coordinate
            y (int): coordinate

        Returns:
            bool: True if yes and False if no.
        """
        if self.data[y][x] == (0, 0): 
            return False
        return True

    def iscoord_inside(self, x, y):
        """Tests if x, y is inside the canvas boundaries.
        
        Args:
            x (int): coordinate
            y (int): coordinate

        Returns:
            bool: True if yes and False if no.
        """
        if (x < 0) or (y < 0):
            return False
        try:
            self.data[y][x]
        except IndexError:
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

        # Testing x and y.
        if not self.iscoord_inside(x, y): return

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
                self.data[y][x] = (0, 0)
        
        # Color picker.
        elif self.tool_mode == 2:
            
            if self.iscoord(x, y) == True:
                p_color, p_id = self.data[y][x]
                
                self.color_hex = p_color
                self.event_generate('<<PickedColorChangeIndicator>>')
                # Event is for informing the program for updating the indicator of paint tool.
        
        # The fill tool.
        # Iterative algorithm actually works similar to the recursive one.
        # So briefly, starting from the clicked position, iterates trough a list that contains "coordinates to fill."
        # It starts with only one, the starting position. After painting this location, looks to the border coordinates
        # and checks if they are suitable for painting. If so, then appends these coordinates to the list, too.
        # The algo uses a for loop, so it does the same process repeatedly on all appended coordinates, like recursion.
        # If the coord already exists in the list, skips. And the code ends, when it iterates over all the coordinates.
        elif self.tool_mode == 3:
            
            # The list.
            fill_list = [(rawx, rawy)]

            # The color, that will be filled.
            fill_area_color = self.data[y][x][0]

            for rawx, rawy in fill_list:

                sqrc = self.to_square_coords(rawx, rawy)
                x, y = self.independent_coords(sqrc)

                if self.iscoord(x, y) == True:
                    p_color, p_id = self.data[y][x]

                    if p_color != self.color_hex:
                        self.delete(p_id)
                        new_id = self.create_rectangle(sqrc, fill=self.color_hex, outline='')
                        self.data[y][x] = (self.color_hex, new_id)
                
                else:
                    new_id = self.create_rectangle(sqrc, fill=self.color_hex, outline='')
                    self.data[y][x] = (self.color_hex, new_id)

                # Checking if the coordinate is suitable or not. 
                # 'try/expect' is to check if the index is out of range.
                # 'not in list' part is, of course, only allows appending if doesn't exist.
                # Lastly, 'x/y > 0' part is to prevent negative indexing.
                s = self.pp_pixel_size
                try:
                    if self.data[y][x+1][0] == fill_area_color:
                        if (rawx+s, rawy) not in fill_list:
                            fill_list.append((rawx+s, rawy))
                except IndexError:
                    pass
                try:
                    if self.data[y][x-1][0] == fill_area_color and x > 0:
                        if (rawx-s, rawy) not in fill_list:
                            fill_list.append((rawx-s, rawy))
                except IndexError:
                    pass                            
                try:
                    if self.data[y+1][x][0] == fill_area_color:
                        if (rawx, rawy+s) not in fill_list:
                            fill_list.append((rawx, rawy+s))
                except IndexError:
                    pass                            
                try:
                    if self.data[y-1][x][0] == fill_area_color and y > 0:
                            if (rawx, rawy-s) not in fill_list:
                                fill_list.append((rawx, rawy-s))
                except IndexError:
                    pass                            
                                                             
    def motion_paint(self, event):
        """Tools when clicking while moving the mouse. Painter and eraser

        Args:
            event (tkinter input event): Used for getting coordinates.
        """
        rawx, rawy = int(self.canvasx(event.x)), int(self.canvasy(event.y))
        sqrc = self.to_square_coords(rawx, rawy)
        x, y = self.independent_coords(sqrc)

        # Testing x and y.
        if not self.iscoord_inside(x, y): return
        
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
                self.data[y][x] = (0, 0)   
    
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

        self.event_generate('<<ToolChanged>>')
        
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
        
