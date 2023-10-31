import customtkinter as ctk 
from image_wigets import *
from PIL import Image, ImageTk, ImageOps, ImageEnhance,ImageFilter
from menu import Menu
import sys,os
import tkinter as tk

class App(ctk.CTk):
    def __init__(self):
        
        #set up
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry("1000x600")
        self.title("Photo Editor")
        self.minsize(800,500)

        try:
            # Set Windows titlebar icon
            if sys.platform.startswith("win"):
                customtkinter_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                icon_path = os.path.abspath(os.path.join(customtkinter_directory, "photoshop", "icon.ico"))
                
                self.after(200, lambda: self.wm_iconphoto(True, tk.PhotoImage(file=icon_path)))
        except Exception:
            print(Exception)

        #layout
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0, weight= 2,uniform= 'a')
        self.columnconfigure(1, weight= 6,uniform= 'a')
        self.init_parameters()

        #canvas data
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        #widget
        self.imageImport = ImageImport(self,self.import_image)

        #run
        self.mainloop()

    def init_parameters(self):
        
        self.pos_vars = {
            'rotate': ctk.DoubleVar(value= ROTATE_DEFAULT),
            'zoom': ctk.DoubleVar(value= ZOOM_DEFAULT),
            'flip': ctk.StringVar(value= FLIP_OPTIONS[0])
        }
        self.color_vars = {
            'brightness':ctk.DoubleVar(value=BRIGHTNESS_DEFAULT),
            'grayscale': ctk.BooleanVar(value=GRAYSCALE_DEFAULT),
            'invert':ctk.BooleanVar(value=INVERT_DEFAULT),
            'vibrance':ctk.DoubleVar(value=VIBRANCE_DEFAULT)
        }
        self.effect_vars ={
            'blur':ctk.DoubleVar(value=BLUR_DEFAULT),
            'contrast': ctk.IntVar(value=CONTRAST_DEFAULT),
            'effect':ctk.StringVar(value=EFFECT_OPTIONS[0]),
        }
        
        lst = [self.pos_vars,self.color_vars,self.effect_vars]

        for tab in lst:
            for var in tab.values():
                var.trace('w', self.manipulate_image)

    def manipulate_image(self, *args):
        self.image = self.original
        #rotate
        if self.pos_vars['rotate'].get() != ROTATE_DEFAULT:
            self.image = self.image.rotate(self.pos_vars['rotate'].get())
        #zoom
        if self.pos_vars['zoom'].get() != ZOOM_DEFAULT:
            self.image = ImageOps.crop(image=self.image, border=self.pos_vars['zoom'].get())
        #idea zoom: lay 1 khung bang canvas o giua anh, scale hinh anh roi crop roi resize
        #flip
        if self.pos_vars['flip'].get() != FLIP_OPTIONS[0]:
            if self.pos_vars['flip'].get() == 'X':
                self.image = ImageOps.mirror(self.image)
            if  self.pos_vars['flip'].get() == 'Y':
                self.image = ImageOps.flip(self.image)
            if  self.pos_vars['flip'].get() == 'Both':
                self.image = ImageOps.flip(self.image)
                self.image = ImageOps.mirror(self.image)

        #brightness and vibrance
        if self.color_vars['brightness'].get() != BRIGHTNESS_DEFAULT:
            brightness_enhancer = ImageEnhance.Brightness(self.image)
            self.image = brightness_enhancer.enhance(self.color_vars['brightness'].get())
        if self.color_vars['vibrance'].get() != VIBRANCE_DEFAULT:
            vibrance_enhancer = ImageEnhance.Color(self.image)
            self.image = vibrance_enhancer.enhance(self.color_vars['vibrance'].get())

        #color: grayscale, invert
        if self.color_vars['grayscale'].get():
            self.image = ImageOps.grayscale(self.image)
        if self.color_vars['invert'].get():
            self.image = ImageOps.invert(self.image)

        #blur and contrast
        if self.effect_vars['blur'].get() != BLUR_DEFAULT:
            self.image = self.image.filter(ImageFilter.GaussianBlur(self.effect_vars['blur'].get()))
        if self.effect_vars['contrast'].get() != CONTRAST_DEFAULT:
            self.image = self.image.filter(ImageFilter.UnsharpMask(self.effect_vars['contrast'].get()))
        match self.effect_vars['effect'].get():
            case 'Emboss': self.image = self.image.filter(ImageFilter.EMBOSS)
            case 'Find Edges': self.image = self.image.filter(ImageFilter.FIND_EDGES)
            case 'Contour': self.image = self.image.filter(ImageFilter.CONTOUR)
            case 'Edge Enhance': self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)


        self.place_image()

    def import_image(self, path):
        self.original = Image.open(path)
        self.image = self.original
        self.image_ratio = self.image.size[0]/self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.imageImport.grid_forget()
        self.imageOutput = ImageOutput(self,self.resize_image)
        self.closeButton = CloseOutput(self,self.close_edit)
        self.menu = Menu(self, self.pos_vars,self.color_vars,self.effect_vars,self.export_image)

    def close_edit(self):
        self.imageOutput.grid_forget()
        self.closeButton.place_forget()
        self.menu.grid_forget()
        self.imageImport = ImageImport(self, self.import_image)

    def resize_image(self, event):
        #current canvas ratio
        self.canvas_ratio = event.width/event.height

        #update canvas attributes
        self.canvas_width = event.width
        self.canvas_height = event.height

        #resize
        if self.canvas_ratio > self.image_ratio:
            self.image_height = int(event.height)
            self.image_width  = int(self.image_height * self.image_ratio)
        else:
            self.image_width  = int(event.width)
            self.image_height = int(self.image_width/ self.image_ratio)
        self.place_image()

    def place_image(self):
        resized_image = self.image.resize((self.image_width,self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.imageOutput.delete('all')
        self.imageOutput.create_image(self.canvas_width/2,self.canvas_height/2,image = self.image_tk)

    def export_image(self, name, file, path):
        export_string = f'{path}/{name}.{file}'
        self.image.save(export_string)

app= App()
app.mainloop()