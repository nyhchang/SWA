import os
import os.path
import sys

from qgis.core import *
from qgis.gui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui_mainWindow import Ui_MainWindow

from constants import *
from mapTools import *


class ForestTrailsWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setupUi(self)

        self.mapCanvas = QgsMapCanvas()
        self.mapCanvas.setCanvasColor(Qt.white)
        self.mapCanvas.show()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.mapCanvas)
        self.centralWidget.setLayout(layout)

    def setupMapLayers(self):
        layers = []
        filename = "C:\\Users\\Nathan\\Desktop\\forestTrails\\data\\basemap4.tif"
        self.baseLayer = QgsRasterLayer(filename, "Some Layer")
        if not self.baseLayer.isValid():
            print ("Layer failed to load")

        QgsProject.instance().addMapLayer(self.baseLayer)
        layers.append(self.baseLayer)
        self.mapCanvas.setExtent(self.baseLayer.extent())

        self.stmFlowLayer = QgsVectorLayer("C:\\Test\\StmFlow.shp", "Storm Flow", "ogr")
        if not self.stmFlowLayer.isValid():
            print ("shp Layer failed to load")

        print(self.stmFlowLayer.extent())
        print(self.baseLayer.extent())
        QgsProject.instance().addMapLayer(self.stmFlowLayer)
        layers.insert(0, self.stmFlowLayer)

        self.mapCanvas.setLayers(layers)



    def zoomIn(self):
        self.mapCanvas.zoomIn()

    def zoomOut(self):
        self.mapCanvas.zoomOut()

    def quit(self):
        pass


    def setPanMode(self):
        pass


    def setEditMode(self):
        pass


    def addTrack(self):
        pass


    def editTrack(self):
        pass


    def deleteTrack(self):
        pass


    def getInfo(self):
        pass


    def setStartPoint(self):
        pass


    def setEndPoint(self):
        pass


    def findShortestPath(self):
        pass


def main():

    QgsApplication.setPrefixPath("C:\\OSGeo4W64\\apps\\qgis", True)
    app = QgsApplication([], False)
    app.initQgis()

    window = ForestTrailsWindow()
    window.show()
    window.raise_()
    window.setupMapLayers()

    app.exec_()
    app.deleteLater()
    window.close()
    QgsApplication.exitQgis()



if __name__ == '__main__':
    main()
