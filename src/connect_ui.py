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
        connectionDialog.resize(514, 78)
        self.gridLayout = QtWidgets.QGridLayout(connectionDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.connectButton = QtWidgets.QPushButton(connectionDialog)
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 1, 1, 1, 1)
        self.portLayout = QtWidgets.QHBoxLayout()
        self.portLayout.setObjectName("portLayout")
        self.portLabel = QtWidgets.QLabel(connectionDialog)
        self.portLabel.setObjectName("portLabel")
        self.portLayout.addWidget(self.portLabel)
        self.portEdit = QtWidgets.QLineEdit(connectionDialog)
        self.portEdit.setObjectName("portEdit")
        self.portLayout.addWidget(self.portEdit)
        self.gridLayout.addLayout(self.portLayout, 1, 0, 1, 1)
        self.hostLayout = QtWidgets.QHBoxLayout()
        self.hostLayout.setObjectName("hostLayout")
        self.hostLabel = QtWidgets.QLabel(connectionDialog)
        self.hostLabel.setObjectName("hostLabel")
        self.hostLayout.addWidget(self.hostLabel)
        self.hostEdit = QtWidgets.QLineEdit(connectionDialog)
        self.hostEdit.setText("")
        self.hostEdit.setObjectName("hostEdit")
        self.hostLayout.addWidget(self.hostEdit)
        self.gridLayout.addLayout(self.hostLayout, 0, 0, 1, 1)
        self.connectionProgress = QtWidgets.QProgressBar(connectionDialog)
        self.connectionProgress.setMinimum(0)
        self.connectionProgress.setMaximum(0)
        self.connectionProgress.setProperty("value", -1)
        self.connectionProgress.setFormat("")
        self.connectionProgress.setObjectName("connectionProgress")
        self.gridLayout.addWidget(self.connectionProgress, 0, 1, 1, 1)

        self.retranslateUi(connectionDialog)
        QtCore.QMetaObject.connectSlotsByName(connectionDialog)

    def retranslateUi(self, connectionDialog):
        _translate = QtCore.QCoreApplication.translate
        connectionDialog.setWindowTitle(_translate("connectionDialog", "Connection Properties"))
        self.connectButton.setText(_translate("connectionDialog", "Connect"))
        self.portLabel.setText(_translate("connectionDialog", "Port:"))
        self.portEdit.setPlaceholderText(_translate("connectionDialog", "8080"))
        self.hostLabel.setText(_translate("connectionDialog", "Host Address:"))
        self.hostEdit.setPlaceholderText(_translate("connectionDialog", "127.0.0.1"))


