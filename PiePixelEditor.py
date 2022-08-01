
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
from PixelCanvas import PixelPaintingCanvas
import PieWrite

class SizeDlg():
    
    def __init__(self, subwindow):
        root = Toplevel(subwindow)
        root.title('New Window')
        
        def exitdlg():
            root.grab_release()
            root.destroy()
        
        root.geometry('60x60+') # TODO:
        root.resizable(False, False)
        
        root.focus()
        root.protocol('WM_DELETE_WINDOW', exitdlg)
        root.transient(subwindow)
        root.wait_visibility()
        root.grab_set()
        
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
        
        self.newcanvas = False
        
        def setstate():
            self.newcanvas = True
            exitdlg()
        
        okbutton = ttk.Button(frame, text='Ok', command=setstate)
        okbutton.grid(column=0, row=2, sticky=(N, S), padx=3, pady=3)
        
        cancelbutton = ttk.Button(frame, text='Cancel', command=exitdlg)
        cancelbutton.grid(column=1, row=2, sticky=(N, S), padx=3, pady=3)
        
        root.wait_window()
        
    def getstate(self):
        return self.newcanvas
    
    def getsize(self):
        return self.w.get(), self.h.get()
      

class PiePixelEditor():
    
    def __init__(self, root):
        self.root = root
        
        root.title('PPP')
        root.option_add('*tearOff', False)
        
        w_max = root.winfo_screenwidth()
        h_max = root.winfo_screenheight()
        root.maxsize(w_max, h_max)
        root.minsize(200, 200)
        
        menubar = Menu(root) # Menu bar
        root['menu'] = menubar
        
        menu_file = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.newcanvas)
        menu_file.add_separator()
        menu_file.add_command(label='Save As...', command=self.save_as_canvas) # Not finished!
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=root.destroy)  

        h_scroll = ttk.Scrollbar(root, orient=HORIZONTAL)
        v_scroll = ttk.Scrollbar(root, orient=VERTICAL)
        self.canvas = PixelPaintingCanvas(root, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set, background='white')
        self.canvas['width'] = 1000
        self.canvas['height'] = 1000
        h_scroll['command'] = self.canvas.xview
        v_scroll['command'] = self.canvas.yview
        
        self.canvas.grid(column=0, row=1)
        h_scroll.grid(column=0, row=2, sticky=(W, E))
        v_scroll.grid(column=1, row=1, sticky=(N, S))

        interface = ttk.Frame(root)
        interface.grid(column=0, row=0, sticky=(N, S, W, E))
        
        # COLOR
        colorframe = ttk.Frame(interface, padding=(5, 3, 3, 0))
        colorframe.grid(column=0, row=0, sticky=(W, E))
        colorselectorstyle = ttk.Style()
        colorselectorstyle.configure('ColorSelector.TFrame', background='#000000', relief='sunken')
        colorselector = ttk.Frame(colorframe, height=33, width=33, style='ColorSelector.TFrame')
        colorselector.grid(column=0, row=0, sticky=W)
        colorselector.bind('<Button-1>', self.choosecolor)
        ttk.Label(colorframe, text='color', anchor='center').grid(column=0, row=1, sticky=(W, N, S))
        
        # ERASER
        eraserframe = ttk.Frame(interface, padding=(5, 3, 3, 0))
        eraserframe.grid(column=1, row=0, sticky=(W, E))
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='raised')
        eraser = ttk.Frame(eraserframe, height=33, width=33, style='Eraser.TFrame')
        eraser.grid(column=0, row=0, sticky=W)
        eraser.bind('<Button-1>', self.seterasermode)
        ttk.Label(eraserframe, text='eraser', anchor='center').grid(column=0, row=1, sticky=(W, N, S)) 
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        
        self.set_win_geo()

    # Simplify these functions
    def choosecolor(self, event):
        colordata = colorchooser.askcolor(title='Choose Color', parent=self.root, initialcolor=self.canvas.getcolor())
        color = colordata[1]
        if color == None:
            color = self.canvas.getcolor()
        self.canvas.setcolor(color)
        
        colorselectorstyle = ttk.Style()
        colorselectorstyle.configure('ColorSelector.TFrame', background=color, relief='sunken')
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='raised')
        
        self.canvas.paint_mode()
        
    def seterasermode(self, event):
        colorselectorstyle = ttk.Style()
        colorselectorstyle.configure('ColorSelector.TFrame', background=self.canvas.getcolor(), relief='raised')
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='sunken')
        
        self.canvas.eraser_mode()
    
    def newcanvas(self):
        new = SizeDlg(self.root)
        state = new.getstate()
        w, h = new.getsize()
        
        if state:
            self.canvas.delete('all')
            self.canvas.reset_data()
            
            self.canvas['scrollregion'] = (0, 0, w, h)
            self.canvas['width'] = w
            self.canvas['height'] = h
            
        self.set_win_geo()
    
    def save_as_canvas(self):
        types_tuple = (('PIE Format', '.pie'), ('BMP Format', '.bmp'), ('PNG Format', '.png'), ('JPEG Format', '.jpg'), ('All Files', '*'))
        filepath = filedialog.asksaveasfilename(parent=self.root, title='Save As', defaultextension='.pie', filetypes=types_tuple)
        
        if filepath == '': return
        
        with open(filepath, 'wb') as fb:
            
            if filepath.endswith('.pie'):
                for p in self.canvas.get_cv_data():
                    x, y = p[0][0], p[0][1]
                    color = p[1]
                    PieWrite.write_p_data(x, y, color, fb)
                    
    def set_win_geo(self, w=800, h=600):
        w_sc = self.root.winfo_screenwidth() 
        h_sc = self.root.winfo_screenheight()
        
        y = (h_sc- h) // 2
        x = (w_sc - w) // 2
        
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))


        

