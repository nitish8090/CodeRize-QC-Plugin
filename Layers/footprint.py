from ..PGDatabase import FootPrintTable, Database, AllocatedAOITable
from qgis.core import QgsDataSourceUri, QgsVectorLayer, QgsProject


class FootprintLayer:

    def __init__(self):
        self.layer = None

    @classmethod
    def get_from_postgres(cls, intersecting_geometry=None):
        uri = QgsDataSourceUri()
        uri.setConnection(
            Database.host,
            str(Database.port),
            Database.database_name,
            Database.user,
            Database.password
        )

        if intersecting_geometry is None:
            where_clause = ''
        else:
            where_clause = f"""
            ST_Intersects({FootPrintTable.schema_name}.{FootPrintTable.name}.{FootPrintTable.geometry_column}, 
            '{intersecting_geometry}')
            """
            # print(where_clause)

        uri.setDataSource(
            FootPrintTable.schema_name,
            FootPrintTable.name,
            FootPrintTable.geometry_column,
            where_clause
        )

        _instance = cls()
        _instance.layer = QgsVectorLayer(uri.uri(), "Footprint Layer", "postgres")
        return _instance

    def add_to_qgis(self):
        if not self.layer.isValid():
            print("Layer %s did not load" % self.layer.name())
        QgsProject.instance().addMapLayers([self.layer])