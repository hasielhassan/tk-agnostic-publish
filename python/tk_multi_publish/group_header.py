# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import tank
from tank.platform.qt import QtCore, QtGui

class GroupHeader(QtGui.QWidget):
    """
    """
    def __init__(self, group_name, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
    
        # set up the UI
        from .ui.group_header import Ui_GroupHeader
        self._ui = Ui_GroupHeader() 
        self._ui.setupUi(self)
        
        self.name = group_name
        
    # @property
    def __get_name(self):
        return self._ui.name_label.toPlainText()
    # @name.setter
    def __set_name(self, value):
        self._ui.name_label.setText(value)
    name=property(__get_name, __set_name)