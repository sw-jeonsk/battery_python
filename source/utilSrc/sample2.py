#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from tkinter import font
import time

def quit(*args):
	root.destroy()

root = Tk()
photo = PhotoImage(file = file="image/number/blue_00.png")
w = Label(root, image=photo)
w.pack()

root.attributes("-fullscreen", True)
root.configure(background='black')
root.bind("<Escape>", quit)     # key
root.bind("x", quit)            # key




root.mainloop()