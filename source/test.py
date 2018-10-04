from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import Canvas

t = Tk()
t.title("Transparency")

frame = Frame(t)
frame.pack()
canvas = Canvas(frame, bg="black", width=500, height=500)
canvas.pack()

photoImage = PhotoImage(file= file="image/weather_cloud.png")
photoimage = PhotoImage(file=file="image/number/blue_00.png")
canvas.create_image(150, 150, image=photoimage)


t.attributes("-fullscreen", True)
t.mainloop()