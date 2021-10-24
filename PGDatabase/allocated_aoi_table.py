from . import Database
from qgis.core import QgsDataSourceUri, QgsVectorLayer


class AllocatedAOITable(Database):
    name = 'allocated_aoi'
    schema_name = "public"
    vendor_name_column = 'vndr_name'
    geometry_column = 'geometry'

    def __init__(self):
        super().__init__()

    def get_all_vendors(self):
        if self.is_connected or self.connection is None:
            sql = f""" 
            SELECT DISTINCT "{self.vendor_name_column}" 
            FROM "{self.schema_name}"."{self.name}" 
            WHERE "{self.vendor_name_column}" is not Null"""
            self.sql_cursor.execute(sql)
            result = self.sql_cursor.fetchall()
            if result is None or len(result) == 0:
                print("[DEBUG] No vendors found to load AOI from")
            else:
                vendor_list = [_[0] for _ in result]
                return vendor_list
        else:
            print("[ERROR] Database is not connected")
            return ['Database Error']


