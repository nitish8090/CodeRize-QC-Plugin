import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from qgis.core import QgsDataSourceUri, QgsVectorLayer, QgsProject
from qgis.utils import iface

from ..PGDatabase import Database, AllocatedAOITable

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
        self.btn_load_aoi.clicked.connect(self.load_aoi)

        self.update_vendor_list()

    def update_vendor_list(self):
        print("[DEBUG] updating vendor list")

        allocated_aoi = AllocatedAOITable()
        vendor_list = allocated_aoi.get_all_vendors()
        vendor_list.append('All')
        self.cbox_vendor_list.addItems(vendor_list)

    def load_aoi(self):
        print("Loading AOI as Layer")

        allocated_aoi_layer = AllocatedAOITable.get_qgis_layer(vendor_name=self.cbox_vendor_list.currentText())
        if not allocated_aoi_layer.isValid():
            print("Layer %s did not load" % allocated_aoi_layer.name())

        QgsProject.instance().addMapLayers([allocated_aoi_layer])
