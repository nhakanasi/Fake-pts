from tkinter import filedialog, Canvas
from setting import *
import customtkinter as ctk

class ImageImport(ctk.CTkFrame):
    #cover the window
    def __init__(self,parent,import_func):
        super().__init__(master= parent)
        self.grid(column = 0, columnspan = 2, row = 0 , sticky = 'nsew')
        self.import_func = import_func

        ctk.CTkButton(text="Open image",master= self,command= self.open_dialog).pack(expand = True)

    def open_dialog(self):
        path = filedialog.askopenfile().name
        self.import_func(path)

class ImageOutput(Canvas):
    
    def __init__(self, parent,resize_image):
        super().__init__(master = parent,background= BACKGROUND_COLOR,bd= 0, highlightthickness = 0,relief="ridge")
        self.grid(row = 0, column= 1, sticky= "nsew",padx = 10, pady= 10)
        self.bind('<Configure>',resize_image)

class CloseOutput(ctk.CTkButton):
    def __init__(self,parent,close_func):
        super().__init__(master= parent, text = 'x',text_color=WHITE,fg_color='transparent',width=40,height=40,corner_radius=0,hover_color=CLOSE_RED, command= close_func)
        self.place(relx = 0.99, rely = 0.01, anchor='ne')

