# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from threading import Thread
import time

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_connectionDialog(object):
    def setupUi(self, connectionDialog):
        connectionDialog.setObjectName("connectionDialog")
        connectionDialog.resize(553, 112)
        self.gridLayout = QtWidgets.QGridLayout(connectionDialog)
        self.gridLayout.setObjectName("gridLayout")
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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.displayNameLabel = QtWidgets.QLabel(connectionDialog)
        self.displayNameLabel.setObjectName("displayNameLabel")
        self.horizontalLayout.addWidget(self.displayNameLabel)
        self.displayNameEdit = QtWidgets.QLineEdit(connectionDialog)
        self.displayNameEdit.setObjectName("displayNameEdit")
        self.horizontalLayout.addWidget(self.displayNameEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 2)
        self.serverLayout = QtWidgets.QVBoxLayout()
        self.serverLayout.setObjectName("serverLayout")
        self.tcpRadioButton = QtWidgets.QRadioButton(connectionDialog)
        self.tcpRadioButton.setChecked(True)
        self.tcpRadioButton.setObjectName("tcpRadioButton")
        self.serverLayout.addWidget(self.tcpRadioButton)
        self.udpRadioButton = QtWidgets.QRadioButton(connectionDialog)
        self.udpRadioButton.setObjectName("udpRadioButton")
        self.serverLayout.addWidget(self.udpRadioButton)
        self.gridLayout.addLayout(self.serverLayout, 0, 1, 2, 1)
        self.connectButton = QtWidgets.QPushButton(connectionDialog)
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 1, 2, 1, 1)
        self.portLayout = QtWidgets.QHBoxLayout()
        self.portLayout.setObjectName("portLayout")
        self.portLabel = QtWidgets.QLabel(connectionDialog)
        self.portLabel.setObjectName("portLabel")
        self.portLayout.addWidget(self.portLabel)
        self.portEdit = QtWidgets.QLineEdit(connectionDialog)
        self.portEdit.setObjectName("portEdit")
        self.portLayout.addWidget(self.portEdit)
        self.gridLayout.addLayout(self.portLayout, 1, 0, 1, 1)
        self.connectionProgress = QtWidgets.QProgressBar(connectionDialog)
        self.connectionProgress.setProperty("value", 0)
        self.connectionProgress.setFormat("")
        self.connectionProgress.setObjectName("connectionProgress")
        self.connectionProgress.hide()
        self.gridLayout.addWidget(self.connectionProgress, 1, 3, 1, 1)

        self.animationThread = Thread(target=self.conn_animate)

        self.retranslateUi(connectionDialog)
        QtCore.QMetaObject.connectSlotsByName(connectionDialog)

    def retranslateUi(self, connectionDialog):
        _translate = QtCore.QCoreApplication.translate
        connectionDialog.setWindowTitle(_translate("connectionDialog", "Connection Properties"))
        self.hostLabel.setText(_translate("connectionDialog", "Host Address:"))
        self.hostEdit.setPlaceholderText(_translate("connectionDialog", "127.0.0.1"))
        self.displayNameLabel.setText(_translate("connectionDialog", "Display Name:"))
        self.tcpRadioButton.setText(_translate("connectionDialog", "TCP"))
        self.udpRadioButton.setText(_translate("connectionDialog", "UDP"))
        self.connectButton.setText(_translate("connectionDialog", "Connect"))
        self.portLabel.setText(_translate("connectionDialog", "Port:"))
        self.portEdit.setPlaceholderText(_translate("connectionDialog", "8080"))

    def conn_animate(self):
        self.connectionProgress.show()

        for i in range(30):
            self.connectionProgress.setInvertedAppearance(False)
            for value in range(0, 101, 10):
                time.sleep(0.05)
                self.connectionProgress.setValue(value)
            self.connectionProgress.setInvertedAppearance(True)
            for value in range(101, -1, -10):
                time.sleep(0.05)
                self.connectionProgress.setValue(value)

    def start_animation(self):
        if not self.animationThread.isAlive():
            self.animationThread.start()

    def stop_animation(self, connect):
        if self.animationThread.isAlive():
            self.animationThread.join(1)
            self.connectionProgress.setInvertedAppearance(False)
            self.connectionProgress.setValue(100)
            if connect:
                self.connectionProgress.setFormat("Connected")
            else:
                self.connectionProgress.setFormat("Failed")