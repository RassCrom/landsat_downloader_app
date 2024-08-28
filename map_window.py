from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
import folium
from PySide6.QtCore import QUrl
import io
import sys, os

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the layout
        layout = QVBoxLayout()

        # Create a Folium map
        self.coords = (50, -4)  # Corrected coordinates order (latitude, longitude)
        self.m = folium.Map(
            title='Test',
            zoom_start=8,
            location=self.coords
        )
        self.m.add_child(
            folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=True)
        )

        # Save the map to an in-memory file
        data = io.BytesIO()
        self.map_path = './map.html'
        self.m.save(self.map_path)

        # Create a QWebEngineView
        webView = QWebEngineView()
        webView.setUrl(QUrl.fromLocalFile(os.path.abspath(self.map_path)))

        # Set up the layout and central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        layout.addWidget(webView)

        self.setWindowTitle("Folium Map in PySide6")

if __name__ == "__main__":
    app = QApplication([])
    widget = MapWindow()
    widget.resize(800, 600)  # Set a more suitable size for viewing the map
    widget.show()
    sys.exit(app.exec())
