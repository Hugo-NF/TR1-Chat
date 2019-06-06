# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow

class Ui_serverWindow(object):
    def setupUi(self, serverWindow):
        serverWindow.setObjectName("serverWindow")
        serverWindow.resize(931, 673)
        self.centralWidget = QtWidgets.QWidget(serverWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.networkFrame = QtWidgets.QGroupBox(self.centralWidget)
        self.networkFrame.setMaximumSize(QtCore.QSize(16777215, 103))
        self.networkFrame.setObjectName("networkFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.networkFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.optionsLayout = QtWidgets.QGridLayout()
        self.optionsLayout.setObjectName("optionsLayout")
        self.hostLabel = QtWidgets.QLabel(self.networkFrame)
        self.hostLabel.setObjectName("hostLabel")
        self.optionsLayout.addWidget(self.hostLabel, 0, 0, 1, 1)
        self.buffLabel = QtWidgets.QLabel(self.networkFrame)
        self.buffLabel.setObjectName("buffLabel")
        self.optionsLayout.addWidget(self.buffLabel, 1, 3, 1, 1)
        self.buffEdit = QtWidgets.QSpinBox(self.networkFrame)
        self.buffEdit.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.buffEdit.setMinimum(512)
        self.buffEdit.setMaximum(16384)
        self.buffEdit.setSingleStep(512)
        self.buffEdit.setProperty("value", 1024)
        self.buffEdit.setObjectName("buffEdit")
        self.optionsLayout.addWidget(self.buffEdit, 1, 4, 1, 1)
        self.bytesLabel = QtWidgets.QLabel(self.networkFrame)
        self.bytesLabel.setObjectName("bytesLabel")
        self.optionsLayout.addWidget(self.bytesLabel, 1, 5, 1, 1)
        self.backlogLabel = QtWidgets.QLabel(self.networkFrame)
        self.backlogLabel.setObjectName("backlogLabel")
        self.optionsLayout.addWidget(self.backlogLabel, 0, 3, 1, 1)
        self.backlogEdit = QtWidgets.QSpinBox(self.networkFrame)
        self.backlogEdit.setSingleStep(5)
        self.backlogEdit.setProperty("value", 10)
        self.backlogEdit.setObjectName("backlogEdit")
        self.optionsLayout.addWidget(self.backlogEdit, 0, 4, 1, 1)
        self.hostEdit = QtWidgets.QLineEdit(self.networkFrame)
        self.hostEdit.setPlaceholderText("")
        self.hostEdit.setObjectName("hostEdit")
        self.optionsLayout.addWidget(self.hostEdit, 0, 1, 1, 1)
        self.noConnectionsLabel = QtWidgets.QLabel(self.networkFrame)
        self.noConnectionsLabel.setObjectName("noConnectionsLabel")
        self.optionsLayout.addWidget(self.noConnectionsLabel, 0, 5, 1, 1)
        self.tcpRadioButton = QtWidgets.QRadioButton(self.networkFrame)
        self.tcpRadioButton.setChecked(True)
        self.tcpRadioButton.setObjectName("tcpRadioButton")
        self.optionsLayout.addWidget(self.tcpRadioButton, 0, 2, 1, 1)
        self.portLabel = QtWidgets.QLabel(self.networkFrame)
        self.portLabel.setObjectName("portLabel")
        self.optionsLayout.addWidget(self.portLabel, 1, 0, 1, 1)
        self.udpRadioButton = QtWidgets.QRadioButton(self.networkFrame)
        self.udpRadioButton.setObjectName("udpRadioButton")
        self.optionsLayout.addWidget(self.udpRadioButton, 1, 2, 1, 1)
        self.portEdit = QtWidgets.QSpinBox(self.networkFrame)
        self.portEdit.setMinimum(1)
        self.portEdit.setMaximum(65535)
        self.portEdit.setProperty("value", 8080)
        self.portEdit.setObjectName("portEdit")
        self.optionsLayout.addWidget(self.portEdit, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.optionsLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLine = QtWidgets.QFrame(self.networkFrame)
        self.verticalLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.verticalLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLine.setObjectName("verticalLine")
        self.horizontalLayout.addWidget(self.verticalLine)
        self.runButton = QtWidgets.QPushButton(self.networkFrame)
        self.runButton.setObjectName("runButton")
        self.horizontalLayout.addWidget(self.runButton)
        self.stopButton = QtWidgets.QPushButton(self.networkFrame)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)
        self.verticalLayout_2.addWidget(self.networkFrame)
        self.outputFrame = QtWidgets.QGroupBox(self.centralWidget)
        self.outputFrame.setObjectName("outputFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.outputFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.serverOutput = QtWidgets.QTextBrowser(self.outputFrame)
        self.serverOutput.setObjectName("serverOutput")
        self.verticalLayout.addWidget(self.serverOutput)
        self.verticalLayout_2.addWidget(self.outputFrame)
        serverWindow.setCentralWidget(self.centralWidget)
        self.statusbar = QtWidgets.QStatusBar(serverWindow)
        self.statusbar.setObjectName("statusbar")
        serverWindow.setStatusBar(self.statusbar)

        self.retranslateUi(serverWindow)
        QtCore.QMetaObject.connectSlotsByName(serverWindow)

    def retranslateUi(self, serverWindow):
        _translate = QtCore.QCoreApplication.translate
        serverWindow.setWindowTitle(_translate("serverWindow", "Output"))
        self.networkFrame.setTitle(_translate("serverWindow", "Network options"))
        self.hostLabel.setText(_translate("serverWindow", "Host:"))
        self.buffLabel.setText(_translate("serverWindow", "Buffer size:"))
        self.bytesLabel.setText(_translate("serverWindow", "bytes"))
        self.backlogLabel.setText(_translate("serverWindow", "Backlog:"))
        self.hostEdit.setText(_translate("serverWindow", "127.0.0.1"))
        self.noConnectionsLabel.setText(_translate("serverWindow", "connections"))
        self.tcpRadioButton.setText(_translate("serverWindow", "TCP"))
        self.portLabel.setText(_translate("serverWindow", "Port:"))
        self.udpRadioButton.setText(_translate("serverWindow", "UDP"))
        self.runButton.setText(_translate("serverWindow", "Run"))
        self.stopButton.setText(_translate("serverWindow", "Stop"))
        self.outputFrame.setTitle(_translate("serverWindow", "Output"))

    def console(self, text):
        self.serverOutput.append(text)

class ServerWindow(QMainWindow):
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?\n" \
                   "Warning: DO NOT quit if server is still running!"
        reply = QMessageBox.question(self, 'Quit',
                                     quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()