# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(917, 437)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.optionsLayout = QtWidgets.QVBoxLayout()
        self.optionsLayout.setObjectName("optionsLayout")
        self.connectionButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.connectionButton.setObjectName("connectionButton")
        self.optionsLayout.addWidget(self.connectionButton)
        self.roomsButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.roomsButton.setObjectName("roomsButton")
        self.optionsLayout.addWidget(self.roomsButton)
        self.verticalLayout.addLayout(self.optionsLayout)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(4)
        self.splitter.setObjectName("splitter")
        self.chatFrame = QtWidgets.QGroupBox(self.splitter)
        self.chatFrame.setObjectName("chatFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.chatFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textViewer = QtWidgets.QTextBrowser(self.chatFrame)
        self.textViewer.setObjectName("textViewer")
        self.horizontalLayout_2.addWidget(self.textViewer)
        self.onlineFrame = QtWidgets.QGroupBox(self.splitter)
        self.onlineFrame.setObjectName("onlineFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.onlineFrame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.onlineList = QtWidgets.QListWidget(self.onlineFrame)
        self.onlineList.setObjectName("onlineList")
        self.horizontalLayout_3.addWidget(self.onlineList)
        self.verticalLayout.addWidget(self.splitter)
        self.sendFrame = QtWidgets.QGroupBox(self.centralwidget)
        self.sendFrame.setObjectName("sendFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.sendFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sendEdit = QtWidgets.QLineEdit(self.sendFrame)
        self.sendEdit.setObjectName("sendEdit")
        self.horizontalLayout.addWidget(self.sendEdit)
        self.sendButton = QtWidgets.QPushButton(self.sendFrame)
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout.addWidget(self.sendButton)
        self.verticalLayout.addWidget(self.sendFrame)
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
        self.onlineFrame.setTitle(_translate("MainWindow", "Online"))
        self.sendFrame.setTitle(_translate("MainWindow", "Send"))
        self.sendButton.setText(_translate("MainWindow", "Send"))

    def write_message(self, msg_text):
        self.textViewer.insertPlainText("{msg_text}\n".format(msg_text=msg_text))

    def clear_message_box(self):
        self.sendEdit.clear()

    def read_message_box(self):
        return self.sendEdit.toPlainText()


class ClientWindow(QMainWindow):
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?\n"\
                   "Warning: Remember to disconnect before quitting"
        reply = QMessageBox.question(self, 'Quit', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
