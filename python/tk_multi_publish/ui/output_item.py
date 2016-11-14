# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'output_item.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_OutputItem(object):
    def setupUi(self, OutputItem):
        OutputItem.setObjectName("OutputItem")
        OutputItem.resize(396, 56)
        OutputItem.setMinimumSize(QtCore.QSize(0, 56))
        OutputItem.setMaximumSize(QtCore.QSize(16777215, 56))
        self.horizontalLayout = QtGui.QHBoxLayout(OutputItem)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(12, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.select_cb = QtGui.QCheckBox(OutputItem)
        self.select_cb.setMinimumSize(QtCore.QSize(0, 0))
        self.select_cb.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.select_cb.setText("")
        self.select_cb.setObjectName("select_cb")
        self.verticalLayout.addWidget(self.select_cb)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.icon_label = QtGui.QLabel(OutputItem)
        self.icon_label.setMinimumSize(QtCore.QSize(40, 40))
        self.icon_label.setMaximumSize(QtCore.QSize(40, 40))
        self.icon_label.setBaseSize(QtCore.QSize(32, 32))
        self.icon_label.setText("")
        self.icon_label.setPixmap(QtGui.QPixmap(":/res/default_output.png"))
        self.icon_label.setScaledContents(False)
        self.icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_label.setIndent(0)
        self.icon_label.setObjectName("icon_label")
        self.horizontalLayout.addWidget(self.icon_label)
        self.details_label = QtGui.QLabel(OutputItem)
        self.details_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.details_label.setMargin(0)
        self.details_label.setIndent(0)
        self.details_label.setObjectName("details_label")
        self.horizontalLayout.addWidget(self.details_label)
        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(OutputItem)
        QtCore.QMetaObject.connectSlotsByName(OutputItem)

    def retranslateUi(self, OutputItem):
        OutputItem.setWindowTitle(QtGui.QApplication.translate("OutputItem", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.details_label.setText(QtGui.QApplication.translate("OutputItem", "<b>Output Name</b><br>Description...<br>the third line...", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
