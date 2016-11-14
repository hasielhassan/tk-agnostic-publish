# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error_list.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_ErrorList(object):
    def setupUi(self, ErrorList):
        ErrorList.setObjectName("ErrorList")
        ErrorList.resize(400, 158)
        self.horizontalLayout = QtGui.QHBoxLayout(ErrorList)
        self.horizontalLayout.setContentsMargins(12, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.main_frame = QtGui.QFrame(ErrorList)
        self.main_frame.setStyleSheet("#main_frame {\n"
"border-style: solid;\n"
"border-width: 1;\n"
"border-radius: 2px;\n"
"}")
        self.main_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.main_frame)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.section_label = QtGui.QLabel(self.main_frame)
        self.section_label.setMinimumSize(QtCore.QSize(0, 20))
        self.section_label.setStyleSheet("#section_label {\n"
"font-size: 10pt\n"
"}")
        self.section_label.setIndent(4)
        self.section_label.setObjectName("section_label")
        self.verticalLayout.addWidget(self.section_label)
        self.line = QtGui.QFrame(self.main_frame)
        self.line.setFrameShadow(QtGui.QFrame.Plain)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.item_frame = QtGui.QFrame(self.main_frame)
        self.item_frame.setStyleSheet("#item_frame {\n"
"border-style: none;\n"
"}")
        self.item_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.item_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.item_frame.setObjectName("item_frame")
        self.verticalLayout.addWidget(self.item_frame)
        self.verticalLayout.setStretch(2, 1)
        self.horizontalLayout.addWidget(self.main_frame)

        self.retranslateUi(ErrorList)
        QtCore.QMetaObject.connectSlotsByName(ErrorList)

    def retranslateUi(self, ErrorList):
        ErrorList.setWindowTitle(QtGui.QApplication.translate("ErrorList", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.section_label.setText(QtGui.QApplication.translate("ErrorList", "<b><font color=\'orange\'>Validation checks returned some messages for your attention:</font></b>", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
