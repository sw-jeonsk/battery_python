from tkinter import *
from enum 	 import Enum


HOMEDIR = "/home/pi/Desktop/github/battery_python/source/"
BATTERY = []
BLUE    = []
GREEN   = []
ORANGE  = []
RED     = []
CHROME  = []

def init():
    global BATTERY, BLUE, GREEN, ORANGE, RED, CHROME

    BATTERY = [	PhotoImage(file=HOMEDIR + "image/battery_0.png"),
                PhotoImage(file=HOMEDIR + "image/battery_10.png"),
                PhotoImage(file=HOMEDIR + "image/battery_20.png"),
                PhotoImage(file=HOMEDIR + "image/battery_30.png"),
                PhotoImage(file=HOMEDIR + "image/battery_40.png"),
                PhotoImage(file=HOMEDIR + "image/battery_50.png"),
                PhotoImage(file=HOMEDIR + "image/battery_60.png"),
                PhotoImage(file=HOMEDIR + "image/battery_70.png"),
                PhotoImage(file=HOMEDIR + "image/battery_80.png"),
                PhotoImage(file=HOMEDIR + "image/battery_90.png"),
                PhotoImage(file=HOMEDIR + "image/battery_100.png")
            ]

##################################NUMBER###################################
###########################################################################
###########################################################################
###########################################################################

    BLUE = [    PhotoImage(file=HOMEDIR + "image/number/blue_00.png"),
                PhotoImage(file=HOMEDIR + "image/number/blue_01.png"),
                PhotoImage(file=HOMEDIR + "image/number/blue_02.png"),
                PhotoImage(file=HOMEDIR + "image/number/blue_03.png"),
                PhotoImage(file=HOMEDIR + "image/number/blue_04.png"),
                PhotoImage(file=HOMEDIR + "image/number/blue_05.png"),
                PhotoImage(file=HOMEDIR + "image/number/blue_06.png"),
                PhotoImage(file=HOMEDIR + "image/number/blue_07.png"),
                PhotoImage(file=HOMEDIR + "image/number/blue_08.png"),
                PhotoImage(file=HOMEDIR + "image/number/blue_09.png")
                    ]

    CHROME = [  PhotoImage(file=HOMEDIR + "image/number/chrome_00.png"),
                PhotoImage(file=HOMEDIR + "image/number/chrome_01.png"),
                PhotoImage(file=HOMEDIR + "image/number/chrome_02.png"),
                PhotoImage(file=HOMEDIR + "image/number/chrome_03.png"),
                PhotoImage(file=HOMEDIR + "image/number/chrome_04.png"),
                PhotoImage(file=HOMEDIR + "image/number/chrome_05.png"),
                PhotoImage(file=HOMEDIR + "image/number/chrome_06.png"),
                PhotoImage(file=HOMEDIR + "image/number/chrome_07.png"),
                PhotoImage(file=HOMEDIR + "image/number/chrome_08.png"),
                PhotoImage(file=HOMEDIR + "image/number/chrome_09.png")
                    ]
    GREEN = [   PhotoImage(file=HOMEDIR + "image/number/green_00.png"),
                PhotoImage(file=HOMEDIR + "image/number/green_01.png"),
                PhotoImage(file=HOMEDIR + "image/number/green_02.png"),
                PhotoImage(file=HOMEDIR + "image/number/green_03.png"),
                PhotoImage(file=HOMEDIR + "image/number/green_04.png"),
                PhotoImage(file=HOMEDIR + "image/number/green_05.png"),
                PhotoImage(file=HOMEDIR + "image/number/green_06.png"),
                PhotoImage(file=HOMEDIR + "image/number/green_07.png"),
                PhotoImage(file=HOMEDIR + "image/number/green_08.png"),
                PhotoImage(file=HOMEDIR + "image/number/green_09.png")
                    ]
    RED = [     PhotoImage(file=HOMEDIR + "image/number/red_00.png"),
                PhotoImage(file=HOMEDIR + "image/number/red_01.png"),
                PhotoImage(file=HOMEDIR + "image/number/red_02.png"),
                PhotoImage(file=HOMEDIR + "image/number/red_03.png"),
                PhotoImage(file=HOMEDIR + "image/number/red_04.png"),
                PhotoImage(file=HOMEDIR + "image/number/red_05.png"),
                PhotoImage(file=HOMEDIR + "image/number/red_06.png"),
                PhotoImage(file=HOMEDIR + "image/number/red_07.png"),
                PhotoImage(file=HOMEDIR + "image/number/red_08.png"),
                PhotoImage(file=HOMEDIR + "image/number/red_09.png")
                    ]
    ORANGE = [  PhotoImage(file=HOMEDIR + "image/number/orange_00.png"),
                PhotoImage(file=HOMEDIR + "image/number/orange_01.png"),
                PhotoImage(file=HOMEDIR + "image/number/orange_02.png"),
                PhotoImage(file=HOMEDIR + "image/number/orange_03.png"),
                PhotoImage(file=HOMEDIR + "image/number/orange_04.png"),
                PhotoImage(file=HOMEDIR + "image/number/orange_05.png"),
                PhotoImage(file=HOMEDIR + "image/number/orange_06.png"),
                PhotoImage(file=HOMEDIR + "image/number/orange_07.png"),
                PhotoImage(file=HOMEDIR + "image/number/orange_08.png"),
                PhotoImage(file=HOMEDIR + "image/number/orange_09.png")
                    ]
    ###########################################################################
    ###########################################################################


    
