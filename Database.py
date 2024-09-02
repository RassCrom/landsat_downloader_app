from PySide6 import QtWidgets
from PySide6.QtCore import Signal

import psycopg2

from shapely.geometry import Polygon
import datetime
import json


columns_for_metadata = [
    'display_id', 'cloud_cover', 'landsat_scene_id', 'acquisition_date',
    'collection_number', 'wrs_path', 'wrs_row', 'land_cloud_cover', 'scene_cloud_cover',
    'sun_elevation_l0ra', 'sun_azimuth_l0ra', 'data_type', 'sensor_id', 'satellite',
    'product_map_projection', 'utm_zone', 'datum', 'ellipsoid', 'scene_center_latitude',
    'scene_center_longitude', 'corner_upper_left_latitude', 'corner_upper_left_longitude',
    'corner_upper_right_latitude', 'corner_upper_right_longitude', 'corner_lower_left_latitude',
    'corner_lower_left_longitude', 'corner_lower_right_latitude', 'corner_lower_right_longitude', 
    'spatial_coverage'
]


class Database(QtWidgets.QWidget):
    connection_established = Signal(object) 

    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.password_for_db = QtWidgets.QLineEdit(self)
        self.password_for_db.setPlaceholderText("Password")
        self.layout.addWidget(self.password_for_db)

        self.database_for_db = QtWidgets.QLineEdit(self)
        self.database_for_db.setPlaceholderText("Database")
        self.layout.addWidget(self.database_for_db)

        self.user_for_db = QtWidgets.QLineEdit(self)
        self.user_for_db.setPlaceholderText("User")
        self.layout.addWidget(self.user_for_db)

        self.host_for_db = QtWidgets.QLineEdit(self)
        self.host_for_db.setPlaceholderText("Host")
        self.layout.addWidget(self.host_for_db)

        self.port_for_db = QtWidgets.QLineEdit(self)
        self.port_for_db.setPlaceholderText("Port")
        self.layout.addWidget(self.port_for_db)

        self.submit_conn_btn = QtWidgets.QPushButton('Submit', self)
        self.layout.addWidget(self.submit_conn_btn)
        self.submit_conn_btn.clicked.connect(self.connect_database)

        self.conn = None


    def connect_database(self):
        try:
            self.conn = psycopg2.connect(
                database=self.database_for_db.text(),
                user=self.user_for_db.text(),
                host=self.host_for_db.text(),
                password=self.password_for_db.text(),
                port=int(self.port_for_db.text()) or int(5432)
            )
            
            QtWidgets.QMessageBox.information(self, "Success", "Connected to the database successfully.")
            self.connection_established.emit(self.conn)
            
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to connect to the database: {e}")

    def get_connection(self):
        return self.conn

    def retrieve_values(self, data, columns):
        result = []
        for col in columns:
            value = data.get(col)
            if isinstance(value, Polygon):
                value = value.wkt
            elif isinstance(value, datetime.datetime):
                value = value.isoformat()
            elif isinstance(value, dict):
                value = json.dumps(value)
            result.append(value)
        return result
    
    def save_metadata(self, conn, data):
        try:
            cur = conn.cursor()
            retrieved_data = self.retrieve_values(data, columns_for_metadata)
            print(len(retrieved_data), len(columns_for_metadata))
            cur.execute(f"INSERT INTO scene_data({', '.join(columns_for_metadata)}) VALUES ({', '.join(repr(value) for value in retrieved_data)})")
            conn.commit()
            cur.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save metadata: {e}")
        finally:
            conn.close()

