# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

from tank.platform.qt import QtCore

class Task(QtCore.QObject):
    """
    Encapsulates a task for use internally within 
    the app - this is converted and passed as a
    dictionary to any hooks.
    """
    modified = QtCore.Signal()
    
    def __init__(self, item, output):
        QtCore.QObject.__init__(self)
        self._item = item
        self._output = output
        self._pre_publish_errors = []
        self._publish_errors = []
        
    @property
    def item(self):
        return self._item
    
    @property
    def output(self):
        return self._output
    
    # @property
    def __get_pre_publish_errors(self):
        return self._pre_publish_errors
    # @pre_publish_errors.setter
    def __set_pre_publish_errors(self, value):
        self._pre_publish_errors = value
        # emit modified signal
        self.modified.emit()
    pre_publish_errors=property(__get_pre_publish_errors, __set_pre_publish_errors)
        
    # @property
    def __get_publish_errors(self):
        return self._publish_errors
    # @publish_errors.setter
    def __set_publish_errors(self, value):
        self._publish_errors = value
        # emit modified signal
        self.modified.emit()
    publish_errors=property(__get_publish_errors, __set_publish_errors)
    
    def as_dictionary(self):
        """
        Return the task as a dictionary ready for passing 
        to the pre-publish and publish hooks
        """
        return {"item":self._item.raw_fields,
                "output":{"name":self._output.name, 
                          "publish_template":self._output.publish_template,
                          "tank_type":self._output.tank_type,
                          }
                }