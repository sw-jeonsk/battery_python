#!/usr/bin/env python3

# import...
from tkinter import *
from tkinter import ttk
from tkinter import Canvas
import constant
from enum 	 import Enum

import logging
import PIL.Image
import threading
import socket
import random
import tkinter.font
import tkinter.font
import RPi.GPIO as GPIO
import serial

import time

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
UART		= None
BAUDRATE	= 38400

TIME = 0
UART_TIME = 0.5
USBPORT = '/dev/ttyAMA0'

##GPIO
S1= 10
S2= 9
S3= 11

S1_flag = 0
S2_flag = 0
S3_flag = 0
#output...
CHARGE_EN1 = 18
CHARGE_EN2 = 23
CHARGE_EN3 = 24
CHARGE_EN4 = 25

#output...
DOOR_EN1 = 12
DOOR_EN2 = 16
DOOR_EN3 = 20
DOOR_EN4 = 21

#input...
SOL_OFF_EN1 = 17
SOL_OFF_EN2 = 27
SOL_OFF_EN3 = 22
SOL_OFF_EN4 = 5

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


DICT_NFC1 = {"01": None, "02" : None, "03" : None, "04" : None, "05": None, "06": None}

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


def uart_server():
	global UART, run, S3_flag, S2_flag, S1_flag

	UART = serial.Serial(USBPORT, BAUDRATE, timeout = UART_TIME)

	GPIO.setup(S1, GPIO.OUT)
	GPIO.setup(S2, GPIO.OUT)
	GPIO.setup(S3, GPIO.OUT)

	### First Uart..
	index = 0
	while run:

		if index == 7:
			index = 0

		GPIO.output(S1, S1_flag)
		GPIO.output(S2, S2_flag)
		GPIO.output(S3, S3_flag)

		readData = UART.readline()

		#read data is not null,,,,,,

		if len(readData) != 0:
			sector_arr = ["01","02", "03", "04", "05", "06"]

			for sector in sector_arr:
				response = read2check(b"#R,T,", sector)

				if response != None:
					DICT_NFC1[sector] = response

					print("sector : " + sector + " value : " + response)

		else:
			pass

		index += 1
def init():
	
	global canvas, frame, Thread1

	
	# root.attributes("-fullscreen", True)

	root.bind("<Escape>", quit)    
	root.bind("x", quit) 

	root.bind("w", weather)
	root.bind("b", battery_state)
	frame.pack()

	Thread1 = threading.Thread(target=uart_server)


	Thread1.start()
	root.after(100, hello_after)
	root.mainloop()

# CMD : #R,T, CMD : 01/02/03
def read2check(cmd, sector):
	global UART

	data = cmd + sector + b"\r\n"
	cmdStr = cmd.decode("ascii")

	UART.write(data)

	readData = UART.readline()

	readStr = readData.decode("ascii")

	if cmdStr in readStr:
		resultData = readStr.replace(cmdStr, "").replace("\r\n", "")

	else:
		resultData = None

	return resultData

def convert(index):

	global S3_flag, S2_flag, S1_flag

	if index == 0:
		S3_flag = 0
		S2_flag = 0
		S1_flag = 0

	elif index == 1:
		S3_flag = 0
		S2_flag = 0
		S1_flag = 1

	elif index == 2:
		S3_flag = 0
		S2_flag = 1
		S1_flag = 0

	elif index == 3:
		S3_flag = 0
		S2_flag = 1
		S1_flag = 1
	elif index == 4:
		S3_flag = 1
		S2_flag = 0
		S1_flag = 0

	elif index == 5:
		S3_flag = 1
		S2_flag = 0
		S1_flag = 1

	elif index == 6:
		S3_flag = 1
		S2_flag = 1
		S1_flag = 0

	elif index == 7:
		S3_flag = 1
		S2_flag = 1
		S1_flag = 1


waitView()
init()
