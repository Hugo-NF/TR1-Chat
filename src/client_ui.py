# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(867, 598)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.connectionButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.connectionButton.setObjectName("connectionButton")
        self.verticalLayout_2.addWidget(self.connectionButton)
        self.roomsButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.roomsButton.setObjectName("roomsButton")
        self.verticalLayout_2.addWidget(self.roomsButton)
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
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.messageBoxLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.messageBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.messageBoxLayout.setObjectName("messageBoxLayout")
        self.messageEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.messageEdit.setObjectName("messageEdit")
        self.messageBoxLayout.addWidget(self.messageEdit)
        self.sendButtonLayout = QtWidgets.QVBoxLayout()
        self.sendButtonLayout.setObjectName("sendButtonLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.sendButtonLayout.addItem(spacerItem)
        self.sendButton = QtWidgets.QPushButton(self.layoutWidget)
        self.sendButton.setObjectName("sendButton")
        self.sendButtonLayout.addWidget(self.sendButton)
        self.messageBoxLayout.addLayout(self.sendButtonLayout)
        self.verticalLayout_2.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 867, 22))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionEnglish = QtWidgets.QAction(MainWindow)
        self.actionEnglish.setObjectName("actionEnglish")
        self.actionPortuguese = QtWidgets.QAction(MainWindow)
        self.actionPortuguese.setObjectName("actionPortuguese")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.menuOptions.addAction(self.actionAbout_Qt)
        self.menuOptions.addAction(self.actionQuit)
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Concord"))
        self.connectionButton.setText(_translate("MainWindow", "Connection"))
        self.roomsButton.setText(_translate("MainWindow", "Rooms"))
        self.chatFrame.setTitle(_translate("MainWindow", "Chat"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionEnglish.setText(_translate("MainWindow", "English"))
        self.actionPortuguese.setText(_translate("MainWindow", "Portuguese"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))

    def write_message(self, username, msg_text):
        self.textViewer.insertPlainText("\n[{username}]: {msg_text}".format(username=username, msg_text=msg_text))

    def clear_message_box(self):
        self.messageEdit.clear()

    def read_message_box(self):
        return self.messageEdit.toPlainText()
