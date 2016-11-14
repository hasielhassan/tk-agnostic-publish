# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'group_header.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_GroupHeader(object):
    def setupUi(self, GroupHeader):
        GroupHeader.setObjectName("GroupHeader")
        GroupHeader.resize(394, 50)
        GroupHeader.setMinimumSize(QtCore.QSize(0, 50))
        GroupHeader.setMaximumSize(QtCore.QSize(16777215, 50))
        self.horizontalLayout = QtGui.QHBoxLayout(GroupHeader)
        self.horizontalLayout.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name_label = QtGui.QLabel(GroupHeader)
        self.name_label.setStyleSheet("#name_label {\n"
"font-size: 16px\n"
"}")
        self.name_label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.name_label.setObjectName("name_label")
        self.verticalLayout.addWidget(self.name_label)
        self.line = QtGui.QFrame(GroupHeader)
        self.line.setFrameShadow(QtGui.QFrame.Plain)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(GroupHeader)
        QtCore.QMetaObject.connectSlotsByName(GroupHeader)

    def retranslateUi(self, GroupHeader):
        GroupHeader.setWindowTitle(QtGui.QApplication.translate("GroupHeader", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.name_label.setText(QtGui.QApplication.translate("GroupHeader", "Group Display Name", None, QtGui.QApplication.UnicodeUTF8))

