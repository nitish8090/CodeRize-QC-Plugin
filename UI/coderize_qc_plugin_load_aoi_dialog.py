import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from qgis.core import QgsDataSourceUri, QgsVectorLayer, QgsProject
from qgis.utils import iface

from ..PGDatabase import Database, AllocatedAOITable
from ..Layers import AllocatedAOILayer, AILayer, FootprintLayer


from coderize_qc_plugin.PGDatabase import AllocatedAOITable

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'coderize_qc_plugin_load_aoi_dialog.ui'))


class CRFeatureApproverDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(CRFeatureApproverDialog, self).__init__(parent)
        self.setupUi(self)

        # self.cbox_vendor_list
        self.btn_load_aoi.clicked.connect(self.load_layers)

        self.update_vendor_list()

    def update_vendor_list(self):
        print("[DEBUG] Updating vendor list")

        allocated_aoi = AllocatedAOITable()
        vendor_list = allocated_aoi.get_all_vendors()
        vendor_list.append('All')
        self.cbox_vendor_list.addItems(vendor_list)

    def load_layers(self):
        print("[DEBUG] Loading Allocated AOI as Layer")
        allocated_aoi_layer = AllocatedAOILayer.get_from_postgres(vendor_name=self.cbox_vendor_list.currentText())
        allocated_aoi_layer.apply_symbology()
        allocated_aoi_layer.add_to_qgis()

        print("[DEBUG] Getting Boundary of Allocated AOI")
        boundary = f"SRID={allocated_aoi_layer.get_srid()};{allocated_aoi_layer.get_outer_boundary()}"

        print("[DEBUG] Loading AI as Layer")
        ai_layer = AILayer.get_from_postgres(intersecting_geometry=boundary)
        ai_layer.add_to_qgis()

        print("[DEBUG] Loading Footprint as Layer")
        footprint_layer = FootprintLayer.get_from_postgres(intersecting_geometry=boundary)
        footprint_layer.add_to_qgis()
