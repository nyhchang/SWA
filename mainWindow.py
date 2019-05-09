# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.actionPan = QAction(MainWindow)
        self.actionPan.setShortcut("Ctrl+1")
        self.actionPan.setCheckable(True)

        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setShortcut(QKeySequence.Quit)

        self.actionZoomIn = QAction(MainWindow)
        self.actionZoomIn.setShortcut(QKeySequence.ZoomIn)

        self.actionZoomOut = QAction(MainWindow)
        self.actionZoomOut.setShortcut(QKeySequence.ZoomOut)

        self.actionEdit = QAction(MainWindow)
        self.actionEdit.setShortcut("Ctrl+2")
        self.actionEdit.setCheckable(True)

        self.actionAddTrack = QAction(MainWindow)
        self.actionAddTrack.setShortcut("Ctrl+A")
        self.actionAddTrack.setCheckable(True)

        self.actionEditTrack = QAction(MainWindow)
        self.actionEditTrack.setShortcut("Ctrl+E")
        self.actionEditTrack.setCheckable(True)

        self.actionDeleteTrack = QAction(MainWindow)
        self.actionDeleteTrack.setShortcut("Ctrl+D")
        self.actionDeleteTrack.setCheckable(True)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.QgsMapCanvas = QgsMapCanvas(self.centralwidget)
        self.QgsMapCanvas.setGeometry(QRect(140, 130, 521, 301))
        self.QgsMapCanvas.setObjectName("QgsMapCanvas")
        self.DitchCheck = QRadioButton(self.centralwidget)
        self.DitchCheck.setGeometry(QRect(690, 460, 77, 18))
        self.DitchCheck.setObjectName("DitchCheck")
        self.PipeCheck = QRadioButton(self.centralwidget)
        self.PipeCheck.setGeometry(QRect(690, 420, 77, 18))
        self.PipeCheck.setObjectName("PipeCheck")
        self.StreetCheck = QRadioButton(self.centralwidget)
        self.StreetCheck.setGeometry(QRect(690, 440, 77, 18))
        self.StreetCheck.setObjectName("StreetCheck")
        self.Export = QPushButton(self.centralwidget)
        self.Export.setGeometry(QRect(320, 500, 141, 31))
        self.Export.setObjectName("Export")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(260, 20, 291, 61))
        self.label.setText("")
        self.label.setPixmap(QPixmap("resources/logo-fs8.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QRect(270, 90, 271, 31))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(30, 140, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QRect(30, 210, 81, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QRect(30, 280, 81, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QRect(30, 350, 81, 23))
        self.pushButton_4.setObjectName("pushButton_4")

        self.toolButton = QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QRect(150, 450, 31, 31))
        self.toolButton.setText("Zoom in")
        self.toolButton.setDefaultAction(self.actionZoomIn)
        icon = QIcon()
        icon.addPixmap(QPixmap("resources/mActionZoomIn.png"))
        self.toolButton.setIcon(icon)
        self.toolButton.setObjectName("toolButton")

        self.toolButton_2 = QToolButton(self.centralwidget)
        self.toolButton_2.setGeometry(QRect(190, 450, 31, 31))
        self.toolButton_2.setText("Zoom out")
        self.toolButton_2.setDefaultAction(self.actionZoomOut)
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("resources/mActionZoomOut.png"), QIcon.Normal, QIcon.Off)
        self.toolButton_2.setIcon(icon1)
        self.toolButton_2.setObjectName("toolButton_2")

        self.toolButton_3 = QToolButton(self.centralwidget)
        self.toolButton_3.setGeometry(QRect(230, 450, 31, 31))
        self.toolButton_3.setText("Edit")
        self.toolButton_3.setDefaultAction(self.actionEdit)
        icon2 = QIcon()
        icon2.addPixmap(QPixmap("resources/mActionEdit.png"), QIcon.Normal, QIcon.Off)
        self.toolButton_3.setIcon(icon2)
        self.toolButton_3.setObjectName("toolButton_2")

        self.toolButton_4 = QToolButton(self.centralwidget)
        self.toolButton_4.setGeometry(QRect(270, 450, 31, 31))
        self.toolButton_4.setText("Pan")
        self.toolButton_4.setDefaultAction(self.actionPan)
        icon3 = QIcon()
        icon3.addPixmap(QPixmap("resources/mActionPan.png"), QIcon.Normal, QIcon.Off)
        self.toolButton_4.setIcon(icon3)
        self.toolButton_4.setObjectName("toolButton_4")

        self.toolButton_5 = QToolButton(self.centralwidget)
        self.toolButton_5.setGeometry(QRect(310, 450, 31, 31))
        self.toolButton_5.setText("Add Track")
        self.toolButton_5.setDefaultAction(self.actionAddTrack)
        icon4 = QIcon()
        icon4.addPixmap(QPixmap("resources/mActionAddTrack.png"), QIcon.Normal, QIcon.Off)
        self.toolButton_5.setIcon(icon4)
        self.toolButton_5.setObjectName("toolButton_5")

        self.toolButton_6 = QToolButton(self.centralwidget)
        self.toolButton_6.setGeometry(QRect(350, 450, 31, 31))
        self.toolButton_6.setText("edit Track")
        self.toolButton_6.setDefaultAction(self.actionEditTrack)
        icon5 = QIcon()
        icon5.addPixmap(QPixmap("resources/mActionEditTrack.png"), QIcon.Normal, QIcon.Off)
        self.toolButton_6.setIcon(icon5)
        self.toolButton_6.setObjectName("toolButton_6")

        self.toolButton_7 = QToolButton(self.centralwidget)
        self.toolButton_7.setGeometry(QRect(390, 450, 31, 31))
        self.toolButton_7.setText("Delete Track")
        self.toolButton_7.setDefaultAction(self.actionDeleteTrack)
        icon8 = QIcon()
        icon8.addPixmap(QPixmap("resources/mActionDeleteTrack.png"), QIcon.Normal, QIcon.Off)
        self.toolButton_7.setIcon(icon8)
        self.toolButton_7.setObjectName("toolButton_6")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_File = QAction(MainWindow)
        self.actionLoad_File.setObjectName("actionLoad_File")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionPrint = QAction(MainWindow)
        self.actionPrint.setObjectName("actionPrint")
        self.menuFile.addAction(self.actionLoad_File)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionPrint)
        self.menubar.addAction(self.menuFile.menuAction())
        self.mapMenu = self.menubar.addMenu("Map")
        self.editMenu = self.menubar.addMenu("Edit")
        self.toolsMenu = self.menubar.addMenu("Tools")

        self.menuFile.addAction(self.actionQuit)
        self.mapMenu.addAction(self.actionZoomIn)
        self.mapMenu.addAction(self.actionZoomOut)
        self.mapMenu.addAction(self.actionPan)
        self.mapMenu.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.DitchCheck.setText(_translate("MainWindow", "Ditch"))
        self.PipeCheck.setText(_translate("MainWindow", "Pipe"))
        self.StreetCheck.setText(_translate("MainWindow", "Street"))
        self.Export.setText(_translate("MainWindow", "Export"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Project Window</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Edit Ditch"))
        self.pushButton_2.setText(_translate("MainWindow", "Edit Pipe"))
        self.pushButton_3.setText(_translate("MainWindow", "Flow Direction"))
        self.pushButton_4.setText(_translate("MainWindow", "LIDAR"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionLoad_File.setText(_translate("MainWindow", "Load New File"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionPrint.setText(_translate("MainWindow", "Print"))


from qgis.gui import QgsMapCanvas