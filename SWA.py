import os
import os.path
import sys

from qgis.core import *
from qgis.gui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mapTools import *
from osgeo import gdal


from mainWindow import Ui_MainWindow
from WelcomeWindow import Ui_Dialog

from mapTools import *

class Welcome(QMainWindow, Ui_Dialog):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.loaded[str].connect(self.onLoadFile)

    def onLoadFile(self, path):
        self.hide()
        self.newWindow = SWAMain(path)
        self.newWindow.show()
        self.newWindow.raise_()
        self.newWindow.setupDatabase()
        self.newWindow.setupMapLayers()
        self.newWindow.setupRenderers()
        self.newWindow.setupMapTools()
        self.newWindow.setPanMode()
        self.newWindow.adjustActions()

class SWAMain(QMainWindow, Ui_MainWindow):
    def __init__(self, path):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.actionQuit.triggered.connect(self.quit)
        self.actionPan.triggered.connect(self.setPanMode)
        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionEdit.triggered.connect(self.setEditMode)
        self.actionAddFlowPath.triggered.connect(self.addFlowPath)
        self.actionEditFlowPath.triggered.connect(self.editFlowPath)
        self.actionDeleteFlowPath.triggered.connect(self.deleteFlowPath)
        self.actionLoad_File.triggered.connect(self.openShp)

        self.mapCanvas = self.QgsMapCanvas
        self.mapCanvas.setCanvasColor(Qt.white)
        self.mapCanvas.setGeometry(QRect(140, 130, 521, 301))
        self.mapCanvas.show()

        self.editing = False
        self.modified = False

    def setupDatabase(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        db_name = os.path.join(cur_dir, "data", "FlowPaths.sqlite")
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
        self.baseLayer = QgsRasterLayer(os.path.join(cur_dir, "data", "basemap", "basemap.xml"), "OSM")
        layers = []
        if not self.baseLayer.isValid():
            print("Layer failed to load")
        crs = QgsCoordinateReferenceSystem(2913)
        self.baseLayer.setCrs(crs)
        QgsProject.instance().addMapLayer(self.baseLayer)
        layers.append(self.baseLayer)
        rect = QgsRectangle(-13735521, 5547682, -13730558, 5551709)
        self.mapCanvas.setExtent(rect)

        uri = QgsDataSourceUri()
        uri.setDatabase(os.path.join(cur_dir, "data", "FlowPaths.sqlite"))
        uri.setDataSource("", "FlowPaths", "GEOMETRY")

        self.FlowPathLayer = QgsVectorLayer(uri.uri(), "FlowPaths", "spatialite")
        QgsProject.instance().addMapLayer(self.FlowPathLayer)

        layers.insert(0, self.FlowPathLayer)
        QgsProject.instance().setCrs(crs)
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


    def setupRenderers(self):
        # Setup the renderer for our FlowPath layer.

        root_rule = QgsRuleBasedRenderer.Rule(None)
        width = .3
        line_colour  = "red"
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

        renderer = QgsRuleBasedRenderer(root_rule)
        self.FlowPathLayer.setRenderer(renderer)




    def createFlowPathSymbol(self, width, line_colour, arrow_colour,
                          direction):
        symbol = QgsLineSymbol.createSimple({})
        symbol.deleteSymbolLayer(0) # Remove default symbol layer.

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
        self.quit()

    def setupMapTools(self):
        self.panTool = PanTool(self.mapCanvas)
        self.panTool.setAction(self.actionPan)
        self.addFlowPathTool = AddFlowPathTool(self.mapCanvas,
                                         self.FlowPathLayer,
                                         self.onFlowPathAdded)
        self.addFlowPathTool.setAction(self.actionAddFlowPath)

        self.editFlowPathTool = EditFlowPathTool(self.mapCanvas,
                                           self.FlowPathLayer,
                                           self.onFlowPathEdited)
        self.editFlowPathTool.setAction(self.actionEditFlowPath)

        self.deleteFlowPathTool = DeleteFlowPathTool(self.mapCanvas,
                                               self.FlowPathLayer,
                                               self.onFlowPathDeleted)
        self.deleteFlowPathTool.setAction(self.actionDeleteFlowPath)


    def zoomIn(self):
        self.mapCanvas.zoomIn()

    def zoomOut(self):
        self.mapCanvas.zoomOut()

    def quit(self):
        if self.editing and self.modified:
            reply = QMessageBox.question(self, "Confirm",
                                         "Save Changes?",
                                         QMessageBox.Yes | QMessageBox.No
                                         | QMessageBox.Cancel,
                                         QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.FlowPathLayer.commitChanges()
            elif reply == QMessageBox.No:
                self.FlowPathLayer.rollBack()

            if reply != QMessageBox.Cancel:
                qApp.quit()
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
        if self.editing:
            if self.modified:
                reply = QMessageBox.question(self, "Confirm", "Save Changes?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.FlowPathLayer.commitChanges()
                else:
                    self.FlowPathLayer.rollBack()
            else:
                self.FlowPathLayer.commitChanges()
            self.FlowPathLayer.triggerRepaint()
            self.editing = False
            self.setPanMode()
        else:
            self.FlowPathLayer.startEditing()
            self.FlowPathLayer.triggerRepaint()
            self.editing = True
            self.modified = False

        self.adjustActions()

    def getInfo(self):
        pass

    def openShp(self):
        shpFileName = QFileDialog.getOpenFileName(None, "Select File")
        if shpFileName[0] != "":
            url = QUrl.fromLocalFile(shpFileName[0])
            filenameunsplit = url.fileName()
            filesplit = filenameunsplit.split(".")
            self.newLayer = QgsVectorLayer(shpFileName[0], filesplit[0], "ogr")
            QgsProject.instance().addMapLayer(self.newLayer)
            currentLayers = self.mapCanvas.layers()
            currentLayers.insert(0, self.newLayer)
            self.mapCanvas.setLayers(currentLayers)
            self.mapCanvas.setExtent(self.newLayer.extent())
            self.mapCanvas.refresh()


def main():
    QgsApplication.setPrefixPath("C:\\OSGeo4W64\\apps\\qgis", True)
    app = QgsApplication([], False)
    app.initQgis()

    firstWindow = Welcome()
    firstWindow.show()

    app.exec_()
    app.deleteLater()
    QgsApplication.exitQgis()


if __name__ == '__main__':
    main()
