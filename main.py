
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser


class PixelPaintingCanvas(Canvas):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.paintcolor = 'black'    
        
        self.bind("<Button-1>", self.paintsinglepixel)
        self.bind("<B1-Motion>", self.paintpixels)
        
    def getcolor(self):
        return self.paintcolor
    
    def setcolor(self, color):
        self.paintcolor = color

    def paintsinglepixel(self, event):
        x, y = self.canvasx(event.x), self.canvasy(event.y)
        
        rect_coords = self.pixelcalc(x, y)
        self.create_rectangle(rect_coords, fill=self.paintcolor, outline=self.paintcolor)
         
    def paintpixels(self, event):
        x, y = self.canvasx(event.x), self.canvasy(event.y)
        
        rect_coords = self.pixelcalc(x, y)
        self.create_rectangle(rect_coords, fill=self.paintcolor, outline=self.paintcolor)
        
    def pixelcalc(self, x, y):
        size = 20
        
        px = x // size
        py = y // size
        
        topx, topy = px*size, py*size
        bottomx, bottomy = (px+1)*size, (py+1)*size
        
        return (topx-2, topy-2, bottomx-2, bottomy-2)
        

class SizeDlg():
    
    def __init__(self, subwindow):
        root = Toplevel(subwindow)
        root.title('New Window')
        
        def exitdlg():
            root.grab_release()
            root.destroy()
        
        root.protocol('WM_DELETE_WINDOW', exitdlg)
        root.transient(subwindow)
        root.wait_visibility()
        root.grab_set()
        
        frame = ttk.Frame(root)
        frame.grid(column=0, row=0, sticky=(N, S, W, E))
        
        ttk.Label(frame, text='Width:').grid(column=0, row=0, sticky=(N, S, W, E))
        ttk.Label(frame, text='Height:').grid(column=0, row=1, sticky=(N, S, W, E))
        
        w = StringVar()
        wentry = ttk.Entry(frame, width=5, textvariable=w)
        wentry.grid(column=1, row=0, sticky=(N, S, W, E))
        
        h = StringVar()
        hentry = ttk.Entry(frame, width=5, textvariable=h)
        hentry.grid(column=1, row=1, sticky=(N, S, W, E))
        
        self.state = 0 
        # 1 -> new win, 0 -> old win
        
        def setstate():
            self.state = 1
            exitdlg()
        
        okbutton = ttk.Button(frame, text='Ok', command=setstate)
        okbutton.grid(column=0, row=2, sticky=(N, S))
        
        cancelbutton = ttk.Button(frame, text='Cancel', command=exitdlg)
        cancelbutton.grid(column=1, row=2, sticky=(N, S))
        
        root.wait_window()
        
    def getstate(self):
        return self.state
        
        


class PiePixelPainter():
    
    def __init__(self, root):
        self.root = root
        
        root.title('PIE PIXEL PAINTER')
        root.option_add('*tearOff', False)
        
        menubar = Menu(root) # Menu bar
        root['menu'] = menubar
        
        menu_file = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_recent = Menu(menu_file)
        menu_file.add_command(label='New', command=self.newcanvas)
        menu_file.add_separator()
        menu_file.add_command(label='Exit')  

        h_scroll = ttk.Scrollbar(root, orient=HORIZONTAL)
        v_scroll = ttk.Scrollbar(root, orient=VERTICAL)
        self.canvas = PixelPaintingCanvas(root, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set, background='white')
        h_scroll['command'] = self.canvas.xview
        v_scroll['command'] = self.canvas.yview
        
        self.canvas.grid(column=0, row=1, sticky=(N, S, W, E))
        h_scroll.grid(column=0, row=2, sticky=(W, E))
        v_scroll.grid(column=1, row=1, sticky=(N, S))
       
        interface = ttk.Frame(root)
        interface.grid(column=0, row=0, sticky=(N, S, W, E))
        
        colorframe = ttk.Frame(interface, padding=(5, 3, 3, 0))
        colorframe.grid(column=0, row=0, sticky=(W, E))
        colorselectorstyle = ttk.Style()
        colorselectorstyle.configure('ColorSelector.TFrame', background='black', relief='sunken')
        colorselector = ttk.Frame(colorframe, height=33, width=33, style='ColorSelector.TFrame')
        colorselector.grid(column=0, row=0, sticky=W)
        colorselector.bind('<Button-1>', self.choosecolor)
        ttk.Label(colorframe, text='color', anchor='center').grid(column=0, row=1, sticky=(W, N, S)) 
        
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
        
        if state == 1:
            self.canvas.delete('all')
            




        

root = Tk()
PiePixelPainter(root)


root.mainloop()