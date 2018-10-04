#!/usr/bin/env python3

# import...
from tkinter import *
from tkinter import ttk
from tkinter import Canvas
from enum 	 import Enum

import logging
import PIL.Image
import threading
import socket
import random
import tkinter.font
import tkinter.font

import time
import constant

## CONST.............

log = logging.getLogger('udp_server')


Width 		= 1280
Height		= 960

IntervalX	= 50	
IntervalY	= 250
NumWidth	= 199
NumHeight	= 254
TMarkSize	= 83

Temp_ThirdX			=	486 +  NumWidth/2
Temp_ThirdY			=	625 + NumHeight/2

Temp_SecondX	 	=	685 + NumWidth/2
Temp_SecondY		=	625 + NumHeight/2

Temp_FirstX	 	=	884 + NumWidth/2
Temp_FirstY	 	=	625 + NumHeight/2

Temp_MarkX		=	1084 + TMarkSize/2
Temp_MarkY		=	625 + TMarkSize/2


Bat_SecondX	 	=	586 + NumWidth/2
Bat_SecondY		=	431 + NumHeight/2

Bat_FirstX	 	=	785 + NumWidth/2
Bat_FirstY	 	=	431 + NumHeight/2

Bat_MarkX		=	984 + TMarkSize/2
Bat_MarkY		=	542 + TMarkSize/2

BarX		= 406
BarY 		= 258


GreetX		= 406 + 406/2
GreetY		= 168 + 168/3

NameX		= 691 + 691/4
NameY		= 282 + 282/8

SentanceX 	= Width/2
SentanceY	= 773 

NoBatteryX  = 468 + 468/2 + 100
NoBatteryY  = 431
run = True
Thread1 = None

BACKGROUND 	= None
THIRD		= None
SECOND 		= None
FIRST 		= None
MARK 		= None
GREET 		= None
NAMEFIELD 	= None
SENTENCE	= None
NOBATTERY	= None
NAME		= None

HOST = '127.0.0.1'
PORT = 1234
UDP_SOCKET = None
TIME = 0

########################################################################################


root = Tk()

frame = Frame(root)

canvas = Canvas(frame, bg = "black", width=Width, height=Height)

canvas.pack()

constant.init()

BLUR 		= PhotoImage(file="image/weather_blur.png")
CLOUD 		= PhotoImage(file="image/weather_cloud.png")
CLOUDSUN 	= PhotoImage(file="image/weather_cloudsun.png")
RAIN 		= PhotoImage(file="image/weather_rain.png")
SUN 		= PhotoImage(file="image/weather_sun.png")


TEMPER_MARK     = PhotoImage(file="image/temper_mark.png")
PERCENT_MARK    = PhotoImage(file="image/percent_mark.png")

GOODBYE     = PhotoImage(file="image/text_goodbye.png")
HELLO       = PhotoImage(file="image/text_hello.png")
NO_BATTERY  = PhotoImage(file="image/text_no_battery.png")

POPUP01     = PhotoImage(file="image/text_field_popup01.png")
POPUP02     = PhotoImage(file="image/text_field_popup02.png")

NAME_FIELD   = PhotoImage(file="image/name_field.png")

BED_BATTERY = PhotoImage(file="image/bed_battery.png")

## 초기 화면... & 대기화면
def waitView():

	global BACKGROUND, NAMEFIELD, GREET, FIRST, SECOND, THIRD, MARK, SENTENCE, NOBATTERY, NAME

	Weather = [BLUR, CLOUD, CLOUDSUN, RAIN, SUN]

	index = random.randrange(0, 4)
	if BACKGROUND == None:
		BACKGROUND 	= canvas.create_image( 1, 0, image=Weather[index], anchor=NW)
		THIRD		= canvas.create_image(Temp_ThirdX, Temp_ThirdY, image= constant.CHROME[1])
		SECOND 		= canvas.create_image(Temp_SecondX, Temp_SecondY, image=constant.CHROME[2])
		FIRST  		= canvas.create_image(Temp_FirstX, Temp_FirstY, image=constant.CHROME[5])
		MARK   		= canvas.create_image(Temp_MarkX, Temp_MarkY, image=TEMPER_MARK)

		GREET 		= canvas.create_image(GreetX, GreetY, image=HELLO)

		NAMEFIELD	= canvas.create_image(BarX * 2 + 30, BarY + 60, image=NAME_FIELD)
		SENTENCE	= canvas.create_image(SentanceX, SentanceY, image=POPUP01)
		NOBATTERY	= canvas.create_image(NoBatteryX, NoBatteryY, image=NO_BATTERY)
		NAME		= canvas.create_text(NameX, NameY, fill="white", font=("Noto Sans Korean", 90),
                        text="Zenny")

	## background change..Noto Sans Korean Light  Abcdefghxxklm
	canvas.itemconfig(BACKGROUND, image=Weather[index])

	## change..
	canvas.itemconfig(SECOND, image=constant.CHROME[2])
	canvas.itemconfig(FIRST, image=constant.CHROME[5])
	canvas.itemconfig(MARK, image=TEMPER_MARK)

	## normal..
	canvas.itemconfig(SECOND, state="normal")
	canvas.itemconfig(FIRST, state="normal")
	canvas.itemconfig(MARK, state="normal")

	## LOCATION CHANGE...
	canvas.coords(FIRST ,Temp_FirstX, Temp_FirstY)
	canvas.coords(SECOND, Temp_SecondX, Temp_SecondY)
	canvas.coords(MARK, Temp_MarkX, Temp_MarkY)

	## HIDDEN..
	canvas.itemconfig(NAME, state='hidden')
	canvas.itemconfig(THIRD, state='hidden')
	canvas.itemconfig(NAMEFIELD, state="hidden")
	canvas.itemconfig(GREET, state='hidden')
	canvas.itemconfig(SENTENCE, state='hidden')
	canvas.itemconfig(NOBATTERY, state='hidden')

	

def badView():

	global BACKGROUND, NAMEFIELD, GREET, FIRST, SECOND, MARK, SENTENCE


	## background change..
	canvas.itemconfig(BACKGROUND, image=BED_BATTERY)

	## NORMAL..
	canvas.itemconfig(NOBATTERY, state='normal')

	## HIDDEN..
	canvas.itemconfig(THIRD, state='hidden')
	canvas.itemconfig(SECOND, state="hidden")
	canvas.itemconfig(FIRST, state='hidden')

	canvas.itemconfig(MARK, state='hidden')
	canvas.itemconfig(NAMEFIELD, state="hidden")
	canvas.itemconfig(GREET, state='hidden')
	canvas.itemconfig(SENTENCE, state='hidden')
	canvas.itemconfig(NAME, state='hidden')



def hello_thread():
	while run:
		print("Hello world")
		time.sleep(1)
	print("goodbye World")
	


def quit(*args):
	global root, run
	root.destroy()
	run = False
	UDP_SOCKET.close()
	Thread1.join()

def weather(*args):

	global canvas, mark, percent_mark

	canvas.itemconfig(BACKGROUND, image=CLOUD)

	## HIDDEN...
	canvas.itemconfig(NAMEFIELD, state="hidden")
	canvas.itemconfig(GREET, state='hidden')

	## NORMAL...
	canvas.itemconfig(SECOND, state="normal")
	canvas.itemconfig(FIRST, state='normal')
	canvas.itemconfig(MARK, state='normal')

	## CHANGE...
	canvas.itemconfig(SECOND, image=constant.CHROME[5])
	canvas.itemconfig(FIRST, image=constant.CHROME[2])
	canvas.itemconfig(MARK, image=TEMPER_MARK)
	
	## LOCATION CHANGE...
	canvas.coords(FIRST ,Temp_FirstX, Temp_FirstY)
	canvas.coords(SECOND, Temp_SecondX, Temp_SecondY)
	canvas.coords(MARK, Temp_MarkX, Temp_MarkY)


def battery_state(*args):

	## BACKGROUND CHANGE...
	canvas.itemconfig(BACKGROUND, image=constant.BATTERY[10])

	## HIDDEN...
	canvas.itemconfig(NAMEFIELD, state="normal")
	canvas.itemconfig(GREET, state='normal')

	## NORMAL...
	canvas.itemconfig(SECOND, state="normal")
	canvas.itemconfig(FIRST, state='normal')
	canvas.itemconfig(MARK, state='normal')

	## CHANGE...
	canvas.itemconfig(SECOND, image=constant.BLUE[9])
	canvas.itemconfig(FIRST, image=constant.BLUE[0])
	canvas.itemconfig(MARK, image=PERCENT_MARK)

	## LOCATION CHANGE...
	canvas.coords(FIRST ,Bat_FirstX, Bat_FirstY)
	canvas.coords(SECOND, Bat_SecondX, Bat_SecondY)
	canvas.coords(MARK, Bat_MarkX, Bat_MarkY)

	
def battery(value):

	global constant

	bat_bg_index = int(value/10)
	first_value =	value%10
	second_value =  int(value/10)
	## BACKGROUND CHANGE...
	
	print(int(bat_bg_index))
	print(int(first_value))
	print(second_value)
	
	canvas.itemconfig(BACKGROUND, image=constant.BATTERY[bat_bg_index])

	## HIDDEN...
	canvas.itemconfig(NOBATTERY, state='hidden')
	canvas.itemconfig(SENTENCE, state='hidden')
	
	if value >= 99:
		canvas.itemconfig(BACKGROUND, image=constant.BATTERY[10])
		canvas.itemconfig(SENTENCE, state='normal')
		canvas.itemconfig(SENTENCE, image=POPUP01)
		canvas.itemconfig(MARK, state='normal')


	elif value == 100:
		canvas.itemconfig(BACKGROUND, image=constant.BATTERY[10])
		canvas.itemconfig(THIRD, state='normal') 				#백의 자리
		canvas.itemconfig(SECOND, image=constant.CHROME[0]) 	#십의 자리
		canvas.itemconfig(FIRST, image=constant.CHROME[0]) 		#일의 자리
		canvas.itemconfig(SENTENCE, state='normal')
		canvas.itemconfig(SENTENCE, image=POPUP01)
		canvas.itemconfig(MARK, state='normal')


	else:
		## NORMAL...
		canvas.itemconfig(NAMEFIELD, state="normal")
		canvas.itemconfig(GREET, state='normal')
		canvas.itemconfig(SECOND, state="normal")
		canvas.itemconfig(FIRST, state='normal')
		canvas.itemconfig(MARK, state='normal')
		canvas.itemconfig(NAME, state='normal')
	

	## CHANGE...
	if value <= 30:
		canvas.itemconfig(SECOND, image=constant.RED[second_value])
		canvas.itemconfig(FIRST, image=constant.RED[first_value])
	elif value <= 55:
		canvas.itemconfig(SECOND, image=constant.ORANGE[second_value])
		canvas.itemconfig(FIRST, image=constant.ORANGE[first_value])
	elif value <= 75:
		canvas.itemconfig(SECOND, image=constant.GREEN[second_value])
		canvas.itemconfig(FIRST, image=constant.GREEN[first_value])
	elif value <= 100:
		canvas.itemconfig(SECOND, image=constant.BLUE[second_value])
		canvas.itemconfig(FIRST, image=constant.BLUE[first_value])
		
	canvas.itemconfig(MARK, image=PERCENT_MARK)

	## LOCATION CHANGE...
	canvas.coords(FIRST ,Bat_FirstX, Bat_FirstY)
	canvas.coords(SECOND, Bat_SecondX, Bat_SecondY)
	canvas.coords(MARK, Bat_MarkX, Bat_MarkY)




def hello_after():
	global TIME

	TIME += 1

	if TIME > 10:
		waitView()
		TIME = 0
	root.after(1000, hello_after)


def udp_server():

	global HOST, PORT, UDP_SOCKET, TIME

	UDP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	UDP_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


	print("Listening on UDP")
	log.info("Listening on UDP %s:%s" % (HOST, PORT))
	UDP_SOCKET.bind((HOST, PORT))

	while run:
		(data, addr) = UDP_SOCKET.recvfrom(128*1024)
		print("data : ", data)
		TIME = 0
		if data == b'wait':
			waitView()
		elif data == b'bad':
			badView()
		elif type(int(data)) == int:
			print(data)
			battery(int(data))
		
		else:
			print(type(data))


# def uart_server():
# 	global UART, run
#
# 	while run:
# 		readData = UART.readline()
#
# 		if len(readData) != 0:
# 			data = readData.decode('ascii')
# 			print(data) #DEBUG
# 			arrData = data.split(',') # #R/T/01/data
# 		else:
# 			pass

def init():
	
	global canvas, frame, Thread1

	
	# root.attributes("-fullscreen", True)

	root.bind("<Escape>", quit)    
	root.bind("x", quit) 

	root.bind("w", weather)
	root.bind("b", battery_state)
	frame.pack()

	Thread1 = threading.Thread(target=udp_server)


	Thread1.start()
	root.after(100, hello_after)
	root.mainloop()



waitView()
init()