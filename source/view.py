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

lock = threading.Lock()

log = logging.getLogger('udp_server')

HOMEDIR 	= "/home/pi/Desktop/github/battery_python/source/"

Width 		= 1024
Height		= 768


Temp_SecondX	 	=	550
Temp_SecondY		=	500

Temp_FirstX	 	=	700
Temp_FirstY	 	=	500

Temp_MarkX		=	850
Temp_MarkY		=	480


Bat_ThirdX	 	=	400
Bat_ThirdY		=	400

Bat_SecondX	 	=	550
Bat_SecondY		=	400

Bat_FirstX	 	=	700
Bat_FirstY	 	=	400

Bat_MarkX		=	850
Bat_MarkY		=	480

BarX		= 330
BarY 		= 250

GreetX		= 330
GreetY		= 150

NameX		= 500
NameY		= 250

SentanceX 	= -100 #안전운전하세요.
SentanceY	= 650 

NoBatteryX  = 468
NoBatteryY  = 431

SlotX		= 50 
SlotY		= 40 
run = True
UART_Thread 	= None #Data and Charge
VIEW_Thread 	= None #View Cycle
LED_Thread  	= None
CHARGE_Thread  	= None
SOL_Thread		= None

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
SLOT		= None

UART		= None
BAUDRATE	= 38400

VALUE = 0
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


DICT_NFC0 = {b"01": None, b"02" : None, b"03" : None, b"04" : None, b"05": None, b"06": None, b"07": None, b"08": None, b"09": None, b"10": None, b"11": None, b"12": None, b"15": None,
			 "view" : 0, "ch_gpio" : VIN1_EN, "qc_gpio": QC_CH_EN1,"qc_enable" : 0,  "led_gpio" : CHARGE_EN1,"sol_gpio" : SOL_OFF_EN1, "door_gpio":DOOR_EN1,  "count" : 0, "discon_count" : 0}
DICT_NFC1 = {b"01": None, b"02" : None, b"03" : None, b"04" : None, b"05": None, b"06": None, b"07": None, b"08": None, b"09": None, b"10": None, b"11": None, b"12": None, b"15": None,
			 "view" : 0, "ch_gpio" : VIN2_EN, "qc_gpio": QC_CH_EN1,"qc_enable" : 0,  "led_gpio" : CHARGE_EN2,"sol_gpio" : SOL_OFF_EN2,"door_gpio" :DOOR_EN2,"count" : 0, "discon_count" : 0}
DICT_NFC2 = {b"01": None, b"02" : None, b"03" : None, b"04" : None, b"05": None, b"06": None, b"07": None, b"08": None, b"09": None, b"10": None, b"11": None, b"12": None, b"15": None,
			 "view" : 0, "ch_gpio" : VIN3_EN, "qc_gpio": QC_CH_EN2,"qc_enable" : 0,  "led_gpio" : CHARGE_EN3,"sol_gpio" : SOL_OFF_EN3,"door_gpio":DOOR_EN3, "count" : 0, "discon_count" : 0}
DICT_NFC3 = {b"01": None, b"02" : None, b"03" : None, b"04" : None, b"05": None, b"06": None, b"07": None, b"08": None, b"09": None, b"10": None, b"11": None, b"12": None, b"15": None,
			 "view" : 0, "ch_gpio" : VIN4_EN, "qc_gpio": QC_CH_EN2,"qc_enable" : 0, "led_gpio" : CHARGE_EN4, "sol_gpio" : SOL_OFF_EN4,"door_gpio":DOOR_EN4, "count" : 0, "discon_count" : 0}

DICT_ARR = [DICT_NFC0, DICT_NFC1, DICT_NFC2, DICT_NFC3]


# weather view...
def waitView():

	global BACKGROUND, NAMEFIELD, GREET, FIRST, SECOND, THIRD, MARK, SENTENCE, NOBATTERY, NAME, SLOT
	index = random.randrange(0, 4)

	Weather = [BLUR, CLOUD, CLOUDSUN, RAIN, SUN]

	canvas.delete("all")
	canvas.create_image( 1, 0, image=Weather[index], anchor=NW)
	canvas.create_image(Temp_SecondX, Temp_SecondY, image=constant.CHROME[2], anchor=NW)
	canvas.create_image(Temp_FirstX, Temp_FirstY, image=constant.CHROME[5], anchor=NW)
	canvas.create_image(Temp_MarkX, Temp_MarkY, image=TEMPER_MARK, anchor=NW)


def badView():

	global BACKGROUND, NAMEFIELD, GREET, FIRST, SECOND, MARK, SENTENCE


	## background change..
	canvas.delete("all")

	canvas.create_image(1, 0, image=BED_BATTERY, anchor=NW)
	canvas.create_image(NoBatteryX, NoBatteryY, image=NOBATTERY, anchor=NW)

	## HIDDEN..




def hello_thread():
	while run:
		logging.info("Hello world")
		time.sleep(1)
	logging.info("goodbye World")
	


def quit(*args):
	global root, run
	try:
		root.destroy()
		run = False
		UART_Thread.join()
		GPIO.cleanup()
	finally:
		GPIO.cleanup()

	
def battery(index):

	global constant, TIME

	try:
		if True:
			name = "Jordan"
			value = index
		else:
			name = DICT_ARR[index][b"01"]
			value =int(DICT_ARR[index][b"05"])

		logging.info("#########################################")
		logging.info("[INDEX] " + str(index))
		logging.info("[NAME] " + name)
		logging.info("[VALUE] " +str(value))

		TIME = 0
		canvas.delete("all")

		if value != 0:
			bat_bg_index = int(value/10)
			first_value =	value%10
			second_value =  int(value/10)

			canvas.create_image(1, 0, image=constant.BATTERY[bat_bg_index], anchor=NW)

		if value > 0  and value < 100:

			if value > 0  and value < 30:
				canvas.create_image(Bat_SecondX, Bat_SecondY, image=constant.RED[second_value], anchor=NW)
				canvas.create_image(Bat_FirstX, Bat_FirstY, image=constant.RED[first_value], anchor=NW)


			elif value >= 30 and value < 80:
				canvas.create_image(Bat_SecondX, Bat_SecondY, image=constant.ORANGE[second_value], anchor=NW)
				canvas.create_image(Bat_FirstX, Bat_FirstY, image=constant.ORANGE[first_value], anchor=NW)


			elif value >=80 and value < 100:
				canvas.create_image(Bat_SecondX, Bat_SecondY, image=constant.GREEN[second_value], anchor=NW)
				canvas.create_image(Bat_FirstX, Bat_FirstY, image=constant.GREEN[first_value], anchor=NW)


		elif value is 0:
			canvas.create_image(1, 0, image=constant.BATTERY[0], anchor=NW)
			canvas.create_image(Bat_SecondX, Bat_SecondY, image=constant.RED[0], anchor=NW)
			canvas.create_image(Bat_FirstX, Bat_FirstY, image=constant.RED[0], anchor=NW)

		elif value is 100:
			canvas.create_image(Bat_ThirdX, Bat_ThirdY, image=constant.GREEN[1], anchor=NW)
			canvas.create_image(Bat_SecondX, Bat_SecondY, image=constant.GREEN[0], anchor=NW)
			canvas.create_image(Bat_FirstX, Bat_FirstY, image=constant.GREEN[0], anchor=NW)
			canvas.create_image(SentanceX, SentanceY, image=POPUP01, anchor=NW)

		#COMMON
		canvas.create_image(BarX, BarY, image=NAME_FIELD, anchor=NW)
		canvas.create_image(GreetX, GreetY, image=HELLO, anchor=NW)
		canvas.create_image(Bat_MarkX, Bat_MarkY, image=PERCENT_MARK, anchor=NW)
		canvas.create_text(NameX, NameY, fill="white", font=("Noto Sans Korean", 80), anchor=NW, text=name)


	## Thread Start..
	except ValueError:
		logging.error("FUNC[battery] Value Error...")
		parameter = str(index) + ", " + str(name) + "," + str(value)
		logging.error(parameter)
	except TypeError:
		logging.error("FUNC[battery] Type Error...")
		parameter = str(index) + ", " + str(name) + "," + str(value)
		logging.error(parameter)




def hello_after():
	global TIME, VALUE

	TIME += 1

	# if TIME > NEXT_VIEW:
	# 	waitView()
	# 	TIME = 0


	battery(100)

	root.after(1500, hello_after)


def uart_server():
	global UART, run, S3_flag, S2_flag, S1_flag, DICT_ARR

	UART = serial.Serial(USBPORT, BAUDRATE, timeout = UART_TIME)

	### First Uart..
	index = 0
	while run:


		if index == 4:
			index = 0

		lock.acquire()
		convert(index)
		lock.release()
		GPIO.output(S1, S1_flag)
		GPIO.output(S2, S2_flag)
		GPIO.output(S3, S3_flag)

		
		try:
			UART.write(b"#R,T,00\r\n")

			readData = UART.readline()
			#read data is not null,,,,,,

			if len(readData) != 0:
				sector_arr = [b"01",b"02", b"03", b"04", b"05", b"06"]
				

				lock.acquire()
				for sector in sector_arr:
					response = read2check(b"#R,T,", sector)
					DICT_ARR[index][sector] = response

				DICT_ARR[index]["view"] = 1
				DICT_ARR[index]["count"] += 1
				DICT_ARR[index]["discon_count"] = 0

				lock.release()

			else:
				#logging.info("[READ] " + readData.decode("ascii"))
				dict_init(index)
			index += 1
		except TypeError:
			logging.error("FUNC[uart_server] TypeError")
		except serial.serialutil.SerialException:
			logging.error("FUNC[uart_server] TypeError")

def view_server():
	global DICT_ARR, run
		
	while run:

		for index in range(1, 4):
			lock.acquire()

			view = DICT_ARR[index -1]["view"]
			name = DICT_ARR[index -1][b"01"]
			lock.release()
			if view == 1: #view UI
				if name != None:	
					logging.info("NAME : " + name)
					battery(index-1)
				else:
					badView()
				time.sleep(NEXT_VIEW -1)


		time.sleep(0.5)

def led_server():
	global DICT_ARR, run

	while run:
		
		for index in range(0, 3):
			lock.acquire()
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
			lock.release()

		time.sleep(1)
	

def charge_server():
	global DICT_ARR, run

	logging.info("charge_server start")
	
	slots = [0,1]

	while run:
	
		for index in range(0, 2):

			lock.acquire()	

			name = DICT_ARR[index][b"01"]
			ch  = DICT_ARR[index]["ch_gpio"]
			sol  = DICT_ARR[index]["sol_gpio"]
			door  = DICT_ARR[index]["door_gpio"]
			value = DICT_ARR[index][b"05"]
			count = DICT_ARR[index]["count"]
			discon_count = DICT_ARR[index]["discon_count"]
			manufacture = DICT_ARR[index][b"15"]

			lock.release()
			
			#TODO
			if  count > 0  and GPIO.input(sol) == True:
				logging.info("door open")
				GPIO.output(door, True)

			if manufacture != None and GPIO.input(sol) == False:

				GPIO.output(ch, True)
				logging.info("#"+str(index) + " charging...")

				if value == "100": #charge 100%
					GPIO.output(ch, False)
			else:
				GPIO.output(ch, False)
			
		
			if  count > 5 and GPIO.input(sol) == False:
				time.sleep(1)
				logging.info("door close")
				GPIO.output(door, False)

			if discon_count > 10 and GPIO.input(door) == True:
				GPIO.output(door, False) 


			

		for slot in slots:
			both_connect = DICT_ARR[slot][b"01"] != None and DICT_ARR[slot + 1][b"01"] != None
			both_disconnect = DICT_ARR[slot][b"01"] == None and DICT_ARR[slot + 1][b"01"] == None
			
			if both_connect or both_disconnect:
				GPIO.output(DICT_ARR[slot]["qc_gpio"], False)
			else:
				GPIO.output(DICT_ARR[slot]["qc_gpio"], True)
				logging.info("#"+str(index) + " quick charging...")
		

		time.sleep(1) 

def sol_server():

	while run:

		if GPIO.input(SOL_OFF_EN1) == False:
			logging.info("SOL EN1 False")
		else:
			logging.info("SOL EN1 True")
		time.sleep(0.5)


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

	GPIO.output(DOOR_EN1, False)
	GPIO.output(DOOR_EN2, False)
	GPIO.output(DOOR_EN3, False)
	GPIO.output(DOOR_EN4, False)

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
	root.attributes("-fullscreen", True)
	root.bind("<Escape>", quit)    
	root.bind("x", quit)
	frame.pack()

	#########################THREAD#########################
	# UART_Thread = threading.Thread(target=uart_server)
	# UART_Thread.start()
	#
	#
	# VIEW_Thread = threading.Thread(target=view_server)
	# VIEW_Thread.start()
	#
	# LED_Thread = threading.Thread(target=led_server)
	# LED_Thread.start()
	#
	# CHARGE_Thread = threading.Thread(target=charge_server)
	# CHARGE_Thread.start()

	#SOL_Thread = threading.Thread(target=sol_server)
	#SOL_Thread.start()

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
	DICT_ARR[index][b"07"] = None
	DICT_ARR[index][b"08"] = None
	DICT_ARR[index][b"09"] = None
	DICT_ARR[index][b"10"] = None
	DICT_ARR[index][b"11"] = None
	DICT_ARR[index][b"12"] = None
	DICT_ARR[index][b"15"] = None

	DICT_ARR[index]["view"] = 0  # 0 : default / 1 : view flag / -1 : wait
	DICT_ARR[index]["count"] = 0
	if DICT_ARR[index]["discon_count"] > 100:
		DICT_ARR[index]["discon_count"] = 5
	DICT_ARR[index]["count"] = 0
	DICT_ARR[index]["discon_count"] += 1




waitView()
init()
