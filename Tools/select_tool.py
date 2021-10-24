from qgis.gui import QgsMapTool, QgsMapToolIdentifyFeature
from qgis.core import QgsProject
from qgis.utils import iface

from ..Layers import AllocatedAOILayer


class SelectorTool(QgsMapToolIdentifyFeature):
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.featureId = None

    def canvasPressEvent(self, event):
        pass

    def canvasMoveEvent(self, event):
        # x = event.pos().x()
        # y = event.pos().y()
        #
        # point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        pass

    def canvasReleaseEvent(self, event):
        # Get the click
        x = event.pos().x()
        y = event.pos().y()

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        print(point)

        layers = QgsProject.instance().mapLayersByName(AllocatedAOILayer.name)
        if len(layers) == 0:
            print(f"No {AllocatedAOILayer.name} found.")
        elif len(layers) > 1:
            print(f"More than 1 {AllocatedAOILayer.name} found.")
        else:
            layer = layers[0]
            layer.removeSelection()

            identified_features = self.identify(event.x(), event.y(), [layer])
            if len(identified_features) == 0:
                print("No features identified")
            else:
                identified_feature = identified_features[0].mFeature
                if not identified_feature.id() == self.featureId:
                    self.featureId = identified_feature.id()
                    layer.select(self.featureId)

                    self.zoom_to_a_feature(identified_feature)

    def activate(self):
        pass

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True

    def zoom_to_a_feature(self, feature):
        bbox = feature.geometry().buffer(20, 1).boundingBox()
        iface.mapCanvas().setExtent(bbox)
        iface.mapCanvas().refresh()
