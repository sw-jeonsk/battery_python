import serial
import RPi.GPIO as GPIO

import time

ser = serial.Serial("/dev/serial/by-id/usb-Silicon_Labs_CP2105_Dual_USB_to_UART_Bridge_Controller_008CBB65-if00-port0", 115200,timeout=5)
ser2 = serial.Serial("/dev/serial/by-id/usb-Silicon_Labs_CP2105_Dual_USB_to_UART_Bridge_Controller_008CBB65-if01-port0", 115200,timeout=5)
ser.write("at\r\n")
ser2.write("at\r\n")
response = ser.readline()
response2 = ser2.readline()


print(response.decode("ascii"))
print(response2.decode("ascii"))

ser.close()


