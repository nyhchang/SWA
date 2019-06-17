import os
import os.path
import sys
import time

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from qgis.core import *
from qgis.gui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mapTools import *
from osgeo import gdal
from qgis.analysis import QgsNativeAlgorithms
from PyQt5 import QtPrintSupport
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5 import QtTest

wkDir = os.path.dirname(os.path.realpath(__file__))
pluginDir = os.path.join(wkDir, "OSGeo4W64\\apps\\qgis\\python\\plugins")
sys.path.append('C:\\OSGeo4W64\\apps\\qgis\\python\\plugins')
import processing
from processing.core.Processing import Processing


from mainWindow import Ui_MainWindow
from WelcomeWindow import Ui_Dialog

from mapTools import *

class Welcome(QDialog, Ui_Dialog):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)



class SWAMain(QMainWindow, Ui_MainWindow):
    def __init__(self,):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.editing = False
        self.modified = False

        self.counter = 0

        self.currentEditingLayer = None


        self.mapCanvas = self.QgsMapCanvas
        self.mapCanvas.setCanvasColor(Qt.white)
        self.mapCanvas.setGeometry(QRect(140, 130, 521, 301))
        self.mapCanvas.show()

        self.setupMapLayers()
        self.setupMapTools(self.baseLayer)
        self.setPanMode()
        self.adjustActions()

        self.actionQuit.triggered.connect(self.quit)
        self.actionPan.triggered.connect(self.setPanMode)
        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionEdit.triggered.connect(self.setEditMode)
        self.actionAddFlowPath.triggered.connect(self.addFlowPath)
        self.actionEditFlowPath.triggered.connect(self.editFlowPath)
        self.actionDeleteFlowPath.triggered.connect(self.deleteFlowPath)
        self.actionLoad_File.triggered.connect(self.openShp)
        self.actionDeleteLayer.triggered.connect(self.deleteLayer)
        self.actionPrint.triggered.connect(self.printMap)
        self.view.currentLayerChanged.connect(self.selectNewLayer)


    def setupDatabase(self, name):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        db_name = os.path.join(cur_dir, "data", name+".sqlite")
        if not os.path.exists(db_name):
            fields = QgsFields()
            fields.append(QgsField("id", QVariant.Int))
            fields.append(QgsField("type", QVariant.String))
            fields.append(QgsField("name", QVariant.String))
            fields.append(QgsField("direction", QVariant.String))

            crs = QgsCoordinateReferenceSystem(2913,
                                               QgsCoordinateReferenceSystem.EpsgCrsId)

            writer = QgsVectorFileWriter(db_name, "utf-8", fields,
                                         QgsWkbTypes.MultiLineString,
                                         crs, "SQLite",
                                         ["SPATIALITE=YES"])
            if writer.hasError() != QgsVectorFileWriter.NoError:
                print("Database create error")

            del writer

    def setupMapLayers(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        list_dir = os.listdir(os.path.join(cur_dir, "data"))
        layers = []
        self.baseLayer = QgsRasterLayer(os.path.join(cur_dir, "data", "basemap", "basemap.xml"), "OSM")
        if not self.baseLayer.isValid():
            print("Layer failed to load")
        crs = QgsCoordinateReferenceSystem(2913)
        self.baseLayer.setCrs(crs)
        QgsProject.instance().addMapLayer(self.baseLayer)
        layers.append(self.baseLayer)
        rect = QgsRectangle(-13735521, 5547682, -13730558, 5551709)
        self.mapCanvas.setExtent(rect)

        self.mapCanvas.setLayers(layers)

        self.root = QgsProject.instance().layerTreeRoot()
        self.bridge = QgsLayerTreeMapCanvasBridge(self.root, self.mapCanvas)
        self.model = QgsLayerTreeModel(self.root)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.model.setFlag(QgsLayerTreeModel.ShowLegend)
        self.view = QgsLayerTreeView()
        self.view.setModel(self.model)
        self.LegendDock = QDockWidget("Layers", self)
        self.LegendDock.setObjectName("layers")
        self.LegendDock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.LegendDock.setWidget(self.view)
        self.LegendDock.setContentsMargins(0, 0, 0, 0)
        self.addDockWidget(Qt.RightDockWidgetArea, self.LegendDock)



    def setupRenderers(self, layer, counter):
        root_rule = QgsRuleBasedRenderer.Rule(None)
        width = .3
        line_colour  = "red"
        while counter > 4:
            counter = counter % 4
        if counter == 1:
            line_colour = "blue"
        if counter == 2:
            line_colour = "green"
        if counter == 3:
            line_colour = "orange"
        if counter == 4:
            line_colour = "purple"

        arrow_colour = "red"
        for FlowPath_direction in ("BOTH",
                                "FORWARD"):

            symbol = self.createFlowPathSymbol(width,
                                            line_colour,
                                            arrow_colour,
                                            FlowPath_direction)
            expression = "(direction='%s')" % FlowPath_direction

            rule = QgsRuleBasedRenderer.Rule(symbol,
                                               filterExp=expression)
            root_rule.appendChild(rule)
        symbol = QgsLineSymbol.createSimple({'line_style': 'dash', 'color': 'red'})
        rule = QgsRuleBasedRenderer.Rule(symbol, elseRule=True)
        root_rule.appendChild(rule)
        self.counter = counter + 1

        renderer = QgsRuleBasedRenderer(root_rule)
        layer.setRenderer(renderer)




    def createFlowPathSymbol(self, width, line_colour, arrow_colour,
                          direction):
        symbol = QgsLineSymbol.createSimple({})
        symbol.deleteSymbolLayer(0)

        symbol_layer = QgsSimpleLineSymbolLayer()
        symbol_layer.setWidth(width)
        symbol_layer.setColor(QColor(line_colour))
        symbol.appendSymbolLayer(symbol_layer)
        registry = QgsSymbolLayerRegistry()
        marker_line_metadata = registry.symbolLayerMetadata("MarkerLine")
        marker_metadata      = registry.symbolLayerMetadata("SimpleMarker")

        symbol_layer = marker_line_metadata.createSymbolLayer({
                        "width"     : "0.26",
                        "color"     : arrow_colour,
                        "rotate"    : "1",
                        "placement" : "interval",
                        "interval"  : "20",
                        "offset"    : "0"})
        sub_symbol = symbol_layer.subSymbol()
        sub_symbol.deleteSymbolLayer(0)

        triangle = marker_metadata.createSymbolLayer({
                        "name"          : "filled_arrowhead",
                        "color"         : arrow_colour,
                        "color_border"  : arrow_colour,
                        "offset"        : "0.0",
                        "size"          : "2",
                        "outline_width" : "0.5",
                        "output_unit"   : "mapunit",
                        "angle"         : "0"})
        sub_symbol.appendSymbolLayer(triangle)
        symbol.appendSymbolLayer(symbol_layer)
        return symbol


    def onFlowPathAdded(self):
        self.modified = True
        self.mapCanvas.refresh()
        self.actionAddFlowPath.setChecked(False)
        self.setPanMode()

    def onFlowPathEdited(self):
        self.modified = True
        self.mapCanvas.refresh()

    def onFlowPathDeleted(self):
        self.modified = True
        self.mapCanvas.refresh()
        self.actionDeleteFlowPath.setChecked(False)
        self.setPanMode()

    def closeEvent(self, event):
        self.quit(event)

    def setupMapTools(self, layer):
        self.panTool = PanTool(self.mapCanvas)
        self.panTool.setAction(self.actionPan)
        self.addFlowPathTool = AddFlowPathTool(self.mapCanvas,
                                         layer,
                                         self.onFlowPathAdded)
        self.addFlowPathTool.setAction(self.actionAddFlowPath)

        self.editFlowPathTool = EditFlowPathTool(self.mapCanvas,
                                           layer,
                                           self.onFlowPathEdited)
        self.editFlowPathTool.setAction(self.actionEditFlowPath)

        self.deleteFlowPathTool = DeleteFlowPathTool(self.mapCanvas,
                                               layer,
                                               self.onFlowPathDeleted)
        self.deleteFlowPathTool.setAction(self.actionDeleteFlowPath)


    def zoomIn(self):
        self.mapCanvas.zoomIn()

    def zoomOut(self):
        self.mapCanvas.zoomOut()

    def quit(self, event):
        if self.editing and self.modified:
            event.ignore()
            reply = QMessageBox.question(self, "Unsaved Work",
                                         "Please click edit mode again to save changes",
                                         QMessageBox.Ok)
        else:
            qApp.quit()


    def setPanMode(self):
        self.mapCanvas.setMapTool(self.panTool)

    def adjustActions(self):
        if self.editing:
            self.actionAddFlowPath.setEnabled(True)
            self.actionEditFlowPath.setEnabled(True)
            self.actionDeleteFlowPath.setEnabled(True)
        else:
            self.actionAddFlowPath.setEnabled(False)
            self.actionEditFlowPath.setEnabled(False)
            self.actionDeleteFlowPath.setEnabled(False)
        if self.view.currentLayer() is not None:
            if self.view.currentLayer().type() == 0:
                if self.view.currentLayer().name()[-4:] != "base":
                    self.actionEdit.setEnabled(True)
                else:
                    self.actionEdit.setEnabled(False)
            else:
                self.actionEdit.setEnabled(False)
        else:
            self.actionEdit.setEnabled(False)

    def addFlowPath(self):
        if self.actionAddFlowPath.isChecked():
            self.mapCanvas.setMapTool(self.addFlowPathTool)
        else:
            self.setPanMode()
        self.adjustActions()

    def editFlowPath(self):
        if self.actionEditFlowPath.isChecked():
            self.mapCanvas.setMapTool(self.editFlowPathTool)
        else:
            self.setPanMode()

    def deleteFlowPath(self):
        if self.actionDeleteFlowPath.isChecked():
            self.mapCanvas.setMapTool(self.deleteFlowPathTool)
        else:
            self.setPanMode()

    def setEditMode(self):
        layer = self.view.currentLayer()
        if layer is None:
            self.errorHandlePopup("No file open", "Please open a shapefile to begin")
        else:
            if self.currentEditingLayer is None:
                if self.editing:
                    if self.modified:
                        reply = QMessageBox.question(self, "Confirm", "Save Changes?", QMessageBox.Yes | QMessageBox.No,
                                                     QMessageBox.Yes)
                        if reply == QMessageBox.Yes:
                            layer.commitChanges()
                        else:
                            layer.rollBack()
                    else:
                        layer.commitChanges()
                    layer.triggerRepaint()
                    self.editing = False
                    self.currentEditingLayer = layer
                    self.setPanMode()
                else:
                    layer.startEditing()
                    layer.triggerRepaint()
                    self.editing = True
                    self.modified = False
            else:
                if self.editing:
                    if self.modified:
                        reply = QMessageBox.question(self, "Confirm", "Save Changes?", QMessageBox.Yes | QMessageBox.No,
                                                     QMessageBox.Yes)
                        if reply == QMessageBox.Yes:
                            self.currentEditingLayer.commitChanges()
                            self.currentEditingLayer = layer
                        else:
                            self.currentEditingLayer.rollBack()
                    else:
                        self.currentEditingLayer.commitChanges()
                    self.currentEditingLayer.triggerRepaint()
                    self.editing = False
                    self.setPanMode()
                else:
                    layer.startEditing()
                    layer.triggerRepaint()
                    self.editing = True
                    self.modified = False

        self.adjustActions()

    def getInfo(self):
        pass

    def openShp(self):
        found = False
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        list_dir = os.listdir(os.path.join(cur_dir, "data"))
        shpFileName = QFileDialog.getOpenFileName(None, "Select File")
        if shpFileName[0] != "":
            try:
                currentLayers = self.mapCanvas.layers()
                url = QUrl.fromLocalFile(shpFileName[0])
                filenameunsplit = url.fileName()
                filesplit = filenameunsplit.split(".")
                parameter = {'INPUT': shpFileName[0], 'TARGET_CRS': 'EPSG:3857', 'OUTPUT': 'memory:Reprojected'}
                reproject = processing.run('qgis:reprojectlayer', parameter)
                self.newLayer = reproject['OUTPUT']
                if self.newLayer.isValid():
                    QgsProject.instance().addMapLayer(self.newLayer)
                    for layer in QgsProject.instance().mapLayers().values():
                        basename = os.path.splitext(os.path.basename(layer.source()))[0]
                    currentLayers.insert(0, self.newLayer)
                    self.mapCanvas.setLayers(currentLayers)
                    self.mapCanvas.setExtent(self.newLayer.extent())
                    self.mapCanvas.refresh()
                    for layer in QgsProject.instance().mapLayers().values():
                        if layer.name() == "Reprojected":
                            layer.setName(filesplit[0] + " base")
                    for f in list_dir:
                        front = os.path.splitext(f)
                        if front[0] == filesplit[0]:
                            found = True
                            uri = QgsDataSourceUri()
                            uri.setDatabase(os.path.join(cur_dir, "data", f))
                            uri.setDataSource("", front[0], "GEOMETRY")
                            self.drawLayer = QgsVectorLayer(uri.uri(), front[0], "spatialite")
                            QgsProject.instance().addMapLayer(self.drawLayer)
                            self.setupRenderers(self.drawLayer, self.counter)
                            currentLayers.append(self.drawLayer)
                    if found == False:
                        self.setupDatabase(filesplit[0])
                        uri = QgsDataSourceUri()
                        uri.setDatabase(os.path.join(cur_dir, "data", filesplit[0] + ".sqlite"))
                        uri.setDataSource("", filesplit[0], "GEOMETRY")
                        self.newlayer1 = QgsVectorLayer(uri.uri(), filesplit[0], "spatialite")
                        QgsProject.instance().addMapLayer(self.newlayer1)
                        self.setupRenderers(self.newlayer1, self.counter)
                        currentLayers.append(self.newlayer1)

            except:
                self.errorHandlePopup("Unable to open file.")

    def selectNewLayer(self):
        if self.editing:
            self.setEditMode()
        self.currentEditingLayer = self.view.currentLayer()
        self.setupMapTools(self.view.currentLayer())
        self.adjustActions()

    def deleteLayer(self):
        deleteConfirmation = QMessageBox.question(self, "Delete",
                                   "Are you sure you want to delete this layer? This will permanently delete all data and files associated with this layer.",
                                   QMessageBox.Yes, QMessageBox.No)
        if deleteConfirmation == QMessageBox.Yes:
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            os.chdir(cur_dir)
            layerToRemove = self.view.currentLayer()
            layerName = layerToRemove.name() + ".sqlite"
            QgsProject.instance().removeMapLayer(layerToRemove)
            if os.path.isfile(layerName):
                try:
                    os.remove(layerName)
                    self.mapCanvas.refresh()
                except (PermissionError, FileNotFoundError):
                    pass

    def errorHandlePopup(self, message, secMessage = ""):
        errHand = QMessageBox()
        errHand.setIcon(QMessageBox.Critical)
        errHand.setText(message)
        if secMessage != "":
            errHand.setInformativeText(secMessage)
        errHand.setWindowTitle("Error")
        errHand.setStandardButtons(QMessageBox.Cancel)
        errHand.exec_()

    def printMap(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):
        self.mapCanvas.render(QPainter(printer))


def handler(msg_type, msg_log_context, msg_string):
    pass



def main():

    QtCore.qInstallMessageHandler(handler)
    QgsApplication.setPrefixPath("C:\\OSGeo4W64\\apps\\qgis", True)
    app = QgsApplication([], False)
    app.initQgis()

    Processing.initialize()
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    firstWindow = Welcome()
    firstWindow.show()
    QtTest.QTest.qWait(5000)
    firstWindow.close()

    secondWindow = SWAMain()
    secondWindow.show()

    app.exec_()
    app.deleteLater()
    QgsApplication.exitQgis()


if __name__ == '__main__':
    main()
