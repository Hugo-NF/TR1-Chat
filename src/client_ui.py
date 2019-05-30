import sys

# Python built-ins
from threading import Thread

# PyQt framework
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

# Created Qt interfaces
from src.mainwindow import Ui_MainWindow
from src.connect import Ui_connectionDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = QMainWindow()
    conn_dialog = QDialog(main_window)

    main_ui = Ui_MainWindow()
    conn_ui = Ui_connectionDialog()

    # Draw the window
    main_ui.setupUi(main_window)
    conn_ui.setupUi(conn_dialog)

    # Application initial configuration
    main_ui.commandLinkButton.clicked.connect(conn_dialog.show)
    conn_ui.connectButton.clicked.connect(conn_ui.connect_animation)

    # Application starting size
    main_window.resize(1024, 768)

    # Show screen to user
    main_window.show()




    sys.exit(app.exec_())
