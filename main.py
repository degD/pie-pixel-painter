
from tkinter import *
from tkinter import ttk


class PixelPainterCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.bind("<Button-1>", self.paintsinglepixel)
        self.bind("<B1-Motion>", self.paintpixels)
        
        self.x = 0
        self.y = 0
    
    def paintsinglepixel(self, event):
        self.x, self.y = self.canvasx(event.x), self.canvasy(event.y)
        
        coords = self.pixelcalc(self.x, self.y)
        self.create_rectangle(*coords, fill='red')
        
        
        
        
    def paintpixels(self, event):
        newx, newy = self.canvasx(event.x), self.canvasy(event.y)
        
        self.create_line(self.x, self.y, newx, newy, width=20)
        self.x, self.y = newx, newy
        
    def pixelcalc(self, x, y):
        print(x, y)
        size = 20
        
        px = x // size
        py = y // size
        
        topx, topy = px*20, py*20
        bottomx, bottomy = (px+1)*20, (py+1)*20
        
        print(topx, topy, bottomx, bottomy)
        return (topx, topy, bottomx, bottomy)


class PiePixelPainter():
    
    def __init__(self, root):
        root.title('PIE PIXEL PAINTER')
        root.option_add('*tearOff', False)
        
        menubar = Menu(root) # Menu bar
        root['menu'] = menubar
        
        menu_file = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_recent = Menu(menu_file)
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_cascade(menu=menu_recent, label='Recent Files')
        menu_file.add_separator()
        menu_file.add_command(label='Save')
        menu_file.add_command(label='Save As...')
        menu_file.add_separator()
        menu_file.add_command(label='Exit')  
        
        menu_edit = Menu(menubar)   
        menubar.add_cascade(menu=menu_edit, label='Edit')
        menu_edit.add_command(label='Undo')
        menu_edit.add_command(label='Redo')
        menu_edit.add_separator()
        menu_edit.add_command(label='Options...')
                
        h_scroll = ttk.Scrollbar(root, orient=HORIZONTAL)
        v_scroll = ttk.Scrollbar(root, orient=VERTICAL)
        canvas = PixelPainterCanvas(root, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        h_scroll['command'] = canvas.xview
        v_scroll['command'] = canvas.yview
        
        canvas.grid(column=0, row=0, sticky=(N, S, W, E))
        h_scroll.grid(column=0, row=1, sticky=(W, E))
        v_scroll.grid(column=1, row=0, sticky=(N, S))
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        
        self.x = 0
        self.y = 0
        
        
        
        

root = Tk()
PiePixelPainter(root)
root.mainloop()