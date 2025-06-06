from mysql.connector import connect, errorcode, Error
from os import environ
import pandas as pd
import csv
import json as js
from datetime import date, datetime
from fastavro import writer as avro_writer
import pyarrow as pa
import os

config = {
    "user": environ['DATABASE_USERNAME'],
    "password": environ['DATABASE_PASSWORD'],
    "host": environ['DATABASE_HOST'],
    "database": environ['DATABASE_NAME'],
    "charset": 'utf8'
}

columns=['ID_VENTA', 'FECHA_VENTA', 'ID_CLIENTE', 'ID_EMPLEADO',
                  'ID_PRODUCTO', 'CANTIDAD', 'PRECIO_UNITARIO', 'DESCUENTO', 'FORMA_PAGO']

def make_folder(path):
    """
    This function checks if the directory exists, and if not, it creates the necessary directories.
    
    :param path: The path where the directory should be created.
    :return: None
    """
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

class DataBaseConnection:
    """ A class to handle the connection to a MySQL database
    and perform data retrieval and conversion to CSV/JSON formats."""
    def __init__(self, config: dict = config):
        """
        Initializes an instance of the DataBaseConnection class.
        Establishes a connection to the MySQL database using the provided configuration parameters.

        Parameters:
            config (dict): A dictionary containing the database connection parameters:
                - user (str): Database username.
                - password (str): Database password.
                - host (str): Database host address.
                - database (str): Name of the database to connect to.
                - charset (str, optional): Character set for the connection. Defaults to 'utf8'.
        Returns:
            None
        """
        self.config = config

        def get_connection():
            try:
                return connect(**self.config)
            except Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
                return None

        def get_data(connection: connect, query: str):
            my_cursor = connection.cursor()
            my_cursor.execute(query)
            data = my_cursor.fetchall()
            my_cursor.close()
            return data

        cnx = get_connection()

        print("Connection established with Data Base")

        self.data = get_data(cnx, "SELECT * FROM UN.VENTAS")

    def data_to_csv(self, path):
        """
        Converts the data from the Data Base to CSV format and saves it to the designated path.

        :param path: Path where the CSV file will be saved.
        :return: None.
        """
        make_folder(path)
        with open(path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(self.data)
    def data_to_json(self, path):
        """
        Converts data to JSON format and saves it to the designated path.

        :param path: Path where the JSON file will be saved.
        :return: None.
        """
        make_folder(path)
        def make_json_safe(row_dict):
            safe = {}
            for k, v in row_dict.items():
                if isinstance(v, (date, datetime)):
                    safe[k] = v.isoformat()
                elif isinstance(v, (str, int, float, bool)) or v is None:
                    safe[k] = v
                else:
                    safe[k] = str(v)
            return safe

        data_dicts = [make_json_safe(dict(zip(columns, row))) for row in self.data]
        
        with open(path, 'w', encoding='utf-8') as f:
            js.dump(data_dicts, f, ensure_ascii=False, indent=4)
    def data_to_avro(self, path):
        """
        Converts data to Avro format and saves it to the designated path.

        :param path: Path where the Avro file will be saved.
        :return: None.
        """
        make_folder(path)
        def to_avro_safe(row_dict):
            safe = {}
            for k, v in row_dict.items():
                if isinstance(v, (date, datetime)):
                    safe[k] = v.isoformat()
                else:
                    safe[k] = v
            return safe
        schema = {
            "doc": "Sales",
            "name": "Sales",
            "namespace": "UN",
            "type": "record",
            "fields": [
                {"name": col, "type": _type} for col, _type in zip(columns,
                ["string", "string", "int", "int", "int", "int", "float", "float", "string"])
            ]
        }
        rows = [to_avro_safe(dict(zip(columns, row))) for row in self.data]
        with open(path, "wb") as out:
            avro_writer(out, schema, rows)
    def data_to_parquet(self, path):
        """
        Converts data to Parquet format and saves it to the designated path.

        :param path: Path where the Parquet file will be saved.
        :return: None.
        """
        make_folder(path)

        def to_serializable(val):
            if isinstance(val, (date, datetime)):
                return val.isoformat()
            return val
        
        df = pd.DataFrame([{k: to_serializable(v) for k, v in zip(columns, row)} for row in self.data])
        df.to_parquet(path, engine="pyarrow", index=False)
        
def save_data_to_files():
    """
    Saves data from the database to CSV, JSON, Avro, and Parquet files.
    This function creates a DataBaseConnection instance, retrieves data from the database,
    and saves it in the specified formats.
    It measures the time taken for each conversion and prints it to the console.
    The data base is then printed.
    """
    db_connection = DataBaseConnection()
    import time as t

    print ("Saving data to files...")
    print("Converting data to CSV, JSON, Avro, and Parquet formats...\n")
    time = t.time()
    db_connection.data_to_csv('data files/data.csv')
    print(f"CSV conversion took {t.time() - time} seconds")
    time = t.time()
    db_connection.data_to_json('data files/data.json')
    print(f"JSON conversion took {t.time() - time} seconds")
    time = t.time()
    db_connection.data_to_avro('data files/data.avro')
    print(f"Avro conversion took {t.time() - time} seconds")
    time = t.time()
    db_connection.data_to_parquet('data files/data.parquet')
    print(f"Parquet conversion took {t.time() - time} seconds")
