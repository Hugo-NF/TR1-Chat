# Project imports
# Python built-in for sockets programming
import sys
from socket import *

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from src.client_ui import ClientWindow, Ui_MainWindow
from src.connect_ui import Ui_connectionDialog
from src.rooms_ui import Ui_roomsDialog


class Client:
    """Handles the communication with the server application"""

    buffer_size = 1024

    def __init__(self, main_ui, rooms_ui, conn_ui):
        """Initializes the client side application with a given host and port"""
        # UI object
        self.main_ui = main_ui
        self.rooms_ui = rooms_ui
        self.conn_ui = conn_ui

        self.conn_ui.connectionProgress.hide()
        self.conn_ui.connectButton.clicked.connect(lambda: self.connect(self.conn_ui.hostEdit.text(),
                                                                        self.conn_ui.portEdit.text()))

    def connect(self, host, port):
        # Socket properties
        self.conn_host = host
        self.conn_port = port
        try:
            self.conn_address = (self.conn_host, int(self.conn_port))
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.conn_ui.connectionProgress.show()
            self.socket.connect(self.conn_address)
            QMessageBox.information(self.main_ui.centralwidget, 'Connected',
                                    "Successfully connected, you may now close connection dialog", QMessageBox.Ok)

            self.conn_ui.connectionProgress.setMaximum(100)
            self.conn_ui.connectionProgress.setValue(100)
            self.conn_ui.connectionProgress.setFormat("Connected")
            self.conn_ui.connectButton.setDisabled(True)
            self.main_ui.connectionButton.setText("Disconnect")
            self.main_ui.connectionButton.clicked.connect(self.disconnect)
        except TypeError:
            QMessageBox.warning(self.main_ui.centralwidget, 'Error', "Check your HOST:PORT configuration",
                                QMessageBox.Ok)
        except ValueError:
            QMessageBox.warning(self.main_ui.centralwidget, 'Error', "Check your HOST:PORT configuration",
                                QMessageBox.Ok)
        except OSError:
            QMessageBox.critical(self.main_ui.centralwidget, 'Error', "Could not find a server at {}:{}"
                                 .format(self.conn_host, self.conn_port), QMessageBox.Ok)
            self.conn_ui.connectionProgress.hide()

    def disconnect(self):
        self.socket.shutdown(2)
        self.socket.close()
        QMessageBox.information(self.main_ui.centralwidget, 'Disconnected',
                                "Disconnected successfully", QMessageBox.Ok)
        self.main_ui.connectionButton.setText("Connection")
        self.main_ui.connectionButton.clicked.disconnect(self.disconnect)
        self.conn_ui.connectionProgress.setMaximum(0)
        self.conn_ui.connectionProgress.setValue(-1)
        self.conn_ui.connectionProgress.hide()
        self.conn_ui.connectButton.setDisabled(False)

    def receive(self):
        while True:
            try:
                message = self.socket.recv(self.buffer_size).decode("utf8")
                self.main_ui.write_message(message)
            except OSError:  # Client has left
                break

    def send(self, message):
        self.socket.send(bytes(message, "utf8"))

    def send_action(self):
        message = self.main_ui.read_message_box()
        self.send(message)

    def treat_message(self, message):
        print()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Concord")
    app.setApplicationName("Concord")

    main_window = ClientWindow()
    conn_dialog = QDialog(main_window)
    rooms_dialog = QDialog(main_window)

    main_ui = Ui_MainWindow()
    conn_ui = Ui_connectionDialog()
    rooms_ui = Ui_roomsDialog()

    # Draw the window
    main_ui.setupUi(main_window)
    conn_ui.setupUi(conn_dialog)
    rooms_ui.setupUi(rooms_dialog)

    # Initialize client
    client = Client(main_ui, rooms_ui, conn_ui)

    # Application initial configuration
    main_ui.connectionButton.clicked.connect(conn_dialog.show)
    main_ui.roomsButton.clicked.connect(rooms_dialog.show)

    # Application initial size
    main_window.resize(1024, 768)

    # Show screen to user
    main_window.show()

    sys.exit(app.exec_())