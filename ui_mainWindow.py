from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Ui_MainWindow(object):
    def setupUi(self, window):
        window.setWindowTitle("Stormwater")

        self.centralWidget = QWidget(window)
        self.centralWidget.setMinimumSize(800, 400)
        window.setCentralWidget(self.centralWidget)

        self.menubar = window.menuBar()
        self.fileMenu = self.menubar.addMenu("File")
        self.mapMenu = self.menubar.addMenu("Map")
        self.editMenu = self.menubar.addMenu("Edit")
        self.toolsMenu = self.menubar.addMenu("Tools")

        self.toolbar = QToolBar(window)
        window.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.actionQuit = QAction("Quit", window)
        self.actionQuit.setShortcut(QKeySequence.Quit)

        self.actionZoomIn = QAction("Zoom In", window)
        self.actionZoomIn.setShortcut(QKeySequence.ZoomIn)

        self.actionZoomOut = QAction("Zoom Out", window)
        self.actionZoomOut.setShortcut(QKeySequence.ZoomOut)

        self.actionPan = QAction("Pan", window)
        self.actionPan.setShortcut("Ctrl+1")
        self.actionPan.setCheckable(True)

        self.actionEdit = QAction("Edit", window)
        self.actionEdit.setShortcut("Ctrl+2")
        self.actionEdit.setCheckable(True)

        self.actionAddTrack = QAction("Add Track", window)
        self.actionAddTrack.setShortcut("Ctrl+A")
        self.actionAddTrack.setCheckable(True)

        self.actionEditTrack = QAction("Edit Track", window)
        self.actionEditTrack.setShortcut("Ctrl+E")
        self.actionEditTrack.setCheckable(True)

        self.actionDeleteTrack = QAction("Delete Track", window)
        self.actionDeleteTrack.setShortcut("Ctrl+D")
        self.actionDeleteTrack.setCheckable(True)

        self.fileMenu.addAction(self.actionQuit)

        self.mapMenu.addAction(self.actionZoomIn)
        self.mapMenu.addAction(self.actionZoomOut)
        self.mapMenu.addAction(self.actionPan)
        self.mapMenu.addAction(self.actionQuit)

        self.toolbar.addAction(self.actionZoomIn)
        self.toolbar.addAction(self.actionZoomOut)
        self.toolbar.addAction(self.actionPan)
        self.toolbar.addAction(self.actionEdit)
        self.toolbar.addAction(self.actionAddTrack)
        self.toolbar.addAction(self.actionEditTrack)
        self.toolbar.addAction(self.actionDeleteTrack)

        self.toolbar.addAction(self.actionQuit)


        window.resize(window.sizeHint())