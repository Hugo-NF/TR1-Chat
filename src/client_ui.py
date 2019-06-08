# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(867, 598)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.connectionButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.connectionButton.setObjectName("connectionButton")
        self.verticalLayout.addWidget(self.connectionButton)
        self.roomsButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.roomsButton.setObjectName("roomsButton")
        self.verticalLayout.addWidget(self.roomsButton)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.chatFrame = QtWidgets.QGroupBox(self.splitter)
        self.chatFrame.setObjectName("chatFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.chatFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textViewer = QtWidgets.QTextBrowser(self.chatFrame)
        self.textViewer.setObjectName("textViewer")
        self.horizontalLayout.addWidget(self.textViewer)
        self.sendFrame = QtWidgets.QGroupBox(self.splitter)
        self.sendFrame.setObjectName("sendFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.sendFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.messageEdit = QtWidgets.QTextEdit(self.sendFrame)
        self.messageEdit.setObjectName("messageEdit")
        self.horizontalLayout_2.addWidget(self.messageEdit)
        self.sendButton = QtWidgets.QPushButton(self.sendFrame)
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout_2.addWidget(self.sendButton)
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Concord"))
        self.connectionButton.setText(_translate("MainWindow", "Connection"))
        self.roomsButton.setText(_translate("MainWindow", "Rooms"))
        self.chatFrame.setTitle(_translate("MainWindow", "Chat"))
        self.sendFrame.setTitle(_translate("MainWindow", "Send"))
        self.sendButton.setText(_translate("MainWindow", "Send"))

    def write_message(self, username, msg_text):
        self.textViewer.insertPlainText("\n[{username}]: {msg_text}".format(username=username, msg_text=msg_text))

    def clear_message_box(self):
        self.messageEdit.clear()

    def read_message_box(self):
        return self.messageEdit.toPlainText()


class ClientWindow(QMainWindow):
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?\n"\
                   "Warning: Remember to disconnect before quitting"
        reply = QMessageBox.question(self, 'Quit', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()