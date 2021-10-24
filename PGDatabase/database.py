import psycopg2
# from .tables import AllocatedAOI


class Database:
    host = "dev3.coderize.in"
    port = 5432
    database_name = "qc_bucket_b47"
    user = "postgres"
    password = "test"

    connection = None
    sql_cursor = None
    is_connected = False

    def __init__(self):
        pass

    @classmethod
    def connect(cls):
        cls.connection = psycopg2.connect(host=cls.host, database=cls.database_name, user=cls.user,
                                          password=cls.password)
        cls.is_connected = True
        cls.sql_cursor = cls.connection.cursor()
