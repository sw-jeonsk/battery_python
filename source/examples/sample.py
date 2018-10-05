#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from tkinter import font
import time

def quit(*args):
	root.destroy()

def show_time():
	txt.set(time.strftime("%H:%M:%S"))
	root.after(1000, show_time)

root = Tk()
photo = PhotoImage(file = file="image/weather_cloud.png")
photo2 = PhotoImage(file = file="image/number/blue_00.png")
w = Label(root, image=photo)
w.pack()

root.attributes("-fullscreen", True)
root.configure(background='black')
root.bind("<Escape>", quit)     # key
root.bind("x", quit)            # key
root.after(1000, show_time)

fnt = font.Font(family='Helvetica', size=128, weight='bold')
txt = StringVar()
txt.set(time.strftime("%H:%M:%S"))

lbl = ttk.Label(root, textvariable=txt, font=fnt, foreground="green", image=photo2)
lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()