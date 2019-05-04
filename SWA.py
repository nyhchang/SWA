import os
import os.path
import sys

from qgis.core import *
from qgis.gui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mapTools import *



from mainWindow import Ui_MainWindow

from mapTools import *
from constants import *


class SWAMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setupUi(self)

        self.actionQuit.triggered.connect(self.quit)
        self.actionPan.triggered.connect(self.setPanMode)
        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionEdit.triggered.connect(self.setEditMode)
        self.actionAddTrack.triggered.connect(self.addTrack)
        self.actionEditTrack.triggered.connect(self.editTrack)
        self.actionDeleteTrack.triggered.connect(self.deleteTrack)

        self.mapCanvas = self.QgsMapCanvas
        self.mapCanvas.setCanvasColor(Qt.white)
        self.mapCanvas.setGeometry(QRect(140, 130, 521, 301))
        self.mapCanvas.show()

        self.editing = False
        self.modified = False
        # layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        # layout.addWidget(self.mapCanvas)
        # self.centralwidget.setLayout(layout)

    def setupDatabase(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        db_name = os.path.join(cur_dir, "data", "tracks.sqlite")
        if not os.path.exists(db_name):
            fields = QgsFields()
            fields.append(QgsField("id", QVariant.Int))
            fields.append(QgsField("type", QVariant.String))
            fields.append(QgsField("name", QVariant.String))
            fields.append(QgsField("direction", QVariant.String))
            fields.append(QgsField("status", QVariant.String))

            crs = QgsCoordinateReferenceSystem(2913,
                                               QgsCoordinateReferenceSystem.EpsgCrsId)

            writer = QgsVectorFileWriter(db_name, "utf-8", fields,
                                         QgsWkbTypes.MultiLineString,
                                         crs, "SQLite",
                                         ["SPATIALITE=YES"])
            if writer.hasError() != QgsVectorFileWriter.NoError:
                print("Error creating tracks database!")

            del writer

    def setupMapLayers(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        layers = []
        filename = os.path.join(cur_dir, "data", "basemap", "basemap4.tif");
        self.baseLayer = QgsRasterLayer(filename, "Some Layer")
        if not self.baseLayer.isValid():
            print("Layer failed to load")

        QgsProject.instance().addMapLayer(self.baseLayer)
        layers.append(self.baseLayer)
        self.mapCanvas.setExtent(self.baseLayer.extent())

        self.stmFlowLayer = QgsVectorLayer(os.path.join(cur_dir, "data", "StmFlow", "StmFlow.shp"), "Storm Flow", "ogr")
        if not self.stmFlowLayer.isValid():
            print("shp Layer failed to load")
        QgsProject.instance().addMapLayer(self.stmFlowLayer)

        uri = QgsDataSourceUri()
        uri.setDatabase(os.path.join(cur_dir, "data", "tracks.sqlite"))
        uri.setDataSource("", "tracks", "GEOMETRY")

        self.trackLayer = QgsVectorLayer(uri.uri(), "Tracks", "spatialite")
        QgsProject.instance().addMapLayer(self.trackLayer)

        layers.insert(0, self.stmFlowLayer)
        layers.insert(0, self.trackLayer)

        self.mapCanvas.setLayers(layers)


    def setupRenderers(self):
        # Setup the renderer for our track layer.

        root_rule = QgsRuleBasedRenderer.Rule(None)

        for track_type in (TRACK_TYPE_ROAD, TRACK_TYPE_WALKING,
                           TRACK_TYPE_BIKE, TRACK_TYPE_HORSE):
            if track_type == TRACK_TYPE_ROAD:
                width = ROAD_WIDTH
            else:
                width = TRAIL_WIDTH

            line_colour  = "red"
            arrow_colour = "red"

            for track_status in (TRACK_STATUS_OPEN, TRACK_STATUS_CLOSED):

                for track_direction in (TRACK_DIRECTION_BOTH,
                                        TRACK_DIRECTION_FORWARD,
                                        TRACK_DIRECTION_BACKWARD):

                    symbol = self.createTrackSymbol(width,
                                                    line_colour,
                                                    arrow_colour,
                                                    track_status,
                                                    track_direction)
                    expression = ("(type='%s') and " +
                                  "(status='%s') and " +
                                  "(direction='%s')") % (
                                  track_type, track_status, track_direction)

                    rule = QgsRuleBasedRenderer.Rule(symbol,
                                                       filterExp=expression)
                    root_rule.appendChild(rule)
        symbol = QgsLineSymbol.createSimple({'line_style': 'dash', 'color': 'red'})
        rule = QgsRuleBasedRenderer.Rule(symbol, elseRule=True)
        root_rule.appendChild(rule)

        renderer = QgsRuleBasedRenderer(root_rule)
        self.trackLayer.setRenderer(renderer)




    def createTrackSymbol(self, width, line_colour, arrow_colour,
                          status, direction):
        symbol = QgsLineSymbol.createSimple({})
        symbol.deleteSymbolLayer(0) # Remove default symbol layer.

        symbol_layer = QgsSimpleLineSymbolLayer()
        symbol_layer.setWidth(width)
        symbol_layer.setColor(QColor(line_colour))
        if status == TRACK_STATUS_CLOSED:
            symbol_layer.setPenStyle(Qt.DotLine)
        symbol.appendSymbolLayer(symbol_layer)

        if direction == TRACK_DIRECTION_FORWARD:
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
                            "size"          : "3",
                            "outline_width" : "0.5",
                            "output_unit"   : "mapunit",
                            "angle"         : "0"})
            sub_symbol.appendSymbolLayer(triangle)
            symbol.appendSymbolLayer(symbol_layer)
        elif direction == TRACK_DIRECTION_BACKWARD:
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
                            "size"          : "3",
                            "outline_width" : "0.5",
                            "output_unit"   : "mapunit",
                            "angle"         : "180"})
            sub_symbol.appendSymbolLayer(triangle)
            symbol.appendSymbolLayer(symbol_layer)

        return symbol


    def onTrackAdded(self):
        self.modified = True
        self.mapCanvas.refresh()
        self.actionAddTrack.setChecked(False)
        self.setPanMode()

    def onTrackEdited(self):
        self.modified = True
        self.mapCanvas.refresh()

    def onTrackDeleted(self):
        self.modified = True
        self.mapCanvas.refresh()
        self.actionDeleteTrack.setChecked(False)
        self.setPanMode()

    def closeEvent(self, event):
        self.quit()

    def setupMapTools(self):
        self.panTool = PanTool(self.mapCanvas)
        self.panTool.setAction(self.actionPan)
        self.addTrackTool = AddTrackTool(self.mapCanvas,
                                         self.trackLayer,
                                         self.onTrackAdded)
        self.addTrackTool.setAction(self.actionAddTrack)

        self.editTrackTool = EditTrackTool(self.mapCanvas,
                                           self.trackLayer,
                                           self.onTrackEdited)
        self.editTrackTool.setAction(self.actionEditTrack)

        self.deleteTrackTool = DeleteTrackTool(self.mapCanvas,
                                               self.trackLayer,
                                               self.onTrackDeleted)
        self.deleteTrackTool.setAction(self.actionDeleteTrack)


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
                self.trackLayer.commitChanges()
            elif reply == QMessageBox.No:
                self.trackLayer.rollBack()

            if reply != QMessageBox.Cancel:
                qApp.quit()
        else:
            qApp.quit()


    def setPanMode(self):
        self.mapCanvas.setMapTool(self.panTool)

    def adjustActions(self):
        if self.editing:
            self.actionAddTrack.setEnabled(True)
            self.actionEditTrack.setEnabled(True)
            self.actionDeleteTrack.setEnabled(True)
        else:
            self.actionAddTrack.setEnabled(False)
            self.actionEditTrack.setEnabled(False)
            self.actionDeleteTrack.setEnabled(False)

    def addTrack(self):
        if self.actionAddTrack.isChecked():
            self.mapCanvas.setMapTool(self.addTrackTool)
        else:
            self.setPanMode()
        self.adjustActions()

    def editTrack(self):
        if self.actionEditTrack.isChecked():
            self.mapCanvas.setMapTool(self.editTrackTool)
        else:
            self.setPanMode()

    def deleteTrack(self):
        if self.actionDeleteTrack.isChecked():
            self.mapCanvas.setMapTool(self.deleteTrackTool)
        else:
            self.setPanMode()

    def setEditMode(self):
        if self.editing:
            if self.modified:
                reply = QMessageBox.question(self, "Confirm", "Save Changes?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.trackLayer.commitChanges()
                else:
                    self.trackLayer.rollBack()
            else:
                self.trackLayer.commitChanges()
            self.trackLayer.triggerRepaint()
            self.editing = False
            self.setPanMode()
        else:
            self.trackLayer.startEditing()
            self.trackLayer.triggerRepaint()
            self.editing = True
            self.modified = False

        self.adjustActions()

    def getInfo(self):
        pass



def main():

    QgsApplication.setPrefixPath("C:\\OSGeo4W64\\apps\\qgis", True)
    app = QgsApplication([], False)
    app.initQgis()

    window = SWAMain()
    window.show()
    window.raise_()
    window.setupDatabase()
    window.setupMapLayers()
    window.setupRenderers()
    window.setupMapTools()
    window.setPanMode()
    window.adjustActions()

    app.exec_()
    app.deleteLater()
    window.close()
    QgsApplication.exitQgis()



if __name__ == '__main__':
    main()
