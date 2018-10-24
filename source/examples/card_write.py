import serial
import RPi.GPIO as GPIO

import time

S3 = 11
S2 = 10
S1 = 9


GPIO.setmode(GPIO.BCM)
GPIO.setup(S3, GPIO.OUT)
GPIO.setup(S2, GPIO.OUT)
GPIO.setup(S1, GPIO.OUT)


GPIO.output(S3, 0) 
GPIO.output(S2, 0) 
GPIO.output(S1, 0) 


ser = serial.Serial("/dev/ttyAMA0", 38400, timeout=1)
flag = 0


def battery_90():
    ser.write(b'#R,T,00\r\n')
    readData = ser.readline()
    print("Manufacture : 00")
    print(readData.decode('ascii'))

    ser.write(b'#W,01,Wendy\r\n')
    ser.write(b'#R,T,01\r\n')
    readData = ser.readline()
    print("User : 01")
    print(readData.decode('ascii'))

    ser.write(b'#W,02,0.001\r\n')
    ser.write(b'#R,T,03\r\n')
    readData = ser.readline()
    print("Cell Min : 02")
    print(readData.decode('ascii'))

    ser.write(b'#W,03,0.001\r\n')
    ser.write(b'#R,T,03\r\n')
    readData = ser.readline()
    print("Cell Max : 03")
    print(readData.decode('ascii'))

    ser.write(b'#W,04,1\r\n')
    ser.write(b'#R,T,04\r\n')
    readData = ser.readline()
    print("Pack1 electric : 04")
    print(readData.decode('ascii'))

    ser.write(b'#W,05,90\r\n')
    ser.write(b'#R,T,05\r\n')
    readData = ser.readline()
    print("SOC : 05")
    print(readData.decode('ascii'))

    ser.write(b'#W,06,10\r\n')
    ser.write(b'#R,T,06\r\n')
    readData = ser.readline()
    print("Temp Min : 06")
    print(readData.decode('ascii'))

    ser.write(b'#W,07,30\r\n')
    ser.write(b'#R,T,07\r\n')
    readData = ser.readline()
    print("Temp Max : 07")
    print(readData.decode('ascii'))

def battery_60():

    ser.write(b'#R,T,00\r\n')
    readData = ser.readline()
    print("Manufacture : 00")
    print(readData.decode('ascii'))

    ser.write(b'#W,01,Jordan\r\n')
    ser.write(b'#R,T,01\r\n')
    readData = ser.readline()
    print("User : 01")
    print(readData.decode('ascii'))

    ser.write(b'#W,02,0.001\r\n')
    ser.write(b'#R,T,03\r\n')
    readData = ser.readline()
    print("Cell Min : 02")
    print(readData.decode('ascii'))

    ser.write(b'#W,03,0.001\r\n')
    ser.write(b'#R,T,03\r\n')
    readData = ser.readline()
    print("Cell Max : 03")
    print(readData.decode('ascii'))

    ser.write(b'#W,04,1\r\n')
    ser.write(b'#R,T,04\r\n')
    readData = ser.readline()
    print("Pack1 electric : 04")
    print(readData.decode('ascii'))


    ser.write(b'#W,05,60\r\n')
    ser.write(b'#R,T,05\r\n')
    readData = ser.readline()
    print("SOC : 05")
    print(readData.decode('ascii'))

    ser.write(b'#W,06,10\r\n')
    ser.write(b'#R,T,06\r\n')
    readData = ser.readline()
    print("Temp Min : 06")
    print(readData.decode('ascii'))

    ser.write(b'#W,07,30\r\n')
    ser.write(b'#R,T,07\r\n')
    readData = ser.readline()
    print("Temp Max : 07")
    print(readData.decode('ascii'))

def battery_10():
    ser.write(b'#R,T,00\r\n')
    readData = ser.readline()
    print("Manufacture : 00")
    print(readData.decode('ascii'))

    ser.write(b'#W,01,Sam\r\n')
    ser.write(b'#R,T,01\r\n')
    readData = ser.readline()
    print("User : 01")
    print(readData.decode('ascii'))

    ser.write(b'#W,02,0.001\r\n')
    ser.write(b'#R,T,03\r\n')
    readData = ser.readline()
    print("Cell Min : 02")
    print(readData.decode('ascii'))

    ser.write(b'#W,03,0.001\r\n')
    ser.write(b'#R,T,03\r\n')
    readData = ser.readline()
    print("Cell Max : 03")
    print(readData.decode('ascii'))

    ser.write(b'#W,04,1\r\n')
    ser.write(b'#R,T,04\r\n')
    readData = ser.readline()
    print("Pack1 electric : 04")
    print(readData.decode('ascii'))


    ser.write(b'#W,05,10\r\n')
    ser.write(b'#R,T,05\r\n')
    readData = ser.readline()
    print("SOC : 05")
    print(readData.decode('ascii'))

    ser.write(b'#W,06,10\r\n')
    ser.write(b'#R,T,06\r\n')
    readData = ser.readline()
    print("Temp Min : 06")
    print(readData.decode('ascii'))

    ser.write(b'#W,07,30\r\n')
    ser.write(b'#R,T,07\r\n')
    readData = ser.readline()
    print("Temp Max : 07")
    print(readData.decode('ascii'))


battery_10()

ser.close()
GPIO.cleanup()
