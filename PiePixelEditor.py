
from hashlib import new
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
    def __init__(self, subwindow, cv_size):
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
        
        ttk.Label(frame, text='Width: ').grid(column=0, row=0, sticky=W)
        ttk.Label(frame, text='Height:').grid(column=0, row=1, sticky=W)
        
        # Adding the size entries.
        cvw, cvh = cv_size

        def entry_check(newval):
            return newval=='' or newval.isnumeric()
        entry_check_wrapper = (root.register(entry_check), '%P')

        self.w = StringVar()
        self.w.set(cvw)
        wentry = ttk.Entry(frame, width=5, textvariable=self.w, validate='key', validatecommand=entry_check_wrapper)
        wentry.grid(column=1, row=0, sticky=(W, E), pady=4)
        
        self.h = StringVar()
        self.h.set(cvh)
        hentry = ttk.Entry(frame, width=5, textvariable=self.h, validate='key', validatecommand=entry_check_wrapper)
        hentry.grid(column=1, row=1, sticky=(W, E), pady=4)

        # Warning text.
        warn_text = 'Warning: Width and height\nshould be between 1-256'
        warn_label = ttk.Label(frame, text=warn_text, font=('TkDefaultFont', 10), foreground='#5e5e5e', anchor='center', justify='center', )
        warn_label.grid(column=0, row=2, columnspan=2, sticky=(W, E))
        
        # A bool value that is bound to the state of new possible window.
        # True if a new canvas will be created and false otherwise.
        self.newcanvas = False
        
        def setstate():
            self.newcanvas = True
            exitdlg()
        
        # Creating the buttons for the dialog.
        okbutton = ttk.Button(frame, text='Ok', command=setstate)
        okbutton.grid(column=0, row=3, sticky=(N, S), padx=3, pady=3)
        
        cancelbutton = ttk.Button(frame, text='Cancel', command=exitdlg)
        cancelbutton.grid(column=1, row=3, sticky=(N, S), padx=3, pady=3)
        
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
            tuple: A tuple with two string items, first is width and second one is height.
        """
        return self.w.get(), self.h.get()
   

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

        # Size values for the canvas. It will be 50x50 by painting pixels. And 
        # Each painting pixel be 20 real pixels wide and high.
        wpp = hpp = 50
        pp_size = 20

        # Creating the scrollable canvas.
        h_scroll = ttk.Scrollbar(root, orient=HORIZONTAL)
        v_scroll = ttk.Scrollbar(root, orient=VERTICAL)        
        self.canvas = PPixelPaintingCanvas(root, yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set, background='white')
        self.canvas.refresh_canvas_data(wpp, hpp, pp_size)
        self.canvas['scrollregion'] = (0, 0, wpp*pp_size, hpp*pp_size)
        self.canvas['width'] = 1000
        self.canvas['height'] = 1000
        h_scroll['command'] = self.canvas.xview
        v_scroll['command'] = self.canvas.yview
        
        self.canvas.grid(column=0, row=1)
        h_scroll.grid(column=0, row=3, sticky=(W, E))
        v_scroll.grid(column=1, row=1, sticky=(N, S))

        # Bottom frame, for zoom and some extra information.
        ttk.Style().configure('Interface.TFrame', background='#dbdbdb')
        bottomframe = ttk.Frame(root, style='Interface.TFrame')
        bottomframe.grid(column=0, row=2, sticky=(N, S, W, E), pady=4)

        # An indicator that shows the current selected tool.
        toolname = StringVar()
        toolname.set('paint tool')

        tool_label = ttk.Label(bottomframe, textvariable=toolname, width=11, background='#dbdbdb', anchor='center')
        tool_label.grid(column=0, row=0, sticky=(W, E), padx=2)

        def tool_changed(event=0):
            mode_dict = {0: 'paint tool', 1: 'eraser', 2: 'color picker', 3: 'fill tool'}

            tool_code = self.canvas.get_mode()
            toolname.set(mode_dict[tool_code])

        self.canvas.bind('<<ToolChanged>>', tool_changed)

        # A thin separator.
        ttk.Separator(bottomframe, orient=VERTICAL).grid(column=1, row=0, sticky=(N, S, W, E))

        # An indicator that shows the canvas size in painting pixels.
        cvsize = StringVar()
        cvsize.set('50x50 px')

        cv_size_label = ttk.Label(bottomframe, textvariable=cvsize, width=11, background='#dbdbdb', anchor='center')
        cv_size_label.grid(column=2, row=0, sticky=W, padx=2)

        def update_size(event=0):
            size_str = self.canvas.get_dimensions()
            cvsize.set(size_str)

        self.canvas.bind('<<NewCanvas>>', update_size)

        # This part is for interface, the part that is above the canvas, where you select tools.
        # Each tool is actually a frame, where each frame consist of more frames and labels in them.
        # The tools are the painter, eraser, color selector, color picker, filler, zoom out, zoom in.
        interface = ttk.Frame(root, style='Interface.TFrame')
        interface.grid(column=0, row=0, sticky=(N, S, W, E))

        # The paint button.
        # The procedure is rather long but actually simple.
        # Because we can't directly change it's color, we are changing the style 
        # of the painter every time we choose a new color. Binding to the left mouse button.
        # Lastly, adding the label.
        ttk.Style().configure('PaintFRM.TFrame', relief='sunken')
        paintframe = ttk.Frame(interface, width=50, height=60, style='PaintFRM.TFrame', borderwidth=2)
        paintframe.grid(column=0, row=0, sticky=(N, S, E, W), padx=3, pady=2)
        paintframe.bind('<Button-1>', self.setpaintmode)
        ttk.Style().configure('Painter.TFrame', background='#000000')
        painter = ttk.Frame(paintframe, height=30, width=40, style='Painter.TFrame', relief='flat')
        painter.grid(column=0, row=0, sticky=W, padx=2, pady=2)
        painter.bind('<Button-1>', self.setpaintmode)
        paintlbl = ttk.Label(paintframe, text='paint', anchor='center')
        paintlbl.grid(column=0, row=1, sticky=N)
        paintlbl.bind('<Button-1>', self.setpaintmode)
        
        # The eraser button.
        # Similar to above, but only changing the relief as style when clicked.
        ttk.Style().configure('EraserFRM.TFrame', relief='raised')
        eraserframe = ttk.Frame(interface, width=50, height=60, style='EraserFRM.TFrame', borderwidth=2)
        eraserframe.grid(column=1, row=0, sticky=(N, S, E, W), padx=3, pady=2)
        eraserframe.bind('<Button-1>', self.seterasermode)        
        ttk.Style().configure('Eraser.TFrame', background='#FFFFFF')
        eraser = ttk.Frame(eraserframe, height=30, width=40, style='Eraser.TFrame', relief='flat')
        eraser.grid(column=0, row=0, sticky=W, padx=2, pady=2)
        eraser.bind('<Button-1>', self.seterasermode) 
        eraserlbl = ttk.Label(eraserframe, text='eraser', style='EraseLabel.TLabel', anchor='center')
        eraserlbl.grid(column=0, row=1, sticky=N)
        eraserlbl.bind('<Button-1>', self.seterasermode) 
        
        # The color selector button.
        # Similar to two preceding tools, only difference is that it uses an label
        # with an image instead of a color. The rest are same.
        ttk.Style().configure('CSelect.TFrame', relief='raised')
        colorframe = ttk.Frame(interface, width=50, height=60, style='CSelect.TFrame', borderwidth=2)
        colorframe.grid(column=2, row=0, sticky=(N, S, E, W), padx=3, pady=2)
        colorframe.bind('<Button-1>', self.choosecolor)
        
        colorselector_img = PhotoImage(file=r'color-wheel.png', width=33, height=33)
        self.imglist.append(colorselector_img)

        colorselector = ttk.Label(colorframe, image=colorselector_img, compound='image')
        colorselector.grid(column=0, row=0, sticky=W)
        colorselector.bind('<Button-1>', self.choosecolor)

        colorlabel = ttk.Label(colorframe, text='color', anchor='center')
        colorlabel.grid(column=0, row=1, sticky=(W, E, N, S))
        colorlabel.bind('<Button-1>', self.choosecolor)
        
        # A separator.
        ttk.Frame(interface, width=5, height=60, relief='raised', borderwidth=2).grid(column=3, row=0, sticky=(N, S, E, W), padx=3, pady=2)
        
        # The color picker.
        ttk.Style().configure('cpFRM.TFrame', relief='raised')
        cpickerfrm = ttk.Frame(interface, width=50, height=60, style='cpFRM.TFrame', borderwidth=2)
        cpickerfrm.grid(column=4, row=0, sticky=(N, S, E, W), padx=3, pady=2)
        cpickerfrm.bind('<Button-1>', self.colorpick)
        
        cpicker_img = PhotoImage(file=r'color-picker.png', width=33, height=33)
        self.imglist.append(cpicker_img)

        cpicker = ttk.Label(cpickerfrm, image=cpicker_img, compound='image')
        cpicker.grid(column=0, row=0, sticky=W)
        cpicker.bind('<Button-1>', self.colorpick)

        cpickerlbl = ttk.Label(cpickerfrm, text='picker', anchor='center')
        cpickerlbl.grid(column=0, row=1, sticky=(W, E, N, S))
        cpickerlbl.bind('<Button-1>', self.colorpick)
        
        # The fill tool.
        ttk.Style().configure('fillFRM.TFrame', relief='raised')
        fillfrm = ttk.Frame(interface, width=50, height=60, style='fillFRM.TFrame', borderwidth=2)
        fillfrm.grid(column=5, row=0, sticky=(N, S, E, W), padx=3, pady=2)
        fillfrm.bind('<Button-1>', self.fill_area)
        
        fill_img = PhotoImage(file=r'fill-tool.png', width=33, height=33)
        self.imglist.append(fill_img)

        filltool = ttk.Label(fillfrm, image=fill_img, compound='image')
        filltool.grid(column=0, row=0, sticky=W)
        filltool.bind('<Button-1>', self.fill_area)

        fill_lbl = ttk.Label(fillfrm, text='fill', anchor='center')
        fill_lbl.grid(column=0, row=1, sticky=(N, S, W, E))
        fill_lbl.bind('<Button-1>', self.fill_area)
        
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

        ttk.Style().configure('fillFRM.TFrame', relief='sunken')        
        ttk.Style().configure('PaintFRM.TFrame', relief='raised')        
        ttk.Style().configure('EraserFRM.TFrame', relief='raised')
        ttk.Style().configure('CSelect.TFrame', relief='raised')
        ttk.Style().configure('cpFRM.TFrame', relief='raised')

        self.canvas.change_mode(3)
        
    def picked_color(self, event=0):
        """Will execute if picked a color to inform the painter and alter it's color.

        Args:
            event (tkinter bind event): Not used.
        """
        ttk.Style().configure('Painter.TFrame', background=self.canvas.color_hex)
        
    def colorpick(self, event=0):
        """Set to color picker mode.
        
        Args:
            event (tkinter bind event): Not used.
        """
        self.canvas.change_mode(2)

        ttk.Style().configure('cpFRM.TFrame', relief='sunken')
        ttk.Style().configure('PaintFRM.TFrame', relief='raised')
        ttk.Style().configure('EraserFRM.TFrame', relief='raised')
        ttk.Style().configure('CSelect.TFrame', relief='raised')
        ttk.Style().configure('fillFRM.TFrame', relief='raised')

    def choosecolor(self, event=0):
        """Raise the color selector dialog and use the chosen
        color as the painting color. And activate the painting tool.

        Args:
            event (tkinter bind event): Not used.
        """
        ttk.Style().configure('CSelect.TFrame', relief='sunken')
        ttk.Style().configure('PaintFRM.TFrame', relief='raised')
        ttk.Style().configure('EraserFRM.TFrame', relief='raised')
        ttk.Style().configure('cpFRM.TFrame', relief='raised')
        ttk.Style().configure('fillFRM.TFrame', relief='raised')

        # Selecting a color.
        colordata = colorchooser.askcolor(title='Choose Color', parent=self.root, initialcolor=self.canvas.getcolor())
        color = colordata[1]
        if color == None:
            color = self.canvas.getcolor()
        self.canvas.setcolor(color)
        
        # Modifing styles because otherwise it's also needed to change the frames.
        ttk.Style().configure('Painter.TFrame', background=color)

        self.setpaintmode()
        
    def setpaintmode(self, event=0):
        """Activate painting.

        Args:
            event (tkinter bind event): Not used.
        """
        ttk.Style().configure('Painter.TFrame', background=self.canvas.getcolor())
        ttk.Style().configure('PaintFRM.TFrame', relief='sunken')
        ttk.Style().configure('EraserFRM.TFrame', relief='raised')
        ttk.Style().configure('CSelect.TFrame', relief='raised')
        ttk.Style().configure('cpFRM.TFrame', relief='raised')
        ttk.Style().configure('fillFRM.TFrame', relief='raised')
        
        self.canvas.change_mode(0)
        
    def seterasermode(self, event=0):
        """Activate the eraser.

        Args:
            event (tkinter bind event): Not used.
        """
        ttk.Style().configure('EraserFRM.TFrame', relief='sunken')
        ttk.Style().configure('PaintFRM.TFrame', relief='raised')
        ttk.Style().configure('CSelect.TFrame', relief='raised')
        ttk.Style().configure('cpFRM.TFrame', relief='raised')
        ttk.Style().configure('fillFRM.TFrame', relief='raised')
        
        # Setting the eraser.
        self.canvas.change_mode(1)
    
    def newcanvas(self):
        """
        Raising the new canvas dialog. Cleaning and editing the existing canvas by the inputs.
        """
        # Creating the dialog and getting the state, for in case of an exit.
        canvas_dimensions = self.canvas.w, self.canvas.h
        new = SizeDlg(self.root, canvas_dimensions)
        state = new.getstate()

        # Editing the canvas.
        if state:
            
            # Being sure that width and height are integers between 1-256.
            wpp, hpp = new.getsize()

            if wpp:
                wpp = int(wpp)
                if wpp > 256:
                    wpp = 256
                    
            if hpp:
                hpp = int(hpp)
                if hpp > 256:
                    hpp = 256

            # The width and height are inputed as painting pixels.
            # So converting them to screen pixels, first.
            size_pp = self.canvas.get_pp_size()
            w, h = wpp*size_pp, hpp*size_pp

            self.canvas.refresh_canvas_data(wpp, hpp, size_pp)
            self.canvas['scrollregion'] = (0, 0, w, h)
            self.canvas['width'] = w
            self.canvas['height'] = h

