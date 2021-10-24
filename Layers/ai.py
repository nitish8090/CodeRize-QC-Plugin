from ..PGDatabase import AITable, Database, AllocatedAOITable
from qgis.core import QgsDataSourceUri, QgsVectorLayer, QgsProject


class AILayer:

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
            ST_Intersects({AITable.schema_name}.{AITable.name}.{AITable.geometry_column}, 
            '{intersecting_geometry}')
            """
            # print(where_clause)

        uri.setDataSource(
            AITable.schema_name,
            AITable.name,
            AITable.geometry_column,
            where_clause
        )

        _instance = cls()
        _instance.layer = QgsVectorLayer(uri.uri(), "AI Layer", "postgres")
        return _instance

    def add_to_qgis(self):
        if not self.layer.isValid():
            print("Layer %s did not load" % self.layer.name())
        QgsProject.instance().addMapLayers([self.layer])
