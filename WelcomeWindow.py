import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class Ui_Dialog(object):
    loaded = QtCore.pyqtSignal(str)
    fileName = None
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setAutoFillBackground(False)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 200, 141, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(80, 100, 241, 71))
        self.textEdit.setObjectName("textEdit")
        self.philomathpic = QtWidgets.QLabel(Dialog)
        self.philomathpic.setGeometry(QtCore.QRect(70, 20, 251, 61))
        self.philomathpic.setText("")
        self.philomathpic.setPixmap(QtGui.QPixmap("../Capstone Project/logo-fs8.png"))
        self.philomathpic.setScaledContents(True)
        self.philomathpic.setObjectName("philomathpic")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton_2.clicked.connect(self.loadFile)

    def loadFile(self):
        self.fileName = QtWidgets.QFileDialog.getOpenFileName(None, "Select File")
        if self.fileName != None:
            self.loaded.emit(self.fileName[0])

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "StormWater Application"))
        self.pushButton_2.setText(_translate("Dialog", "Load File"))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Welcome to the Stormwater Application</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))







if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


