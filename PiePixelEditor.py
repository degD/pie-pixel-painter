
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
from PPixelCanvas import PPixelPaintingCanvas
import PieWrite
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
        wentry = ttk.Entry(frame, width=5, textvariable=self.w)
        wentry.grid(column=1, row=0, sticky=(N, S, W, E), pady=4)
        
        self.h = StringVar()
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
        
        # This option is for preventing tearing off menus.
        root.option_add('*tearOff', False)
        
        # Setting the minimum and maximum sizes for the editor.
        w_max = root.winfo_screenwidth()
        h_max = root.winfo_screenheight()
        root.maxsize(w_max, h_max)
        root.minsize(200, 200)
        
        # Creating the menubar and menus under it.
        menubar = Menu(root)
        root['menu'] = menubar
        
        menu_file = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.newcanvas)
        menu_file.add_separator()
        menu_file.add_command(label='Save As...', command=self.save_as_canvas)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=root.destroy)  

        # Creating the scrollable canvas, with default size of 200x200 painting pixels.
        h_scroll = ttk.Scrollbar(root, orient=HORIZONTAL)
        v_scroll = ttk.Scrollbar(root, orient=VERTICAL)        
        self.canvas = PPixelPaintingCanvas(root, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set, background='white')
        self.canvas['width'] = 1000
        self.canvas['height'] = 1000
        h_scroll['command'] = self.canvas.xview
        v_scroll['command'] = self.canvas.yview
        
        self.canvas.grid(column=0, row=1)
        h_scroll.grid(column=0, row=2, sticky=(W, E))
        v_scroll.grid(column=1, row=1, sticky=(N, S))

        # This part is for interface, the part that is above the canvas, where you select tools.
        # Each tool is actually a frame, where each frame consist of more frames and labels in them.
        interface = ttk.Frame(root)
        interface.grid(column=0, row=0, sticky=(N, S, W, E))
        
        # The color button.
        # The procedure is rather long but actually simple.
        # Creating a main frame first, then creating the color selector as a frame in it.
        # Because we can't directly change it's color, we are changing the style 
        # of the color selector every time we choose a new color. Binding the left mouse button.
        # Lastly, adding the label.
        colorframe = ttk.Frame(interface, padding=(5, 3, 3, 0))
        colorframe.grid(column=0, row=0, sticky=(W, E))
        colorselectorstyle = ttk.Style()
        colorselectorstyle.configure('ColorSelector.TFrame', background='#000000', relief='sunken')
        colorselector = ttk.Frame(colorframe, height=33, width=33, style='ColorSelector.TFrame')
        colorselector.grid(column=0, row=0, sticky=W)
        colorselector.bind('<Button-1>', self.choosecolor)
        ttk.Label(colorframe, text='color', anchor='center').grid(column=0, row=1, sticky=(W, N, S))
        
        # The eraser button.
        # Similar to above, but only changing the relief as style when clicked. 
        eraserframe = ttk.Frame(interface, padding=(5, 3, 3, 0))
        eraserframe.grid(column=1, row=0, sticky=(W, E))
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='raised')
        eraser = ttk.Frame(eraserframe, height=33, width=33, style='Eraser.TFrame')
        eraser.grid(column=0, row=0, sticky=W)
        eraser.bind('<Button-1>', self.seterasermode)
        ttk.Label(eraserframe, text='eraser', anchor='center').grid(column=0, row=1, sticky=(W, N, S)) 
        
        # Adjusting the weights for resizing correctly.
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        
        # Setting the starting location of the editor to center of the screen.
        w_sc = self.root.winfo_screenwidth() 
        h_sc = self.root.winfo_screenheight()
        
        y = (h_sc - 800) // 2
        x = (w_sc - 600) // 2
        
        self.root.geometry('800x600+%d+%d' % (x, y))

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
        colorselectorstyle = ttk.Style()
        colorselectorstyle.configure('ColorSelector.TFrame', background=color, relief='sunken')
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='raised')
        
        # Setting to the painting mode.
        self.canvas.paint_mode()
        
    def seterasermode(self, event):
        """Activate the eraser.

        Args:
            event (tkinter bind event): Not used.
        """
        colorselectorstyle = ttk.Style()
        colorselectorstyle.configure('ColorSelector.TFrame', background=self.canvas.getcolor(), relief='raised')
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='sunken')
        
        # Setting the eraser.
        self.canvas.eraser_mode()
    
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
            self.canvas.delete('all')
            self.canvas.reset_data()
            self.canvas['scrollregion'] = (0, 0, w, h)
            self.canvas['width'] = w
            self.canvas['height'] = h
    
    def save_as_canvas(self):
        """
        Raising a file selecting dialog. If the file exists, then saves the existing file with a new name.
        Otherwise just saves normally.
        
        Possible file formats:
            PIE, BMP, PNG, JPG
        """ 
        # Can save in one of those formats.
        types_tuple = (('PIE Format', '.pie'), ('BMP Format', '.bmp'), ('PNG Format', '.png'), ('JPEG Format', '.jpg'))
        filepath = filedialog.asksaveasfilename(parent=self.root, title='Save As', defaultextension='.pie', filetypes=types_tuple)
        
        # If the user selects nothing, then returns from the function.
        if filepath == '': return
        
        with open(filepath, 'wb') as fb:
            
            if filepath.endswith('.pie'):
                data = self.canvas.get_cv_data()
                PieWrite.write_p_data(data, fb)
