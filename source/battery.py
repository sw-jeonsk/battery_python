

class batView():
    def __init__(self, _value, _name):
        self.m_NumValue = _value
        self.m_StrName = _name
        self.m_ArrFristNumXY = [0, 0]
        self.m_ArrSecondNumXY = [0, 0]
        self.m_ArrPercentXY = [0,0]
        self.m_ArrBarXY = [0, 0]

    def checkVariable(self):
        print("checkVariable-----------")
        print("NAME : " + self.m_StrName)
        print("VALUE : " + self.m_NumValue)


