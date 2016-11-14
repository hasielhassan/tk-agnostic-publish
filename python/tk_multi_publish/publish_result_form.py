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
 
class PublishResultForm(QtGui.QWidget):
    """
    Implementation of the main publish UI
    """
    
    close = QtCore.Signal()
    
    def __init__(self, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
    
        self._status = True
        self._errors = []
    
        # set up the UI
        from .ui.publish_result_form import Ui_PublishResultForm
        self._ui = Ui_PublishResultForm() 
        self._ui.setupUi(self)
        
        self._ui.close_btn.clicked.connect(self._on_close)
        
        self._update_ui()
        
    # @property
    def __get_status(self):
        return self._status
    # @status.setter
    def __set_status(self, value):
        self._status = value
        self._update_ui()
    status=property(__get_status, __set_status)
    
    # @property
    def __get_errors(self):
        return self._errors
    # @errors.setter
    def __set_errors(self, value):
        self._errors = value
        self._update_ui()
    errors=property(__get_errors, __set_errors)
        
    def _on_close(self):
        self.close.emit()
        
    def _update_ui(self):
        self._ui.status_icon.setPixmap(QtGui.QPixmap([":/res/failure.png", ":/res/success.png"][self._status]))
        self._ui.status_title.setText(["Failure!", "Success"][self._status])
        
        details = ""
        if self._status:
            details = ("Your Publish has  successfully completed. Your "
                      "work has been shared, your scene has been "
                      "versioned up and your mates have been notified!")
        else:
            details = "\n\n".join(self._errors)
        self._ui.status_details.setText(details)
        
        
        
        
        
        
        
        
        
        