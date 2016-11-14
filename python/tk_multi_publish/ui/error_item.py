# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error_item.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_ErrorItem(object):
    def setupUi(self, ErrorItem):
        ErrorItem.setObjectName("ErrorItem")
        ErrorItem.resize(324, 36)
        self.horizontalLayout = QtGui.QHBoxLayout(ErrorItem)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.error_label = QtGui.QLabel(ErrorItem)
        self.error_label.setMinimumSize(QtCore.QSize(0, 0))
        self.error_label.setStyleSheet("")
        self.error_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.error_label.setObjectName("error_label")
        self.horizontalLayout.addWidget(self.error_label)

        self.retranslateUi(ErrorItem)
        QtCore.QMetaObject.connectSlotsByName(ErrorItem)

    def retranslateUi(self, ErrorItem):
        ErrorItem.setWindowTitle(QtGui.QApplication.translate("ErrorItem", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.error_label.setText(QtGui.QApplication.translate("ErrorItem", "<font color=\'orange\'>Validation Name</font><br>Details on how to fix etc.", None, QtGui.QApplication.UnicodeUTF8))

