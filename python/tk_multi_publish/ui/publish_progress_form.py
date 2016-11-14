# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_progress_form.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_PublishProgressForm(object):
    def setupUi(self, PublishProgressForm):
        PublishProgressForm.setObjectName("PublishProgressForm")
        PublishProgressForm.resize(651, 384)
        self.verticalLayout_4 = QtGui.QVBoxLayout(PublishProgressForm)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(-1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtGui.QSpacerItem(20, 100, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem1)
        self.title = QtGui.QLabel(PublishProgressForm)
        self.title.setStyleSheet("#title {\n"
"font-size: 24px;\n"
"}")
        self.title.setObjectName("title")
        self.verticalLayout_3.addWidget(self.title)
        self.progress_bar = QtGui.QProgressBar(PublishProgressForm)
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progress_bar")
        self.verticalLayout_3.addWidget(self.progress_bar)
        self.details = QtGui.QLabel(PublishProgressForm)
        self.details.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.details.setWordWrap(False)
        self.details.setObjectName("details")
        self.verticalLayout_3.addWidget(self.details)
        self.stage_progress_bar = QtGui.QProgressBar(PublishProgressForm)
        self.stage_progress_bar.setProperty("value", 24)
        self.stage_progress_bar.setObjectName("stage_progress_bar")
        self.verticalLayout_3.addWidget(self.stage_progress_bar)
        spacerItem2 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.verticalLayout_3.setStretch(5, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_4.setStretch(0, 1)

        self.retranslateUi(PublishProgressForm)
        QtCore.QMetaObject.connectSlotsByName(PublishProgressForm)

    def retranslateUi(self, PublishProgressForm):
        PublishProgressForm.setWindowTitle(QtGui.QApplication.translate("PublishProgressForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("PublishProgressForm", "Publishing...", None, QtGui.QApplication.UnicodeUTF8))
        self.details.setText(QtGui.QApplication.translate("PublishProgressForm", "(Details)", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
