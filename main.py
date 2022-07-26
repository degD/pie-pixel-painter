
from tkinter import *
from tkinter import ttk


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
        

root = Tk()
PiePixelPainter(root)
root.mainloop()