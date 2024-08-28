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


class Database:
    def __init__(self, password, db, user, host, port):
        self.conn = psycopg2.connect(
            database=db,
            user=user,
            host=host,
            password=password,
            port=int(port))

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
    
    def save_metadata(self, data):
        cur = self.conn.cursor()
        retrieved_data = self.retrieve_values(data, columns_for_metadata)
        print(len(retrieved_data), len(columns_for_metadata))
        cur.execute(f"INSERT INTO scene_data({', '.join(columns_for_metadata)}) VALUES ({', '.join(repr(value) for value in retrieved_data)})")
        self.conn.commit()
        cur.close()
        self.conn.close()