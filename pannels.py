from tkinter import filedialog
from typing import Callable, Optional, Tuple, Union
import customtkinter as ctk
from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.image import CTkImage
from setting import *

class Panel(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(master = parent, fg_color= DARK_GREY)
        self.pack(fill = 'x',pady = 4, ipady = 8)

class SliderPanel(Panel):
    def __init__(self, parent, text, data_var,min_value,max_value):
        super().__init__(parent=parent)

        self.rowconfigure((0,1),weight=1)
        self.columnconfigure((0,1),weight=1)
        self.data_var = data_var
        self.data_var.trace('w', self.update_text)

        ctk.CTkLabel(self,text=text).grid(column = 0, row = 0,sticky = 'w', padx = 5)
        self.num_label = ctk.CTkLabel(self,text= data_var.get()) 
        self.num_label.grid(column = 1, row = 0,sticky = 'e', padx = 5)
        ctk.CTkSlider(self,
                      fg_color= SLIDER_BG,
                      variable= self.data_var,
                      from_= min_value,
                      to = max_value,).grid(row = 1, column = 0, columnspan = 2, sticky = 'ew',padx = 5, pady = 5)
    
    def update_text(self, *args):
        self.num_label.configure(text = f'{round(self.data_var.get(),2)}')

class SegmentedPanel(Panel):
    def __init__(self, parent,text,data_var,options):
        super().__init__(parent)
        ctk.CTkLabel(self,text= text).pack()
        ctk.CTkSegmentedButton(self,variable=data_var,values = options).pack(expand= True,fill='both',padx = 4, pady =4)

class SwitchPanel(Panel):
    def __init__(self, parent,*args):
        super().__init__(parent)   
        for var, text in args:
            switch = ctk.CTkSwitch(self,text=text,variable=var,button_color=BLUE,fg_color=SLIDER_BG)
            switch.pack(side = 'left', expand = True, fill = "both", padx = 5, pady =5)

class DropDownPanel(ctk.CTkOptionMenu):
    def __init__(self,parent,data_var,options):
        super().__init__(master = parent,values=options,fg_color=DARK_GREY,button_color=DROPDOWN_MAIN_COLOR,button_hover_color=DROPDOWN_HOVER_COLOR,dropdown_fg_color=DROPDOWN_MENU_COLOR,variable=data_var)
        self.pack(fill = 'x', pady = 4)

class RevertButton(ctk.CTkButton):
    def __init__(self,parent, *args):
        super().__init__(master=parent, text='Revert')
        self.pack(side='bottom',pady  =10)
        self.args = args
    def revert(self):
        for option, reset in self.args:
            option.set(reset)

class FileNamePanel(Panel):
    def __init__(self, parent,name_string, file_string):
        super().__init__(parent)
        #data
        self.name_string = name_string
        self.name_string.trace('w',self.update_text)
        self.file_string = file_string

        #checkboxes
        ctk.CTkEntry(self,textvariable=self.name_string).pack(fill = 'x', padx = 20, pady = 5)
        frame = ctk.CTkFrame(self, fg_color= 'transparent')
        jpg_check = ctk.CTkCheckBox(frame, text= 'jpg',variable=self.file_string, command= lambda: self.click('jpg'),onvalue='jpg',offvalue='png')
        jpg_check = ctk.CTkCheckBox(frame, text= 'png', variable=self.file_string, command= lambda: self.click('png'),onvalue='png',offvalue='jpg')
        jpg_check.pack(side = 'left', fill = 'x', expand = True)
        jpg_check.pack(side = 'left', fill = 'x', expand = True)
        frame.pack(fill = 'x', expand = True,padx = 20)

        #preview
        self.output = ctk.CTkLabel(self, text='')
        self.output.pack()
    
    def click(self, text):
        self.file_string.set(text)
        self.update_text()

    def update_text(self, *args):
        if self.name_string.get():
            text = self.name_string.get().replace(' ','_') + '.' + self.file_string.get()
            self.output.configure(text=text)

class FilePathPanel(Panel):
    def __init__(self, parent,path_string):
        super().__init__(parent)
        #data
        self.path_string = path_string
        export_button = ctk.CTkButton(self,text='Open Explorer',command=self.open_file_dialog).pack(pady = 5)
        path_entry = ctk.CTkEntry(self,textvariable=self.path_string).pack(expand = True,fill = 'both',padx = 5, pady = 5)
    
    def open_file_dialog(self):
        self.path_string.set(filedialog.askdirectory())

class SaveButton(ctk.CTkButton):
    def __init__(self,parent, export_image,name_string, file_string, path_string):
        super().__init__(master=parent, text='Save', command= self.save)
        self.export_image= export_image
        self.name_string= name_string
        self.file_string= file_string
        self.path_string= path_string
        self.pack(side='bottom',pady = 10)
        
    def save(self):
        self.export_image(self.name_string.get(),self.file_string.gte(),self.path_string.get())