
from tkinter import *
from tkinter import ttk


class PixelPaintingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.bind("<Button-1>", self.paintsinglepixel)
        self.bind("<B1-Motion>", self.paintpixels)
    
    def paintsinglepixel(self, event):
        x, y = self.canvasx(event.x), self.canvasy(event.y)
        
        rect_coords = self.pixelcalc(x, y)
        self.create_rectangle(rect_coords, fill='red', outline='red')
         
    def paintpixels(self, event):
        x, y = self.canvasx(event.x), self.canvasy(event.y)
        
        rect_coords = self.pixelcalc(x, y)
        self.create_rectangle(rect_coords, fill='red', outline='red')
        
    def pixelcalc(self, x, y):
        size = 20
        
        px = x // size
        py = y // size
        
        topx, topy = px*size, py*size
        bottomx, bottomy = (px+1)*size, (py+1)*size
        
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
        canvas = PixelPaintingCanvas(root, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set, background='white')
        h_scroll['command'] = canvas.xview
        v_scroll['command'] = canvas.yview
        
        canvas.grid(column=0, row=0, sticky=(N, S, W, E))
        h_scroll.grid(column=0, row=1, sticky=(W, E))
        v_scroll.grid(column=1, row=0, sticky=(N, S))
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        

        
        
        
        

root = Tk()
PiePixelPainter(root)
root.mainloop()