from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class WGetInfo(QWidget):
    def __init__(self,parent,_kiwoom):
        global kiwoom
        super(QWidget,self).__init__(parent)
        kiwoom = _kiwoom

       # kiwoom.OnReceiveTrData.connect(self.receive_trdata)

        self.layout = QVBoxLayout()

        self.label = QLabel('종목코드: ', )
        self.label.move(20, 20)

        self.layout.addWidget(self.label)

        self.code_edit = QLineEdit()
        self.code_edit.move(80, 20)
        self.code_edit.setText("039490")

        self.layout.addWidget(self.code_edit)

        self.btn1 = QPushButton("조회", )
        self.btn1.move(190, 20)
        #self.btn1.clicked.connect(self.btn_basic_query)

        self.layout.addWidget(self.btn1)

        self.text_edit = QTextEdit()
        self.text_edit.setGeometry(10, 60, 280, 80)
        self.text_edit.setEnabled(False)

        self.layout.addWidget(self.text_edit)

        self.setLayout(self.layout)

   
