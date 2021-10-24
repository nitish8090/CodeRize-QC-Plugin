from ..PGDatabase import AllocatedAOITable, Database
from qgis.core import QgsDataSourceUri, QgsVectorLayer, QgsProject, QgsMarkerSymbol
from qgis.core import QgsCategorizedSymbolRenderer, QgsRendererCategory, QgsLineSymbol, QgsFillSymbol

import shapely.wkt
from shapely.ops import unary_union


class AllocatedAOILayer:
    name = 'Allocated AOI'

    def __init__(self):
        self.layer = None

    @classmethod
    def get_from_postgres(cls, vendor_name):
        uri = QgsDataSourceUri()
        uri.setConnection(
            Database.host,
            str(Database.port),
            Database.database_name,
            Database.user,
            Database.password
        )

        where_clause = "" if vendor_name is 'All' else f"{AllocatedAOITable.vendor_name_column} = '{vendor_name}'"

        uri.setDataSource(
            AllocatedAOITable.schema_name,
            AllocatedAOITable.name,
            AllocatedAOITable.geometry_column,
            where_clause
        )

        _instance = cls()
        _instance.layer = QgsVectorLayer(uri.uri(), cls.name, "postgres")
        return _instance

    def add_to_qgis(self):
        if not self.layer.isValid():
            print("Layer %s did not load" % self.layer.name())

        QgsProject.instance().addMapLayers([self.layer])

    def get_outer_boundary(self):
        """ Return geometry as WKT """
        a = []
        for feature in self.layer.getFeatures():
            p = shapely.wkt.loads(feature.geometry().asWkt())
            a.append(p)
        m = unary_union(a)
        print(m.wkt)
        return f"{m.wkt}"

    def get_srid(self):
        return self.layer.crs().srsid()

    def apply_symbology(self):

        qc_statuses = {'Pending': 'red', 'Approved': 'green', '': 'yellow'}

        categories = []
        for qc_status, color in qc_statuses.items():
            symbol = QgsFillSymbol.createSimple(
                {'color': '255,0,0,0', 'outline_color': color, 'outline_style': 'solid'})
            print(symbol.symbolLayers()[0].properties())
            categories.append(QgsRendererCategory(qc_status, symbol, qc_status))

        categorized_renderer = QgsCategorizedSymbolRenderer('qc_status', categories)

        self.layer.setRenderer(categorized_renderer)
        self.layer.triggerRepaint()
