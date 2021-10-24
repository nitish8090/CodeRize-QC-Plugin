from . import Database


class FootPrintTable(Database):
    name = 'building_footprints'
    schema_name = "public"
    geometry_column = 'geometry'

    def __init__(self):
        super(FootPrintTable, self).__init__()

