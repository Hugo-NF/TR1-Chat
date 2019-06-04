import sys

# PyQt framework
from PyQt5.QtWidgets import QApplication, QMainWindow

# Created Qt interfaces
from src.server_ui import Ui_serverWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Concord Server")
    app.setApplicationName("Concord Server")

    main_window = QMainWindow()
    main_ui = Ui_serverWindow()

    # Draw the window
    main_ui.setupUi(main_window)

    # Application initial size
    main_window.resize(1024, 768)

    # Show screen to user
    main_window.show()

    sys.exit(app.exec_())