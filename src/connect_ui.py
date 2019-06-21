# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_connectionDialog(object):
    def setupUi(self, connectionDialog):
        connectionDialog.setObjectName("connectionDialog")
        connectionDialog.resize(410, 111)
        self.gridLayout = QtWidgets.QGridLayout(connectionDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hostLabel = QtWidgets.QLabel(connectionDialog)
        self.hostLabel.setObjectName("hostLabel")
        self.horizontalLayout.addWidget(self.hostLabel)
        self.hostEdit = QtWidgets.QLineEdit(connectionDialog)
        self.hostEdit.setObjectName("hostEdit")
        self.horizontalLayout.addWidget(self.hostEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.portLabel = QtWidgets.QLabel(connectionDialog)
        self.portLabel.setObjectName("portLabel")
        self.horizontalLayout_2.addWidget(self.portLabel)
        self.portEdit = QtWidgets.QLineEdit(connectionDialog)
        self.portEdit.setObjectName("portEdit")
        self.horizontalLayout_2.addWidget(self.portEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.connectButton = QtWidgets.QPushButton(connectionDialog)
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 1, 2, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.nicknameLabel = QtWidgets.QLabel(connectionDialog)
        self.nicknameLabel.setObjectName("nicknameLabel")
        self.horizontalLayout_3.addWidget(self.nicknameLabel)
        self.nicknameEdit = QtWidgets.QLineEdit(connectionDialog)
        self.nicknameEdit.setObjectName("nicknameEdit")
        self.horizontalLayout_3.addWidget(self.nicknameEdit)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.connectionProgress = QtWidgets.QProgressBar(connectionDialog)
        self.connectionProgress.setMinimum(0)
        self.connectionProgress.setMaximum(0)
        self.connectionProgress.setProperty("value", -1)
        self.connectionProgress.setFormat("")
        self.connectionProgress.setObjectName("connectionProgress")
        self.gridLayout.addWidget(self.connectionProgress, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)

        self.retranslateUi(connectionDialog)
        QtCore.QMetaObject.connectSlotsByName(connectionDialog)
        connectionDialog.setTabOrder(self.hostEdit, self.portEdit)
        connectionDialog.setTabOrder(self.portEdit, self.nicknameEdit)
        connectionDialog.setTabOrder(self.nicknameEdit, self.connectButton)

    def retranslateUi(self, connectionDialog):
        _translate = QtCore.QCoreApplication.translate
        connectionDialog.setWindowTitle(_translate("connectionDialog", "Connection Properties"))
        self.hostLabel.setText(_translate("connectionDialog", "Host Address:"))
        self.hostEdit.setText(_translate("connectionDialog", "127.0.0.1"))
        self.hostEdit.setPlaceholderText(_translate("connectionDialog", "127.0.0.1"))
        self.portLabel.setText(_translate("connectionDialog", "Port:"))
        self.portEdit.setText(_translate("connectionDialog", "8080"))
        self.portEdit.setPlaceholderText(_translate("connectionDialog", "8080"))
        self.connectButton.setText(_translate("connectionDialog", "Connect"))
        self.nicknameLabel.setText(_translate("connectionDialog", "Nickname:"))


