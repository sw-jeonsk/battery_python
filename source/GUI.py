from tkinter import *
from tkinter import ttk
from tkinter import Canvas
from time import sleep


class view():

    def __init__(self,_background, _photoimage):

        self.m_ArrBackgroundXY = _background
        self.m_Canvas = None
        self.m_Photo = _photoimage

        self.batteryXY()
        self.waitXY()
        self.state = "INIT"

    def batteryXY(self):
        self.m_ArrBatBGXY = [1,0]
        self.m_ArrFristNumXY = [0, 0]
        self.m_ArrBatThirdNumXY = [0, 0]
        self.m_ArrBatSecondNumXY = [0, 0]
        self.m_ArrBatPercentXY = [0,0]
        self.m_ArrBarXY = [0, 0]

    def waitXY(self):
        self.m_ArrWaitBGXY = [1,0]
        self.m_ArrTempSecondNumXY = [0, 0]
        self.m_ArrTempPercentXY = [0, 0]
        self.m_ArrTempXY = [0, 0]

    def checkVariable(self):

        print("checkVariable-----------")
        print("WIDTH : " + str(self.m_ArrBackgroundXY[0]))
        print("HEIGHT : " + str(self.m_ArrBackgroundXY[1]))

    def viewSetting(self,  _root, _frame) :

        self.m_TkRoot = _root
        self.m_TkFrame = _frame
        self.m_Canvas = Canvas(self.m_TkFrame, bg = "black", width=self.m_ArrBackgroundXY[0], height = self.m_ArrBackgroundXY[1])
        self.m_Canvas.pack()
        bg = self.m_Canvas.create_image(0, 0, image=self.m_Photo["weather_sun"])

        self.m_TkRoot.attributes("-fullscreen", True)

        self.m_TkRoot.bind("<Escape>", quit)
        self.m_TkRoot.bind("x", quit)
        self.m_TkFrame.pack()

        self.m_TkRoot.after(1000, self.runView)

        self.m_TkRoot.mainloop()

        return self.m_TkRoot

    def quit(self, *args) -> None:
        self.m_TkRoot.destroy()

    def runView(self, _name= None , _value= None):
        # 시리얼 통신해야하고,,
        # 화면 전환 해야하고,,
        # LED 깜빡거리게 해야하고,,

        if self.state == "INIT":

            print("runView")

        self.m_TkRoot.after(1000, self.runView)




