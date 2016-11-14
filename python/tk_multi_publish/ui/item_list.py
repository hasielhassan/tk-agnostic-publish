# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'item_list.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_ItemList(object):
    def setupUi(self, ItemList):
        ItemList.setObjectName("ItemList")
        ItemList.resize(397, 265)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(ItemList)
        self.horizontalLayout_2.setContentsMargins(12, 2, 2, 2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.main_frame = QtGui.QFrame(ItemList)
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
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.section_label = QtGui.QLabel(self.main_frame)
        self.section_label.setStyleSheet("#section_label {\n"
"font-size: 10pt\n"
"}")
        self.section_label.setIndent(4)
        self.section_label.setObjectName("section_label")
        self.horizontalLayout.addWidget(self.section_label)
        self.expand_label = QtGui.QLabel(self.main_frame)
        self.expand_label.setMinimumSize(QtCore.QSize(20, 20))
        self.expand_label.setBaseSize(QtCore.QSize(20, 20))
        self.expand_label.setText("")
        self.expand_label.setPixmap(QtGui.QPixmap(":/res/group_expand.png"))
        self.expand_label.setScaledContents(False)
        self.expand_label.setAlignment(QtCore.Qt.AlignCenter)
        self.expand_label.setObjectName("expand_label")
        self.horizontalLayout.addWidget(self.expand_label)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        self.horizontalLayout_2.addWidget(self.main_frame)

        self.retranslateUi(ItemList)
        QtCore.QMetaObject.connectSlotsByName(ItemList)

    def retranslateUi(self, ItemList):
        ItemList.setWindowTitle(QtGui.QApplication.translate("ItemList", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.section_label.setText(QtGui.QApplication.translate("ItemList", "<b>n items available</b>, <i>expand to turn individual items on and off</i>", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
