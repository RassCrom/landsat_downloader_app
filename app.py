import os
from landsatxplore.api import API

import PySide6.QtCore
import sys
from PySide6 import QtCore, QtWidgets

from CredentialWindow import CredentialsWindow
    

print(PySide6.QtCore.__version__)


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.saved_user = ""  # Variable to save the username
        self.saved_pass = ""  # Variable to save the password

        self.username = QtWidgets.QLineEdit(self)
        self.password = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Enter username: ")
        self.password.setPlaceholderText("Enter password: ")

        # Set the password field to hide input text
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.submit_cred_btn = QtWidgets.QPushButton("Submit")
        self.text = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.submit_cred_btn)

        self.submit_cred_btn.clicked.connect(self.save_input)

    @QtCore.Slot()
    def save_input(self):
        self.saved_user = self.username.text()
        self.saved_pass = self.password.text()
        
        # Call check_credentials with the entered username and password
        self.check_credentials(self.saved_user, self.saved_pass)

    @QtCore.Slot()
    def check_credentials(self, username, password):
        try:
            # Attempt to initialize the API with the given credentials
            api = API(username, password)
            # If successful, show a new window with the credentials
            self.show_credentials_window(username, password)
            # Close the current window
            self.close()
        except Exception as e:
            self.text.setText("Failed to authenticate. Please check your username and password.")
            print(f"Error: {e}")

    def show_credentials_window(self, username, password):
        # Create and show the new window with the credentials
        self.credentials_window = CredentialsWindow(username, password)
        self.credentials_window.setWindowTitle("Credentials")
        self.credentials_window.resize(800, 500)
        self.credentials_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(200, 150)
    widget.show()

    sys.exit(app.exec())
