from tkinter import *

import battery
import GUI
from os import listdir
from os import path

from time import sleep
import PIL.Image

imagePath = "C:\\Users\seokyu\Desktop\github\\battery_python\source\image"
def search(_imagepath):

    #이미지 폴더 안에는 png.. 파일만
    imageName = [image[:-4] for image in listdir(_imagepath)]
    absPathimages = [ path.join(_imagepath, image) for image in listdir(_imagepath)]
    photoImages = {}

    for (name, absPath) in zip (imageName, absPathimages):
        photoImages[name] = PhotoImage(file=absPath)

    return photoImages



#메인 함수 정의...
def main():
    ##VARIABLE..############################
    ArrBackgroundXY = [1024, 768]
    tkRoot = Tk()
    tkFrame = Frame(tkRoot)
    ########################################

    photoImages = search(imagePath)

    gui = GUI.view(ArrBackgroundXY, photoImages)

    gui.viewSetting(tkRoot, tkFrame)
    #
    # bat = battery.batView()
    #
    # bat.hello()

if __name__ == '__main__':
    main()