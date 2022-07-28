
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser

# Separate it from this file
class PixelPaintingCanvas(Canvas):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.paintcolor = '#000000' # 7 character    
        
        self.bind("<Button-1>", self.paintsinglepixel)
        self.bind("<B1-Motion>", self.paintpixels)
        
        self.data = {}
        # Find a way to speed this up.
        
    def getcolor(self):
        return self.paintcolor
    
    def setcolor(self, color):
        self.paintcolor = color
    
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
        
    def pixelcalc(self, x, y):
        size = 20
        
        px = x // size
        py = y // size
        
        topx, topy = px*size, py*size
        bottomx, bottomy = (px+1)*size, (py+1)*size
        
        return (topx, topy, bottomx, bottomy)
        

class SizeDlg():
    
    def __init__(self, subwindow):
        root = Toplevel(subwindow)
        root.title('New Window')
        
        def exitdlg():
            root.grab_release()
            root.destroy()
        
        root.focus()
        root.resizable(False, False)
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
        

class PiePixelPainter():
    
    def __init__(self, root):
        self.root = root
        
        root.title('PPP')
        root.option_add('*tearOff', False)
        
        root.minsize(200, 200)
        root.maxsize(1000, 800)
        
        menubar = Menu(root) # Menu bar
        root['menu'] = menubar
        
        menu_file = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_recent = Menu(menu_file)
        menu_file.add_command(label='New', command=self.newcanvas)
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
        
        colorframe = ttk.Frame(interface, padding=(5, 3, 3, 0))
        colorframe.grid(column=0, row=0, sticky=(W, E))
        colorselectorstyle = ttk.Style()
        colorselectorstyle.configure('ColorSelector.TFrame', background='#000000', relief='sunken')
        colorselector = ttk.Frame(colorframe, height=33, width=33, style='ColorSelector.TFrame')
        colorselector.grid(column=0, row=0, sticky=W)
        colorselector.bind('<Button-1>', self.choosecolor)
        ttk.Label(colorframe, text='color', anchor='center').grid(column=0, row=1, sticky=(W, N, S))
        
        eraserframe = ttk.Frame(interface, padding=(5, 3, 3, 0))
        eraserframe.grid(column=1, row=0, sticky=(W, E))
        eraserstyle = ttk.Style()
        eraserstyle.configure('Eraser.TFrame', background='#FFFFFF', relief='sunken')
        eraser = ttk.Frame(eraserframe, height=33, width=33, style='Eraser.TFrame')
        eraser.grid(column=0, row=0, sticky=W)
        ttk.Label(eraserframe, text='eraser', anchor='center').grid(column=0, row=1, sticky=(W, N, S)) 
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

    def choosecolor(self, *args):
        color = colorchooser.askcolor(initialcolor=self.canvas.getcolor())[1]
        self.canvas.setcolor(color)
        colorselectorstyle = ttk.Style()
        colorselectorstyle.configure('ColorSelector.TFrame', background=self.canvas.getcolor(), relief='sunken')
    
    def newcanvas(self):
        new = SizeDlg(self.root)
        state = new.getstate()
        w, h = new.getsize()
        
        if state:
            self.canvas.delete('all')
            
            self.canvas['scrollregion'] = (0, 0, w, h)
            self.canvas['width'] = w
            self.canvas['height'] = h
            

root = Tk()
PiePixelPainter(root)
root.mainloop()