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
import logging
import optparse
import datetime

LOGGING_LEVELS = {'critical': logging.CRITICAL,
                  'error': logging.ERROR,
                  'warning': logging.WARNING,
                  'info': logging.INFO,
                  'debug': logging.DEBUG}
## CONST.............

log = logging.getLogger('udp_server')

HOMEDIR 	= "/home/pi/Desktop/github/battery_python/source/"

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
UART_Thread 	= None #Data and Charge
VIEW_Thread 	= None #View Cycle
LED_Thread  	= None
CHARGE_Thread  	= None

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
NEXT_VIEW = 5 #seconds
UART_TIME = 1 
USBPORT = '/dev/ttyAMA0'

##GPIO
S1= 10
S2= 9
S3= 11

S1_flag = 0
S2_flag = 0
S3_flag = 0

#output...LED
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


#OUTPUT..CHARGE
VIN1_EN = 6
VIN2_EN = 13
VIN3_EN = 19
VIN4_EN = 26

QC_CH_EN1 = 8
QC_CH_EN2 = 7


########################################################################################


root = Tk()

frame = Frame(root)

canvas = Canvas(frame, bg = "black", width=Width, height=Height)

canvas.pack()

constant.init()

BLUR 		= PhotoImage(file=HOMEDIR + "image/weather_blur.png")
CLOUD 		= PhotoImage(file=HOMEDIR + "image/weather_cloud.png")
CLOUDSUN 	= PhotoImage(file=HOMEDIR + "image/weather_cloudsun.png")
RAIN 		= PhotoImage(file=HOMEDIR + "image/weather_rain.png")
SUN 		= PhotoImage(file=HOMEDIR + "image/weather_sun.png")


TEMPER_MARK     = PhotoImage(file=HOMEDIR + "image/temper_mark.png")
PERCENT_MARK    = PhotoImage(file=HOMEDIR + "image/percent_mark.png")

GOODBYE     = PhotoImage(file=HOMEDIR + "image/text_goodbye.png")
HELLO       = PhotoImage(file=HOMEDIR + "image/text_hello.png")
NO_BATTERY  = PhotoImage(file=HOMEDIR + "image/text_no_battery.png")

POPUP01     = PhotoImage(file=HOMEDIR + "image/text_field_popup01.png")
POPUP02     = PhotoImage(file=HOMEDIR + "image/text_field_popup02.png")

NAME_FIELD   = PhotoImage(file=HOMEDIR + "image/name_field.png")

BED_BATTERY = PhotoImage(file=HOMEDIR + "image/bed_battery.png")


DICT_NFC0 = {b"01": None, b"02" : None, b"03" : None, b"04" : None, b"05": None, b"06": None, "view" : 0, "ch_gpio" : VIN1_EN, "qc_gpio": QC_CH_EN1, "led_gpio" : CHARGE_EN1,  "discon_count" : 0}
DICT_NFC1 = {b"01": None, b"02" : None, b"03" : None, b"04" : None, b"05": None, b"06": None, "view" : 0, "ch_gpio" : VIN2_EN, "qc_gpio": QC_CH_EN1, "led_gpio" : CHARGE_EN2, "discon_count" : 0}
DICT_NFC2 = {b"01": None, b"02" : None, b"03" : None, b"04" : None, b"05": None, b"06": None, "view" : 0, "ch_gpio" : VIN3_EN, "qc_gpio": QC_CH_EN2, "led_gpio" : CHARGE_EN3, "discon_count" : 0}
DICT_NFC3 = {b"01": None, b"02" : None, b"03" : None, b"04" : None, b"05": None, b"06": None, "view" : 0, "ch_gpio" : VIN4_EN, "qc_gpio": QC_CH_EN2, "led_gpio" : CHARGE_EN4,"discon_count" : 0}
DICT_NFC4 = {b"01": None, b"02" : None, b"03" : None, b"04" : None, b"05": None, b"06": None, "view" : 0, "ch_gpio" : False}
DICT_NFC5 = {b"01": None, b"02" : None, b"03" : None, b"04" : None, b"05": None, b"06": None, "view" : 0, "charge" : False}
DICT_NFC6 = {b"01": None, b"02" : None, b"03" : None, b"04" : None, b"05": None, b"06": None, "view" : 0, "charge" : False}
DICT_NFC7 = {b"01": None, b"02" : None, b"03" : None, b"04" : None, b"05": None, b"06": None, "view" : 0, "charge" : False}

DICT_ARR = [DICT_NFC0, DICT_NFC1, DICT_NFC2, DICT_NFC3, DICT_NFC4, DICT_NFC5, DICT_NFC6, DICT_NFC7]


# weather view...
def waitView():

	global BACKGROUND, NAMEFIELD, GREET, FIRST, SECOND, THIRD, MARK, SENTENCE, NOBATTERY, NAME
	index = random.randrange(0, 4)

	Weather = [BLUR, CLOUD, CLOUDSUN, RAIN, SUN]

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
		logging.info("Hello world")
		time.sleep(1)
	logging.info("goodbye World")
	


def quit(*args):
	global root, run
	root.destroy()
	run = False
	UART_Thread.join()
	GPIO.cleanup()

	
def battery(index):

	global constant, TIME

	try:
		#init.>>>>;
		name = DICT_ARR[index][b"01"]
		value =int(DICT_ARR[index][b"05"])

		logging.info("#########################################")
		logging.info("[INDEX] " + str(index))
		logging.info("[NAME] " + name)
		logging.info("[VALUE] " +str(value))

		TIME = 0
		bat_bg_index = int(value/10)
		first_value =	value%10
		second_value =  int(value/10)


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
			canvas.itemconfig(THIRD, state='normal')
			canvas.itemconfig(SECOND, image=constant.CHROME[0])
			canvas.itemconfig(FIRST, image=constant.CHROME[0])
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

			canvas.itemconfig(NAME, text=name)

		## CHANGE...
		if value < 30:
			canvas.itemconfig(SECOND, image=constant.RED[second_value])
			canvas.itemconfig(FIRST, image=constant.RED[first_value])

		elif value < 80:
			canvas.itemconfig(SECOND, image=constant.ORANGE[second_value])
			canvas.itemconfig(FIRST, image=constant.ORANGE[first_value])
		elif value < 100:
			canvas.itemconfig(SECOND, image=constant.GREEN[second_value])
			canvas.itemconfig(FIRST, image=constant.GREEN[first_value])

		canvas.itemconfig(MARK, image=PERCENT_MARK)

		## LOCATION CHANGE...
		canvas.coords(FIRST ,Bat_FirstX, Bat_FirstY)
		canvas.coords(SECOND, Bat_SecondX, Bat_SecondY)
		canvas.coords(MARK, Bat_MarkX, Bat_MarkY)

		## Thread Start..
	except ValueError:
		logging.error("FUNC[battery] Value Error...")
		parameter = str(index) + ", " + str(name) + "," + str(value)
		logging.error(parameter)



def hello_after():
	global TIME

	TIME += 1

	if TIME > NEXT_VIEW:
		waitView()
		TIME = 0
	root.after(1000, hello_after)


def uart_server():
	global UART, run, S3_flag, S2_flag, S1_flag, DICT_ARR

	UART = serial.Serial(USBPORT, BAUDRATE, timeout = UART_TIME)

	### First Uart..
	index = 0
	while run:

		if index == 4:
			index = 0

		convert(index)
		GPIO.output(S1, S1_flag)
		GPIO.output(S2, S2_flag)
		GPIO.output(S3, S3_flag)

		UART.write(b"#R,T,00\r\n")

		readData = UART.readline()
		
		try:
			#read data is not null,,,,,,

			if len(readData) != 0:
				sector_arr = [b"01",b"02", b"03", b"04", b"05", b"06"]

				for sector in sector_arr:
					response = read2check(b"#R,T,", sector)
					DICT_ARR[index][sector] = response

				DICT_ARR[index]["view"] = 1
				DICT_ARR[index]["discon_count"] = 0

			else:
				#logging.info("[READ] " + readData.decode("ascii"))
				dict_init(index)
			index += 1

		except TypeError:
			logging.error("FUNC[uart_server] TypeError")

def view_server():
	global DICT_ARR, run
		
	while run:

		for index in range(1, 4):
			view = DICT_ARR[index -1]["view"]
			name = DICT_ARR[index -1][b"01"]
			if view == 1: #view UI
				if name != None:	
					battery(index-1)
				else:
					badView()
				time.sleep(NEXT_VIEW -1)

		time.sleep(0.5)

def led_server():
	global DICT_ARR, run

	while run:
		
		for index in range(0, 3):
			name = DICT_ARR[index][b"01"]
			value = DICT_ARR[index][b"05"]
			led_gpio = DICT_ARR[index]["led_gpio"]

			if value != None and name != None:
				led_gpio = DICT_ARR[index]["led_gpio"]
				
				if value == "100":
					GPIO.output(led_gpio, True)
				else:
					flag = GPIO.input(led_gpio)
					GPIO.output(led_gpio, not flag)
			else:
				GPIO.output(led_gpio, False)

		time.sleep(1)
	
def charge_server():
	global DICT_ARR, run

	slots = [0,2]

	while run:
		
		for index in range(0, 3):
			name = DICT_ARR[index][b"01"]
			pin  = DICT_ARR[index]["ch_gpio"]

			if name != None:
				GPIO.output(pin, True)
				logging.info("#"+str(index) + " charging...")
			else:
				GPIO.output(pin, False)

		for slot in slots:
			both_connect = DICT_ARR[slot][b"01"] != None and DICT_ARR[slot + 1][b"01"] != None
			both_disconnect = DICT_ARR[slot][b"01"] == None and DICT_ARR[slot + 1][b"01"] == None
			
			if both_connect or both_disconnect:
				GPIO.output(DICT_ARR[slot]["qc_gpio"], False)
			else:
				GPIO.output(DICT_ARR[slot]["qc_gpio"], True)
				logging.info("#"+str(index) + " quick charging...")

		time.sleep(1)
		

		  




def init():
	
	global canvas, frame, UART_Thread
	##########################GPIO##########################
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(S1, GPIO.OUT)
	GPIO.setup(S2, GPIO.OUT)
	GPIO.setup(S3, GPIO.OUT)

	GPIO.setup(CHARGE_EN1, GPIO.OUT)
	GPIO.setup(CHARGE_EN2, GPIO.OUT)
	GPIO.setup(CHARGE_EN3, GPIO.OUT)
	GPIO.setup(CHARGE_EN4, GPIO.OUT)

	GPIO.setup(DOOR_EN1, GPIO.OUT)
	GPIO.setup(DOOR_EN2, GPIO.OUT)
	GPIO.setup(DOOR_EN3, GPIO.OUT)
	GPIO.setup(DOOR_EN4, GPIO.OUT)

	GPIO.setup(SOL_OFF_EN1, GPIO.IN)
	GPIO.setup(SOL_OFF_EN2, GPIO.IN)
	GPIO.setup(SOL_OFF_EN3, GPIO.IN)
	GPIO.setup(SOL_OFF_EN4, GPIO.IN)

	GPIO.setup(VIN1_EN, GPIO.OUT)
	GPIO.setup(VIN2_EN, GPIO.OUT)
	GPIO.setup(VIN3_EN, GPIO.OUT)
	GPIO.setup(VIN4_EN, GPIO.OUT)

	GPIO.setup(QC_CH_EN1, GPIO.OUT)
	GPIO.setup(QC_CH_EN2, GPIO.OUT)

	##########################LOG###########################
	now = datetime.datetime.now()
	logFile =HOMEDIR +  "logs/" + now.strftime("%m%d%H%M_") + "battery.log"
	parser = optparse.OptionParser()
	parser.add_option('-l', '--logging-level', help='Logging level')
	parser.add_option('-f', '--logging-file', help='Logging file name')
	(options, args) = parser.parse_args()
	logging_level = LOGGING_LEVELS.get(options.logging_level, logging.NOTSET)
	logging.basicConfig(level=logging_level, filename=logFile,
						format='%(asctime)s %(levelname)s: %(message)s',
						datefmt='%Y-%m-%d %H:%M:%S',
						filemode='w')
	########################################################
	#root.attributes("-fullscreen", True)
	root.bind("<Escape>", quit)    
	root.bind("x", quit)
	frame.pack()
	#########################THREAD#########################
	UART_Thread = threading.Thread(target=uart_server)
	UART_Thread.start()


	VIEW_Thread = threading.Thread(target=view_server)
	VIEW_Thread.start()

	LED_Thread = threading.Thread(target=led_server)
	LED_Thread.start()

	CHARGE_Thread = threading.Thread(target=charge_server)
	CHARGE_Thread.start()

	########################################################
	root.after(100, hello_after)
	root.mainloop()

# CMD : #R,T, CMD : 01/02/03:
def read2check(cmd, sector):
	global UART
		
	resultData = None
	data = cmd + sector + b"\r\n"
	cmdStr = "#R," + sector.decode("ascii") + ","

	UART.write(data)

	readData = UART.readline()

	try:
		if readData != None:
			readStr = readData.decode("ascii")

			if cmdStr in readStr:
				resultData = readStr.replace(cmdStr, "").replace("\r\n", "").replace("\r", "").replace("\x00","")

			else:
				resultData = None
	
	except UnicodeDecodeError:
		logging.error("fail battery")
		return resultData
		
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

def dict_init(index):
	global DICT_ARR, DICT_NFC1, DICT_NFC0, DICT_NFC2, DICT_NFC3, DICT_NFC4, DICT_NFC5, DICT_NFC6, DICT_NFC7
	
	DICT_ARR[index][b"01"] = None 
	DICT_ARR[index][b"02"] = None 
	DICT_ARR[index][b"03"] = None 
	DICT_ARR[index][b"04"] = None 
	DICT_ARR[index][b"05"] = None 
	DICT_ARR[index][b"06"] = None 
	DICT_ARR[index]["view"] = 0  # 0 : default / 1 : view flag / -1 : wait
	if DICT_ARR[index]["discon_count"] > 100:
		DICT_ARR[index]["dicson_count"] = 5
	DICT_ARR[index]["discon_count"] += 1




waitView()
init()
