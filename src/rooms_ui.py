# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rooms.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_roomsDialog(object):
    def setupUi(self, roomsDialog):
        roomsDialog.setObjectName("roomsDialog")
        roomsDialog.resize(453, 364)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(roomsDialog)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.middleSplitter = QtWidgets.QSplitter(roomsDialog)
        self.middleSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.middleSplitter.setObjectName("middleSplitter")
        self.roomsFrame = QtWidgets.QGroupBox(self.middleSplitter)
        self.roomsFrame.setObjectName("roomsFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.roomsFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.refreshButton = QtWidgets.QToolButton(self.roomsFrame)
        self.refreshButton.setObjectName("refreshButton")
        self.verticalLayout.addWidget(self.refreshButton)
        self.roomsList = QtWidgets.QListWidget(self.roomsFrame)
        self.roomsList.setObjectName("roomsList")
        self.verticalLayout.addWidget(self.roomsList)
        self.buttonsRoomLayout = QtWidgets.QHBoxLayout()
        self.buttonsRoomLayout.setObjectName("buttonsRoomLayout")
        self.leaveButton = QtWidgets.QPushButton(self.roomsFrame)
        self.leaveButton.setObjectName("leaveButton")
        self.buttonsRoomLayout.addWidget(self.leaveButton)
        self.joinButton = QtWidgets.QPushButton(self.roomsFrame)
        self.joinButton.setObjectName("joinButton")
        self.buttonsRoomLayout.addWidget(self.joinButton)
        self.verticalLayout.addLayout(self.buttonsRoomLayout)
        self.roomCreateFrame = QtWidgets.QGroupBox(self.roomsFrame)
        self.roomCreateFrame.setObjectName("roomCreateFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.roomCreateFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.roomCreateLayout = QtWidgets.QHBoxLayout()
        self.roomCreateLayout.setObjectName("roomCreateLayout")
        self.roomNameLabel = QtWidgets.QLabel(self.roomCreateFrame)
        self.roomNameLabel.setObjectName("roomNameLabel")
        self.roomCreateLayout.addWidget(self.roomNameLabel)
        self.roomNameEdit = QtWidgets.QLineEdit(self.roomCreateFrame)
        self.roomNameEdit.setObjectName("roomNameEdit")
        self.roomCreateLayout.addWidget(self.roomNameEdit)
        self.createButton = QtWidgets.QPushButton(self.roomCreateFrame)
        self.createButton.setObjectName("createButton")
        self.roomCreateLayout.addWidget(self.createButton)
        self.verticalLayout_4.addLayout(self.roomCreateLayout)
        self.verticalLayout.addWidget(self.roomCreateFrame)
        self.horizontalLayout_3.addWidget(self.middleSplitter)

        self.retranslateUi(roomsDialog)
        QtCore.QMetaObject.connectSlotsByName(roomsDialog)

    def retranslateUi(self, roomsDialog):
        _translate = QtCore.QCoreApplication.translate
        roomsDialog.setWindowTitle(_translate("roomsDialog", "Rooms"))
        self.roomsFrame.setTitle(_translate("roomsDialog", "Available Rooms"))
        self.refreshButton.setText(_translate("roomsDialog", "Refresh"))
        self.leaveButton.setText(_translate("roomsDialog", "Leave"))
        self.joinButton.setText(_translate("roomsDialog", "Join"))
        self.roomCreateFrame.setTitle(_translate("roomsDialog", "Create a room"))
        self.roomNameLabel.setText(_translate("roomsDialog", "Name:"))
        self.createButton.setText(_translate("roomsDialog", "Create"))

    def add_room(self, room):
        self.roomsList.addItem(room)

    def clear_rooms(self):
        self.roomsList.clear()
