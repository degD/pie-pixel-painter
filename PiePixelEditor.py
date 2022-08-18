
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from PPixelCanvas import PPixelPaintingCanvas
# Importing modules.

# pixel -> pixel as we know
# ppixel -> PIEpixel or PAINTING pixel

class SizeDlg():
    """
    A class for generating new window/size dialogs.
    """
    def __init__(self, subwindow):
        """Generate a dialog window.
        
        Args:
            subwindow (tkinter root window): A tkinter window.
            
        Methods:
            getstate :     
        """
        root = Toplevel(subwindow)
        root.title('New Window')
        
        # A function for exiting the dialog safely.
        def exitdlg():
            root.grab_release()
            root.destroy()
        
        # Placing the dialog where the mouse pointer points.
        # winfo_pointer -> Pointer coordinates relative to left corner of the root window.
        # winfo_vroot -> Coordinates of the left corner of the root window relative to screen.
        abs_pointerx = root.winfo_pointerx() - root.winfo_vrootx()
        abs_pointery = root.winfo_pointery() - root.winfo_vrooty()
        root.geometry('+%d+%d' % (abs_pointerx, abs_pointery))

        # Some adjustments for the dialog.
        root.focus()
        root.resizable(False, False)
        root.protocol('WM_DELETE_WINDOW', exitdlg)
        root.transient(subwindow)
        root.wait_visibility()
        root.grab_set()
        
        # Decorating the window.
        frame = ttk.Frame(root)
        frame.grid(column=0, row=0, sticky=(N, S, W, E), padx=5, pady=5)
        
        ttk.Label(frame, text='Width:').grid(column=0, row=0, sticky=(N, S, W, E))
        ttk.Label(frame, text='Height:').grid(column=0, row=1, sticky=(N, S, W, E))
        
        self.w = StringVar()
        self.w.set(0)
        wentry = ttk.Entry(frame, width=5, textvariable=self.w)
        wentry.grid(column=1, row=0, sticky=(N, S, W, E), pady=4)
        
        self.h = StringVar()
        self.h.set(0)
        hentry = ttk.Entry(frame, width=5, textvariable=self.h)
        hentry.grid(column=1, row=1, sticky=(N, S, W, E), pady=4)
        
        # A bool value that is bound to the state of new possible window.
        # True if a new canvas will be created and false otherwise.
        self.newcanvas = False
        
        def setstate():
            self.newcanvas = True
            exitdlg()
        
        # Creating the buttons for the dialog.
        okbutton = ttk.Button(frame, text='Ok', command=setstate)
        okbutton.grid(column=0, row=2, sticky=(N, S), padx=3, pady=3)
        
        cancelbutton = ttk.Button(frame, text='Cancel', command=exitdlg)
        cancelbutton.grid(column=1, row=2, sticky=(N, S), padx=3, pady=3)
        
        # For blocking execution until this window destroyed.
        root.wait_window()
        
    def getstate(self):
        """Return what is going to happen for the canvas after this
        dialog closes.

        Returns:
            bool: True if a new canvas will be created and false otherwise.
        """
        return self.newcanvas
    
    def getsize(self):
        """Return the width and height of new canvas, as painting pixels.

        Returns:
            tuple: A tuple with two integer items, first is width and second one is height.
        """
        return int(self.w.get()), int(self.h.get())
   

class PiePixelEditor():
    """
    Main editor class. Pixel editor.
    """
    def __init__(self, root):
        """Create a pixel editor.

        Args:
            root (tkinter root window): Any tkinter window.
        """
        self.root = root
        
        root.title('PPP')
        
        # To store image objects and protect them from getting garbage collected.
        self.imglist = []
        
        # This option is for preventing tearing off menus.
        root.option_add('*tearOff', False)
        
        # Setting the minimum and maximum sizes for the editor.
        w_max = root.winfo_screenwidth()
        h_max = root.winfo_screenheight()
        root.maxsize(w_max, h_max)
        root.minsize(200, 200)
        
        # Creating the menubar.
        menubar = Menu(root)
        root['menu'] = menubar
        menubar.add_command(label='New', command=self.newcanvas)

        # Creating the scrollable canvas, with default size of 50x50 painting pixels.
        h_scroll = ttk.Scrollbar(root, orient=HORIZONTAL)
        v_scroll = ttk.Scrollbar(root, orient=VERTICAL)        
        self.canvas = PPixelPaintingCanvas(root, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set, background='white')
        self.canvas.refresh_canvas_data(1000, 1000)
        self.canvas['width'] = 1000
        self.canvas['height'] = 1000
        h_scroll['command'] = self.canvas.xview
        v_scroll['command'] = self.canvas.yview
        
        self.canvas.grid(column=0, row=1)
        h_scroll.grid(column=0, row=2, sticky=(W, E))
        v_scroll.grid(column=1, row=1, sticky=(N, S))

        # This part is for interface, the part that is above the canvas, where you select tools.
        # Each tool is actually a frame, where each frame consist of more frames and labels in them.
        # The tools are the painter, eraser, color selector, color picker, filler, zoom out, zoom in.
        interface = ttk.Frame(root)
        interface.grid(column=0, row=0, sticky=(N, S, W, E))

        # The paint button.
        # The procedure is rather long but actually simple.
        # Because we can't directly change it's color, we are changing the style 
        # of the painter every time we choose a new color. Binding to the left mouse button.
        # Lastly, adding the label.
        paintframe = ttk.Frame(interface, width=50, height=60, relief='groove', borderwidth=2)
        paintframe.grid(column=0, row=0, sticky=(N, S, E, W), padx=3)
        paintstyle = ttk.Style()
        paintstyle.configure('Painter.TFrame', background='#000000', relief='sunken')
        painter = ttk.Frame(paintframe, height=33, width=33, style='Painter.TFrame')
        painter.grid(column=0, row=0, sticky=W, padx=2, pady=2)
        painter.bind('<Button-1>', self.setpaintmode)
        ttk.Label(paintframe, text='paint', anchor='center').grid(column=0, row=1, sticky=(W, E, N, S)) 
        
        # The eraser button.
        # Similar to above, but only changing the relief as style when clicked. 
        eraserframe = ttk.Frame(interface, width=50, height=60, relief='groove', borderwidth=2)
        eraserframe.grid(column=1, row=0, sticky=(N, S, E, W), padx=3)
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='raised')
        eraser = ttk.Frame(eraserframe, height=33, width=33, style='Eraser.TFrame')
        eraser.grid(column=0, row=0, sticky=W, padx=2, pady=2)
        eraser.bind('<Button-1>', self.seterasermode)
        ttk.Label(eraserframe, text='eraser', anchor='center').grid(column=0, row=1, sticky=(W, E, N, S)) 
        
        # The color selector button.
        # Similar to two preceding tools, only difference is that it uses an label
        # with an image instead of a color. The rest are same.
        colorframe = ttk.Frame(interface, width=50, height=60, relief='groove', borderwidth=2)
        colorframe.grid(column=2, row=0, sticky=(N, S, E, W), padx=3)
        
        colorselector_img = PhotoImage(file=r'color-wheel.png', width=33, height=33)
        self.imglist.append(colorselector_img)
        colorselector = ttk.Label(colorframe, compound='image')
        colorselector['image'] = colorselector_img
        
        colorselector.grid(column=0, row=0, sticky=W)
        colorselector.bind('<Button-1>', self.choosecolor)
        ttk.Label(colorframe, text='color', anchor='center').grid(column=0, row=1, sticky=(W, E, N, S))
        
        # A separator.
        ttk.Frame(interface, width=5, height=60, relief='raised', borderwidth=2).grid(column=3, row=0, sticky=(N, S, E, W), padx=3)
        
        # The color picker.
        cpickerfrm = ttk.Frame(interface, width=50, height=60, relief='groove', borderwidth=2)
        cpickerfrm.grid(column=4, row=0, sticky=(N, S, E, W), padx=3)
        
        cpicker_img = PhotoImage(file=r'color-picker.png', width=33, height=33)
        self.imglist.append(cpicker_img)
        cpicker = ttk.Label(cpickerfrm, compound='image')
        cpicker['image'] = cpicker_img
        
        cpicker.grid(column=0, row=0, sticky=W)
        cpicker.bind('<Button-1>', self.colorpick)
        ttk.Label(cpickerfrm, text='picker', anchor='center').grid(column=0, row=1, sticky=(W, E, N, S))
        
        # The fill tool.
        fillfrm = ttk.Frame(interface, width=50, height=60, relief='groove', borderwidth=2)
        fillfrm.grid(column=5, row=0, sticky=(N, S, E, W), padx=3)
        
        fill_img = PhotoImage(file=r'fill-tool.png', width=33, height=33)
        self.imglist.append(fill_img)
        filltool = ttk.Label(fillfrm, compound='image')
        filltool['image'] = fill_img
        
        filltool.grid(column=0, row=0, sticky=W)
        filltool.bind('<Button-1>', self.fill_area)
        ttk.Label(fillfrm, text='fill', anchor='center').grid(column=0, row=1, sticky=(N, S, W, E))
        
        # The canvas will raise an event, as we pick a new color. Catching the event
        # and binding it, to be able to change the color of painter when needed.
        self.canvas.bind('<<PickedColorChangeIndicator>>', self.picked_color)
        
        # Adjusting the weights for resizing correctly.
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        
        # Setting the starting location of the editor to center of the screen.
        w_sc = self.root.winfo_screenwidth() 
        h_sc = self.root.winfo_screenheight()
        
        y = (h_sc - 800) // 2
        x = (w_sc - 600) // 2
        
        self.root.geometry('800x600+%d+%d' % (x, y))
    
    def fill_area(self, event):
        """Set to color fill mode.
        
        Args:
            event (tkinter bind event): Not used.
        """
        self.canvas.change_mode(3)

        painterstyle = ttk.Style()
        painterstyle.configure('Painter.TFrame', background=self.canvas.color_hex, relief='raised')
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='raised')  
        
    def picked_color(self, event):
        """Will execute if picked a color to inform the painter and alter it's color.

        Args:
            event (tkinter bind event): Not used.
        """
        painterstyle = ttk.Style()
        painterstyle.configure('Painter.TFrame', background=self.canvas.color_hex)
        
    def colorpick(self, event):
        """Set to color picker mode.
        
        Args:
            event (tkinter bind event): Not used.
        """
        self.canvas.change_mode(2)

        painterstyle = ttk.Style()
        painterstyle.configure('Painter.TFrame', background=self.canvas.color_hex, relief='raised')
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='raised')   

    def choosecolor(self, event):
        """Raise the color selector dialog and use the chosen
        color as the painting color. And activate the painting tool.

        Args:
            event (tkinter bind event): Not used.
        """
        # Selecting a color.
        colordata = colorchooser.askcolor(title='Choose Color', parent=self.root, initialcolor=self.canvas.getcolor())
        color = colordata[1]
        if color == None:
            color = self.canvas.getcolor()
        self.canvas.setcolor(color)
        
        # Modifing styles because otherwise it's also needed to change the frames.
        painterstyle = ttk.Style()
        painterstyle.configure('Painter.TFrame', background=color, relief='sunken')
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='raised')
        
        # Setting to the painting mode.
        self.canvas.change_mode(0)
        
    def setpaintmode(self, event):
        """Activate painting.

        Args:
            event (tkinter bind event): Not used.
        """
        painterstyle = ttk.Style()
        painterstyle.configure('Painter.TFrame', background=self.canvas.getcolor(), relief='sunken')
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='raised')
        
        self.canvas.change_mode(0)
        
    def seterasermode(self, event):
        """Activate the eraser.

        Args:
            event (tkinter bind event): Not used.
        """
        painterstyle = ttk.Style()
        painterstyle.configure('Painter.TFrame', background=self.canvas.getcolor(), relief='raised')
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='sunken')
        
        # Setting the eraser.
        self.canvas.change_mode(1)
    
    def newcanvas(self):
        """
        Raising the new canvas dialog. Cleaning and editing the existing canvas by the inputs.
        """
        # Creating the dialog and getting the state, for in case of an exit.
        new = SizeDlg(self.root)
        state = new.getstate()
        
        # The width and height are inputed as painting pixels.
        # So converting them to screen pixels first.
        size_pp = self.canvas.get_pp_size()
        wpp, hpp = new.getsize()
        w, h = wpp*size_pp, hpp*size_pp
        
        # Editing the canvas.
        if state:
            self.canvas.refresh_canvas_data(w, h)
            self.canvas['scrollregion'] = (0, 0, w, h)
            self.canvas['width'] = w
            self.canvas['height'] = h
