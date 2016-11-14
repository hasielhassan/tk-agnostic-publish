# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_form.ui'
#
# Created: Sun Oct 02 22:45:00 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_PublishForm(object):
    def setupUi(self, PublishForm):
        PublishForm.setObjectName("PublishForm")
        PublishForm.resize(794, 549)
        PublishForm.setAutoFillBackground(False)
        self.verticalLayout = QtGui.QVBoxLayout(PublishForm)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.work_drag_area = QtGui.QWidget(PublishForm)
        self.work_drag_area.setObjectName("work_drag_area")
        self.horizontalLayout = QtGui.QHBoxLayout(self.work_drag_area)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.primary_icon_label = QtGui.QLabel(self.work_drag_area)
        self.primary_icon_label.setMinimumSize(QtCore.QSize(80, 80))
        self.primary_icon_label.setMaximumSize(QtCore.QSize(80, 80))
        self.primary_icon_label.setBaseSize(QtCore.QSize(32, 32))
        self.primary_icon_label.setText("")
        self.primary_icon_label.setPixmap(QtGui.QPixmap(":/res/default_header.png"))
        self.primary_icon_label.setScaledContents(False)
        self.primary_icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.primary_icon_label.setObjectName("primary_icon_label")
        self.horizontalLayout.addWidget(self.primary_icon_label)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.primary_details_label = QtGui.QLabel(self.work_drag_area)
        self.primary_details_label.setStyleSheet("#primary_details_label {\n"
"}")
        self.primary_details_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.primary_details_label.setMargin(0)
        self.primary_details_label.setObjectName("primary_details_label")
        self.verticalLayout_2.addWidget(self.primary_details_label)
        self.primary_error_label = QtGui.QLabel(self.work_drag_area)
        self.primary_error_label.setMinimumSize(QtCore.QSize(0, 0))
        self.primary_error_label.setStyleSheet("")
        self.primary_error_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.primary_error_label.setWordWrap(True)
        self.primary_error_label.setMargin(0)
        self.primary_error_label.setObjectName("primary_error_label")
        self.verticalLayout_2.addWidget(self.primary_error_label)
        self.verticalLayout_2.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addWidget(self.work_drag_area)
        self.pages = QtGui.QStackedWidget(PublishForm)
        self.pages.setObjectName("pages")
        self.publish_details = PublishDetailsForm()
        self.publish_details.setObjectName("publish_details")
        self.pages.addWidget(self.publish_details)
        self.publish_progress = PublishProgressForm()
        self.publish_progress.setObjectName("publish_progress")
        self.pages.addWidget(self.publish_progress)
        self.publish_result = PublishResultForm()
        self.publish_result.setObjectName("publish_result")
        self.pages.addWidget(self.publish_result)
        self.verticalLayout.addWidget(self.pages)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(PublishForm)
        self.pages.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(PublishForm)

    def retranslateUi(self, PublishForm):
        PublishForm.setWindowTitle(QtGui.QApplication.translate("PublishForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.primary_details_label.setText(QtGui.QApplication.translate("PublishForm", "<span style=\'font-size: 16px\'}><b>Output Name</b></span><span style=\'font-size: 12px\'}><br>Description...<br>the third line...</span>", None, QtGui.QApplication.UnicodeUTF8))
        self.primary_error_label.setText(QtGui.QApplication.translate("PublishForm", "<html><head/><body><p><span style=\" color:#ffa500;\">Validation Name</span><br/>Details on how to fix etc.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

from ..publish_progress_form import PublishProgressForm
from ..publish_details_form import PublishDetailsForm
from ..publish_result_form import PublishResultForm
from . import resources_rc
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_form.ui'
#
# Created: Sun Oct 09 22:50:25 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PublishForm(object):
    def setupUi(self, PublishForm):
        PublishForm.setObjectName("PublishForm")
        PublishForm.resize(794, 549)
        PublishForm.setAutoFillBackground(False)
        self.verticalLayout = QtGui.QVBoxLayout(PublishForm)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.work_drag_area = QtGui.QWidget(PublishForm)
        self.work_drag_area.setObjectName("work_drag_area")
        self.horizontalLayout = QtGui.QHBoxLayout(self.work_drag_area)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.primary_icon_label = QtGui.QLabel(self.work_drag_area)
        self.primary_icon_label.setMinimumSize(QtCore.QSize(80, 80))
        self.primary_icon_label.setMaximumSize(QtCore.QSize(80, 80))
        self.primary_icon_label.setBaseSize(QtCore.QSize(32, 32))
        self.primary_icon_label.setText("")
        self.primary_icon_label.setPixmap(QtGui.QPixmap(":/res/default_header.png"))
        self.primary_icon_label.setScaledContents(False)
        self.primary_icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.primary_icon_label.setObjectName("primary_icon_label")
        self.horizontalLayout.addWidget(self.primary_icon_label)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.primary_details_label = QtGui.QLabel(self.work_drag_area)
        self.primary_details_label.setStyleSheet("#primary_details_label {\n"
"}")
        self.primary_details_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.primary_details_label.setMargin(0)
        self.primary_details_label.setObjectName("primary_details_label")
        self.verticalLayout_2.addWidget(self.primary_details_label)
        self.primary_error_label = QtGui.QLabel(self.work_drag_area)
        self.primary_error_label.setMinimumSize(QtCore.QSize(0, 0))
        self.primary_error_label.setStyleSheet("")
        self.primary_error_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.primary_error_label.setWordWrap(True)
        self.primary_error_label.setMargin(0)
        self.primary_error_label.setObjectName("primary_error_label")
        self.verticalLayout_2.addWidget(self.primary_error_label)
        self.verticalLayout_2.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addWidget(self.work_drag_area)
        self.pages = QtGui.QStackedWidget(PublishForm)
        self.pages.setObjectName("pages")
        self.publish_details = PublishDetailsForm()
        self.publish_details.setObjectName("publish_details")
        self.pages.addWidget(self.publish_details)
        self.publish_progress = PublishProgressForm()
        self.publish_progress.setObjectName("publish_progress")
        self.pages.addWidget(self.publish_progress)
        self.publish_result = PublishResultForm()
        self.publish_result.setObjectName("publish_result")
        self.pages.addWidget(self.publish_result)
        self.verticalLayout.addWidget(self.pages)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(PublishForm)
        self.pages.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(PublishForm)

    def retranslateUi(self, PublishForm):
        PublishForm.setWindowTitle(QtGui.QApplication.translate("PublishForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.primary_details_label.setText(QtGui.QApplication.translate("PublishForm", "<html><head/><body><p><span style=\" font-size:16px; font-weight:600;\">Agnostic publish </span><span style=\" font-size:12px;\"><br/>Drag and drop your external editable work file...<br/>...</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.primary_error_label.setText(QtGui.QApplication.translate("PublishForm", "<html><head/><body><p><span style=\" color:#ffa500;\">Validation Name</span><br/>Details on how to fix etc.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

from ..publish_progress_form import PublishProgressForm
from ..publish_details_form import PublishDetailsForm
from ..publish_result_form import PublishResultForm
import resources_rc
