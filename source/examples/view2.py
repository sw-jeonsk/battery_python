from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import Canvas
from enum 	 import Enum
import PIL.Image
import PIL.ImageTk
import time

Width 		= 1280
Height		= 960
IntervalX	= 50	
IntervalY	= 250
NumWidth	= 199
NumHeight	= 254
TMarkSize	= 83

SecondX	 	=	685 + NumWidth/2
SecondY		=	625 + NumHeight/2

FirstX	 	=	884 + NumWidth/2
FirstY	 	=	625 + NumHeight/2

MarkX		=	1084 + TMarkSize/2
MarkY		=	625 + TMarkSize/2


class MainWindow():
    def __init__ (self, main):
        
        print("init")
        self.frame = Frame(root)

        self.canvas = Canvas(self.frame, bg = "black", width=Width, height=Height)

        self.canvas.pack()


        photo = PhotoImage(file = file="image/weather_cloudsun.png")

        self.my_images = []

        self.my_images.append(PhotoImage(file = file="image/number/chrome_02.png"))
        self.my_images.append(PhotoImage(file = file="image/number/chrome_00.png"))
        self.my_images.append(PhotoImage(file = file="image/temper_mark.png"))

        # secondNumber = PhotoImage(file= file="image/number/chrome_02.png")
        # firstNumber = PhotoImage(file= file="image/number/chrome_00.png")
        # temper_mark = PhotoImage(file= file="image/temper_mark.png")

        self.canvas.create_image( 1, 0, image=photo, anchor=NW)
        second = self.canvas.create_image(SecondX, SecondY, image=self.my_images[0])
        first  = self.canvas.create_image( FirstX, FirstY, image=self.my_images[1])
        mark   = self.canvas.create_image( MarkX, MarkY, image=self.my_images[2])

        root.attributes("-fullscreen", True)

        root.configure()
        root.bind("<Escape>", quit)     # key
        root.bind("x", quit) 
        self.frame.pack()
    def quit(self):
        global root
        root.destroy()


root = Tk()
MainWindow(root)
root.mainloop()