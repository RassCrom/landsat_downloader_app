from PySide6 import QtWidgets, QtCore
from API import API_download

from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer


class CredentialsWindow(QtWidgets.QWidget):
    def __init__(self, username, password):
        super().__init__()

        self.user_landsat = username
        self.pass_landsat = password
        self.available_scenes = []

        # Initialize API
        self.api = API(self.user_landsat, self.pass_landsat)

        # Initialize input fields with placeholder text
        self.cloud_cover_input = QtWidgets.QLineEdit(self)
        self.cloud_cover_input.setPlaceholderText("Enter cloud coverage (0-100): ")

        self.x_coord_input = QtWidgets.QLineEdit(self)
        self.x_coord_input.setPlaceholderText("x coordinate: ")

        self.y_coord_input = QtWidgets.QLineEdit(self)
        self.y_coord_input.setPlaceholderText("y coordinate: ")

        # Use QDateEdit for start and end dates
        self.start_date_label = QtWidgets.QLabel("Start date: ", self)
        self.start_date_input = QtWidgets.QDateEdit(self)
        self.start_date_input.setCalendarPopup(True)

        self.end_date_label = QtWidgets.QLabel("End date: ", self)
        self.end_date_input = QtWidgets.QDateEdit(self)
        self.end_date_input.setCalendarPopup(True)

        # Combo box with Landsat dataset IDs
        self.combo_box = QtWidgets.QComboBox(self)
        self.datasets_ids = [
            'landsat_tm_c2_l1',
            'landsat_tm_c2_l2',
            'landsat_etm_c2_l1',
            'landsat_etm_c2_l2',
            'landsat_ot_c2_l1',
            'landsat_ot_c2_l2'
        ]
        self.combo_box.addItems(self.datasets_ids)

        self.results = QtWidgets.QLabel(self)
        self.results.setText("No results yet.")

        self.submit_search_params_btn = QtWidgets.QPushButton("Submit Parameters", self)

        # Layout configuration
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.combo_box)
        self.layout.addWidget(self.x_coord_input)
        self.layout.addWidget(self.y_coord_input)
        self.layout.addWidget(self.start_date_label)
        self.layout.addWidget(self.start_date_input)
        self.layout.addWidget(self.end_date_label)
        self.layout.addWidget(self.end_date_input)
        self.layout.addWidget(self.cloud_cover_input)
        self.layout.addWidget(self.results)
        self.layout.addWidget(self.submit_search_params_btn)

        self.submit_search_params_btn.clicked.connect(self.show_result)

    @QtCore.Slot()
    def show_result(self):
        # Check if required inputs are provided
        if not self.x_coord_input.text() or not self.y_coord_input.text() or not self.start_date_input.date() or not self.end_date_input.date():
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter both X and Y coordinates and start and end date.")
            return

        try:
            # Convert inputs to appropriate types
            cloud_cover = int(self.cloud_cover_input.text()) if self.cloud_cover_input.text() else 100
            x_coord = float(self.x_coord_input.text())
            y_coord = float(self.y_coord_input.text())

            start_date = self.start_date_input.date().toString('yyyy-MM-dd')
            end_date = self.end_date_input.date().toString('yyyy-MM-dd')

            dataset = self.combo_box.currentText()

            # Perform the search
            scenes = self.api.search(
                dataset=dataset,
                latitude=y_coord,
                longitude=x_coord,
                start_date=start_date,
                end_date=end_date,
                max_cloud_cover=cloud_cover,
                max_results=12
            )

            sorted_scenes = sorted(scenes, key=lambda scene: scene['cloud_cover'])

            print(f"{len(sorted_scenes)} scenes found.")
            if sorted_scenes:
                self.available_scenes = [scene['display_id'] for scene in sorted_scenes]
                results_text = "\n".join(self.available_scenes)
                self.results.setText(f"Scenes found:\n{results_text}")

                download_scene = API_download(self.user_landsat, self.pass_landsat)

                # Clear search params widgets
                for i in reversed(range(self.layout.count())): 
                    widget = self.layout.itemAt(i).widget()
                    if widget:
                        widget.deleteLater()

                self.scene_to_download_list = QtWidgets.QComboBox(self)
                self.scene_to_download_list.setPlaceholderText("Choose scene number to download")
                self.scene_to_download_list.addItems(self.available_scenes)
                self.layout.addWidget(self.scene_to_download_list)

                self.download = QtWidgets.QPushButton("Download scene", self)
                self.layout.addWidget(self.download)

                self.output_dir = QtWidgets.QLineEdit(self)
                self.output_dir.setPlaceholderText("Paste directory path")
                self.layout.addWidget(self.output_dir)

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


                self.download.clicked.connect(lambda: download_scene.download_scene(sorted_scenes, self.scene_to_download_list.currentText(), self.password_for_db.text(), self.database_for_db.text(), self.user_for_db.text(), self.host_for_db.text(), self.port_for_db.text(), self.output_dir.text()))

            else:
                self.results.setText("No scenes found.")
            
            for scene in scenes:
                print(scene['acquisition_date'].strftime('%Y-%m-%d'))
                
        except ValueError as e:
            print("Invalid input value.")
            print(f"Error: {e}")
        except Exception as e:
            print("Failed to search for scenes.")
            print(f"Error: {e}")

    @QtCore.Slot()
    def calculate_indices(self):
        pass
