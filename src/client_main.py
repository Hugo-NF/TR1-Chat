import sys

# PyQt framework
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

# Created Qt interfaces
from src.client_ui import Ui_MainWindow
from src.connect_ui import Ui_connectionDialog
from src.rooms_ui import Ui_roomsDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Concord")
    app.setApplicationName("Concord")

    main_window = QMainWindow()
    conn_dialog = QDialog(main_window)
    rooms_dialog = QDialog(main_window)

    main_ui = Ui_MainWindow()
    conn_ui = Ui_connectionDialog()
    rooms_ui = Ui_roomsDialog()

    # Draw the window
    main_ui.setupUi(main_window)
    conn_ui.setupUi(conn_dialog)
    rooms_ui.setupUi(rooms_dialog)

    # Application initial configuration
    # main_ui.roomsButton.hide()
    main_ui.connectionButton.clicked.connect(conn_dialog.show)
    main_ui.roomsButton.clicked.connect(rooms_dialog.show)

    conn_ui.connectButton.clicked.connect(conn_ui.start_animation)


    # Application initial size
    main_window.resize(1024, 768)

    # Show screen to user
    main_window.show()

    sys.exit(app.exec_())