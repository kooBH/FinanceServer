from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class WGetInfo(QWidget):
    def __init__(self,parent,_kiwoom):
        global kiwoom
        super(QWidget,self).__init__(parent)
        kiwoom = _kiwoom

       # kiwoom.OnReceiveTrData.connect(self.receive_trdata)

        self.layout_main = QVBoxLayout()
        ################ DISPLAY   #########################################
        self.widget_display = QWidget()
        self.layout_display = QHBoxLayout()

        self.label_code = QLabel('종목코드: ', )
        #self.label_code.move(20, 20)
        self.layout_display.addWidget(self.label_code)

        self.code_edit = QLineEdit()
        #self.code_edit.move(80, 20)
        self.code_edit.setText("039490")
        self.layout_display.addWidget(self.code_edit)

        self.label_name = QLabel('종목명: ', )
        self.layout_display.addWidget(self.label_name)

        self.widget_display.setLayout(self.layout_display)
        self.layout_main.addWidget(self.widget_display)
        #################################################################       
        self.btn1 = QPushButton("조회" )
        self.btn1.move(190, 20)
        self.btn1.clicked.connect(lambda: self.GetNameOfTR(self.code_edit.text()))

        self.btn_get_data = QPushButton("데이터 저장")
        self.btn_get_data.setEnabled(False)
        self.layout_main.addWidget(self.btn_get_data)
        self.btn_get_data.clicked.connect(lambda : kiwoom.req_minute_data(self.code_edit.text()))

        self.layout_main.addWidget(self.btn1)

        self.text_edit = QTextEdit()
        self.text_edit.setGeometry(10, 60, 280, 80)
        self.text_edit.setEnabled(False)

        self.layout_main.addWidget(self.text_edit)

        self.setLayout(self.layout_main)
    
    def GetNameOfTR(self,tr):
        global kiwoom
        name = kiwoom.dynamicCall("GetMasterCodeName(QString)", [tr])
        print('GetNameOfTR : ' + str(name))
        self.label_name.setText('종목명 : ' + str(name))
        self.btn_get_data.setEnabled(True)

   
