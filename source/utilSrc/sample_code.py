#!/usr/bin/python 

# uses the curses library to make a terminal screen that allows
# the user to communicate with Atlas Scientific boards

import serial # required for communication with boards
import RPi.GPIO as GPIO
from time import strftime, sleep # used for timestamps, delays

def main(stdscr):
    #screen parameters
    pos_text = 0 # the position of the cursor in the user input area
    
    #USB parameters
    usbport = '/dev/ttyAMA0'
    ser = serial.Serial(usbport, 38400, timeout = 1) # sets the serial port to the specified port, with a 9600 baud rate
    # Timeout = 0 tells the serial port to not wait for input if there is non 
    
    # declare and initialize the data buffers

    #channel = 0
    GPIO.setmode(GPIO.BCM)
    S0_pin = 18
    S1_pin = 23
    channel = '0' # intial channel
    GPIO.setup(S0_pin, GPIO.OUT) # S0 
    GPIO.setup(S1_pin, GPIO.OUT) # S1
    GPIO.output(S0_pin, False)
    GPIO.output(S1_pin, False)

    try:          
        while True:
            readData = ser.readline() 

            print(readData.decode('ascii')
    
        except KeyboardInterrupt: 
            GPIO.cleanup() # frees GPIO driver from usage
            print("EXIT")
                    
if __name__ == '__main__':
    curses.wrapper(main) # wraps the curses window to undo the changes it makes to the terminal on exits and exceptions

