from . import Database
from qgis.core import QgsDataSourceUri, QgsVectorLayer


class AITable(Database):
    name = 'ai_points'
    schema_name = "public"
    geometry_column = 'geometry'

    def __init__(self):
        super(AITable, self).__init__()

