from PySide6 import QtWidgets
from PySide6.QtWidgets import QCheckBox

from landsatxplore.earthexplorer import EarthExplorer
import os

from Database import Database


def find_object_by_key_value(lst, key, value):
    return next((item for item in lst if item.get(key) == value), None)


class API_download(QtWidgets.QWidget):
    def __init__(self, user, password, sorted_scenes, available_scenes_list):
        super().__init__()

        self.user_api = user
        self.pass_api = password
        self.sorted_scenes = sorted_scenes
        self.ee = EarthExplorer(user, password)
        self.db_connection = None

        self.layout = QtWidgets.QVBoxLayout(self)

        self.scene_to_download_list = QtWidgets.QComboBox(self)
        self.scene_to_download_list.setPlaceholderText("Choose scene number to download")
        self.scene_to_download_list.addItems(available_scenes_list)
        self.layout.addWidget(self.scene_to_download_list)

        self.output_dir = QtWidgets.QLineEdit(self)
        self.output_dir.setPlaceholderText("Paste directory path")
        self.layout.addWidget(self.output_dir)

        self.download = QtWidgets.QPushButton("Download scene", self)
        self.layout.addWidget(self.download)
        self.download.clicked.connect(self.download_scene)

        # self.metadata_db = QCheckBox("Save metadata to Database", self)
        # self.metadata_db.stateChanged.connect(self)
        # self.layout.addWidget(self.metadata_db)

        self.database_conn_btn = QtWidgets.QPushButton("Connect DB", self)
        self.layout.addWidget(self.database_conn_btn)
        self.database_conn_btn.clicked.connect(self.show_database_conn_window)


    # def checked_metadata_saver(self):
    #     if self.metadata_db:
    #         self.database_conn_btn = QtWidgets.QPushButton("Connect DB", self)
    #         self.layout.addWidget(self.database_conn_btn)
    #         self.database_conn_btn.clicked.connect(self.show_database_conn_window)

    def show_database_conn_window(self):
        # Create and show the new window with the db connection
        self.credentials_window = Database()
        self.credentials_window.setWindowTitle("Database")
        self.credentials_window.connection_established.connect(self.handle_connection)
        self.credentials_window.resize(800, 500)
        self.credentials_window.show()

    def handle_connection(self, connection):
        self.db_connection = connection
        QtWidgets.QMessageBox.information(self, "Info", "Database connection established and returned.")

    def download_scene(self):
        idx = self.scene_to_download_list.currentText()
        dir = self.output_dir.text() if self.output_dir.text() else './data'
        chosen_scene = find_object_by_key_value(self.sorted_scenes, 'display_id', idx)
        # output_dir = self.output_dir.text() if self.output_dir.text() else dir
        print(self.sorted_scenes)
        print(idx)
        print(chosen_scene)
        if chosen_scene:
            if not os.path.exists(dir):
                os.makedirs(dir)
            
            metadata_to_database = Database()
            print('Downloading started')
            try:
                # self.ee.download(chosen_scene['display_id'], output_dir=os.path.join(dir))
                pass
            except Exception as e:
                print(f"Error during download: {e}")
                return
            
            print('Downloading ended')

            print('Writing metadata to PSQL')
            try:
                if self.db_connection:
                    metadata_to_database.save_metadata(self.db_connection, chosen_scene)
                else:
                    QtWidgets.QMessageBox.information(self, "Info", "Metadata is not saved to database (Metadata saving option is not checked or connection Error).")
            except Exception as e:
                print(f"Error during download: {e}")
                return
            print('Writing metadata to PSQL finished')
            self.logout_ee()

    def logout_ee(self):
        self.ee.logout()