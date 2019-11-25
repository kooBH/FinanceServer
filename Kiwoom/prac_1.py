import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

import mod
import kiwoom

class W_Main(QWidget):
    def __init__(self,parent):
        global kiwoom
        super(QWidget,self).__init__(parent)

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 280, 80)
        self.text_edit.setEnabled(False)

        kiwoom.OnEventConnect.connect(self.event_connect)

        self.layout.addWidget(self.text_edit)

        self.WGetInfo = mod.WGetInfo(self,kiwoom)
        self.layout.addWidget(self.WGetInfo)

        self.setLayout(self.layout)
        print('W_Main init.')


    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")


class MainWindow(QMainWindow):
    def __init__(self):
        global kiwoom
        super().__init__()

        kiwoom = kiwoom.kiwoom()
        kiwoom.comm_connect()
        #데이터 요청
        #kiwoom.req_minute_data('005930')
        
        #kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        #ret = kiwoom.dynamicCall("CommConnect()")

        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 150)
        self.W_Main = W_Main(self)
        self.setCentralWidget(self.W_Main)
        self.show()
        print('Main Window init.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow= MainWindow()
    MainWindow.show()
    app.exec_()