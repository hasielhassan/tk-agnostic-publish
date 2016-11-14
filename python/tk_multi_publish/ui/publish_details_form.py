# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_details_form.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_PublishDetailsForm(object):
    def setupUi(self, PublishDetailsForm):
        PublishDetailsForm.setObjectName("PublishDetailsForm")
        PublishDetailsForm.resize(771, 592)
        self.verticalLayout = QtGui.QVBoxLayout(PublishDetailsForm)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setSpacing(4)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.items_title_label = QtGui.QLabel(PublishDetailsForm)
        self.items_title_label.setStyleSheet("#items_title_label {\n"
"font-size: 14px\n"
"}")
        self.items_title_label.setIndent(4)
        self.items_title_label.setObjectName("items_title_label")
        self.verticalLayout_7.addWidget(self.items_title_label)
        self.publishes_stacked_widget = QtGui.QStackedWidget(PublishDetailsForm)
        self.publishes_stacked_widget.setStyleSheet("")
        self.publishes_stacked_widget.setObjectName("publishes_stacked_widget")
        self.publishes_page = QtGui.QWidget()
        self.publishes_page.setObjectName("publishes_page")
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.publishes_page)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.task_scroll = QtGui.QScrollArea(self.publishes_page)
        self.task_scroll.setStyleSheet("#task_scroll {\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-radius: 2px;\n"
"border-color: rgb(32,32,32);\n"
"}")
        self.task_scroll.setWidgetResizable(True)
        self.task_scroll.setObjectName("task_scroll")
        self.contents = QtGui.QWidget()
        self.contents.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.contents.setObjectName("contents")
        self.task_scroll.setWidget(self.contents)
        self.horizontalLayout_7.addWidget(self.task_scroll)
        self.publishes_stacked_widget.addWidget(self.publishes_page)
        self.no_publishes_page = QtGui.QWidget()
        self.no_publishes_page.setStyleSheet("")
        self.no_publishes_page.setObjectName("no_publishes_page")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.no_publishes_page)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.no_publishes_frame = QtGui.QFrame(self.no_publishes_page)
        self.no_publishes_frame.setStyleSheet("#no_publishes_frame {\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-radius: 2px;\n"
"border-color: rgb(32,32,32);\n"
"}")
        self.no_publishes_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.no_publishes_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.no_publishes_frame.setObjectName("no_publishes_frame")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.no_publishes_frame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem = QtGui.QSpacerItem(0, 88, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem1 = QtGui.QSpacerItem(0, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.label_3 = QtGui.QLabel(self.no_publishes_frame)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_9.addWidget(self.label_3)
        spacerItem2 = QtGui.QSpacerItem(0, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        spacerItem3 = QtGui.QSpacerItem(0, 88, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.verticalLayout_2.addWidget(self.no_publishes_frame)
        self.publishes_stacked_widget.addWidget(self.no_publishes_page)
        self.verticalLayout_7.addWidget(self.publishes_stacked_widget)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.info_title_label = QtGui.QLabel(PublishDetailsForm)
        self.info_title_label.setStyleSheet("#info_title_label {\n"
"font-size: 14px\n"
"}")
        self.info_title_label.setIndent(4)
        self.info_title_label.setObjectName("info_title_label")
        self.verticalLayout_5.addWidget(self.info_title_label)
        self.info_frame = QtGui.QFrame(PublishDetailsForm)
        self.info_frame.setStyleSheet("#info_frame {\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-radius: 2px;\n"
"border-color: rgb(32,32,32);\n"
"}")
        self.info_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.info_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.info_frame.setObjectName("info_frame")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.info_frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.task_header_label = QtGui.QLabel(self.info_frame)
        self.task_header_label.setStyleSheet("QLabel {\n"
"font-size: 12px;\n"
"}")
        self.task_header_label.setObjectName("task_header_label")
        self.verticalLayout_6.addWidget(self.task_header_label)
        self.sg_task_stacked_widget = QtGui.QStackedWidget(self.info_frame)
        self.sg_task_stacked_widget.setObjectName("sg_task_stacked_widget")
        self.sg_task_menu_page = QtGui.QWidget()
        self.sg_task_menu_page.setObjectName("sg_task_menu_page")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.sg_task_menu_page)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.sg_task_combo = QtGui.QComboBox(self.sg_task_menu_page)
        self.sg_task_combo.setObjectName("sg_task_combo")
        self.horizontalLayout_4.addWidget(self.sg_task_combo)
        self.sg_task_stacked_widget.addWidget(self.sg_task_menu_page)
        self.sg_task_label_page = QtGui.QWidget()
        self.sg_task_label_page.setObjectName("sg_task_label_page")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.sg_task_label_page)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.sg_task_label = QtGui.QLabel(self.sg_task_label_page)
        self.sg_task_label.setIndent(12)
        self.sg_task_label.setObjectName("sg_task_label")
        self.horizontalLayout_5.addWidget(self.sg_task_label)
        self.sg_task_stacked_widget.addWidget(self.sg_task_label_page)
        self.verticalLayout_6.addWidget(self.sg_task_stacked_widget)
        spacerItem4 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem4)
        self.label_7 = QtGui.QLabel(self.info_frame)
        self.label_7.setStyleSheet("QLabel {\n"
"font-size: 12px;\n"
"}")
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.thumbnail_frame = QtGui.QFrame(self.info_frame)
        self.thumbnail_frame.setStyleSheet("#thumbnail_frame {\n"
"border-style: solid;\n"
"border-color: rgb(32,32,32);\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"background: rgb(117,117,117);\n"
"}")
        self.thumbnail_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.thumbnail_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.thumbnail_frame.setObjectName("thumbnail_frame")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.thumbnail_frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.thumbnail_widget = ThumbnailWidget(self.thumbnail_frame)
        self.thumbnail_widget.setMinimumSize(QtCore.QSize(200, 130))
        self.thumbnail_widget.setMaximumSize(QtCore.QSize(200, 130))
        self.thumbnail_widget.setStyleSheet("")
        self.thumbnail_widget.setObjectName("thumbnail_widget")
        self.horizontalLayout_3.addWidget(self.thumbnail_widget)
        self.horizontalLayout_6.addWidget(self.thumbnail_frame)
        spacerItem5 = QtGui.QSpacerItem(0, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        spacerItem6 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem6)
        self.label_8 = QtGui.QLabel(self.info_frame)
        self.label_8.setStyleSheet("QLabel {\n"
"font-size: 12px;\n"
"}")
        self.label_8.setObjectName("label_8")
        self.verticalLayout_6.addWidget(self.label_8)
        self.comments_edit = QtGui.QTextEdit(self.info_frame)
        self.comments_edit.setMinimumSize(QtCore.QSize(300, 0))
        self.comments_edit.setObjectName("comments_edit")
        self.verticalLayout_6.addWidget(self.comments_edit)
        self.verticalLayout_6.setStretch(7, 1)
        self.verticalLayout_5.addWidget(self.info_frame)
        self.verticalLayout_5.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.cancel_btn = QtGui.QPushButton(PublishDetailsForm)
        self.cancel_btn.setMinimumSize(QtCore.QSize(80, 0))
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_2.addWidget(self.cancel_btn)
        self.publish_btn = QtGui.QPushButton(PublishDetailsForm)
        self.publish_btn.setMinimumSize(QtCore.QSize(80, 0))
        self.publish_btn.setObjectName("publish_btn")
        self.horizontalLayout_2.addWidget(self.publish_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(PublishDetailsForm)
        self.publishes_stacked_widget.setCurrentIndex(1)
        self.sg_task_stacked_widget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(PublishDetailsForm)

    def retranslateUi(self, PublishDetailsForm):
        PublishDetailsForm.setWindowTitle(QtGui.QApplication.translate("PublishDetailsForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.items_title_label.setText(QtGui.QApplication.translate("PublishDetailsForm", "Choose Additional Items to Publish:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PublishDetailsForm", "<i>This publisher does not have any optional items to choose from.<br><br>Only your current work file will be published.</i>", None, QtGui.QApplication.UnicodeUTF8))
        self.info_title_label.setText(QtGui.QApplication.translate("PublishDetailsForm", "Add Information about your Publish:", None, QtGui.QApplication.UnicodeUTF8))
        self.task_header_label.setText(QtGui.QApplication.translate("PublishDetailsForm", "What Shotgun Task are you working on?", None, QtGui.QApplication.UnicodeUTF8))
        self.sg_task_label.setText(QtGui.QApplication.translate("PublishDetailsForm", "Anm, Animation", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("PublishDetailsForm", "Add a Thumbnail?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("PublishDetailsForm", "Any Comments?", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_btn.setText(QtGui.QApplication.translate("PublishDetailsForm", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.publish_btn.setText(QtGui.QApplication.translate("PublishDetailsForm", "Publish", None, QtGui.QApplication.UnicodeUTF8))

from ..publish_details_form import ThumbnailWidget
from . import resources_rc
